import collections
import datetime
from typing import Mapping

import django.db.models.functions as db_functions
from django.db.models import Count, DateField

from . import models


class Registration:

    date_field = 'date'

    def get_queryset(self):
        raise NotImplementedError

    def get_span_queryset(self, _period_step, start, end):
        qs = self.get_queryset().annotate(
            _date_field=db_functions.Cast(self.date_field, DateField()))
        kwargs = {'_date_field__gte': start, '_date_field__lt': end}
        return qs.filter(**kwargs)

    def get_group_queryset(self, period_step, start, end):
        query = self.get_span_queryset(period_step, start, end)
        ann_kwargs = {}
        if period_step == models.STEP_DAY:
            ann_kwargs['_date'] = db_functions.TruncDay(
                self.date_field, output_field=DateField())
            ann_kwargs['_month'] = db_functions.TruncMonth(self.date_field)
            ann_kwargs['_year'] = db_functions.TruncYear(self.date_field)
        if period_step == models.STEP_MONTH:
            ann_kwargs['_date'] = db_functions.TruncMonth(
                self.date_field, output_field=DateField())
            ann_kwargs['_year'] = db_functions.TruncYear(self.date_field)
        if period_step == models.STEP_YEAR:
            ann_kwargs['_date'] = db_functions.TruncYear(
                self.date_field, output_field=DateField())

        return query.annotate(**ann_kwargs).values(*ann_kwargs.keys())

    def count(self, start, end, period_step) -> Mapping[datetime.date, int]:
        group = self.get_group_queryset(period_step, start, end)
        result = dict((item['_date'], item['_c']) for item in
                      group.annotate(_c=Count('id')).values('_c', '_date'))
        return result


class Registry(collections.OrderedDict):

    def register(self, reg: Registration):
        self[reg.key] = reg

    def choices(self):
        for key, value in self.items():
            yield key, value.label

    def count(self, criteria):
        stats = self[criteria.stats_key]
        start, end = criteria.chart.span()
        return stats.count(start, end, criteria.chart.period_step)


class ModelRegistration(Registration):

    def __init__(self, model):
        self.model = model
        self.meta = getattr(self.model, '_meta')
        if not self.meta:
            raise RuntimeError(
                'Model {} is missing Meta class'.format(self.model))

    def get_queryset(self):
        return self.model.objects

    @property
    def key(self):
        return '{}.{}'.format(self.meta.app_label, self.meta.model_name)

    @property
    def label(self):
        return self.meta.verbose_name_plural.title()


class MetricRegistration(Registration):

    def __init__(self, metric):
        # metric is probably a lazy object
        self.metric = metric
        lazy_func = getattr(metric, '_setupfunc')
        if lazy_func:
            contents = lazy_func.__closure__[1].cell_contents
            self.ref = contents['ref']
            domain = contents['domain']
            lazy_func = getattr(domain, '_setupfunc')
            if lazy_func:
                contents = lazy_func.__closure__[1].cell_contents
                self.domain_ref = contents['ref']
            else:
                self.domain_ref = metric.domain.ref
        else:
            self.ref = metric.ref

    @property
    def key(self):
        return 'trackstats:{}.{}'.format(self.domain_ref, self.ref)

    @property
    def label(self):
        return '{} {} Stats'.format(self.domain_ref, self.ref).title()

    def get_queryset(self):
        from trackstats.models import StatisticByDate
        return StatisticByDate.objects.filter(metric=self.metric)

    def get_span_queryset(self, period_step, start, end):
        from trackstats.models import Period
        kwargs = {self.date_field + '__gte': start,
                  self.date_field + '__lt': end}
        if period_step == models.STEP_DAY:
            kwargs['period'] = Period.DAY
        elif period_step == models.STEP_MONTH:
            kwargs['period'] == Period.MONTH
        else:
            # trackstats doesn't actually support year
            kwargs['period'] = Period.LIFETIME
        return self.get_queryset().filter(**kwargs)

    def count(self, start, end, period_step) -> Mapping[datetime.date, int]:
        group = self.get_group_queryset(period_step, start, end)
        result = dict((item['_date'], item['value']) for item in
                      group.values('value', '_date'))
        return result


REGISTRY = Registry()


def register(registration: Registration):
    REGISTRY.register(registration)


def register_model(model):
    register(ModelRegistration(model))


def register_metric(metric):
    register(MetricRegistration(metric))


def get_registry_ids():
    return REGISTRY.keys()
