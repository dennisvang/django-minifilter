from django.utils import timezone
from django.test import TestCase, RequestFactory
from tests.models import TestModel
from minifilter.filters import search_filter, parameter_filter


TEST_DATA = [
    dict(name='abc', date=timezone.datetime(2021, 1, 1).date()),
    dict(name='bcd', date=timezone.datetime(2022, 1, 1).date()),
    dict(name='cde', date=timezone.datetime(2022, 2, 1).date()),
    dict(name='def', date=timezone.datetime(2023, 1, 1).date()),
    dict(name='efg', date=timezone.datetime(2023, 2, 1).date()),
    dict(name='fgh', date=timezone.datetime(2023, 3, 1).date()),
]


class QueryTests(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()
        for data in TEST_DATA:
            TestModel.objects.create(**data)

    def test_search_filter_name(self):
        cases = [('', TestModel.objects.count()),
                 ('abcd', 0), ('abc', 1), ('bc', 2), ('c', 3)]
        for search_text, expected_count in cases:
            queryset, form = search_filter(
                queryset=TestModel.objects.all(),
                request=self.request_factory.get(f'?search={search_text}'),
                search_fields=['name'])
            with self.subTest(case=search_text):
                self.assertEqual(expected_count, queryset.count())

    def test_parameter_filter_year(self):
        cases = ['2021', '2022', '2023']
        for year in cases:
            expected_count = int(year[-1])
            queryset, parameter_choices = parameter_filter(
                queryset=TestModel.objects.all(),
                request=self.request_factory.get(f'?year={year}'),
                filter_parameters=[('year', 'date__year')])
            with self.subTest(case=expected_count):
                self.assertEqual(expected_count, queryset.count())
                self.assertEqual(dict(year=cases), parameter_choices)

    def test_parameter_filter_year_month(self):
        queryset, parameter_choices = parameter_filter(
            queryset=TestModel.objects.all(),
            request=self.request_factory.get('?year=2022&month=1'),
            filter_parameters=[
                ('year', 'date__year'), ('month', 'date__month')])
        self.assertEqual(1, queryset.count())
        self.assertEqual(
            dict(year=['2021', '2022', '2023'],
                 month=['1', '2']),  # year 2022 only has months 1 and 2
            parameter_choices)
