from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={"placeholder": "ایمیل"}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور"}),
                               required=True)


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="نام", max_length=50, min_length=4,
                                 widget=forms.TextInput(attrs={"placeholder": "نام"}), required=True)
    last_name = forms.CharField(label="نام خانوادگی", max_length=50, min_length=4,
                                widget=forms.TextInput(attrs={"placeholder": "نام خانوادگی"}), required=True)
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={"placeholder": "ایمیل"}))
    phone = forms.CharField(label="شماره همراه", max_length=14, min_length=11,
                            widget=forms.TextInput(attrs={"placeholder": "شماره همراه"}), required=True,
                            error_messages={'max_length': 'صحیح : "09** *** ****"',
                                            'min_length': 'صحیح : "09** *** ****"'})
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور"}),
                                required=True)
    password2 = forms.CharField(label="تکرار رمز عبور", required=True,
                                widget=forms.PasswordInput(attrs={"placeholder": "تکرار رمز عبور"}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']