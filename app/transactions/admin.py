import urllib.request

from django.contrib import admin

# Register your models here.
from .models import *


class InstitutionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Institution, InstitutionAdmin)


class UserInstitutionAddForm(forms.ModelForm):
    class Meta:
        model = UserInstitution
        fields = "__all__"
        widgets = {"password": forms.PasswordInput(render_value=True)}


# TODO: do something about showing login/passwords
class UserInstitutionChangeForm(forms.ModelForm):
    class Meta:
        model = UserInstitution
        fields = "__all__"
        widgets = {
            "login": forms.TextInput(),
            "password": forms.PasswordInput(render_value=False),
        }


class AccountInline(admin.StackedInline):
    model = Account
    extra = 0
    show_change_link = True


class UserInstitutionAdmin(admin.ModelAdmin):
    form = UserInstitutionChangeForm
    list_display = ["user", "institution"]
    inlines = [AccountInline]

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["user"] = request.user.pk

        return initial

    def save_model(self, request, obj, form, change):
        # TODO: encrypt password if changed
        if change and form.is_valid():
            response = urllib.request.urlopen("http://scraper:3000")

            if response.getcode() == 200:
                output = response.read()
                print(output)
            else:
                print(response.getcode())

        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = UserInstitutionAddForm
        return super().get_form(request, obj, **kwargs)


admin.site.register(UserInstitution, UserInstitutionAdmin)


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)


class UserLabelAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["user"] = request.user.pk

        return initial


admin.site.register(UserLabel, UserLabelAdmin)
