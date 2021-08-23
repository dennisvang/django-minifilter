# django-minifilter

The django-minifilter app provides minimal filter functionality for list views, including:

- a filter search box

- filter links

This is compatible with pagination.

# Quick example

Consider the following simple model:

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
from djminifilter import FilterMixin
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
{% include 'djminifilter/includes/search.html' %}
{% include 'djminifilter/includes/filter.html' %}
<div>
    <ol>
        {% for obj in page_obj %}
            <li>{{ obj.name }} - {{ obj.date }}</li>
        {% endfor %}
    </ol>
</div>
{% include 'djminifilter/includes/pagination.html' %}
</body>
</html>
```


