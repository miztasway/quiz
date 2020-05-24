from django import forms

from .models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password_again(self, *args, **kwargs):
        p = self.cleaned_data['password']
        p_2 = self.cleaned_data['password_again']
        if p_2 != p:
            raise forms.ValidationError('Password inputs must be the same')
        return p