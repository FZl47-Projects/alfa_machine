from django.views.generic import TemplateView


class MenuComponent(TemplateView):
    USER_ROLES_MENU = {
        'super_user': 'general/components/menu.html',
        'control_project_user': 'control_project/components/menu.html',
        'control_quality_user': 'control_quality/components/menu.html',
        'commerce_user': 'commerce/components/menu.html',
        'procurement_commerce_user': 'commerce/components/menu.html',
        'financial_user': 'financial/components/menu.html',
        'warehouse_user': 'warehouse/components/menu.html',
        'production_user': 'production/components/menu.html',
        'technical_user': 'technical/components/menu.html',
    }

    def get_template_names(self):
        user_role = self.request.user.role
        try:
            return [self.USER_ROLES_MENU[user_role]]
        except KeyError:
            raise KeyError('you must define user role and template name in MenuComponent')
