from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Record


# -----------------------------
# Register User Form
# -----------------------------
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# -----------------------------
# Add / Update Record Form
# -----------------------------
class AddRecordForm(forms.ModelForm):

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
        label=""
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
        label=""
    )

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
        label=""
    )

    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
        label=""
    )

    work_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Work Phone", "class": "form-control"}),
        label=""
    )

    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}),
        label=""
    )

    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
        label=""
    )

    state = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "State", "class": "form-control"}),
        label=""
    )

    zipcode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}),
        label=""
    )

    class Meta:
        model = Record
        exclude = ("user",)
