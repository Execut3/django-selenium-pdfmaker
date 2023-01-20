from django.db import models

from django.utils.translation import ugettext_lazy as _


def file_upload_to(instance, filename):
    return "converted-pdf/{}".format(instance.id, filename)


class ConvertedPDF(models.Model):
    url = models.URLField(
        verbose_name=_('Visited URL')
    )
    file = models.FileField(
        upload_to=file_upload_to,
        verbose_name=_('PDF File')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )

    def __str__(self):
        return f'{self.url}, {self.file.name}'
