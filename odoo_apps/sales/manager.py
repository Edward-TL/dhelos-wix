"""
"""
# from copy import copy
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

from odoo_apps.client import OdooClient, RPCHandlerMetaclass
from odoo_apps.models import SALES
from odoo_apps.response import Response
from odoo_apps.sales.objects import Quotation, QuotationLine, Invoice

from odoo_apps.utils.multicompany import multicompany_correction, correction_error
from odoo_apps.utils.time_management import date_normalizer

GENERAL_PURPOSE_SALES_ORDER_LINE_FIELDS = (
        'id',
        'order_id',
        'order_partner_id',
        'salesman_id',
        'product_id',
        'product_template_id',
        'display_name',
        'product_qty',
        'product_uom',
        'product_uom_qty'
)

GENERAL_PURPOSE_SALES_ORDER_FIELDS = (
    'id',
    'display_name',
    'partner_id',
    'amount_total',
    'create_date',
    'date_order',
    'reference',
    'note',
    'user_id',
    'amount_paid'
)

@dataclass
class SalesManager(metaclass=RPCHandlerMetaclass):
    """
    Search for products store on Client's database.
    
    Args:
        - client: OdooClient.

    Every dictionary value is an ID, as every key is the
    value name. This makes it easier and faster to verify in
    further actions.
    """
    client: OdooClient
    preload: bool = True

    def __post_init__(self):
        if self.preload:
            pass
        pass

    def create_quotation(self, quotation: Quotation) -> Response:
        """
        By a given Quotation, creates it, considering that if there is a 
        multicompany setup, will update the fields that commonly cause conflicts
        when creating.
 
        """
        quotation_vals = quotation.export_to_dict()
        multicompany_check = multicompany_correction(quotation_vals)

        creation_response = self.client.create(
            SALES.ORDER,
            vals = quotation_vals,
            domains = [
                ['name', '=', quotation.name]
            ]
        )

        quotation.id = creation_response.object

        if multicompany_check:
            correction_response = self.client.update(
                SALES.ORDER,
                records_ids = [quotation.id],
                new_vals = multicompany_check
            )

            if correction_response.status_code not in [200,201]:
                correction_error(
                    update_response = creation_response,
                    correction_msg = correction_response.msg
                    )

        return creation_response

    def add_quotation_line(self, quotation: Quotation, quotation_line: QuotationLine) -> Response:
        """
        Creates a quotation line to a given quotation.
        """
        vals = quotation_line.export_to_dict()

        domain_keys = [k for k in vals.keys() if 'qty' not in k]

        order_line_domain = [
            [key, '=', vals[key]] for key in domain_keys
        ]

        resp = self.client.create(
            SALES.ORDER_LINE,
            vals = quotation_line.export_to_dict(),
            domains = order_line_domain
        )

        quotation_line.id = resp.object
        if quotation.product_lines is None:
            quotation.product_lines = [quotation_line.id]
        else:
            quotation.product_lines.append(quotation_line.id)

        return resp

    def make_invoice(self, quotation: Quotation) -> Response:
        """
        Updates state of given quotation to transform it into an Invoice
        """
        # 1. Prepare context for the wizard
        context = {
            'active_model': 'sale.order',
            'active_ids': [quotation.id],
            'active_id': quotation.id,
        }
        
        # 2. Create the invoicing wizard
        wizard_id = self.client.execute_kw(
            'sale.advance.payment.inv', 'create',
            # Option to invoice what is delivered
            [{'advance_payment_method': 'delivered'}]
            , {'context': context}
        )
        
        # 3. Execute the action to create the final invoice
        action = self.client.models.execute_kw(
            self.client.db, self.client.uid, self.client.password,
            'sale.advance.payment.inv', 'create_invoices',
            [wizard_id], {'context': context}
        )

        # 4. Extract the created invoice ID from the returned action
        if action and isinstance(action, dict) and action.get('res_id'):
            return action.get('res_id')

        # Fallback: search for the invoice in the sales order
        order_data = self.client.models.execute_kw(
            self.client.db, self.client.uid, self.client.password,
            'sale.order', 'read',
            [quotation.id], {'fields': ['invoice_ids']}
        )
        
        if order_data and order_data[0]['invoice_ids']:
            # Take the last created invoice
            return order_data[0]['invoice_ids'][-1]
        
        return None


    def confirm_sale_order(self, quotation: Quotation) -> Response:
        """
        By confirming the given quotation, converts it to a sales order.
        This automatically generates the invoice in draft state if the product is configured for it.
        """
        return self.client.execute_kw(
            SALES.ORDER,
            'action_confirm',
            [quotation.id]
        )

    def delete_quotation(self, quotation: Quotation) -> Response:
        """
        Deletes the given quotation from Client's Odoo DB
        """

        return self.client.delete(
            SALES.ORDER,
            ids = quotation.id
        )

    def update_quotation(self, quotation: Quotation, update_vals: dict) -> Response:
        """
        Updates quotation data
        """
        return self.client.update(
            SALES.ORDER,
            records_ids = quotation.id,
            new_vals = update_vals
        )

    def update_quotation_line(self, quotation_line: QuotationLine, update_vals: dict) -> Response:
        """
        Updates quotation line data
        """
        return self.client.update(
            SALES.ORDER,
            records_ids = quotation_line.id,
            new_vals = update_vals
        )

    def sales_of_the_day(
            self,
            check_date: date | datetime | str,
            by: Literal['order_line', 'order'] = 'order_line',
            fields = GENERAL_PURPOSE_SALES_ORDER_LINE_FIELDS) -> list:
        """
        Check all products sold for a given date.
        """
        
        check_date = date_normalizer(check_date)

        model = SALES.ORDER_LINE
        if by == 'order':
            model = SALES.ORDER
            fields = GENERAL_PURPOSE_SALES_ORDER_FIELDS

        return self.client.search_read(
            model,
            domain = [
                ['create_date', '>', check_date]
            ],
            fields =GENERAL_PURPOSE_SALES_ORDER_LINE_FIELDS
        )