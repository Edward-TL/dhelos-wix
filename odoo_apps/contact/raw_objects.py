"""
"""
import os

from dataclasses import dataclass# , field
# from typing import Optional, BinaryIO
# from datetime import datetime
from odoo_apps.type_hints.contacts import (
    # ActivityExceptionDecoration,
    # ActivityState,
    # AutopostBills,
    CompanyType,
    # FollowupReminderType,
    # FollowupStatus,
    # InvoiceEdiFormat,
    # InvoiceSendingMethod,
    # L10nMxEdiFiscalRegime,
    # L10nMxEdiPaymentPolicy,
    # L10nMxEdiUsage,
    # L10nMxTypeOfOperation,
    Lang,
    # PeppolEas,
    Trust,
    Type
)
from odoo_apps.type_hints.time_zone import Tz


def load_docstring_from_md(filepath):
    """Loads content from a Markdown file and returns it as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: Markdown file not found at {filepath}"

@dataclass
class Partner:

    # id: int
    # display_name: str = 'Fatima Evia'
    # message_is_follower: bool = False
    # message_follower_ids: Optional[list] = False
    # message_partner_ids: Optional[list] = False
    # message_ids: list = field(default_factory=[224])
    # has_message: bool = True
    # message_needaction: bool = False
    # message_needaction_counter: int = 0
    # message_has_error: bool = False
    # message_has_error_counter: int = 0
    # message_attachment_count: int = 0
    # rating_ids: Optional[list] = False
    # website_message_ids: Optional[list] = False
    # message_has_sms_error: bool = False
    # email_normalized: str
    # is_blacklisted: bool = False
    # message_bounce: int = 5
    # activity_ids: Optional[list] = False
    # activity_state: ActivityState = 'False'
    # activity_user_id: list = False
    # activity_type_id: list = False
    # activity_type_icon: str = False
    # activity_date_deadline: Optional[datetime | str] = False
    # my_activity_date_deadline: Optional[datetime | str] = False
    # activity_summary: str = False
    # activity_exception_decoration: ActivityExceptionDecoration = 'False'
    # activity_exception_icon: str = False
    # activity_calendar_event_id: list = False
    # # image_1920: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # image_1024: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # image_512: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # image_256: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # image_128: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # avatar_1920: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # avatar_1024: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # avatar_512: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # avatar_256: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    # avatar_128: Optional[BinaryIO] = PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnID8+PHN2ZyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayc+PHJlY3QgZmlsbD0naHNsKDI1NiwgNDclLCA0NSUpJyBoZWlnaHQ9JzE4MCcgd2lkdGg9JzE4MCcvPjx0ZXh0IGZpbGw9JyNmZmZmZmYnIGZvbnQtc2l6ZT0nOTYnIHRleHQtYW5jaG9yPSdtaWRkbGUnIHg9JzkwJyB5PScxMjUnIGZvbnQtZmFtaWx5PSdzYW5zLXNlcmlmJz5BPC90ZXh0Pjwvc3ZnPg==
    name: str
    complete_name: str
    # parent_id: list = False
    # parent_name: str = False
    # child_ids: Optional[list] = False
    # ref: str = False
    lang: Lang = 'es_MX'
    # active_lang_count: int = 2
    tz: Tz = 'America/Mexico_City'
    tz_offset: str = '-0600'
    # user_id: list = False
    
    # RFC
    vat: str = False
    fiscal_country_codes: str = 'MX'
    partner_vat_placeholder: str = 'no aplica'
    # vat_label: str = 'RFC'

    # same_vat_partner_id: list = False
    # same_company_registry_partner_id: list = False
    # company_registry: str = False
    company_registry_label: str
    # company_registry_placeholder: str = False
    # bank_ids: Optional[list] = False
    # website: str = False
    # comment: Optional[str] = False
    # category_id: Optional[list] = False
    active: bool = True
    employee: bool = True
    # function: str = False
    type: Type = 'contact'
    type_address_label: str = 'Dirección'
    street: str = False
    street2: str = False
    zip: str = False
    city: str = False
    state_id: list = False
    # country_id: list = False
    country_code: str = "MX"
    # partner_latitude: float = 0.0
    # partner_longitude: float = 0.0
    email: str
    # email_formatted: str
    phone: str = False
    is_company: bool = False
    is_public: bool = False
    industry_id: list = False
    company_type: CompanyType = 'person' # Literal['person', 'company']
    company_id: int = 1 # centro contable de teapa
    # color: int = 0
    # user_ids: list = field(default_factory=[2])
    main_user_id: int = 2 # 
    partner_share: bool = False
    # contact_address: str = ''
    commercial_partner_id: int = 3 # 
    # commercial_company_name: str = False
    # company_name: str = False
    # barcode: str = False
    # self: int = 3 # 
    # application_statistics: Optional[object] = False
    # contact_address_complete: str = ''
    # channel_ids: list = field(default_factory=[1, 2, 3])
    # channel_member_ids: list = field(default_factory=[1, 2, 3])
    # is_in_call: bool = False
    # rtc_session_ids: Optional[list] = False
    # contact_address_inline: str = ''
    # starred_message_ids: Optional[list] = False
    # im_status: str = 'offline'
    # image_medium: Optional[BinaryIO] = False
    # signup_type: str = False
    # meeting_count: int = 0
    # meeting_ids: Optional[list] = False
    # calendar_last_notif_ack: Optional[datetime | str] = '2025-07-31 15:23:35'
    # phone_sanitized: str = False
    # phone_sanitized_blacklisted: bool = False
    # phone_blacklisted: bool = False
    # phone_mobile_search: str = False
    # property_product_pricelist: int = 1 # Default (MXN)
    # specific_property_product_pricelist: list = False
    # ocn_token: str = False
    # certifications_count: int = 0
    # certifications_company_count: int = 0
    # upcoming_appointment_ids: Optional[list] = False
    # payment_token_ids: Optional[list] = False
    
    
    payment_token_count: int = 0
    
    
    # signature_count: int = 0
    # partner_company_registry_placeholder: str = ''
    # duplicate_bank_partner_ids: Optional[list] = False


    # credit: float = 0.0
    # credit_to_invoice: float = 0.0
    # credit_limit: float = 0.0
    
    use_partner_credit_limit: bool = False
    show_credit_limit: bool = False
    # days_sales_outstanding: float = 0.0
    # debit: float = 0.0
    # total_invoiced: float = 0.0
    currency_id: int = 33 # MXN
    
    # property_account_payable_id: int = 76 # 201.01.01 Nacionales
    # property_account_receivable_id: int = 53 # 105.01.01 Tiendas Chedraui

    # property_account_position_id: list = False
    # property_payment_term_id: list = False
    # property_supplier_payment_term_id: list = False
    # ref_company_ids: Optional[list] = False
    supplier_invoice_count: int = 0
    account_move_count: int = 0
    # invoice_ids: Optional[list] = False
    # contract_ids: Optional[list] = False
    bank_account_count: int = 0
    trust: Trust = 'normal'
    # ignore_abnormal_invoice_date: bool = False
    # ignore_abnormal_invoice_amount: bool = False
    # invoice_sending_method: InvoiceSendingMethod = 'False'
    # invoice_edi_format: InvoiceEdiFormat = 'False'
    # invoice_edi_format_store: str = False
    # display_invoice_edi_format: bool = True
    # invoice_template_pdf_report_id: list = False
    # available_invoice_template_pdf_report_ids: list = field(default_factory=[231])
    # display_invoice_template_pdf_report_id: bool = False
    # supplier_rank: int = 0
    # customer_rank: int = 0
    # autopost_bills: AutopostBills = 'ask'
    # duplicated_bank_account_partners_count: int = 0
    # property_outbound_payment_method_line_id: list = False
    # property_inbound_payment_method_line_id: list = False
    # employee_ids: list = field(default_factory=[1])
    # employees_count: int = 1
    # project_ids: Optional[list] = False
    # task_ids: Optional[list] = False
    # task_count: int = 0
    # property_stock_customer: int = 5 # Partners/Customers
    # property_stock_supplier: int = 4 # Partners/Vendors
    # picking_warn_msg: str = False
    # is_ubl_format: bool = False
    # is_peppol_edi_format: bool = False
    # peppol_endpoint: str = False
    # peppol_eas: PeppolEas = 'False'
    # available_peppol_eas: Optional[object] = field(
    #     default_factory = [
    #         '9923', '9922', '0151', '9914', '9915', '0208', '9925',
    #         '9924', '9926', '9934', '9928', '9929', '0096', '0184',
    #         '0198', '0191', '9931', '0037', '0216', '0213', '0002',
    #         '0009', '9957', '0225', '0240', '0204', '9930', '9933',
    #         '9910', '0196', '9935', '0211', '0097', '0188', '0221',
    #         '0218', '9939', '9936', '0200', '9937', '9938', '9942',
    #         '0230', '9943', '9940', '9941', '0106', '0190', '9944',
    #         '0192', '9945', '9946', '9947', '9948', '0195', '9949',
    #         '9950', '9920', '0007', '9955', '9927', '0183', '9952',
    #         '0235', '9932', '9959', '0060', '0088', '0130', '0135',
    #         '0142', '0193', '0199', '0201', '0202', '0209', '0210',
    #         '9913', '9918', '9919', '9951', '9953', 'AN', 'AQ', 'AS',
    #         'AU', 'EM'
    #         ]
    # )
    # vies_valid: bool = False
    # perform_vies_validation: bool = False
    # property_purchase_currency_id: list = False
    # purchase_order_count: int = 0
    # purchase_warn_msg: str = False
    # receipt_reminder_email: bool = False
    # reminder_date_before_receipt: int = 1
    # buyer_id: list = False
    # online_partner_information: str = False
    # account_represented_company_ids: Optional[list] = False
    # l10n_mx_edi_addenda_ids: Optional[list] = False
    # l10n_mx_edi_fiscal_regime: L10nMxEdiFiscalRegime = 'False'
    # l10n_mx_edi_ieps_breakdown: bool = False
    # l10n_mx_edi_usage: L10nMxEdiUsage = 'False'
    # l10n_mx_edi_payment_method_id: list = False
    # l10n_mx_edi_payment_policy: L10nMxEdiPaymentPolicy = 'False'
    # purchase_line_ids: Optional[list] = False
    # on_time_rate: float = -1.0
    # sale_order_count: int = 0
    # sale_order_ids: Optional[list] = False
    # sale_warn_msg: str = False
    # followup_next_action_date: Optional[datetime | str] = False
    # unreconciled_aml_ids: Optional[list] = False
    # unpaid_invoice_ids: Optional[list] = False
    # unpaid_invoices_count: int = 0
    # total_all_due: float = 0.0
    # total_all_overdue: float = 0.0
    # total_due: float = 0.0
    # total_overdue: float = 0.0
    # followup_status: FollowupStatus = 'no_action_needed'
    # followup_line_id: list = False
    # followup_reminder_type: FollowupReminderType = 'automatic'
    # followup_responsible_id: list = False
    # has_moves: bool = False
    # l10n_mx_type_of_third: str = '05'
    # l10n_mx_type_of_operation: L10nMxTypeOfOperation = 'False'
    # l10n_mx_nationality: str = False

