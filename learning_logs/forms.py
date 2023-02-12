from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_name', 'text', 'tags']
        labels = {'entry_name': 'Say my name!', 'text': '', 'tags': 'Add tags'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
