import json
import urllib.request

from django.db import models
from django import forms
from django.contrib.auth.models import User


class Institution(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserInstitution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, blank=True
    )
    login = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    encrypted_login = models.TextField(null=True, blank=True)
    encrypted_password = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.login or self.password:
            data = {
                "login": self.login,
                "password": self.password,
            }
            data = urllib.parse.urlencode(data).encode()

            with urllib.request.urlopen(
                "http://scraper:3000/encrypt", data=data
            ) as response:
                if response.getcode() == 200:
                    output = json.loads(response.read())
                    print(output)
                    if self.login:
                        self.encrypted_login = json.dumps(output["user"])
                    if self.password:
                        self.encrypted_password = json.dumps(output["pass"])

            self.login = None
            self.password = None

        # do something with the response
        # Add your custom logic here
        super().save(*args, **kwargs)

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
    # TODO: foreign key, optional?
    category = models.CharField(max_length=100)
    # TODO: optional
    notes = models.CharField(max_length=150)
    labels = models.ManyToManyField(UserLabel, blank=True)

    def __str__(self):
        amount = float(self.amount) / 100
        amount = "${:,.2f}".format(amount)
        return "[%s] %s | %s" % (self.date, self.vendor, amount)
