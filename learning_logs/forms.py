from django import forms
# from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from .models import Topic, Entry


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_name', 'text']
        labels = {'entry_name': '', 'text': ''}
        widget = forms.CharField(widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10}))
