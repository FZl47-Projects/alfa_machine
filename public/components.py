from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MenuComponent(LoginRequiredMixin, TemplateView):
    USER_ROLES_MENU = {
        'super_user': 'general/components/menu.html',
        'control_project_user': '',
        'control_quality_user': '',
        'commerce_user': '',
        'procurement_commerce_user': '',
        'financial_user': '',
        'warehouse_user': '',
        'production_user': '',
        'technical_user': '',
    }

    def get_template_names(self):
        user_role = self.request.user.role
        try:
            return [self.USER_ROLES_MENU[user_role]]
        except KeyError:
            raise KeyError('you must define user role and template name in MenuComponent')
