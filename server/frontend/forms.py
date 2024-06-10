from django import forms
from accounts.models import *
from froala_editor.widgets import FroalaEditor

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name', 'description', 'teacher','number', 'academy', 'address', 
            'capacity', 'total_class_hours', 'day_of_week', 'start_time', 'end_time'
        ]
class HomeworkForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = Homework
        fields = ['name', 'difficulty', 'due_date', 'tags', 'content', 'attachment']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['student', 'homework', 'content']