import urllib.parse

import django.db.models as db_models
import django.db.models.aggregates as db_aggregates


class QuerySpec:
    """Parse and handle several kinds of queries for the charts

    The query language is pretty similar to Django's regular queries, with
    two additions:

    * keys & values are urlencoded, and multiple filters can be joined with '&'
    * query + ":" + function name can be used to specify an aggregate function
      to add to the filter

    Examples (is_filter=False):

    ``page__category:count`` (group views by their page's category count)
        ``query.values(x=Count('page__category')).annotate(F('x')

    Examples (is_filter=True):

    ``group__name__contains=Foo%20Bar``
        query.filter(group__name__contains='Foo Bar')
    ``group__users:count__lt=6``
        ``query.annotate(x=Count(group__users)).filter(x__lt=6)``
    ``group__users__isnull``
        ``query.annotate(x=Count(group__users)).filter(x__lt=6)``


    Invalid text strings

    ``group__name__contains``
        invalid because ``__contains`` needs to be compared with a value
    ``page__category``
        invalid because category many-to-many to many relationship
    """

    # nb. make range work right
    FIELD_LOOKUPS = {'exact', 'iexact', 'contains', 'icontains', 'in', 'gt',
                     'gte', 'lt', 'lte', 'startswith', 'endswith', 'range',
                     'date', 'month', 'day', 'week', 'weekday', 'quarter',
                     'time', 'hour', 'minute', 'second', 'isnull', 'regex',
                     'iregex'}

    FUNCS = {
        'avg': db_aggregates.Avg,
        'count': db_aggregates.Count,
        'max': db_aggregates.Max,
        'min': db_aggregates.Min,
        'stddev': db_aggregates.StdDev,
        'sum': db_aggregates.Sum,
        'variance': db_aggregates.Variance,
    }

    def __init__(self, axis_text: str, group_text: str, filter_text: str):
        """
        :param axis_text: Text for the y axis query
        :param group_text: Text for the group by query
        :param filter_text: Text for the filter query
        """
        if '&' in axis_text:
            raise ValueError('Multiple filters (&) not supported in axis text')
        if not axis_text:
            axis_text = 'id:count'
        self.axis_parts = [QuerySpecPart(part, False)
                           for part in axis_text.split('&')
                           if part != '']
        self.group_parts = [QuerySpecPart(part, False)
                            for part in group_text.split('&')
                            if part != '']
        self.filter_parts = [QuerySpecPart(part, True)
                             for part in filter_text.split('&')
                             if part != '']

    def update_queryset(self, qs, x_annotations, x_value):
        annotations = dict(('_django_adminstats_x_{}'.format(k), v) for k, v
                           in x_annotations.items())
        filters = {}
        values = {}
        axis_values = {}
        axis_annotations = {
            '_django_adminstats_x': db_models.F(
                '_django_adminstats_x_{}'.format(x_value))
        }
        final_values = ['_django_adminstats_x']

        for index, qsp in enumerate(self.filter_parts):
            if qsp.func is None:
                filters[qsp.col] = qsp.value
            else:
                key = '_django_adminstats_f_{}'.format(index)
                annotations[key] = qsp.expression_col()
                if qsp.func_lookup:
                    key = key + '__' + qsp.func_lookup
                filters[key] = qs.value
        for index, qsp in enumerate(self.axis_parts):
            value_key = '_django_adminstats_a_{}'.format(index)
            annotate_key = '_django_adminstats_axis_{}'.format(index)
            axis_values[value_key] = qsp.expression_col()
            axis_annotations[annotate_key] = db_models.F(value_key)
            final_values.append(annotate_key)
        for index, qsp in enumerate(self.group_parts):
            value_key = '_django_adminstats_gv_{}'.format(index)
            annotate_key = '_django_adminstats_group_{}'.format(index)
            axis_values[value_key] = qsp.expression_col()
            axis_annotations[annotate_key] = db_models.F(value_key)
            final_values.append(annotate_key)
        if filters:
            qs = qs.filter(**filters)
        return qs.values(**values).annotate(**annotations).values(
            **axis_values).annotate(**axis_annotations).values(*final_values)


class QuerySpecPart:

    FUNCS = {
        'avg': db_aggregates.Avg,
        'count': db_aggregates.Count,
        'max': db_aggregates.Max,
        'min': db_aggregates.Min,
        'stddev': db_aggregates.StdDev,
        'sum': db_aggregates.Sum,
        'variance': db_aggregates.Variance,
    }

    def __init__(self, text: str, is_filter: bool):
        if not is_filter:
            if '=' in text:
                raise ValueError(
                    'Filters (=) not supported in {}'.format(text))
            else:
                col_func, self.value = urllib.parse.unquote(text), ''

        else:
            if '=' not in text:
                raise ValueError(
                    'Filters (=) are required in {}'.format(text))
            else:
                col_func, self.value = (urllib.parse.unquote(part) for part
                                        in text.split('=', 1))

        self.col, func = (col_func.split(':', 1)
                          if ':' in col_func else (col_func, ''))
        func_name, self.func_lookup = (func.split('__', 1) if '__' in func
                                       else (func, ''))
        if func_name == '':
            self.func = None
        elif func_name not in self.FUNCS:
            raise ValueError('Unrecognized function {}', func_name)
        else:
            self.func = self.FUNCS[func_name]
        if is_filter and self.func_lookup:
            raise ValueError(
                'Function lookups aren\'t allowed in filter queries')

    def expression_col(self):
        """Used with not filter lookups, gets the expression to query.

        This will normally return an F() value or an aggregate function
        like Count(field)
        """
        exp = self.func if self.func else db_models.F
        return exp(self.col)
