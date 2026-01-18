"""
"""

from dataclasses import dataclass, field

from typing import Optional
from datetime import datetime

from odoo_apps.client import OdooClient
from odoo_apps.models import SALES
from odoo_apps.response import Response
from odoo_apps.utils.cleaning import sort_dict

from odoo_apps.type_hints.sales import (
    CompanyPriceInclude,
    L10nMxEdiPaymentPolicy,
    L10nMxEdiUsage,
    State,
    TaxCalculationRoundingMethod,
    TermsType
)

@dataclass
class Quotation:
    """
    `access_token`: [char] Security Token
    `access_url`: [char] Customer Portal URL
    `access_warning`: [text] Access warning
    `activity_calendar_event_id`: [many2one] Next Activity Calendar Event
    `activity_date_deadline`: [date] Next Activity Deadline
    `activity_exception_decoration`: [selection] Type of the exception activity on record.
        - `warning` -> `Alert`
        - `danger` -> `Error`
    `activity_exception_icon`: [char] Icon to indicate an exception activity.
    `activity_ids`: [one2many] Activities
    `activity_state`: [selection] Status based on activities
        Overdue: Due date is already passed
        Today: Activity date is today
        Planned: Future activities.
        - `overdue` -> `Overdue`
        - `today` -> `Today`
        - `planned` -> `Planned`
    `activity_summary`: [char] Next Activity Summary
    `activity_type_icon`: [char] Font awesome icon e.g. fa-tasks
    `activity_type_id`: [many2one] Next Activity Type
    `activity_user_id`: [many2one] Responsible User
    `amount_invoiced`: [monetary] Already invoiced
    `amount_paid`: [float] Sum of transactions made in through the online payment form that are in the state 'done' or 'authorized' and linked to this order.
    `amount_tax`: [monetary] Taxes
    `amount_to_invoice`: [monetary] Un-invoiced Balance
    `amount_total`: [monetary] Total
    `amount_undiscounted`: [float] Amount Before Discount
    `amount_untaxed`: [monetary] Untaxed Amount
    `authorized_transaction_ids`: [many2many] Authorized Transactions
    `available_quotation_document_ids`: [many2many] Available Quotation Documents
    `campaign_id`: [many2one] This is a name that helps you keep track of your different campaign efforts, e.g. Fall_Drive, Christmas_Special
    `client_order_ref`: [char] Customer Reference
    `closed_task_count`: [integer] Closed Task Count
    `commitment_date`: [datetime] This is the delivery date promised to the customer. If set, the delivery order will be scheduled based on this date rather than product lead times.
    `company_id`: [many2one] Company
    `company_price_include`: [selection] Default on whether the sales price used on the product and invoices with this Company includes its taxes.
        - `tax_included` -> `Tax Included`
        - `tax_excluded` -> `Tax Excluded`
    `completed_task_percentage`: [float] Completed Task Percentage
    `country_code`: [char] The ISO country code in two chars. 
        You can use this field for quick search.
    `create_date`: [datetime] Creation Date
    `create_uid`: [many2one] Created by
    `currency_id`: [many2one] Currency
    `currency_rate`: [float] Currency Rate
    `customizable_pdf_form_fields`: [json] Customizable PDF Form Fields
    `date_order`: [datetime] Creation date of draft/sent orders,
        Confirmation date of confirmed orders.
    `delivery_count`: [integer] Delivery Orders
    `delivery_status`: [selection] Blue: Not Delivered/Started
            Orange: Partially Delivered
            Green: Fully Delivered
        - `pending` -> `Not Delivered`
        - `started` -> `Started`
        - `partial` -> `Partially Delivered`
        - `full` -> `Fully Delivered`
    `display_name`: [char] Display Name
    `duplicated_order_ids`: [many2many] Duplicated Order
    `effective_date`: [datetime] Completion date of the first delivery order.
    `expected_date`: [datetime] Delivery date you can promise to the customer, computed from the minimum lead time of the order lines in case of Service products. In case of shipping, the shipping policy of the order will be taken into account to either use the minimum or maximum lead time of the order lines.
    `fiscal_position_id`: [many2one] Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices.The default value comes from the customer.
    `has_active_pricelist`: [boolean] Has Active Pricelist
    `has_archived_products`: [boolean] Has Archived Products
    `has_message`: [boolean] Has Message
    `id`: [integer] ID
    `incoterm`: [many2one] International Commercial Terms are a series of predefined commercial terms used in international transactions.
    `incoterm_location`: [char] Incoterm Location
    `invoice_count`: [integer] Invoice Count
    `invoice_ids`: [many2many] Invoices
    `invoice_status`: [selection] Invoice Status
        - `upselling` -> `Upselling Opportunity`
        - `invoiced` -> `Fully Invoiced`
        - `to invoice` -> `To Invoice`
        - `no` -> `Nothing to Invoice`
    `is_expired`: [boolean] Is Expired
    `is_pdf_quote_builder_available`: [boolean] Is Pdf Quote Builder Available
    `is_product_milestone`: [boolean] Is Product Milestone
    `journal_id`: [many2one] If set, the SO will invoice in this journal; otherwise the sales journal with the lowest sequence is used.
    `json_popover`: [char] JSON data for the popover widget
    `l10n_mx_edi_cfdi_to_public`: [boolean] Send the CFDI with recipient 'publico en general'
    `l10n_mx_edi_payment_method_id`: [many2one] Indicates the way the invoice was/will be paid, where the options could be: Cash, Nominal Check, Credit Card, etc. Leave empty if unkown and the XML will show 'Unidentified'.
    `l10n_mx_edi_payment_policy`: [selection] Payment Policy
        - `PPD` -> `PPD`
        - `PUE` -> `PUE`
    `l10n_mx_edi_usage`: [selection] The code that corresponds to the use that will be made of the receipt by the recipient.
        - `G01` -> `Acquisition of merchandise`
        - `G02` -> `Returns, discounts or bonuses`
        - `G03` -> `General expenses`
        - `I01` -> `Constructions`
        - `I02` -> `Office furniture and equipment investment`
        - `I03` -> `Transportation equipment`
        - `I04` -> `Computer equipment and accessories`
        - `I05` -> `Dices, dies, molds, matrices and tooling`
        - `I06` -> `Telephone communications`
        - `I07` -> `Satellite communications`
        - `I08` -> `Other machinery and equipment`
        - `D01` -> `Medical, dental and hospital expenses.`
        - `D02` -> `Medical expenses for disability`
        - `D03` -> `Funeral expenses`
        - `D04` -> `Donations`
        - `D05` -> `Real interest effectively paid for mortgage loans (room house)`
        - `D06` -> `Voluntary contributions to SAR`
        - `D07` -> `Medical insurance premiums`
        - `D08` -> `Mandatory School Transportation Expenses`
        - `D09` -> `Deposits in savings accounts, premiums based on pension plans.`
        - `D10` -> `Payments for educational services (Colegiatura)`
        - `S01` -> `Without fiscal effects`
    `late_availability`: [boolean] True if any related picking has late availability
    `locked`: [boolean] Locked orders cannot be modified.
    `medium_id`: [many2one] This is the method of delivery, e.g. Postcard, Email, or Banner Ad
    `message_attachment_count`: [integer] Attachment Count
    `message_follower_ids`: [one2many] Followers
    `message_has_error`: [boolean] If checked, some messages have a delivery error.
    `message_has_error_counter`: [integer] Number of messages with delivery error
    `message_has_sms_error`: [boolean] If checked, some messages have a delivery error.
    `message_ids`: [one2many] Messages
    `message_is_follower`: [boolean] Is Follower
    `message_needaction`: [boolean] If checked, new messages require your attention.
    `message_needaction_counter`: [integer] Number of messages requiring action
    `message_partner_ids`: [many2many] Followers (Partners)
    `milestone_count`: [integer] Milestone Count
    `my_activity_date_deadline`: [date] My Activity Deadline
    `name`: [char] Order Reference
    `note`: [html] Terms and conditions
    `order_line`: [one2many] Order Lines
    `origin`: [char] Reference of the document that generated this sales order request
    `partner_credit_warning`: [text] Partner Credit Warning
    `partner_id`: [many2one] Customer
    `partner_invoice_id`: [many2one] Invoice Address
    `partner_shipping_id`: [many2one] Delivery Address
    `payment_term_id`: [many2one] Payment Terms
    `pending_email_template_id`: [many2one] Pending Email Template
    `picking_ids`: [one2many] Transfers
    `picking_policy`: [selection] If you deliver all products at once, the delivery order will be scheduled based on the greatest product lead time. Otherwise, it will be based on the shortest.
        - `direct` -> `As soon as possible`
        - `one` -> `When all products are ready`
    `planning_first_sale_line_id`: [many2one] Planning First Sale Line
    `planning_hours_planned`: [float] Planning Hours Planned
    `planning_hours_to_plan`: [float] Planning Hours To Plan
    `planning_initial_date`: [date] Planning Initial Date
    `prepayment_percent`: [float] The percentage of the amount needed that must be paid by the customer to confirm the order.
    `pricelist_id`: [many2one] If you change the pricelist, only newly added lines will be affected.
    `procurement_group_id`: [many2one] Procurement Group
    `project_account_id`: [many2one] Project Account
    `project_count`: [integer] Number of Projects
    `project_id`: [many2one] A task will be created for the project upon sales order confirmation. The analytic distribution of this project will also serve as a reference for newly created sales order items.
    `project_ids`: [many2many] Projects
    `purchase_order_count`: [integer] Number of Purchase Order Generated
    `quotation_document_ids`: [many2many] Headers/Footers
    `rating_ids`: [one2many] Ratings
    `reference`: [char] The payment communication of this sale order.
    `require_payment`: [boolean] Request a online payment from the customer to confirm the order.
    `require_signature`: [boolean] Request a online signature from the customer to confirm the order.
    `sale_order_option_ids`: [one2many] Optional Products Lines
    `sale_order_template_id`: [many2one] Quotation Template
    `sale_warning_text`: [text] Internal warning for the partner or the products as set by the user.
    `show_create_project_button`: [boolean] Show Create Project Button
    `show_json_popover`: [boolean] Has late picking
    `show_project_button`: [boolean] Show Project Button
    `show_task_button`: [boolean] Show Task Button
    `show_update_fpos`: [boolean] Has Fiscal Position Changed
    `show_update_pricelist`: [boolean] Has Pricelist Changed
    `signature`: [binary] Signature
    `signed_by`: [char] Signed By
    `signed_on`: [datetime] Signed On
    `source_id`: [many2one] This is the source of the link, e.g. Search Engine, another domain, or name of email list
    `spreadsheet_id`: [many2one] Spreadsheet
    `spreadsheet_ids`: [one2many] Spreadsheets
    `spreadsheet_template_id`: [many2one] Quote calculator
    `state`: [selection] Status
        - `draft` -> `Quotation`
        - `sent` -> `Quotation Sent`
        - `sale` -> `Sales Order`
        - `cancel` -> `Cancelled`
    `tag_ids`: [many2many] Tags
    `tasks_count`: [integer] Tasks
    `tasks_ids`: [many2many] Tasks associated with this sale
    `tax_calculation_rounding_method`: [selection] Tax Calculation Rounding Method
        - `round_per_line` -> `Round per Line`
        - `round_globally` -> `Round Globally`
    `tax_country_id`: [many2one] Tax Country
    `tax_totals`: [binary] Tax Totals
    `team_id`: [many2one] Sales Team
    `terms_type`: [selection] Terms & Conditions format
        - `plain` -> `Add a Note`
        - `html` -> `Add a link to a Web Page`
    `transaction_ids`: [many2many] Transactions
    `type_name`: [char] Type Name
    `user_id`: [many2one] Salesperson
    `validity_date`: [date] Validity of the order, after that you will not able to sign & pay the quotation.
    `visible_project`: [boolean] Display project
    `warehouse_id`: [many2one] Warehouse
    `website_message_ids`: [one2many] Website communication history
    `write_date`: [datetime] Last Updated on
    `write_uid`: [many2one] Last Updated by
    """

    name: str
    display_name: Optional[str] = None

    state: State = 'draft'

    user_id: int = 2 # Sales person [1, OdooBot]
    partner_id: int = 25 # AMIGOCANCUN SA DE CV
    company_id: int = 1 # centro contable de teapa


    # de la factura

    # commitment_date: Optional[datetime | str] = '2025-08-29 06:00:00'
    # validity_date: Optional[datetime | str] = '2025-09-21'

    payment_term_id: int = 4 # 30 Days
    pricelist_id: int = 1 # Default (MXN)
    currency_id: int = 33 # MXN

    id: int = None
    team_id: int = 1 # Sales

    # amount_untaxed: float = 7068.36
    # amount_tax: float = 1130.94
    # amount_total: float = 8199.3
    # amount_to_invoice: float = 8199.3
    # amount_invoiced: float = 0.0
    # amount_undiscounted: float = 7068.36

    # amount_paid: float = 0.0

    # invoice_count: int = 0
    # invoice_ids: Optional[list] = False
    # invoice_status: InvoiceStatus = 'no'

    # sale_warning_text: str = ''
    # transaction_ids: Optional[list] = False
    # authorized_transaction_ids: Optional[list] = False

    country_code: str = 'MX'
    company_price_include: CompanyPriceInclude = 'tax_included'

    duplicated_order_ids: Optional[list] = False
    expected_date: Optional[datetime | str] = '2025-08-22 06:49:18'
    is_expired: bool = False

    partner_credit_warning: str = ''

    tax_calculation_rounding_method: TaxCalculationRoundingMethod = 'round_globally'
    tax_country_id: int = 156 # Mexico
    # tax_totals: Optional[BinaryIO] = {'currency_id': 33, 'currency_pd': 0.01, 'company_currency_id': 33, 'company_currency_pd': 0.01, 'has_tax_groups': True, 'subtotals': [{'tax_groups': [{'id': 4, 'involved_tax_ids': [16], 'tax_amount_currency': 1130.94, 'tax_amount': 1130.94, 'base_amount_currency': 7068.36, 'base_amount': 7068.36, 'display_base_amount_currency': 7068.36, 'display_base_amount': 7068.36, 'group_name': 'VAT 16%', 'group_label': False}], 'tax_amount_currency': 1130.94, 'tax_amount': 1130.94, 'base_amount_currency': 7068.36, 'base_amount': 7068.36, 'name': 'Subtotal'}], 'base_amount_currency': 7068.36, 'base_amount': 7068.36, 'tax_amount_currency': 1130.94, 'tax_amount': 1130.94, 'same_tax_base': True, 'total_amount_currency': 8199.3, 'total_amount': 8199.3}

    terms_type: TermsType = 'plain'
    type_name: str = 'Cotización'

    
    l10n_mx_edi_cfdi_to_public: bool = False
    l10n_mx_edi_payment_method_id: int = 1 # Efectivo
    l10n_mx_edi_usage: L10nMxEdiUsage = 'G01'
    l10n_mx_edi_payment_policy: L10nMxEdiPaymentPolicy = 'PPD'
    
    # sale_order_template_id: list = False
    # sale_order_option_ids: Optional[list] = False
    # purchase_order_count: int = 0
    # incoterm: list = False
    # incoterm_location: str = False
    # picking_policy: PickingPolicy = 'direct'
    
    warehouse_id: int = 1 # centro contable de teapa
    product_lines: Optional[list] = None
    def __post_init__(self):
        if self.display_name is None:
            self.display_name = self.name

    def export_to_dict(self, drop: Optional[tuple] = ('domain', 'id', 'studio_fields')) -> dict:
        """
        Returns the dictionary version of the class
        """
        data = self.__dict__.copy()
        if drop is not None:
            for drop_field in drop:
                if drop_field in data:
                    del data[drop_field]
        
        data_ref = data.copy()

        for k, v in data_ref.items():
            if str(v) in ['nan', 'None', 'False']:
                del data[k]

        return sort_dict(data)
    
    def upload(self, odoo: OdooClient) -> Response:
        """
        Upload to Odoo Database
        """

        resp = odoo.create(
            SALES.ORDER,
            vals = self.export_to_dict(),
            domains = [
                ['name', '=', self.name]
            ]
        )

        self.id = resp.object

        return resp



@dataclass
class QuotationLine:
    """
    `allowed_uom_ids`: [many2many] Allowed Uom
    `amount_invoiced`: [monetary] Invoiced Amount
    `amount_to_invoice`: [monetary] Un-invoiced Balance
    `analytic_distribution`: [json] Analytic Distribution
    `analytic_line_ids`: [one2many] Analytic lines
    `analytic_precision`: [integer] Analytic Precision
    `available_product_document_ids`: [many2many] Available Product Documents
    `combo_item_id`: [many2one] Combo Item
    `company_id`: [many2one] Company
    `company_price_include`: [selection] Default on whether the sales price used on the product and invoices with this Company includes its taxes.
        - `tax_included` -> `Tax Included`
        - `tax_excluded` -> `Tax Excluded`
    `create_date`: [datetime] Created on
    `create_uid`: [many2one] Created by
    `currency_id`: [many2one] Currency
    `customer_lead`: [float] Number of days between the order confirmation and the shipping of the products to the customer
    `discount`: [float] Discount (%)
    `display_name`: [char] Display Name
    `display_qty_widget`: [boolean] Display Qty Widget
    `display_type`: [selection] Display Type
        - `line_section` -> `Section`
        - `line_note` -> `Note`
    `distribution_analytic_account_ids`: [many2many] Distribution Analytic Account
    `extra_tax_data`: [json] Extra Tax Data
    `forecast_expected_date`: [datetime] Forecast Expected Date
    `free_qty_today`: [float] Free Qty Today
    `id`: [integer] ID
    `invoice_lines`: [many2many] Invoice Lines
    `invoice_status`: [selection] Invoice Status
        - `upselling` -> `Upselling Opportunity`
        - `invoiced` -> `Fully Invoiced`
        - `to invoice` -> `To Invoice`
        - `no` -> `Nothing to Invoice`
    `is_configurable_product`: [boolean] Is the product configurable?
    `is_downpayment`: [boolean] Down payments are made when creating invoices from a sales order. They are not copied when duplicating a sales order.
    `is_expense`: [boolean] Is true if the sales order line comes from an expense or a vendor bills
    `is_mto`: [boolean] Is Mto
    `is_product_archived`: [boolean] Is Product Archived
    `is_service`: [boolean] Is a Service
    `is_storable`: [boolean] A storable product is a product for which you manage stock.
    `linked_line_id`: [many2one] Linked Order Line
    `linked_line_ids`: [one2many] Linked Order Lines
    `linked_virtual_id`: [char] Linked Virtual
    `move_ids`: [one2many] Stock Moves
    `name`: [text] Description
    `order_id`: [many2one] Order Reference
    `order_partner_id`: [many2one] Customer
    `planning_hours_planned`: [float] Planning Hours Planned
    `planning_hours_to_plan`: [float] Planning Hours To Plan
    `planning_slot_ids`: [one2many] Planning Slot
    `price_reduce_taxexcl`: [monetary] Price Reduce Tax excl
    `price_reduce_taxinc`: [monetary] Price Reduce Tax incl
    `price_subtotal`: [monetary] Subtotal
    `price_tax`: [float] Total Tax
    `price_total`: [monetary] Total
    `price_unit`: [float] Unit Price
    `pricelist_item_id`: [many2one] Pricelist Item
    `product_custom_attribute_value_ids`: [one2many] Custom Values
    `product_document_ids`: [many2many] The product documents for this order line that will be merged in the PDF quote.
    `product_id`: [many2one] Product
    `product_no_variant_attribute_value_ids`: [many2many] Extra Values
    `product_template_attribute_value_ids`: [many2many] Attribute Values
    `product_template_id`: [many2one] Product Template
    `product_type`: [selection] Goods are tangible materials and merchandise you provide.
A service is a non-material product you provide.
        - `consu` -> `Goods`
        - `service` -> `Service`
        - `combo` -> `Combo`
    `product_uom_id`: [many2one] Unit
    `product_uom_qty`: [float] Quantity
    `product_uom_readonly`: [boolean] Product Uom Readonly
    `product_updatable`: [boolean] Can Edit Product
    `project_id`: [many2one] Generated Project
    `purchase_line_count`: [integer] Number of generated purchase items
    `purchase_line_ids`: [one2many] Purchase line generated by this Sales item on order confirmation, or when the quantity was increased.
    `qty_available_today`: [float] Qty Available Today
    `qty_delivered`: [float] Delivery Quantity
    `qty_delivered_method`: [selection] According to product configuration, the delivered quantity can be automatically computed by mechanism:
  - Manual: the quantity is set manually on the line
  - Analytic From expenses: the quantity is the quantity sum from posted expenses
  - Timesheet: the quantity is the sum of hours recorded on tasks linked to this sale line
  - Stock Moves: the quantity comes from confirmed pickings

        - `manual` -> `Manual`
        - `analytic` -> `Analytic From Expenses`
        - `stock_move` -> `Stock Moves`
        - `milestones` -> `Milestones`
    `qty_invoiced`: [float] Invoiced Quantity
    `qty_invoiced_posted`: [float] Invoiced Quantity (posted)
    `qty_to_deliver`: [float] Qty To Deliver
    `qty_to_invoice`: [float] Quantity To Invoice
    `reached_milestones_ids`: [one2many] Reached Milestones
    `route_ids`: [many2many] Routes
    `sale_line_warn_msg`: [text] Message for Sales Order Line
    `sale_order_option_ids`: [one2many] Optional Products Lines
    `salesman_id`: [many2one] Salesperson
    `scheduled_date`: [datetime] Scheduled Date
    `selected_combo_items`: [char] Selected Combo Items
    `sequence`: [integer] Sequence
    `service_tracking`: [selection] Create on Order
        - `no` -> `Nothing`
        - `task_global_project` -> `Task`
        - `task_in_project` -> `Project & Task`
        - `project_only` -> `Project`
    `state`: [selection] Order Status
        - `draft` -> `Quotation`
        - `sent` -> `Quotation Sent`
        - `sale` -> `Sales Order`
        - `cancel` -> `Cancelled`
    `task_id`: [many2one] Generated Task
    `tax_calculation_rounding_method`: [selection] Tax calculation rounding method
        - `round_per_line` -> `Round per Line`
        - `round_globally` -> `Round Globally`
    `tax_country_id`: [many2one] Tax Country
    `tax_ids`: [many2many] Taxes
    `technical_price_unit`: [float] Technical Price Unit
    `translated_product_name`: [text] Translated Product Name
    `untaxed_amount_invoiced`: [monetary] Untaxed Invoiced Amount
    `untaxed_amount_to_invoice`: [monetary] Untaxed Amount To Invoice
    `virtual_available_at_date`: [float] Virtual Available At Date
    `virtual_id`: [char] Virtual
    `warehouse_id`: [many2one] Warehouse
    `write_date`: [datetime] Last Updated on
    `write_uid`: [many2one] Last Updated by
    """

    order_id: int # S00001
    product_id: int
    product_uom_qty: float
    
    product_template_id: int = 36

    company_id: int = 1 # centro contable de teapa

    sequence: int = 10
    
    # [ILUCOMAG180SS] Cople lineal 180° para rieles magnéticos modelos ILUTMAG2624SS e ILUTMAG2651SS.

    product_template_attribute_value_ids: Optional[list] = False
    product_custom_attribute_value_ids: Optional[list] = False
    product_no_variant_attribute_value_ids: Optional[list] = False

    # tax_ids: list = field(default_factory=[16])
    pricelist_item_id: list = False
    
    selected_combo_items: str = False
    combo_item_id: list = False


    
    qty_delivered: float | bool = False
    qty_invoiced: float  | bool = False
    qty_invoiced_posted: float | bool = False
    qty_to_invoice: float  | bool = False
    
    # order_partner_id: int = 25 # AMIGOCANCUN SA DE CV
    # salesman_id: int = 2 # Fatima Evia
    # state: State = 'draft'
    # tax_country_id: int = 156 # Mexico

    id: Optional[int] = None

    def __post_init__(self):
        if self.qty_to_invoice is False:
            self.qty_to_invoice = self.product_uom_qty

    def export_to_dict(self, drop: Optional[tuple] = ('domain', 'id', 'studio_fields')) -> dict:
        """
        Returns the dictionary version of the class
        """
        data = self.__dict__.copy()
        if drop is not None:
            for drop_field in drop:
                if drop_field in data:
                    del data[drop_field]
        
        data_ref = data.copy()

        for k, v in data_ref.items():
            if str(v) in ['nan', 'None', 'False']:
                del data[k]

        return sort_dict(data)
    
    def upload(self, odoo: OdooClient) -> Response:
        """
        Upload to Odoo Database
        """

        vals = self.export_to_dict()

        domain_keys = [k for k in vals.keys() if 'qty' not in k]

        order_line_domain = [
            [key, '=', vals[key]] for key in domain_keys
        ]

        # print(order_line_domain)
        resp = odoo.create(
            SALES.ORDER_LINE,
            vals = self.export_to_dict(),
            domains = order_line_domain
        )

        self.id = resp.object

        return resp


@dataclass
class Invoice:
    """
    Representation of an Invoice
    """
    quotation_id: int

    def __post_init__(self):
        pass
