from math import ceil
from django.test import TestCase, RequestFactory
from django.views.generic import ListView
from tests.models import TestModel
from minifilter.mixins import FilterMixin


class MockView(FilterMixin, ListView):
    model = TestModel
    search_fields = ['name']
    filter_parameters = [('year', 'date__year'), ('month', 'date__month')]


class FilterMixinTests(TestCase):
    fixtures = ['test_data']

    def test_get_context_data_pagination(self):
        mock_view = MockView(paginate_by=2)
        cases = [2021, 2022, 2023]
        for year in cases:
            # https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#testing-class-based-views
            mock_view.setup(request=RequestFactory().get(f'?year={year}'))
            context = mock_view.get_context_data()
            paginator = context['paginator']
            expected_objects = list(TestModel.objects.filter(date__year=year))
            expected_pages = ceil(len(expected_objects) / mock_view.paginate_by)
            with self.subTest(case=year):
                self.assertEqual(expected_pages, paginator.num_pages)
                self.assertEqual(
                    expected_objects,
                    [obj for page_obj in paginator for obj in page_obj],
                )
