from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RoomForm(forms.Form):
    room = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'room_name'}),label=False)
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        room = cleaned_data.get('room')
        if Room.objects.filter(name=room):
            alert("Room Name is already taken.")
            raise forms.ValidationError("Room Name is already taken.")
        
        return cleaned_data