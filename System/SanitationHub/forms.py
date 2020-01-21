from django import forms
from django.core.mail.message import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.conf import settings

from .models import User, Organisation, Dataset

import pandas as pd

class ContactForm(forms.Form):
    '''
    Form for contacting Gather.

    For now, only prints in the console screen the information,
    go to settings.py to add the server details.

    '''
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea())

    def send_mail(self):

        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        content = f'Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}'

        mail = EmailMessage(
            subject=subject,
            body=content,
            from_email= email,
            to=['hub@gatherhub.org'],
            headers={'Reply_To': email}
        ).send()

class SignUpForm(UserCreationForm):

    # Field responsible for linking users and organisations and also responsible for unlocking features
    organisation_code = forms.CharField(label='Organisation Code', max_length=6, required=False)
            
    class Meta:
        model = User
        # Fields that are going to be available on the webpage
        fields = ('first_name', 'last_name','email', 'username')
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        return cleaned_data


    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.organisation_id = self.checkOrg(self.cleaned_data['organisation_code'])
        if commit:
            user.save()
        return user

    def checkOrg(self, typedCode):
        # Verify if organisation code provided by user exists
        organisations = Organisation.objects.all()

        try:
            result = organisations.get(codeID = typedCode)
            return result
        except :
            return None
            # TODO: raise Exception(f'{typedCode} - Company not found!') - make it a pop-up
        
class DatasetUploadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.organisation = kwargs.pop('organisation')
        super(DatasetUploadForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Dataset
        fields = ('filename',)

    def save(self, commit = True):
        data = super().save(commit = True)
        data.ipAddress = self.getClientIp()
        data.organisation = Organisation.objects.get(codeID = self.organisation.codeID)
        if commit:
            data.save()
        return data

    def clean_filename(self):
        actual_csv = self.cleaned_data['filename']
        # Check size and format first, then check if the file has the columns
        name = actual_csv.name
        if name.endswith(settings.FILE_UPLOAD_TYPE):
            if actual_csv.size < int(settings.MAX_UPLOAD_SIZE):
                return self.checkValidity(actual_csv)
            else:
                raise forms.ValidationError("File is too big!")
        else:
            raise forms.ValidationError("File is not in the correct format!")

        

    def checkValidity(self, df):
        # Verify if the file uploaded follows all the rules

        # TODO: Add more rules to be followed accordingly to the data standard resolution
        df_pandas = pd.read_csv(df)
        columns = ['latitude','longitude','capacity','people_usi','last_clean','storage_ty']
        for col in df_pandas.columns:
            if col in columns:
                columns.remove(col)
                
        if columns:
            raise Exception(f"Your dataset don't have all the required columns {columns}")
        else:
            return df


    def getClientIp(self):
        # Get user IP, to verify if the user is uploading from a common place
        xForwardedFor =  self.request.META.get('HTTP_X_FORWARDED_FOR')

        if xForwardedFor:
            ip = xForwardedFor.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        return ip

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name', 'profilePic')
    email = forms.CharField(disabled=True)
    username = forms.CharField(disabled=True)
    

    
