from django.db import models
from django import forms
from django.contrib.auth.models import User


# TODO: needs more details for *how* to get account details
class Institution(models.Model):
    name = models.CharField(max_length=100)
    login_page = models.URLField()
    notes = models.TextField(null=True, blank=True)
    details_page = models.URLField()

    def __str__(self):
        return self.name


class PasswordField(forms.CharField):
    widget = forms.PasswordInput()


class PasswordModelField(models.CharField):
    """
    Django Password Field
    """

    def formfield(self, **kwargs):
        defaults = {"form_class": PasswordField}
        defaults.update(kwargs)
        return super(PasswordModelField, self).formfield(**defaults)


def getRandomPassword():
    return User.objects.make_random_password(length=24)


class UserInstitution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, blank=True
    )
    login = models.CharField(max_length=100)
    password = PasswordModelField(
        max_length=50, help_text="ch0053 50m37h1n6 600d! :D", default=getRandomPassword
    )

    def __str__(self):
        return "%s %s" % (self.user, self.institution)

    class Meta:
        unique_together = ("user", "institution")


class Account(models.Model):
    user_institution = models.ForeignKey(UserInstitution, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    enabled = models.BooleanField(
        default=True,
        help_text="If disabled, this account will never be fetched, and will not be shown in reports",
    )

    def __str__(self):
        return "(%s) %s" % (self.user_institution, self.name)


class UserLabel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "(%s) %s" % (self.user, self.name)


TRANSACTION_CHOICES = [
    ("DEBIT", "Debit"),
    ("CREDIT", "Credit"),
]


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField()
    # TODO: probably a foreignkey here
    vendor = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    modified_description = models.CharField(max_length=100, null=True, blank=True)
    amount = models.PositiveIntegerField(help_text="amount in cents!")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    # TODO: foreign key
    category = models.CharField(max_length=100)
    notes = models.CharField(max_length=150)
    labels = models.ManyToManyField(UserLabel, blank=True)

    def __str__(self):
        amount = float(self.amount) / 100
        amount = "${:,.2f}".format(amount)
        return "[%s] %s | %s" % (self.date, self.vendor, amount)
