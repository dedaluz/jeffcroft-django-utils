from django import template
from django.utils.safestring import mark_safe
 
register = template.Library()

@register.filter
def get_links(value):
  """
  Returns links found in an (X)HTML string as Python objects for iteration in templates.

    <ul>
      {% for link in object.body|markdown|get_links %}
        <li><a href="{{ link.href }}">{{ link.title }}</a></li>
      {% endfor %}
    </ul>

  """
  
  try:
    from bs4 import BeautifulSoup
  except ImportError:
    from django.conf import settings
    if settings.DEBUG:
      raise template.TemplateSyntaxError, "Error in {% get_links %} filter: The Python BeautifulSoup library aren't installed."
    return value
  soup = BeautifulSoup(value)
  return [ {'href': a.get('href'), 'title': a.get('title', a.text) } for a in soup.find_all('a') ]