from django import forms
from accounts.models import User
from django.contrib.auth.forms import PasswordChangeForm


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="نام", max_length=50, min_length=4,
                                 widget=forms.TextInput(attrs={"placeholder": "نام"}), required=True)
    last_name = forms.CharField(label="نام خانوادگی", max_length=50, min_length=4,
                                widget=forms.TextInput(attrs={"placeholder": "نام خانوادگی"}), required=True)
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={"placeholder": "ایمیل"}))
    phone = forms.CharField(label="شماره همراه", max_length=14, min_length=11,
                            widget=forms.TextInput(attrs={"placeholder": "شماره همراه"}), required=True,
                            error_messages={'max_length': 'صحیح : "09** *** ****"',
                                            'min_length': 'صحیح : "09** *** ****"'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'col-8'


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="رمز عبور فعلی",
                                   widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور فعلی"}),
                                   required=True)
    new_password1 = forms.CharField(label="رمز عبور جدید",
                                    widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور جدید"}),
                                    required=True)
    new_password2 = forms.CharField(label="تکرار رمز عبور جدید",
                                    widget=forms.PasswordInput(attrs={"placeholder": "تکرار رمز عبور جدید"}),
                                    required=True)

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'col-8'
