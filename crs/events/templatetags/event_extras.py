from django import template
from django.utils import timezone
from crs.utils import format_phone_number


register = template.Library()


def pluralize_days(n):
    """Возвращает 'день'/'дня'/'дней' в зависимости от числа n."""
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return 'день'
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return 'дня'
    return 'дней'


def _next_occurrence(event_date, today):
    """Ближайшая календарная дата с тем же днём и месяцем, что у event_date —
    в этом году или в следующем. Год самого event_date (например, год рождения)
    для этого расчёта не имеет значения."""
    try:
        candidate = event_date.replace(year=today.year)
    except ValueError:
        # 29 февраля в невисокосный год — переносим на 1 марта
        candidate = event_date.replace(year=today.year, month=3, day=1)

    if candidate < today:
        try:
            candidate = candidate.replace(year=today.year + 1)
        except ValueError:
            candidate = candidate.replace(year=today.year + 1, month=3, day=1)

    return candidate


@register.simple_tag
def days_until(event_date):
    """Возвращает строку вида 'через 3 дня' / 'сегодня' / 'завтра'.
    Считает от ближайшего наступления события (день+месяц), а не от
    исходной даты со старым годом — иначе для дня рождения из 1992-го
    результат всегда был бы «N дней назад»."""
    today = timezone.localdate()
    candidate = _next_occurrence(event_date, today)
    delta = (candidate - today).days

    if delta == 0:
        return 'сегодня'
    elif delta == 1:
        return 'завтра'
    else:
        return f'через {delta} {pluralize_days(delta)}'


@register.filter
def format_phone(value):
    return format_phone_number(value)