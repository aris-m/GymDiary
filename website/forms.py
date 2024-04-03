from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import WorkoutSession, Workout, Goal, HealthMetric
from django.core.exceptions import ValidationError
from django.utils import timezone


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
            
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	
    
class WorkoutSessionForm(forms.ModelForm):
    date = forms.DateField(label="Date", widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}), required=True)
    duration = forms.IntegerField(label="Duration (Minutes)", max_value=10000, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    notes = forms.CharField(label="Notes", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    
    class Meta:
        model = WorkoutSession
        fields = ('date', 'duration', 'notes')

class WorkoutForm(forms.ModelForm):
    name = forms.CharField(label="name", max_length=100, widget=forms.DateTimeInput(attrs={'class': 'form-control'}), required=True)
    
    class Meta:
        model = Workout
        fields = ['name', 'type', 'muscle_groups'] 

    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['type'].label = 'Type'
        self.fields['type'].widget = forms.RadioSelect(choices=Workout.TYPE_CHOICES)
        self.fields['type'].required = True
        
        self.fields['muscle_groups'].widget.attrs['class'] = 'form-check-input'
        self.fields['muscle_groups'].widget.attrs['type'] = 'checkbox'
        self.fields['muscle_groups'].label = 'Muscle Groups'
        self.fields['muscle_groups'].widget = forms.CheckboxSelectMultiple(choices=Workout.MUSCLE_GROUP_CHOICES)
        self.fields['muscle_groups'].required = False
        
class GoalForm(forms.ModelForm):
    description = forms.CharField(label="Description", max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True)
    accomplished = forms.BooleanField(label="Accomplished", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=False, required=False)

    class Meta:
        model = Goal
        fields = ['description', 'accomplished']


class HealthMetricForm(forms.ModelForm):
    date = forms.DateField(label="Date", widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}), required=True)
    weight = forms.FloatField(label="Weight", max_value=1000, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    unit = forms.ChoiceField(label="Unit", choices=HealthMetric.UNITS, widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    calories = forms.FloatField(label="Calories Intake", max_value=100000, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = HealthMetric
        fields = ['date', 'weight', 'unit', 'calories']
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise ValidationError("Date cannot be in the future.")
        if HealthMetric.objects.filter(date=date).exists():
            raise ValidationError("A HealthMetric object with this date already exists.")
        return date