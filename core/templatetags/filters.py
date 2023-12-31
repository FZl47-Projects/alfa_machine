from django import template


# Create library instance
register = template.Library()


# Check user has permission to modify
@register.filter
def inquiry_has_permission(user, url_name: str = None):
    allowed = ['commerce_user', 'procurement_commerce_user']

    if user.role == 'super_user' or (user.role in allowed and not url_name):
        return True

    if user.role in allowed and not url_name == 'inquiry':
        return True

    return False


# Check user has permission to modify
@register.filter
def task_has_permission(user):
    allowed = ['super_user', 'control_project_user']

    if user.role in allowed:
        return True

    return False
