from django import forms
from courses.models import Course
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf, .png, .txt, .mp4'})
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:  
                raise forms.ValidationError("File size must be under 10MB.")
            if not file.name.endswith(('.pdf', '.png', '.txt', '.mp4')):
                raise forms.ValidationError("Unsupported file format.")
            return file

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),  
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
