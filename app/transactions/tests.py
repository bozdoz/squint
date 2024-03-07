import json
import urllib.request
from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models

from .models import Institution, UserInstitution, Account, Transaction, UserLabel


class TestUserInstitution(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.institution = Institution.objects.create(name="Test Institution")

    def test_str(self):
        user_institution = UserInstitution.objects.create(
            user=self.user, institution=self.institution
        )
        self.assertEqual(str(user_institution), "testuser Test Institution")

    def test_save(self):
        user_institution = UserInstitution(user=self.user, institution=self.institution)
        data = {
            "login": "testlogin",
            "password": "password",
        }
        data = urllib.parse.urlencode(data).encode()

        with urllib.request.urlopen(
            "http://scraper:3000/encrypt", data=data
        ) as response:
            if response.getcode() == 200:
                output = json.loads(response.read())
                if user_institution.login:
                    user_institution.encrypted_login = json.dumps(output["user"])
                if user_institution.password:
                    user_institution.encrypted_password = json.dumps(output["pass"])

        user_institution.save()

        self.assertEqual(
            user_institution.encrypted_login, "eyJ1c2VyIjoiVGVzdGxvZ2luIiwK"
        )
        self.assertEqual(user_institution.encrypted_password, "<KEY>")

    def test_meta_unique_together(self):
        user_institution1 = UserInstitution(
            user=self.user, institution=self.institution
        )
        user_institution2 = UserInstitution(
            user=self.user, institution=self.institution
        )
        with self.assertRaises(models.IntegrityError):
            user_institution1.save()
            user_institution2.save()


class TestAccount(TestCase):
    def setUp(self):
        self.user_institution = UserInstitution.objects.create(
            user=self.user, institution=self.institution
        )

    def test_str(self):
        account = Account.objects.create(
            user_institution=self.user_institution, name="Test Account"
        )
        self.assertEqual(str(account), "(%s) Test Account" % self.user_institution)


class TestTransaction(TestCase):
    def setUp(self):
        self.user_institution = UserInstitution.objects.create(
            user=self.user, institution=self.institution
        )
        self.account = Account.objects.create(
            user_institution=self.user_institution, name="Test Account"
        )

    def test_str(self):
        transaction = Transaction.objects.create(
            account=self.account,
            date=date.today(),
            vendor="Test Vendor",
            description="Test Description",
            modified_description="Test Modified Description",
            amount=1234,
            transaction_type="DEBIT",
            category="Test Category",
            notes="Test Notes",
        )
        self.assertEqual(
            str(transaction),
            "[%s] Test Vendor | .34" % transaction.date,
        )


class TestInstitution(TestCase):
    def test_str(self):
        institution = Institution(name="Test Institution")
        self.assertEqual(str(institution), "Test Institution")


class TestUserLabel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

    def test_str(self):
        label = UserLabel(user=self.user, name="Test Label")
        self.assertEqual(str(label), "testuser Test Label")
