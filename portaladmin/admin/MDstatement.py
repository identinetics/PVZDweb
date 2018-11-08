from datetime import timedelta

from django import forms
from django.contrib import admin
from django.utils import timezone
from django.conf import settings

from ..signals import md_statement_edit_starts
from ..models import CheckOut, MDstatement

class MDstatementForm(forms.ModelForm):

    class Meta:
        model = MDstatement
        exclude = ['checkout_status']


@admin.register(MDstatement)
class MDstatementAdmin(admin.ModelAdmin):
    form = MDstatementForm
    actions = None
    readonly_fields = (
        'get_boilerplate_help',
        'get_entityID',
        'status',
        'valid',
        'authorized',
        'is_delete',
        'get_signer_subject',
        'ed_uploaded_filename',
        'get_validation_message',
        'created_at',
        'updated_at',
    )
    list_display = (
        'get_entityID',
        'status',
        'valid',
        'authorized',
        'is_delete',
        'get_validation_message_trunc',
        'updated',
        'admin_note',
    )
    search_fields = ('get_entityID', 'status', )
    fieldsets = (
        (None, {
            'fields': ('get_boilerplate_help', )
        }),
        ('Entity', {
            'fields': (
                'get_entityID',
                'is_delete',
            )
        }),
        ('Datei hochladen', {
            'fields': (
                'ed_file_upload',
                'ed_uploaded_filename',
            )
        }),
        ('Prozess Status', {
            'fields': (
                'status',
                'valid',
                'authorized',
                'get_validation_message',
            )
        }),
        ('Adminsitrative Attribute', {
            'fields': (
                ('created_at', 'updated_at', ),
                'get_signer_subject',
                'admin_note',
            )
        }),
        ('EntityDescriptor XML', {
            'classes': ('collapse',),
            'fields': ('ed_uploaded', ),
        }),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):

        delta_min = getattr(settings, 'PORTALADMIN_CHECKOUT_MINUTES', 15)
        datetime_ago = timezone.now() - timedelta(minutes=delta_min)

        try:
            md_statement = MDstatement.objects.get(id=object_id)
        except MDstatement.DoesNotExist:
            return

        if md_statement.checkout_status:
            # CheckOut by another user
            if md_statement.checkout_status.checkout_by != request.user \
                    and md_statement.checkout_status.created_at > datetime_ago:
                # we need to create custom error page or disable UI of admin form
                assert False, 'The Metadaten Statement is locked by another user, please try again later'

        md_statement_edit_starts.send(sender=MDstatement, md_statement=md_statement, current_user=request.user)

        return super().change_view(request, object_id, form_url, extra_context)


