### Evaluated Queryset Paginator

This python package has been developed in order to overcome the issues of the default `django.core.Paginator` which does not paginate the evaluate query sets properly.

#### Functions

  * `__init__()`
    Constructor of the class which takes two parameters as input:
    1. `query_set`: The entire query set that needs to be paginated
    2. `objects_per_page`: The number of objects that are required for each page

  * `paginate()`
    This function is called by the constructor by default and performs the main task of forming the pages

  * `page()`
    Input parameters- `page_number` and returns the total number of pages generated


### Exceptions

  * `EmptyPageException`
    This Exception is raised when the `objects_per_page` value passed is 0

  * `EmptyQuerysetException`
    This Exception is raised when the total number of objects in the `query_set` is 0
