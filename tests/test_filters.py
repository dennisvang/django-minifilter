import string
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase, RequestFactory
from tests.models import TestModel
from minifilter.filters import search_filter, parameter_filter


class QueryTests(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()
        alphabet = string.ascii_lowercase
        name_length = 3
        for i in range(len(alphabet) - name_length + 1):
            name = alphabet[i:i+name_length]
            date = timezone.now() + timedelta(hours=i*12)
            TestModel.objects.create(name=name, date=date)

    def test_search_filter(self):
        cases = [('', TestModel.objects.count()),
                 ('abcd', 0), ('abc', 1), ('bc', 2), ('c', 3)]
        for search_text, expected_count in cases:
            queryset, form = search_filter(
                queryset=TestModel.objects.all(),
                request=self.request_factory.get(f'?search={search_text}'),
                search_fields=['name'])
            with self.subTest(search_text=search_text):
                self.assertEqual(expected_count, queryset.count())

    def test_parameter_filter(self):
        pass
