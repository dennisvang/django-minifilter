from django.test import TestCase
from minifilter.forms import SearchForm


class SearchFormTests(TestCase):
    def test_set_placeholder(self):
        text = 'some placeholder'
        form = SearchForm()
        form.set_placeholder(text=text)
        self.assertIn(text, form.as_p())
