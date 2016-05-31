
from django import template

register = template.Library()


@register.simple_tag
def edit(droplet_price, atual_droplet_price):
    return droplet_price - atual_droplet_price
