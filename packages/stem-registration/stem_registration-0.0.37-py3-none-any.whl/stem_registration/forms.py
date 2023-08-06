from cities_light.models import Country
from django.conf import settings
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget
from registration.forms import RegistrationFormUniqueEmail
from django.forms.fields import CharField, ImageField

from django import forms
from django.utils.translation import ugettext as _

from stem_registration.models import RegistrationData


class RegistrationDataForm(forms.ModelForm):
    class Meta:
        model = RegistrationData
        fields = '__all__'


class RegistrationForm(RegistrationFormUniqueEmail):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        registration_form_fields = RegistrationDataForm().fields
        if not getattr(settings, 'SHOW_LOGIN', True):
            self.fields['username'].required = False

        if not getattr(settings, 'SHOW_LAST_FIRST_NAME', True):
            # Делаем поля скрытыми
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()

        if getattr(settings, 'SHOW_CONTRACTOR_TYPE', True):
            # self.fields['contractor_type'] = registration_form_fields['contractor_type']
            # self.fields['contractor_type'].choices = RegistrationData.CONTRACTOR_TYPE
            # self.fields['contractor_type'].initial = RegistrationData.PRIVATE_PERSON
            # self.fields['contractor_type'].widget = forms.RadioSelect()
            self.fields['contractor_type'] = forms.ChoiceField(
                required=False,
                choices=RegistrationData.CONTRACTOR_TYPE,
                widget=forms.RadioSelect(),
                label=_("Компания"), initial=RegistrationData.PRIVATE_PERSON
            )

        _show_address = getattr(settings, 'SHOW_ADDRESS', True)
        if _show_address:
            self.fields['address'] = registration_form_fields['address']
            self.fields['address'].required = True
            self.fields['address_optional'] = registration_form_fields['address_optional']
            self.fields['city'] = registration_form_fields['city']
            self.fields['country'] = registration_form_fields['country']
            self.fields['country'].widget = ModelSelect2Widget(
                    model=Country,
                    search_fields=['name__icontains'],
                )
            self.fields['zip'] = registration_form_fields['zip']

            # self.fields['address'] = CharField(max_length=30, label=_("Адрес"))
            # self.fields['address_optional'] = CharField(max_length=30, required=False, label=_("Адрес дополнительно"))
            # self.fields['city'] = CharField(max_length=30, label=_("Город"))
            # self.fields['country'] = forms.ModelChoiceField(
            #     queryset=Country.objects.all(),
            #     widget=ModelSelect2Widget(
            #         model=Country,
            #         search_fields=['name__icontains'],
            #     )
            # )
            # self.fields['zip'] = CharField(max_length=30, label=_("Индекс"))

        _show_billing_address = getattr(settings, 'SHOW_BILLING_ADDRESS', True)
        if _show_billing_address:
            if _show_address:
                self.fields['same'] = forms.BooleanField(
                    widget=forms.CheckboxInput(), label=_("Same"),
                    required=False, initial=True
                )

            self.fields['billing_address'] = registration_form_fields['billing_address']
            self.fields['bill_address_optional'] = registration_form_fields['bill_address_optional']
            self.fields['bill_city'] = registration_form_fields['bill_city']
            self.fields['bill_zip'] = registration_form_fields['bill_zip']
            self.fields['bill_country'] = registration_form_fields['bill_country']
            self.fields['bill_country'].widget = ModelSelect2Widget(
                model=Country,
                search_fields=['name__icontains'],
            )

            # self.fields['billing_address'] = CharField(max_length=30, required=False, label=_("Адрес"))
            # self.fields['bill_address_optional'] = CharField(
            #     max_length=30, required=False,
            #     label=_("Адрес дополнительно")
            # )
            # self.fields['bill_city'] = CharField(max_length=30, required=False, label=_("Город"))
            # self.fields['bill_zip'] = CharField(max_length=30, required=False, label=_("Индекс"))
            # self.fields['bill_country'] = forms.ModelChoiceField(
            #     required=False,
            #     queryset=Country.objects.all(),
            #     widget=ModelSelect2Widget(
            #         model=Country,
            #         search_fields=['name__icontains'],
            #     )
            # )

        if getattr(settings, 'SHOW_NUMBER', True):
            self.fields['number'] = registration_form_fields['number']
            self.fields['number'].required = getattr(settings, 'NUMBER_IS_REQUIRED', True)
            # self.fields['number'] = CharField(
            #     max_length=30, label=_("Номер телефона"),
            #     required=getattr(settings, 'NUMBER_IS_REQUIRED', True)
            # )

        if getattr(settings, 'SHOW_TAX_NUMBER', True):
            self.fields['tax_number'] = registration_form_fields['tax_number']
            self.fields['tax_number'].required = getattr(settings, 'TAX_NUMBER_IS_REQUIRED', True)
            # self.fields['tax_number'] = CharField(
            #     max_length=12, required=getattr(settings, 'TAX_NUMBER_IS_REQUIRED', True), label=_('ИНН')
            # )
        if getattr(settings, 'SHOW_ID_CARD_FIELDS', True):
            for field in ('file1', 'file2', 'file3', 'file4', 'file5'):
                self.fields[field] = registration_form_fields[field]
                self.fields[field].widget = forms.FileInput(attrs={'class': 'd-none file'})

            # self.fields['file1'] = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
            # self.fields['file2'] = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
            # self.fields['file3'] = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
            # self.fields['file4'] = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
            # self.fields['file5'] = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))

        if getattr(settings, 'SHOW_NAME_LEGAL', True):
            self.fields['name_legal'] = registration_form_fields['name_legal']
            self.fields['name_legal'].required = getattr(settings, 'NAME_LEGAL_IS_REQUIRED', False)
            # self.fields['name_legal'] = CharField(
            #     max_length=255, label=_("Полное наименование"),
            #     required=getattr(settings, 'NAME_LEGAL_IS_REQUIRED', False)
            # )
        if getattr(settings, 'SHOW_ACCOUNTING_NUMBER', True):
            self.fields['accounting_number'] = registration_form_fields['accounting_number']
            # self.fields['accounting_number'] = CharField(max_length=30, label=_("ЕГРПОУ"), required=False)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.is_active = False

        if user.username == '':
            user.username = user.email

        user.save()

        fields = (
            'contractor_type',
            'address',
            'address_optional',
            'country',
            'city',
            'zip',
            'billing_address',
            'bill_address_optional',
            'bill_city',
            'bill_zip',
            'number',
            'tax_number',
            'country',
            'bill_country',
            'file1', 'file2', 'file3', 'file4', 'file5',
        )

        registration_data = {}
        for item in self.cleaned_data:
            if item in fields:
                registration_data[item] = self.cleaned_data[item]

        RegistrationData.objects.create(user=user, **registration_data)

        if commit:
            user.save()
            return user
