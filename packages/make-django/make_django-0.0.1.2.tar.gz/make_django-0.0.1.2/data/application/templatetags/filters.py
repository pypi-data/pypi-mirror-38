from django import template
import datetime as dt
import re


register = template.Library()


@register.filter
def minus(value, arg):
    return (value or 0) - (arg or 0)


@register.filter
def plus(value, arg):
    return (value or 0) + (arg or 0)


@register.filter
def multiply(value, arg):
    return (value or 0) * (arg or 0)


@register.filter
def to_int(value):
    return int(value)


@register.filter(is_safe=False)
def empty(value, arg=''):
    """If value is empty, use given default."""
    if not value:
        return arg
    return value


@register.filter()
def wrap(value, arg=''):
    if value:
        return str(arg).replace('%s', str(value))
    return ''


@register.filter()
def withs(value, arg=''):
    if value:
        return str(value).replace('%s', str(arg))
    return ''


@register.filter()
def replace(value, arg=''):
    if value and arg:
        return str(value).replace(re.split(r'\s*\|\s*', arg)[0], re.split(r'\s*\|\s*', arg)[1])
    return ''


@register.filter()
def split(value, arg=''):
    if value and arg:
        return str(value).split(str(arg))
    return ''


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in re.split(r'\s*,\s*', the_list)


@register.filter()
def match(value, arg=''):
    if re.match(arg, value):
        return True


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value, append=False, sep=''):
        self.var_name = var_name
        self.var_value = var_value
        self.append = append
        self.sep = sep

    def render(self, context):
        values = []

        for value in self.var_value.split('+'):
            try:
                value = template.Variable(value).resolve(context)
            except template.VariableDoesNotExist:
                value = ''
            values.append(value)

        if len(values) > 1:
            value = self.sep.join([v for v in values if v])
        else:
            value = values[0]

        if not self.append:
            context[self.var_name] = value
        else:
            if self.sep and context[self.var_name]:
                value = self.sep + value
            context[self.var_name] += value

        return u""


# Usage: {% set some_var = '123' %}
@register.tag(name='set')
def set_var(parser, token):
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = \"<var_value>\" %}")

    append = True if parts[2] == '+=' else False
    sep = ''
    if len(parts) > 4:
        arg = parts[4].split('=')

        if len(arg) == 2 and arg[0] == 'sep':
            sep = re.sub(r'^["\']|[\'"]$', '', arg[1])

    return SetVarNode(parts[1], parts[3], append, sep)


@register.filter
def humanize_time(t, args=None, hours_in_day=24, show_days=True):
    hours_in_day = hours_in_day
    show_days = show_days
    if isinstance(args, str):
        args = re.split(',\s*', args)
        if args:
            hours_in_day = int(args[0])
            if len(args) == 2:
                show_days = False if args[1] in (None, 'False') else True

    if t is not None:
        if isinstance(t, str) and t.isdigit():
            t = int(t)

        if isinstance(t, (int, float)):
            postfix = 's'
            if t >= 60:
                t /= 60; postfix = 'm'
                if t >= 60:
                    t /= 60; postfix = 'h'
                    if show_days and t >= hours_in_day:
                        t /= hours_in_day; postfix = 'd'

            return '%s%s' % (int(t), postfix)
        return t


@register.filter
def time(sec):
    if sec > 86400:
        return '%id %s' % (sec / 86400, time(sec % 86400))
    elif sec > 3600:
        return '%ih %s' % (sec / 3600, time(sec % 3600))
    elif sec > 0:
        return '%02im %02is' % (sec / 60, sec % 60)
    else:
        return '%is' % sec


@register.filter
def simple_time(sec):
    d = dt.timedelta(seconds=sec)
    s = re.sub(r':00$', '', str(d))
    return re.sub(r'(^[1-9]):', r'0\1:', s)


@register.filter
def date(value, _format='%d.%m.%Y'):
    if value.__class__.__name__ == 'date':
        return value.strftime(_format)
    return value


@register.filter
def datetime(value, _format='%d.%m.%Y %H:%M'):
    if value.__class__.__name__ == 'Timestamp':
        value = value.to_pydatetime()

    if isinstance(value, dt.datetime):
        return value.strftime(_format)

    elif isinstance(value, dt.date):
        return value.strftime(_format or '%d.%m.%Y')

    elif isinstance(value, dt.timedelta):
        return humanize_time(value.total_seconds())

    return value


@register.filter
def datetime_delta(delta):
    if delta:
        map = {
            'д': delta.days,
            'ч':  int(delta.seconds/60/60),
            'м':  int(delta.seconds/60 % 60),
            'с':  int(delta.seconds % 60),
        }

        out = ''
        for k, v in map.items():
            if v:
                out += f'{v}{k} '

        return out.rstrip()
