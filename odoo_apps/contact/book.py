"""
Contact book
"""

from dataclasses import dataclass, field
from typing import Literal
import pandas as pd

from odoo_apps.client import OdooClient
from odoo_apps.response import Response,standarize_response
from odoo_apps.models import CONTACTS

from odoo_apps.utils.operators import Operator

ReferenceField = Literal[
    'phone',
    'name',
    'email',
    'employee',
    'complete_name'
]

JSON_FIELDS_REF = {
    "json_var": "odoo_var",
    "clients_phones": 'phone',
    "client_name": 'name',
    "contact_email": 'email',
    "client_id": 'id',
    "client_full_name": 'complete_name',
}

@dataclass
class ContactBook:
    """
    Represents a Contact book, thinked for search clients/users info,
    create or edit it.
    """
    client: OdooClient
    preload: bool = True
    json_fields_ref: dict = field(default_factory = lambda: JSON_FIELDS_REF)

    def __post_init__(self):
        if self.preload:
            self.contacts = pd.DataFrame(
                self.client.search_read(
                    model = CONTACTS.PARTNER,
                    fields = list(self.json_fields_ref.values())
                )
            )

    def get_contact_id(
        self, by: ReferenceField, reference: str, operator: Operator = '='
        ) -> int:
        """
        Returns JUST id value according to a simple domain
        """
        return self.client.search_read(
            model = CONTACTS.PARTNER,
            domain = [
                [by, operator, reference]
            ]
        )[0]['id']

    def check_register_contacts(self, references: list[str], by_field:ReferenceField = 'phone') -> list:
        """Validates contact registration, primarily focusing on the first contact.

        This function checks if phone numbers from a request are registered in the
        provided `phone_guide` (ContactBook).

        If the `missing_numbers` list is populated, a standardized error response is returned.
        Otherwise, the function returns the contacts ID (or `None`) `clients_phones`.

        Args:
            phone_guide (ContactBook): An instance of a ContactBook-like class
                used to look up contact IDs by phone number.
            request_json (dict): A dictionary containing the request data.
                It's expected to have a 'BODY' key, which in turn contains:
                - `clients_phones` (list): A list of phone numbers to check.
                The function primarily processes the first phone number in this list.

        Returns:
            The contacts IDs (list[int]) of `request_json['BODY']['clients_phones']`.
            If it is found some None values, return an Error Response.
        """
        
        contact_book_ids = [
            self.get_contact_id(
                by = by_field,
                reference = contact_reference
                ) for contact_reference in references
        ]

        missing_numbers = [
            {
                phone: book_id
            } for phone, book_id in zip(
                references, contact_book_ids
                ) if book_id is None

        ]

        if len(missing_numbers) > 0:
            conctact_error_msg = 'Unknown partner on Conctact Book. Unknown contacts: '
            conctact_error_msg += f"{missing_numbers}. Please register the missing contacts."

            return standarize_response(
                request = {
                    'contat-info': references,
                    'reference-field': by_field
                },
                response = Response(
                    action = "get",
                    model = CONTACTS.PARTNER,
                    object = None,
                    status = 'NOT FOUND',
                    status_code = 404,
                    msg = conctact_error_msg
                )
            )
        
        return contact_book_ids
    