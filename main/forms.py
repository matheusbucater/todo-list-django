from django import forms

class CreateNewListForm(forms.Form):

    title = forms.CharField(label='Título', max_length=255)
    task = forms.CharField(label='Tarefa', max_length=255)
