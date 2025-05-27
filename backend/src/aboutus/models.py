from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Semester
from core.utils import DraftJSEditorField
from sso.models import User

class KISADivision(models.IntegerChoices):
    WEB = 1, _('Web Division')
    FINANCE = 2, _('Finace Division')
    PPR = 3, _('PPR Division')
    EVENTS = 4, _('Events Division')
    WELFARE = 5, _('Welfare Division')
    SECRETARY = 6, _('Secretary')
    VICE_PRESIDENT = 7, _('Vice President')
    PRESIDENT = 8, _('President')

class KISAMember(models.Model):
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)
    image = models.ImageField(null=True, blank=True)
    sns_link = models.URLField(blank=True, null=True)

class KISARole(models.Model):
    members = models.ManyToManyField(KISAMember)
    semester = models.ForeignKey(Semester, models.CASCADE, db_index=True)
    division = models.IntegerField(choices=KISADivision.choices)
    is_head = models.BooleanField()

    class Meta:
        unique_together = ['semester', 'division', 'is_head']

    def __str__(self) -> str:
        return str(self.semester)

class KISADivisionContent(models.Model):
    division = models.IntegerField(choices=KISADivision.choices, db_index=True)
    content = DraftJSEditorField()