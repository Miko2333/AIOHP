from django import forms
from accounts.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name', 'description', 'teacher','number', 'academy', 'address', 
            'capacity', 'total_class_hours', 'day_of_week', 'start_time', 'end_time'
        ]
