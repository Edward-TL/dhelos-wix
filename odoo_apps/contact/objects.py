"""
"""
import os

from dataclasses import dataclass
from typing import Optional
# from datetime import datetime

from odoo_apps.client import OdooClient
from odoo_apps.models import CONTACTS
from odoo_apps.response import Response
from odoo_apps.type_hints.contacts import (
    CompanyType,
    Lang
)
from odoo_apps.type_hints.time_zone import Tz

from odoo_apps.utils.cleaning import sort_dict

def load_docstring_from_md(filepath):
    """Loads content from a Markdown file and returns it as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: Markdown file not found at {filepath}"

@dataclass
class Partner:
    """
    Partner representation
    """
    name: str
    phone: str = False
    email: Optional[str | bool] = False
    # RFC
    vat: str = False

    street: str = False
    street2: str = False
    zip: str = False
    city: str = False
    state_id: list = False
    country_id: int = 156

    company_type: CompanyType = 'person' # Literal['person', 'company']

    # ID DE LA EMPRESA
    company_registry: Optional[str] = False

    lang: Lang = 'es_MX'
    tz: Tz = 'America/Mexico_City'
    tz_offset: str = '-0600'
    fiscal_country_codes: str = 'MX'
    # company_registry_label: str
    employee: bool = True
    # type: Type = 'contact' # ['contact', 'invoice', 'delivery', 'other'] 
    country_code: str = "MX"
    id: Optional[int] = None

    def __post_init__(self):
        if isinstance(self.phone, int):
            self.phone = str(self.phone)

    def export_to_dict(self, drop: Optional[tuple] = ('domain', 'id', 'studio_fields')) -> dict:
        """
        Returns the dictionary version of the class
        """
        data = self.__dict__.copy()
        if drop is not None:
            for field in drop:
                if field in data:
                    del data[field]
        data_ref = data.copy()
        for k, v in data_ref.items():
            if v is None or str(v) == 'nan':
                del data[k]

        return sort_dict(data)

    def upload(self, odoo: OdooClient) -> Response:
        """
        Loads to Odoo with the given client
        """
        resp = odoo.create(
            CONTACTS.PARTNER,
            vals = self.export_to_dict(),
            domains = [
                ['vat', '=', self.vat],
                ['name', '=', self.name]
            ]
        )

        self.id = resp.object

        return resp
