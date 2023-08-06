import logging
import uuid
from xml.etree import ElementTree as ET

import lasso
import requests
import requests.exceptions

from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.models import Group
from django.utils import six
from django.utils.encoding import force_text

from . import utils, app_settings, models


class UserCreationError(Exception):
    pass


class DefaultAdapter(object):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)

    def get_idp(self, entity_id):
        '''Find the first IdP definition matching entity_id'''
        for idp in self.get_idps():
            if entity_id == idp['ENTITY_ID']:
                return idp

    def get_identity_providers_setting(self):
        return app_settings.IDENTITY_PROVIDERS

    def get_idps(self):
        for i, idp in enumerate(self.get_identity_providers_setting()):
            if 'METADATA_URL' in idp and 'METADATA' not in idp:
                verify_ssl_certificate = utils.get_setting(
                    idp, 'VERIFY_SSL_CERTIFICATE')
                try:
                    response = requests.get(idp['METADATA_URL'], verify=verify_ssl_certificate)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    self.logger.error(
                        u'retrieval of metadata URL %r failed with error %s for %d-th idp',
                        idp['METADATA_URL'], e, i)
                    continue
                idp['METADATA'] = response.text
            elif 'METADATA' in idp:
                if idp['METADATA'].startswith('/'):
                    idp['METADATA'] = open(idp['METADATA']).read()
            else:
                self.logger.error(u'missing METADATA or METADATA_URL in %d-th idp', i)
                continue
            if 'ENTITY_ID' not in idp:
                try:
                    doc = ET.fromstring(idp['METADATA'])
                except (TypeError, ET.ParseError):
                    self.logger.error(u'METADATA of %d-th idp is invalid', i)
                    continue
                if doc.tag != '{%s}EntityDescriptor' % lasso.SAML2_METADATA_HREF:
                    self.logger.error(u'METADATA of %d-th idp has no EntityDescriptor root tag', i)
                    continue

                if not 'entityID' in doc.attrib:
                    self.logger.error(
                        u'METADATA of %d-th idp has no entityID attribute on its root tag', i)
                    continue
                idp['ENTITY_ID'] = doc.attrib['entityID']
            yield idp

    def authorize(self, idp, saml_attributes):
        if not idp:
            return False
        required_classref = utils.get_setting(idp, 'AUTHN_CLASSREF')
        if required_classref:
            given_classref = saml_attributes['authn_context_class_ref']
            if given_classref is None or \
                    given_classref not in required_classref:
                raise PermissionDenied
        return True

    def format_username(self, idp, saml_attributes):
        realm = utils.get_setting(idp, 'REALM')
        username_template = utils.get_setting(idp, 'USERNAME_TEMPLATE')
        try:
            username = force_text(username_template).format(
                realm=realm, attributes=saml_attributes, idp=idp)[:30]
        except ValueError:
            self.logger.error(u'invalid username template %r', username_template)
        except (AttributeError, KeyError, IndexError) as e:
            self.logger.error(
                u'invalid reference in username template %r: %s', username_template, e)
        except Exception as e:
            self.logger.exception(u'unknown error when formatting username')
        else:
            return username

    def create_user(self, user_class):
        return user_class.objects.create(username=uuid.uuid4().hex[:30])

    def finish_create_user(self, idp, saml_attributes, user):
        username = self.format_username(idp, saml_attributes)
        if not username:
            self.logger.warning('could not build a username, login refused')
            raise UserCreationError
        user.username = username
        user.save()

    def lookup_user(self, idp, saml_attributes):
        User = auth.get_user_model()
        transient_federation_attribute = utils.get_setting(idp, 'TRANSIENT_FEDERATION_ATTRIBUTE')
        if saml_attributes['name_id_format'] == lasso.SAML2_NAME_IDENTIFIER_FORMAT_TRANSIENT:
            if (transient_federation_attribute
                    and saml_attributes.get(transient_federation_attribute)):
                name_id = saml_attributes[transient_federation_attribute]
                if not isinstance(name_id, six.string_types):
                    if len(name_id) == 1:
                        name_id = name_id[0]
                    else:
                        self.logger.warning('more than one value for attribute %r, cannot federate',
                                            transient_federation_attribute)
                        return None
            else:
                return None
        else:
            name_id = saml_attributes['name_id_content']
        issuer = saml_attributes['issuer']
        try:
            return User.objects.get(saml_identifiers__name_id=name_id,
                                    saml_identifiers__issuer=issuer)
        except User.DoesNotExist:
            if not utils.get_setting(idp, 'PROVISION'):
                self.logger.warning('provisionning disabled, login refused')
                return None
            user = self.create_user(User)
            saml_id, created = models.UserSAMLIdentifier.objects.get_or_create(
                name_id=name_id, issuer=issuer, defaults={'user': user})
            if created:
                try:
                    self.finish_create_user(idp, saml_attributes, user)
                except UserCreationError:
                    user.delete()
                    return None
                self.logger.info('created new user %s with name_id %s from issuer %s',
                                 user, name_id, issuer)
            else:
                user.delete()
                user = saml_id.user
                self.logger.info('looked up user %s with name_id %s from issuer %s',
                                 user, name_id, issuer)
        return user

    def provision(self, user, idp, saml_attributes):
        self.provision_attribute(user, idp, saml_attributes)
        self.provision_superuser(user, idp, saml_attributes)
        self.provision_groups(user, idp, saml_attributes)

    def provision_attribute(self, user, idp, saml_attributes):
        realm = utils.get_setting(idp, 'REALM')
        attribute_mapping = utils.get_setting(idp, 'ATTRIBUTE_MAPPING')
        attribute_set = False
        for field, tpl in attribute_mapping.items():
            try:
                value = force_text(tpl).format(realm=realm, attributes=saml_attributes, idp=idp)
            except ValueError:
                self.logger.warning(u'invalid attribute mapping template %r', tpl)
            except (AttributeError, KeyError, IndexError, ValueError) as e:
                self.logger.warning(
                    u'invalid reference in attribute mapping template %r: %s', tpl, e)
            else:
                model_field = user._meta.get_field(field)
                if hasattr(model_field, 'max_length'):
                    value = value[:model_field.max_length]
                if getattr(user, field) != value:
                    old_value = getattr(user, field)
                    setattr(user, field, value)
                    attribute_set = True
                    self.logger.info(u'set field %s of user %s to value %r (old value %r)', field,
                                     user, value, old_value)
        if attribute_set:
            user.save()

    def provision_superuser(self, user, idp, saml_attributes):
        superuser_mapping = utils.get_setting(idp, 'SUPERUSER_MAPPING')
        if not superuser_mapping:
            return
        attribute_set = False
        for key, values in superuser_mapping.items():
            if key in saml_attributes:
                if not isinstance(values, (tuple, list)):
                    values = [values]
                values = set(values)
                attribute_values = saml_attributes[key]
                if not isinstance(attribute_values, (tuple, list)):
                    attribute_values = [attribute_values]
                attribute_values = set(attribute_values)
                if attribute_values & values:
                    if not (user.is_staff and user.is_superuser):
                        user.is_staff = True
                        user.is_superuser = True
                        attribute_set = True
                        self.logger.info('flag is_staff and is_superuser added to user %s', user)
                    break
        else:
            if user.is_superuser or user.is_staff:
                user.is_staff = False
                user.is_superuser = False
                self.logger.info('flag is_staff and is_superuser removed from user %s', user)
                attribute_set = True
        if attribute_set:
            user.save()

    def provision_groups(self, user, idp, saml_attributes):
        User = user.__class__
        group_attribute = utils.get_setting(idp, 'GROUP_ATTRIBUTE')
        create_group = utils.get_setting(idp, 'CREATE_GROUP')
        if group_attribute in saml_attributes:
            values = saml_attributes[group_attribute]
            if not isinstance(values, (list, tuple)):
                values = [values]
            groups = []
            for value in set(values):
                if create_group:
                    group, created = Group.objects.get_or_create(name=value)
                else:
                    try:
                        group = Group.objects.get(name=value)
                    except Group.DoesNotExist:
                        continue
                groups.append(group)
            for group in Group.objects.filter(pk__in=[g.pk for g in groups]).exclude(user=user):
                self.logger.info(
                    u'adding group %s (%s) to user %s (%s)', group, group.pk, user, user.pk)
                User.groups.through.objects.get_or_create(group=group, user=user)
            qs = User.groups.through.objects.exclude(
                group__pk__in=[g.pk for g in groups]).filter(user=user)
            for rel in qs:
                self.logger.info(u'removing group %s (%s) from user %s (%s)', rel.group,
                                 rel.group.pk, rel.user, rel.user.pk)
            qs.delete()
