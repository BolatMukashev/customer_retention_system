from django import template
from django.utils import timezone

register = template.Library()


def pluralize_days(n):
    """Возвращает 'день'/'дня'/'дней' в зависимости от числа n."""
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return 'день'
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return 'дня'
    return 'дней'


@register.simple_tag
def days_until(event_date):
    """Возвращает строку вида 'через 3 дня' / 'сегодня' / 'вчера'."""
    today = timezone.localdate()
    delta = (event_date - today).days

    if delta == 0:
        return 'сегодня'
    elif delta == 1:
        return 'завтра'
    elif delta == -1:
        return 'вчера'
    elif delta > 0:
        return f'через {delta} {pluralize_days(delta)}'
    else:
        return f'{abs(delta)} {pluralize_days(delta)} назад'