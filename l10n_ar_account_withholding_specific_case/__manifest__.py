# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Automatic Argentinian Withholdings on Payments - Specific Cases",
    "summary": """
        This module extends the functionality of Automatic Argentinian Withholdings on Payments to support specific cases, not possible with the default types of withholdings.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["FedericoGregori"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Accounting",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["l10n_ar_account_withholding"],
    "data": [
        "views/account_tax_views.xml",
    ],
}
