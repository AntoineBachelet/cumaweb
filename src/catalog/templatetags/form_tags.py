from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Add specified CSS classes to a form field.
    
    Usage: {{ form.field|add_class:"form-control" }}
    """
    css_classes = value.field.widget.attrs.get('class', '')
    # If there are already classes, append the new ones
    if css_classes:
        css_classes = f"{css_classes} {arg}"
    else:
        css_classes = arg
    
    return value.as_widget(attrs={'class': css_classes})