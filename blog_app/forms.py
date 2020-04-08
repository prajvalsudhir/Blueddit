from django import forms
from .models import post,comment
from django.contrib.auth.models import User
from .models import userinfo

class postform(forms.ModelForm):
    class Meta():
        model = post
        #user should be only able to edit the title and text of the post
        fields = ('creator','title','text')
        #adding some widgets to the fields for extra features like for editing the text on selecting it
        widgets = {
            # defining a class so that we can edit the css later
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editarea medium-editor-textarea'}),
            #for medium website like post editing
           }

class commentform(forms.ModelForm):
    class Meta():
        model = comment
        fields = ('author','text')

        widgets = {
             'author':forms.TextInput(attrs={'class': 'textinputclass'}),
             'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    verify_pass = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        all_clean = super().clean()
        opass = all_clean['password']
        vpass = all_clean['verify_pass']

        if opass != vpass:
            raise forms.ValidationError('enter the correct password again')

    class Meta():
        model = User
        fields = ('username','email','password')