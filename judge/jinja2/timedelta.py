import datetime

from judge.jinja2 import registry
from judge.utils.timedelta import nice_repr


@registry.filter
def timedelta(value, display='long'):
    if value is None:
        return value
    return nice_repr(value, display)


@registry.filter
def second(value: datetime.time):
    return value.hour * 3600 + value.minute * 60 + value.second + (value.microsecond // 1000) / 1000


@registry.filter
def timestampdelta(value, display='long'):
    value = datetime.timedelta(seconds=value)
    return timedelta(value, display)


@registry.filter
def seconds(timedelta):
    return timedelta.total_seconds()


@registry.filter
@registry.render_with('time-remaining-fragment.html')
def as_countdown(timedelta):
    return {'countdown': timedelta}
