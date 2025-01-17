from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import Document, Profile,EmergencyContact,DocumentImage
from django.core.validators import FileExtensionValidator
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


ext_validator = FileExtensionValidator(['jpeg','pdf'])

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    # first_name = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    # last_name = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ('username','email','password1','password2')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with email already exist')
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['username'].widget.attrs['placeholder']= 'username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = "<span class='form-text text-muted'><small>Required. 150 characters or fewer. Letters, digit and @</small></span>"

        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['placeholder']= 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = "<span class='form-text text-muted'><small>pass must containe capital letters and sign</small></span>"

        self.fields['password2'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['placeholder']= 'Confirm-Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = "<span class='form-text text-muted'><small>Password does not match</small></span>"

class UpdateUserForm(forms.ModelForm):
    # image = forms.ImageField(label='profile picture')
    # email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    profile_bio = forms.CharField(label='Profile Bio',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Bio'}))
    first_name = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    phone_number = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile number with country code'}))
    house_address = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Home Address'}))
    city = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}))
    state = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}))
    country = forms.CharField(label='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}))
    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    
    class Meta:
        model = Profile
        fields = ('profile_bio','first_name','last_name','phone_number','gender','house_address','city','state','country')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password'].widget.attrs['disabled'] = 'disabled'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content',]

class DocumentImageForm(forms.ModelForm):
    class Meta:
        model = DocumentImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept':'.jpeg,.png,.pdf'})
        }

DocumentImageFormSet = modelformset_factory(DocumentImage, form=DocumentImageForm, extra=5)  

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'relationship', 'email']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
       