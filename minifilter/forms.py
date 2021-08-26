from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=150, required=False, label='')

    def set_placeholder(self, text):
        self.fields['search'].widget.attrs.update({'placeholder': text})
