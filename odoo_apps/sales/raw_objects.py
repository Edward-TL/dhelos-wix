"""
"""

from dataclasses import dataclass, field
from typing import Optional, BinaryIO
from datetime import datetime

from odoo_apps.type_hints.sales import (
    ActivityExceptionDecoration,
    ActivityState,
    CompanyPriceInclude,
    DeliveryStatus,
    InvoiceStatus,
    L10nMxEdiPaymentPolicy,
    L10nMxEdiUsage,
    PickingPolicy,
    State,
    TaxCalculationRoundingMethod,
    TermsType,

    # ORDER LINE
    DisplayType,
    ProductType,
    QtyDeliveredMethod,
    ServiceTracking
)

@dataclass
class Sale:
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


    id: int = 1
    display_name: str = 'S00001'
    campaign_id: list = False
    source_id: list = False
    medium_id: list = False
    activity_ids: Optional[list] = False
    activity_state: ActivityState = 'False'
    activity_user_id: list = False
    activity_type_id: list = False
    activity_type_icon: str = False
    activity_date_deadline: Optional[datetime | str] = False
    my_activity_date_deadline: Optional[datetime | str] = False
    activity_summary: str = False
    activity_exception_decoration: ActivityExceptionDecoration = 'False'
    activity_exception_icon: str = False
    activity_calendar_event_id: list = False
    message_is_follower: bool = True
    message_follower_ids: list = field(default_factory=[331])
    message_partner_ids: list = field(default_factory=[3])
    message_ids: list = field(default_factory=[698])
    has_message: bool = True
    message_needaction: bool = False
    message_needaction_counter: int = 0
    message_has_error: bool = False
    message_has_error_counter: int = 0
    message_attachment_count: int = 0
    rating_ids: Optional[list] = False
    website_message_ids: Optional[list] = False
    message_has_sms_error: bool = False
    access_url: str = '/my/orders/1'
    access_token: str = False
    access_warning: str = ''
    name: str = 'S00001'
    company_id: int = 1 # centro contable de teapa
    partner_id: int = 25 # AMIGOCANCUN SA DE CV
    state: State = 'draft'
    locked: bool = False
    has_archived_products: bool = False
    client_order_ref: str = False
    create_date: Optional[datetime | str] = '2025-08-22 06:40:25'
    commitment_date: Optional[datetime | str] = '2025-08-29 06:00:00'
    date_order: Optional[datetime | str] = '2025-08-22 06:38:27'
    origin: str = False
    reference: str = False
    pending_email_template_id: list = False
    require_signature: bool = False
    require_payment: bool = False
    prepayment_percent: float = 1.0
    signature: Optional[BinaryIO] = False
    signed_by: str = False
    signed_on: Optional[datetime | str] = False
    validity_date: Optional[datetime | str] = '2025-09-21'
    journal_id: list = False
    note: Optional[str] = False
    partner_invoice_id: int = 25 # AMIGOCANCUN SA DE CV
    partner_shipping_id: int = 25 # AMIGOCANCUN SA DE CV
    fiscal_position_id: list = False
    payment_term_id: int = 4 # 30 Days
    pricelist_id: int = 1 # Default (MXN)
    currency_id: int = 33 # MXN
    currency_rate: float = 1.0
    user_id: int = 2 # Fatima Evia
    team_id: int = 1 # Sales
    amount_untaxed: float = 7068.36
    amount_tax: float = 1130.94
    amount_total: float = 8199.3
    amount_to_invoice: float = 8199.3
    amount_invoiced: float = 0.0
    invoice_count: int = 0
    invoice_ids: Optional[list] = False
    invoice_status: InvoiceStatus = 'no'
    sale_warning_text: str = ''
    transaction_ids: Optional[list] = False
    authorized_transaction_ids: Optional[list] = False
    amount_paid: float = 0.0
    tag_ids: Optional[list] = False
    amount_undiscounted: float = 7068.36
    country_code: str = 'MX'
    company_price_include: CompanyPriceInclude = 'tax_included'
    duplicated_order_ids: Optional[list] = False
    expected_date: Optional[datetime | str] = '2025-08-22 06:49:18'
    is_expired: bool = False
    partner_credit_warning: str = ''
    tax_calculation_rounding_method: TaxCalculationRoundingMethod = 'round_globally'
    tax_country_id: int = 156 # Mexico
    tax_totals: Optional[BinaryIO] = {'currency_id': 33, 'currency_pd': 0.01, 'company_currency_id': 33, 'company_currency_pd': 0.01, 'has_tax_groups': True, 'subtotals': [{'tax_groups': [{'id': 4, 'involved_tax_ids': [16], 'tax_amount_currency': 1130.94, 'tax_amount': 1130.94, 'base_amount_currency': 7068.36, 'base_amount': 7068.36, 'display_base_amount_currency': 7068.36, 'display_base_amount': 7068.36, 'group_name': 'VAT 16%', 'group_label': False}], 'tax_amount_currency': 1130.94, 'tax_amount': 1130.94, 'base_amount_currency': 7068.36, 'base_amount': 7068.36, 'name': 'Subtotal'}], 'base_amount_currency': 7068.36, 'base_amount': 7068.36, 'tax_amount_currency': 1130.94, 'tax_amount': 1130.94, 'same_tax_base': True, 'total_amount_currency': 8199.3, 'total_amount': 8199.3}
    terms_type: TermsType = 'plain'
    type_name: str = 'Cotización'
    show_update_fpos: bool = False
    has_active_pricelist: bool = True
    show_update_pricelist: bool = False
    create_uid: int = 2 # Fatima Evia
    write_uid: int = 2 # Fatima Evia
    write_date: Optional[datetime | str] = '2025-08-22 06:40:25'
    l10n_mx_edi_cfdi_to_public: bool = False
    l10n_mx_edi_payment_method_id: int = 1 # Efectivo
    l10n_mx_edi_usage: L10nMxEdiUsage = 'G01'
    l10n_mx_edi_payment_policy: L10nMxEdiPaymentPolicy = 'PPD'
    sale_order_template_id: list = False
    sale_order_option_ids: Optional[list] = False
    purchase_order_count: int = 0
    incoterm: list = False
    incoterm_location: str = False
    picking_policy: PickingPolicy = 'direct'
    warehouse_id: int = 1 # centro contable de teapa
    picking_ids: Optional[list] = False
    delivery_count: int = 0
    delivery_status: DeliveryStatus = 'False'
    late_availability: bool = False
    procurement_group_id: list = False
    effective_date: Optional[datetime | str] = False
    json_popover: str = '{"popoverTemplate": "sale_stock.DelayAlertWidget", "late_elements": []}'
    show_json_popover: bool = False
    available_quotation_document_ids: Optional[list] = False
    is_pdf_quote_builder_available: bool = False
    quotation_document_ids: Optional[list] = False
    customizable_pdf_form_fields: Optional[object] = False
    spreadsheet_template_id: list = False
    spreadsheet_ids: Optional[list] = False
    spreadsheet_id: list = False
    planning_hours_planned: float = 0.0
    planning_hours_to_plan: float = 0.0
    planning_first_sale_line_id: list = False
    planning_initial_date: Optional[datetime | str] = '2025-08-22'
    tasks_ids: Optional[list] = False
    tasks_count: int = 0
    visible_project: bool = False
    project_ids: Optional[list] = False
    project_count: int = 0
    milestone_count: int = 0
    is_product_milestone: bool = False
    show_create_project_button: bool = False
    show_project_button: bool = False
    show_task_button: bool = False
    closed_task_count: int = 0
    completed_task_percentage: float = 0.0
    project_id: list = False
    project_account_id: list = False

@dataclass
class OrderLine:
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

    id: int = 1
    display_name: str = 'S00001 - [ILUCOMAG180SS] Cople lineal 180° para rieles magnéticos modelos ILUTMAG2624SS e ILUTMAG2651SS. (AMIGOCANCUN SA DE CV)'
    analytic_distribution: Optional[object] = False
    analytic_precision: int = 2
    distribution_analytic_account_ids: Optional[list] = False
    order_id: int = 1 # S00001
    sequence: int = 10
    company_id: int = 1 # centro contable de teapa
    currency_id: int = 33 # MXN
    order_partner_id: int = 25 # AMIGOCANCUN SA DE CV
    salesman_id: int = 2 # Fatima Evia
    state: State = 'draft'
    tax_country_id: int = 156 # Mexico
    display_type: DisplayType = 'False'
    is_configurable_product: bool = False
    is_downpayment: bool = False
    is_expense: bool = False
    product_id: int = 36 # [ILUCOMAG180SS] Cople lineal 180° para rieles magnéticos modelos ILUTMAG2624SS e ILUTMAG2651SS.
    product_template_id: int = 36 # [ILUCOMAG180SS] Cople lineal 180° para rieles magnéticos modelos ILUTMAG2624SS e ILUTMAG2651SS.
    product_template_attribute_value_ids: Optional[list] = False
    product_custom_attribute_value_ids: Optional[list] = False
    product_no_variant_attribute_value_ids: Optional[list] = False
    is_product_archived: bool = False
    name: str = '[ILUCOMAG180SS] Cople lineal 180° para rieles magnéticos modelos ILUTMAG2624SS e ILUTMAG2651SS.'
    translated_product_name: str = '[ILUCOMAG180SS] Cople lineal 180° para rieles magnéticos modelos ILUTMAG2624SS e ILUTMAG2651SS.'
    product_uom_qty: float = 1.0
    product_uom_id: int = 1 # Units
    allowed_uom_ids: list = field(default_factory=[1])
    linked_line_id: list = False
    linked_line_ids: Optional[list] = False
    virtual_id: str = False
    linked_virtual_id: str = False
    selected_combo_items: str = False
    combo_item_id: list = False
    tax_ids: list = field(default_factory=[16])
    pricelist_item_id: list = False
    price_unit: float = 50.15
    technical_price_unit: float = 50.15
    discount: float = 0.0
    price_subtotal: float = 43.23
    price_tax: float = 6.920000000000002
    price_total: float = 50.15
    price_reduce_taxexcl: float = 43.23
    price_reduce_taxinc: float = 50.15
    customer_lead: float = 0.0
    qty_delivered_method: QtyDeliveredMethod = 'stock_move'
    qty_delivered: float = 0.0
    qty_invoiced: float = 0.0
    qty_invoiced_posted: float = 0.0
    qty_to_invoice: float = 0.0
    analytic_line_ids: Optional[list] = False
    invoice_lines: Optional[list] = False
    invoice_status: InvoiceStatus = 'no'
    untaxed_amount_invoiced: float = 0.0
    amount_invoiced: float = 0.0
    untaxed_amount_to_invoice: float = 0.0
    amount_to_invoice: float = 50.15
    extra_tax_data: Optional[object] = False
    product_type: ProductType = 'consu'
    service_tracking: ServiceTracking = 'no'
    product_updatable: bool = True
    product_uom_readonly: bool = False
    tax_calculation_rounding_method: TaxCalculationRoundingMethod = 'round_globally'
    company_price_include: CompanyPriceInclude = 'tax_included'
    sale_line_warn_msg: str = False
    create_uid: int = 2 # Fatima Evia
    create_date: Optional[datetime | str] = '2025-08-22 06:40:25'
    write_uid: int = 2 # Fatima Evia
    write_date: Optional[datetime | str] = '2025-08-22 06:40:25'
    sale_order_option_ids: Optional[list] = False
    purchase_line_ids: Optional[list] = False
    purchase_line_count: int = 0
    route_ids: Optional[list] = False
    move_ids: Optional[list] = False
    virtual_available_at_date: float = 0.0
    scheduled_date: Optional[datetime | str] = '2025-08-29 06:00:00'
    forecast_expected_date: Optional[datetime | str] = False
    free_qty_today: float = 0.0
    qty_available_today: float = 0.0
    warehouse_id: int = 1 # centro contable de teapa
    qty_to_deliver: float = 1.0
    is_mto: bool = False
    display_qty_widget: bool = True
    is_storable: bool = True
    available_product_document_ids: Optional[list] = False
    product_document_ids: Optional[list] = False
    is_service: bool = False
    planning_slot_ids: Optional[list] = False
    planning_hours_planned: float = 0.0
    planning_hours_to_plan: float = 0.0
    project_id: list = False
    task_id: list = False
    reached_milestones_ids: Optional[list] = False