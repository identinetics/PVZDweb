from django.db import models


class STPbetreiber(models.Model):
    '''
    Stammportalbetreiber als Teilmenge von gvOrg.
    '''

    class Meta:
        verbose_name = 'STPbetreiber'
        verbose_name_plural = 'STPbetreiber'

    gvOuID = models.CharField(
        unique=True,
        verbose_name='gvOuId',
        max_length=32)
    cn = models.CharField(
        verbose_name='Bezeichnung (cn)',
        help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK -  Referat nationale und internationale Koordination)',
        max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum',) #default=django.utils.timezone.now())
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.gvOuID = self.gvOuID.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.gvOuID