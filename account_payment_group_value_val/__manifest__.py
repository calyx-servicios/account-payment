# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Payment Value Validation",
    "summary": """
        This module adds a validation in values of 
        Supplier Payment and Partner Anticipe""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["JhoneM"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["base", "account_payment_group"],
    "data": ["views/res_config_settings.xml"],
}
