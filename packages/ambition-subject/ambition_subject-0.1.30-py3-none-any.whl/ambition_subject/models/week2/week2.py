from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import date_not_future, datetime_not_future
from edc_constants.choices import YES_NO
from edc_visit_tracking.managers import CrfModelManager

from ...managers import CurrentSiteManager
from ..list_models import Antibiotic, Day14Medication, OtherDrug
from ..model_mixins import CrfModelMixin, ClinicalAssessmentModelMixin


class Week2(ClinicalAssessmentModelMixin, CrfModelMixin):

    discharged = models.CharField(
        verbose_name='Discharged?',
        max_length=25,
        choices=YES_NO)

    discharge_date = models.DateField(
        validators=[date_not_future],
        null=True,
        blank=True)

    research_discharge_date = models.DateField(
        verbose_name='On which date did the research team feel the patient was well '
        'enough to go home?',
        validators=[date_not_future],
        null=True,
        blank=True)

    died = models.CharField(
        verbose_name='Died?',
        max_length=25,
        choices=YES_NO)

    death_date_time = models.DateTimeField(
        validators=[datetime_not_future],
        null=True,
        blank=True)

    ampho_start_date = models.DateField(
        verbose_name='Amphotericin B start date: ',
        validators=[date_not_future],
        null=True,
        blank=True)

    ampho_end_date = models.DateField(
        verbose_name='Amphotericin B end date: ',
        validators=[date_not_future],
        null=True,
        blank=True)

    ampho_duration = models.IntegerField(
        verbose_name='Amphotericin B treatment duration',
        null=True,
        blank=True)

    flucon_start_date = models.DateField(
        verbose_name='Fluconazole start date:',
        validators=[date_not_future],
        null=True,
        blank=True)

    flucon_stop_date = models.DateField(
        verbose_name='Fluconazole end date:',
        validators=[date_not_future],
        null=True,
        blank=True)

    flucon_duration = models.IntegerField(
        verbose_name='Fluconazole treatment duration:',
        null=True,
        blank=True)

    flucy_start_date = models.DateField(
        verbose_name='Flucytosine start date:',
        validators=[date_not_future],
        null=True,
        blank=True)

    flucy_stop_date = models.DateField(
        verbose_name='Flucytosine end date:',
        validators=[date_not_future],
        null=True,
        blank=True)

    flucy_duration = models.IntegerField(
        verbose_name='Flucytosine treatment duration:',
        null=True,
        blank=True)

    ambi_start_date = models.DateField(
        verbose_name='Ambisome start date:',
        validators=[date_not_future],
        null=True,
        blank=True)

    ambi_stop_date = models.DateField(
        verbose_name='Ambisome end date:',
        validators=[date_not_future],
        null=True,
        blank=True)

    ambi_duration = models.IntegerField(
        verbose_name='Ambisome treatment duration:',
        null=True,
        blank=True)

    drug_intervention = models.ManyToManyField(
        OtherDrug,
        verbose_name="Other drugs/interventions given during first 14 days",)

    drug_intervention_other = models.TextField(
        verbose_name='If other, please specify:',
        blank=True,
        # max_length=50,
        null=True)

    antibiotic = models.ManyToManyField(
        Antibiotic,
        blank=True,
        verbose_name="Were any of the following antibiotics given?",)

    antibiotic_other = models.TextField(
        verbose_name='If other antibiotics, please specify:',
        # max_length=50,
        null=True,
        blank=True)

    blood_received = models.CharField(
        verbose_name='Blood transfusion received?',
        max_length=25,
        choices=YES_NO)

    units = models.IntegerField(
        verbose_name='If YES, no. of units',
        validators=[MinValueValidator(1)],
        null=True,
        blank=True)

    temperature = models.FloatField(
        verbose_name='Temperature',
        null=True,
        blank=True,
        default=None)

    weight = models.DecimalField(
        verbose_name='Weight:',
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        decimal_places=1,
        max_digits=4,
        help_text='kg')

    medicines = models.ManyToManyField(
        Day14Medication,
        verbose_name='Medicine day 14:')

    medicine_other = models.TextField(
        verbose_name='If other, please specify:',
        null=True,
        blank=True)

    significant_dx = models.CharField(
        verbose_name='Other significant diagnoses since enrolment?',
        max_length=25,
        choices=YES_NO)

    significant_dx_datetime = models.DateTimeField(
        validators=[date_not_future],
        null=True,
        blank=True)

    flucon_missed_doses = models.CharField(
        verbose_name='Were any Fluconazole drug doses missed?',
        max_length=25,
        choices=YES_NO)

    amphotericin_missed_doses = models.CharField(
        verbose_name='Were any Amphotericin B drug doses missed?',
        max_length=25,
        choices=YES_NO)

    other_significant_dx = models.CharField(
        verbose_name='Other significant diagnosis since enrollment?',
        max_length=5,
        choices=YES_NO)

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = 'Week 2'
        verbose_name_plural = 'Week 2'
