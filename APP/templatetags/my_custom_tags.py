from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite buscar um valor em um dicionário pela sua chave."""
    return dictionary.get(key)