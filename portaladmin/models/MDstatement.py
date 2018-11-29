from django.db import models
import json
import tempfile

from ..constants import *
from PVZDpy.samled_validator import SamlEdValidator
from django.conf import settings
from ..policydict import getPolicyDict_from_json
from fedop.models.namespace import Namespaceobj


class CheckOut(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MDstatementAbstract(models.Model):
    class Meta:
        abstract = True
        ordering = ['-updated_at']
        verbose_name = 'Metadaten Statement'

    def __init__(self, *args, **kw):
        super(MDstatementAbstract, self).__init__(*args, **kw)
        self._ed_uploaded_old = self.ed_uploaded
        self._ed_signed_old = self.ed_signed
        self._ed_file_upload_name_old = self.ed_file_upload.name

    status = models.CharField(
        verbose_name='Workflow Status',
        default=STATUS_CREATED, null=True,
        choices=STATUS_CHOICES,
        max_length=14)
    ed_file_upload = models.FileField(
        upload_to='upload/', default='', null=True, blank=True,
        verbose_name='EntityDescriptor hochladen',)
    ed_uploaded = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor hochgeladen',
        help_text='SAML EntityDescriptor (geladen, nicht signiert)',
        max_length=100000)
    ed_uploaded_filename = models.CharField(
        verbose_name='Upload Filename',
        default=None, null=True,
        max_length=100)
    ed_signed = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor signiert',
        help_text='SAML EntityDescriptor (signiert)',
        max_length=100000)
    admin_note = models.TextField(
        blank=True, null=True,
        verbose_name='Admin Notiz',
        max_length=1000)
    entityID = models.CharField(
        blank=True, null=True,
        max_length=300)
#    namespaceobj = models.ForeignKey(
#        Namespaceobj,
#        on_delete=models.PROTECT,
#        help_text='Namespace')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    def is_delete(self):
        self.validate()
        return self.ed_val.deletionRequest

    def get_validation_message(self):
        self.validate()
        if getattr(self.ed_val, 'val_mesg_dict', False):
            return json.dumps(self.ed_val.val_mesg_dict, indent=2)
        else:
            return ''
    get_validation_message.short_description = 'validation message'

    def get_validation_message_trunc(self):
        self.validate()
        if getattr(self.ed_val, 'val_mesg_dict', False):
            m = json.dumps(self.ed_val.val_mesg_dict, indent=2)
            m = m[0:47]+'...' if len(m) > 47 else m
            return m
        else:
            return ''
    get_validation_message_trunc.short_description = 'error'

    @property
    def valid(self):
        self.validate()
        if getattr(self.ed_val, 'content_val_ok', False):
            return self.ed_val.content_val_ok
        else:
            return False

    @property
    def namespace(self):
        self.validate()
        if getattr(self.ed_val, 'ed', False):
            return self.ed_val.ed.get_namespace()

    @property
    def operation(self):
        if not getattr(self.ed_val, 'ed', False):
            return ''
        if not self.ed_val.ed.get_entityid_hostname():
            return ''
        if self.is_delete():
            return 'delete'
        return 'add/mod'

    @property
    def orgid(self):
        self.validate()
        if getattr(self.ed_val, 'ed', False):
            return self.ed_val.ed.get_orgid()

    @property
    def orgcn(self):
        self.validate()
        if getattr(self.ed_val, 'ed', False):
            return self.ed_val.ed.get_orgcn()

    @property
    def updated(self):
        return self.updated_at.strftime("%Y%m%d %H:%M")

    @property
    def authorized(self):
        self.validate()
        if getattr(self.ed_val, 'authz_ok', False):
            return False
        else:
            return self.ed_val.authz_ok

    def get_signer_subject(self):
        self.validate()
        return getattr(self.ed_val, 'signer_cert_cn', False)
    get_signer_subject.short_description = 'Signiert von'


    def get_boilerplate_help(self):
        return "Ein Metadaten Statement wird erstellt und geändert, indem eine Datei mit einem " \
               "SAML Entity Descriptor hochgeladen wird. Für die Signatur ist in der Listansicht " \
               "der Eintrag zu markieren und die Aktion zum signieren auszuführen."
    get_boilerplate_help.short_description = ''


    def serialize_json(self):
        dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
        wanted_keys = (
            'admin_note',
            'ed_signed',
            'ed_uploaded',
            'ed_uploaded_filename',
            'entityID',
            'status',
        )
        self_dict = dictfilt(self.__dict__, wanted_keys)
        return json.dumps(self_dict, sort_keys=True, indent=2)

    def __str__(self):
        self.validate()
        if getattr(self.ed_val, 'entityID', False):
            return str(self.ed_val.entityID)
        else:
            return ''

    def validate(self):
        if not getattr(self, 'ed_val', None):
            self.ed_val = SamlEdValidator(getPolicyDict_from_json())
        if self.ed_signed:
            self.ed_val.validate_entitydescriptor(ed_str_new=self.ed_signed, sigval=True)
        elif self.ed_uploaded:
            self.ed_val.validate_entitydescriptor(ed_str_new=self.ed_uploaded, sigval=False)
        pass

    def save(self, *args, **kwargs):
        def _fail_if_updating_not_allowed():
            if self.status == STATUS_ACCEPTED:
                raise ValidationError(_('Cannot change if status = ' + STATUS_ACCEPTED), code='invalid')

        def _read_uploaded_file_on_change():
            if self.ed_file_upload.file:
                ed_file_upload_name_new = self.ed_file_upload.file.name or ''
                if self._ed_file_upload_name_old != ed_file_upload_name_new:
                    self.ed_uploaded = self.ed_file_upload.file.read().decode('utf-8')
                    self.ed_signed = None
                elif not self.ed_uploaded:
                    self.ed_uploaded = self.ed_file_upload.file.read().decode('utf-8')

        def _set_status_on_upload():
            if self.ed_uploaded:
                if self.ed_uploaded != self._ed_uploaded_old:
                    if self.status in (STATUS_CREATED, STATUS_REJECTED):
                        self.status = STATUS_UPLOADED

        def _set_computed_fields():
                self.ed_uploaded_filename = self.ed_file_upload.file.name
                self.entityID = self._get_entityID()


        _fail_if_updating_not_allowed()
        _read_uploaded_file_on_change()
        _set_status_on_upload()
        _set_computed_fields()
        super().save(*args, **kwargs)

    def _get_entityID(self):
        self.validate()
        eid = self.ed_val.entityID
        if eid:
            return eid
        elif self.ed_uploaded:
            return '?'
        else:
            return ''


class MDstatement(MDstatementAbstract):

    checkout_status = models.ForeignKey(CheckOut, blank=True,
                                        related_name="md_statements",
                                        null=True, on_delete=models.SET_NULL)
