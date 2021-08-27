# django-minifilter

The django-minifilter package provides minimal filter functionality for list views, including:

- a filter search box

- filter links

The package is compatible with django's pagination.

Here's an example of a very basic list-view, showing a search box that filters by name, and links that filter by year and month:

![basic example of filtered list view](https://raw.githubusercontent.com/dennisvang/django-minifilter/main/documentation/example.png "simple example")

# Installation

The `django-minifilter` package is [available on pypi](https://pypi.org/project/django-minifilter/) and can be installed via `pip`:

```bash
pip install django-minifilter
```

or via `pipenv`:

```bash
pipenv install django-minifilter
```

Then add `minifilter` to `INSTALLED_APPS` in your django settings.

# Quick example

Suppose we have the following simple model, part of an application called `myapp`:

```python
from django.db import models
from django.utils import timezone

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
```

Here's how we would create a generic list view with a search box filter, links that filter by year and month, and pagination:

```python
from django.views import generic
from minifilter.mixins import FilterMixin
from myapp.models import MyModel


class MyListView(FilterMixin, generic.ListView):
    model = MyModel
    template_name = 'myapp/mymodel_list.html'
    paginate_by = 10
    search_fields = ['name']
    filter_parameters = [
        # (url-parameter-name, lookup)
        ('year', 'start_date__year'),
        ('month', 'start_date__month'),
    ]
```

And here's a simple template for the above:

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My filtered list view</title>
</head>
<body>
{% include 'minifilter/includes/search.html' %}
{% include 'minifilter/includes/parameters.html' %}
<div>
    <ol>
        {% for obj in page_obj %}
            <li>{{ obj.name }} - {{ obj.date }}</li>
        {% endfor %}
    </ol>
</div>
{% include 'minifilter/includes/pagination.html' %}
</body>
</html>
```

Instead of a generic class-based view, we could also create a function-based list view:

```python
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
from minifilter.filters import search_filter, parameter_filter
from myapp.models import MyModel


def my_list_view(request):
    queryset = MyModel.objects.all()
    # filter by search term
    queryset, search_form = search_filter(
        queryset=queryset, request=request,
        search_fields=['name'])
    # filter queryset based on url query parameters
    queryset, parameter_choices = parameter_filter(
        queryset=queryset, request=request,
        filter_parameters=[
            ('year', 'start_date__year'),
            ('month', 'start_date__month')])
    # paginate filtered queryset
    # see: https://docs.djangoproject.com/en/stable/topics/pagination/
    paginator = Paginator(object_list=queryset, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # build response
    return TemplateResponse(
        request, template='myapp/mymodel_list.html',
        context=dict(
            page_obj=page_obj,
            parameter_choices=parameter_choices,
            search_form=search_form,
        )
    )
```
