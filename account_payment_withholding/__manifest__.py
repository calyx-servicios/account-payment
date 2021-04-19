# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "withholding number/Payment Amount in Company Currency",
    "summary": """
        Add a columns to payment report""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DarwinAndrade"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["account_withholding", "account_payment_group"],
    "data": ["views/account_payment_view.xml"],
}
