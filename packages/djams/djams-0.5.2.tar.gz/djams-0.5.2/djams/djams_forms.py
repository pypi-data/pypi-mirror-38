from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm, PasswordChangeForm, UserChangeForm
from .models import *


def get_generic_model_form(model_class, form_fields, lookup_key=None):

    print("Form_fields: %s" %(form_fields))
    class DynamicForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = form_fields
                
        def __init__(self, *args, **kwargs):
            super(DynamicForm, self).__init__(*args, **kwargs)

            # you can iterate all fields here
            for fname, f in self.fields.items():

                print(fname)
                if 'password' in fname:
                    f.widget = forms.PasswordInput(attrs={'class': 'form-control'})
                    #f.widget.attrs['class'] = 'form-control'

                if f.widget.__class__.__name__ == forms.CheckboxInput().__class__.__name__:
                    f.widget.attrs['class'] = 'form-control left-align-checkbox'
                else:
                    f.widget.attrs['class'] = 'form-control'

    return DynamicForm

def get_generic_inline_modelform_set(model_class, form_fields, lookup_key=None):
    second_model = ADMIN_LOOKUP[lookup_key]['extra_fk_fields']
    modelform_set = inlineformset_factory(model_class)
    
    return modelform_set

class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid() :
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data

def get_one_to_one_combined_form(parentform, childform):

    class One_to_One_ModelForm(CombinedFormBase):
        form_classes = [parentform, childform]

    return One_to_One_ModelForm

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = ADM_CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = ADM_CustomUser
        fields = ('username', 'email')

class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = ADM_CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'is_staff', 'is_active')
        
        widgets = { 'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                    'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                    'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                    'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
                    'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                    'password2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
                  }

class UserEnquiryMsgForm(ModelForm):
    class Meta:
        model = ADM_EnquiryMessage
        fields = {'message'}
        widgets = {'message': forms.Textarea(attrs={'class': 'form-control'})
                  }

class EYTeamForm(ModelForm):
    class Meta:
        model = ADM_Team
        fields = {'name': 'leader'}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'leader': forms.TextInput(attrs={'class': 'form-control'})
                  }

class HelpPageForm(ModelForm):
    class Meta:
        model = ADM_HelpPage
        fields = {'name', 'narrative'}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'narrative': forms.Textarea(attrs={'class': 'form-control'})
                  }

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
                  }

class ProfileForm(ModelForm):
    class Meta:
        model = ADM_UserProfile
        fields = ('employerco', 'resident_country')
        widgets = {'employerco': forms.Select(attrs={'class': 'form-control'}),
                   'resident_country': forms.Select(attrs={'class': 'form-control'}),
        }