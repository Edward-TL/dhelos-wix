"""
Store interest Odoo models
"""

from dataclasses import dataclass, fields
import inspect
from .utils.cleaning import generate_dict

@dataclass
class TableExample:
    """
    Example of a table
    """
    _name = 'name'
    module = 'name.module'
    def __post_init__(self):
        self.modules = generate_dict(self)

def string_class(data_obj: TableExample) -> str:
    """
    Generate a string representation of the class.
    :param data_obj: Data Class to generate the string from.
    :return: String representation of the class.
    """
    str_class = ""
    print(data_obj.modules.items)
    for k,v in data_obj.modules.items():
        str_class += f"{k}: {v} \n"

    return str_class

@dataclass
class Product:
    """
    Class representing a product in Odoo.
    """
    _name = 'product'
    ATTRIBUTE_CUSTOM_VALUE = 'product.attribute.custom.value'
    ATTRIBUTE_VALUE = 'product.attribute.value'
    ATTRIBUTE = 'product.attribute'
    CATALOG_MIXIN = 'product.catalog.mixin'
    CATEGORY = 'product.category'
    COMBO_ITEM = 'product.combo.item'
    COMBO = 'product.combo'
    DOCUMENT = 'product.document'
    IMAGE = 'product.image'
    LABEL_LAYOUT = 'product.label.layout'
    PACKAGING = 'product.packaging'
    PRICELIST_ITEM = 'product.pricelist.item'
    PRICELIST = 'product.pricelist'
    PRODUCT = 'product.product'
    PUBLIC_CATEGORY = 'product.public.category'
    REMOVAL = 'product.removal'
    REPLENISH = 'product.replenish'
    RIBBON = 'product.ribbon'
    SUPPLIERINFO = 'product.supplierinfo'
    TAG = 'product.tag'
    TEMPLATE_ATTRIBUTE_EXCLUSION = 'product.template.attribute.exclusion'
    TEMPLATE_ATTRIBUTE_LINE = 'product.template.attribute.line'
    TEMPLATE_ATTRIBUTE_VALUE = 'product.template.attribute.value'
    TEMPLATE = 'product.template'
    UNSPSC_CODE = 'product.unspsc.code'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

PRODUCT = Product()

@dataclass
class Stock:
    """
    Class representing the Stock in Odoo.
    """
    BACKORDER_CONFIRMATION = 'stock.backorder.confirmation'
    BACKORDER_CONFIRMATION_LINE = 'stock.backorder.confirmation.line'
    CHANGE_PRODUCT_QTY = 'stock.change.product.qty'
    FORECASTED_PRODUCT_PRODUCT = 'stock.forecasted_product_product'
    FORECASTED_PRODUCT_TEMPLATE = 'stock.forecasted_product_template'
    INVENTORY_ADJUSTMENT_NAME = 'stock.inventory.adjustment.name'
    INVENTORY_CONFLICT = 'stock.inventory.conflict'
    INVENTORY_WARNING = 'stock.inventory.warning'
    LOCATION = 'stock.location'
    LOT_REPORT = 'stock.lot.report'
    LOT = 'stock.lot'
    MOVE_LINE = 'stock.move.line'
    MOVE = 'stock.move'
    ORDERPOINT_SNOOZE = 'stock.orderpoint.snooze'
    PACKAGE_DESTINATION = 'stock.package.destination'
    PACKAGE_TYPE = 'stock.package.type'
    PACKAGE_LEVEL = 'stock.package_level'
    PICKING_TYPE = 'stock.picking.type'
    PICKING = 'stock.picking'
    PUTAWAY_RULE = 'stock.putaway.rule'
    QUANT_PACKAGE = 'stock.quant.package'
    QUANT_RELOCATE = 'stock.quant.relocate'
    QUANT = 'stock.quant'
    QUANTITY_HISTORY = 'stock.quantity.history'
    REPLENISH_MIXIN = 'stock.replenish.mixin'
    REPLENISHMENT_INFO = 'stock.replenishment.info'
    REPLENISHMENT_OPTION = 'stock.replenishment.option'
    REPORT = 'stock.report'
    REQUEST_COUNT = 'stock.request.count'
    RETURN_PICKING = 'stock.return.picking'
    RETURN_PICKING_LINE = 'stock.return.picking.line'
    ROUTE = 'stock.route'
    RULE = 'stock.rule'
    RULES_REPORT = 'stock.rules.report'
    SCRAP_REASON_TAG = 'stock.scrap.reason.tag'
    SCRAP = 'stock.scrap'
    STORAGE_CATEGORY = 'stock.storage.category'
    STORAGE_CATEGORY_CAPACITY = 'stock.storage.category.capacity'
    TRACEABILITY_REPORT = 'stock.traceability.report'
    TRACK_CONFIRMATION = 'stock.track.confirmation'
    TRACK_LINE = 'stock.track.line'
    VALUATION_LAYER = 'stock.valuation.layer'
    VALUATION_LAYER_REVALUATION = 'stock.valuation.layer.revaluation'
    WAREHOUSE_ORDERPOINT = 'stock.warehouse.orderpoint'
    WAREHOUSE = 'stock.warehouse'
    WARN_INSUFFICIENT_QTY = 'stock.warn.insufficient.qty'
    WARN_INSUFFICIENT_QTY_SCRAP = 'stock.warn.insufficient.qty.scrap'
    WARN_INSUFFICIENT_QTY_UNBUILD = 'stock.warn.insufficient.qty.unbuild'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

STOCK = Stock()


@dataclass
class Calendar:
    """
    Class representing Calendar tables in Odoo.
    """
    _name = 'calendar'
    ALARM = 'calendar.alarm'
    ALARM_MANAGER = 'calendar.alarm_manager'
    ATTENDEE = 'calendar.attendee'
    BOOKING_LINE = 'calendar.booking.line'
    BOOKING = 'calendar.booking'
    EVENT_TYPE = 'calendar.event.type'
    EVENT = 'calendar.event'
    FILTERS = 'calendar.filters'
    POPOVER_DELETE_WIZARD = 'calendar.popover.delete.wizard'
    PROVIDER_CONFIG = 'calendar.provider.config'
    RECURRENCE = 'calendar.recurrence'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

CALENDAR = Calendar()

@dataclass
class Appointment:
    """
    Class representing Appointment tables in Odoo.
    """
    _name = 'appointment'
    ANSWER_INPUT = 'appointment.answer.input'
    ANSWER = 'appointment.answer'
    BOOKING_LINE = 'appointment.booking.line'
    INVITE = 'appointment.invite'
    MANAGE_LEAVES = 'appointment.manage.leaves'
    QUESTION = 'appointment.question'
    RESOURCE = 'appointment.resource'
    SLOT = 'appointment.slot'
    TYPE = 'appointment.type'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)
        
APPOINTMENT = Appointment()

@dataclass
class Resource:
    """
    ** CALENDAR_ATTENDANCE = Work Detail.
    ** CALENDAR_LEAVES = Resource Time Off Detail.
     - CALENDAR = Resource Working Time: Calendar model for a resource.
        It has:
            * attendance_ids: list of `resource.calendar.attendance` that are a working interval
                in a given weekday.
            * leave_ids: list of leaves linked to this calendar.
                A leave can be general or linked to a specific resource, depending on its
                `resource_id`.
                
        All methods in this class use "intervals".
            An "interval" is a tuple -> (begin_datetime, end_datetime).
            A list of intervals is therefore a list of tuples:
            
                            [(begin_datetime, end_datetime)]
            
            holding several intervals of work or leaves. 
    - MIXIN = Resource Mixin: The base model, which is implicitly inherited by all models.
    ** RESOURCE = Resources

    ** [Main super-class for regular database-persisted.
        Odoo models are created by inheriting from this class]
    """


    _name = "resource"
    CALENDAR_ATTENDANCE = 'resource.calendar.attendance'
    CALENDAR_LEAVES = 'resource.calendar.leaves'
    CALENDAR = 'resource.calendar'
    MIXIN = 'resource.mixin'
    RESOURCE = 'resource.resource'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

RESOURCE = Resource()

@dataclass
class Res:
    BANK = 'res.bank'
    COMPANY = 'res.company'
    CONFIG_SETTINGS = 'res.config.settings'
    CONFIG = 'res.config'
    COUNTRY_GROUP = 'res.country.group'
    COUNTRY_STATE = 'res.country.state'
    COUNTRY = 'res.country'
    CURRENCY_RATE = 'res.currency.rate'
    CURRENCY = 'res.currency'
    DEVICE_LOG = 'res.device.log'
    DEVICE = 'res.device'
    GROUPS = 'res.groups'
    LANG = 'res.lang'
    PARTNER_AUTOCOMPLETE_SYNC = 'res.partner.autocomplete.sync'
    PARTNER_BANK = 'res.partner.bank'
    PARTNER_CATEGORY = 'res.partner.category'
    PARTNER_INDUSTRY = 'res.partner.industry'
    PARTNER_TITLE = 'res.partner.title'
    PARTNER = 'res.partner'
    USERS_APIKEYS = 'res.users.apikeys'
    USERS_APIKEYS_DESCRIPTION = 'res.users.apikeys.description'
    USERS_APIKEYS_SHOW = 'res.users.apikeys.show'
    USERS_DELETION = 'res.users.deletion'
    USERS_IDENTITYCHECK = 'res.users.identitycheck'
    USERS_LOG = 'res.users.log'
    USERS_SETTINGS = 'res.users.settings'
    USERS_SETTINGS_VOLUMES = 'res.users.settings.volumes'
    USERS = 'res.users'

    @classmethod
    def export_to_dict(cls) -> dict:
        """
        Regresa un diccionario con los atributos de la CLASE.
        Filtra para incluir solo las constantes en mayúsculas.
        """
        return {
            key: value
            for key, value in cls.__dict__.items()
            if key.isupper() and not key.startswith('_')
        }

RES = Res()
RES.models = RES.export_to_dict()

@dataclass
class Contacts:
    """
    Tables here are the one related to the Contacts info
    """
    _name = 'res'
    COMPANY = 'res.company'
    GROUPS = 'res.groups'
    PARTNER_BANK = 'res.partner.bank'
    PARTNER_CATEGORY = 'res.partner.category'
    PARTNER_INDUSTRY = 'res.partner.industry'
    PARTNER_TITLE = 'res.partner.title'
    PARTNER = 'res.partner'
    USERS = 'res.users'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

CONTACTS = Contacts()

@dataclass
class Pos:
    """Point Of Sale tables"""
    _name = 'pos'
    BILL = 'pos.bill'
    BUS_MIXIN = 'pos.bus.mixin'
    CATEGORY = 'pos.category'
    CLOSE_SESSION_WIZARD = 'pos.close.session.wizard'
    CONFIG = 'pos.config'
    DAILY_SALES_REPORTS_WIZARD = 'pos.daily.sales.reports.wizard'
    DETAILS_WIZARD = 'pos.details.wizard'
    LOAD_MIXIN = 'pos.load.mixin'
    MAKE_PAYMENT = 'pos.make.payment'
    NOTE = 'pos.note'
    ORDER_LINE = 'pos.order.line'
    ORDER = 'pos.order'
    PACK_OPERATION_LOT = 'pos.pack.operation.lot'
    PAYMENT_METHOD = 'pos.payment.method'
    PAYMENT = 'pos.payment'
    PRINTER = 'pos.printer'
    SESSION = 'pos.session'
    DISPLAY = 'pos_preparation_display.display'
    ORDER_STAGE = 'pos_preparation_display.order.stage'
    ORDER = 'pos_preparation_display.order'
    ORDERLINE = 'pos_preparation_display.orderline'
    RESET_WIZARD = 'pos_preparation_display.reset.wizard'
    STAGE = 'pos_preparation_display.stage'
    CUSTOM_LINK = 'pos_self_order.custom_link'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

POS = Pos()

@dataclass
class Account:
    """Account Tables"""
    TAG = 'account.account.tag'
    ACCOUNT = 'account.account'
    ACCRUED_ORDERS_WIZARD = 'account.accrued.orders.wizard'
    AGED_PARTNER_BALANCE_REPORT_HANDLER = 'account.aged.partner.balance.report.handler'
    AGED_PAYABLE_REPORT_HANDLER = 'account.aged.payable.report.handler'
    AGED_RECEIVABLE_REPORT_HANDLER = 'account.aged.receivable.report.handler'
    ANALYTIC_ACCOUNT = 'account.analytic.account'
    ANALYTIC_APPLICABILITY = 'account.analytic.applicability'
    ANALYTIC_DISTRIBUTION_MODEL = 'account.analytic.distribution.model'
    ANALYTIC_LINE = 'account.analytic.line'
    ANALYTIC_PLAN = 'account.analytic.plan'
    ASSET_GROUP = 'account.asset.group'
    ASSET_REPORT_HANDLER = 'account.asset.report.handler'
    ASSET = 'account.asset'
    AUTO_RECONCILE_WIZARD = 'account.auto.reconcile.wizard'
    AUTOMATIC_ENTRY_WIZARD = 'account.automatic.entry.wizard'
    AUTOPOST_BILLS_WIZARD = 'account.autopost.bills.wizard'
    BALANCE_SHEET_REPORT_HANDLER = 'account.balance.sheet.report.handler'
    BANK_RECONCILIATION_REPORT_HANDLER = 'account.bank.reconciliation.report.handler'
    BANK_SELECTION = 'account.bank.selection'
    BANK_STATEMENT = 'account.bank.statement'
    BANK_STATEMENT_LINE = 'account.bank.statement.line'
    BANK_STATEMENT_LINE_TRANSIENT = 'account.bank.statement.line.transient'
    CASH_FLOW_REPORT_HANDLER = 'account.cash.flow.report.handler'
    CASH_ROUNDING = 'account.cash.rounding'
    CHANGE_LOCK_DATE = 'account.change.lock.date'
    CHART_TEMPLATE = 'account.chart.template'
    CODE_MAPPING = 'account.code.mapping'
    CUSTOMER_STATEMENT_REPORT_HANDLER = 'account.customer.statement.report.handler'
    DEFERRED_EXPENSE_REPORT_HANDLER = 'account.deferred.expense.report.handler'
    DEFERRED_REPORT_HANDLER = 'account.deferred.report.handler'
    DEFERRED_REVENUE_REPORT_HANDLER = 'account.deferred.revenue.report.handler'
    DISALLOWED_EXPENSES_CATEGORY = 'account.disallowed.expenses.category'
    DISALLOWED_EXPENSES_FLEET_REPORT_HANDLER = 'account.disallowed.expenses.fleet.report.handler'
    DISALLOWED_EXPENSES_RATE = 'account.disallowed.expenses.rate'
    DISALLOWED_EXPENSES_REPORT_HANDLER = 'account.disallowed.expenses.report.handler'
    DUPLICATE_TRANSACTION_WIZARD = 'account.duplicate.transaction.wizard'
    EC_SALES_REPORT_HANDLER = 'account.ec.sales.report.handler'
    EDI_COMMON = 'account.edi.common'
    EDI_XML_CII = 'account.edi.xml.cii'
    EDI_XML_UBL_20 = 'account.edi.xml.ubl_20'
    EDI_XML_UBL_21 = 'account.edi.xml.ubl_21'
    EDI_XML_UBL_A_NZ = 'account.edi.xml.ubl_a_nz'
    EDI_XML_UBL_BIS3 = 'account.edi.xml.ubl_bis3'
    EDI_XML_UBL_DE = 'account.edi.xml.ubl_de'
    EDI_XML_UBL_EFFF = 'account.edi.xml.ubl_efff'
    EDI_XML_UBL_NL = 'account.edi.xml.ubl_nl'
    EDI_XML_UBL_SG = 'account.edi.xml.ubl_sg'
    FINANCIAL_YEAR_OP = 'account.financial.year.op'
    FISCAL_POSITION = 'account.fiscal.position'
    FISCAL_POSITION_ACCOUNT = 'account.fiscal.position.account'
    FISCAL_POSITION_TAX = 'account.fiscal.position.tax'
    FISCAL_YEAR = 'account.fiscal.year'
    FOLLOWUP_REPORT = 'account.followup.report'
    FOLLOWUP_REPORT_HANDLER = 'account.followup.report.handler'
    FULL_RECONCILE = 'account.full.reconcile'
    GENERAL_LEDGER_REPORT_HANDLER = 'account.general.ledger.report.handler'
    GENERIC_TAX_REPORT_HANDLER = 'account.generic.tax.report.handler'
    GENERIC_TAX_REPORT_HANDLER_TAX = 'account.generic.tax.report.handler.account.tax'
    GENERIC_TAX_REPORT_HANDLER_TAX_ACCOUNT = 'account.generic.tax.report.handler.tax.account'
    GROUP = 'account.group'
    IMPORT_SUMMARY = 'account.import.summary'
    INCOTERMS = 'account.incoterms'
    INVOICE_REPORT = 'account.invoice.report'
    INVOICE_EXTRACT_WORDS = 'account.invoice_extract.words'
    JOURNAL_GROUP = 'account.journal.group'
    JOURNAL_REPORT_HANDLER = 'account.journal.report.handler'
    JOURNAL = 'account.journal'
    LOAN_CLOSE_WIZARD = 'account.loan.close.wizard'
    LOAN_COMPUTE_WIZARD = 'account.loan.compute.wizard'
    LOAN_LINE = 'account.loan.line'
    LOAN = 'account.loan'
    LOCK_EXCEPTION = 'account.lock_exception'
    MERGE_WIZARD = 'account.merge.wizard'
    MERGE_WIZARD_LINE = 'account.merge.wizard.line'
    MISSING_TRANSACTION_WIZARD = 'account.missing.transaction.wizard'
    MOVE_LINE = 'account.move.line'
    MOVE_REVERSAL = 'account.move.reversal'
    MOVE_SEND = 'account.move.send'
    MOVE_SEND_BATCH_WIZARD = 'account.move.send.batch.wizard'
    MOVE_SEND_WIZARD = 'account.move.send.wizard'
    MOVE = 'account.move'
    MULTICURRENCY_REVALUATION_REPORT_HANDLER = 'account.multicurrency.revaluation.report.handler'
    MULTICURRENCY_REVALUATION_WIZARD = 'account.multicurrency.revaluation.wizard'
    ONLINE_ACCOUNT = 'account.online.account'
    ONLINE_LINK = 'account.online.link'
    PARTIAL_RECONCILE = 'account.partial.reconcile'
    PARTNER_LEDGER_REPORT_HANDLER = 'account.partner.ledger.report.handler'
    PAYMENT_METHOD = 'account.payment.method'
    PAYMENT_METHOD_LINE = 'account.payment.method.line'
    PAYMENT_REGISTER = 'account.payment.register'
    PAYMENT_TERM = 'account.payment.term'
    PAYMENT_TERM_LINE = 'account.payment.term.line'
    PAYMENT = 'account.payment'
    RECONCILE_MODEL = 'account.reconcile.model'
    RECONCILE_MODEL_LINE = 'account.reconcile.model.line'
    RECONCILE_MODEL_PARTNER_MAPPING = 'account.reconcile.model.partner.mapping'
    RECONCILE_WIZARD = 'account.reconcile.wizard'
    REPORT_ANNOTATION = 'account.report.annotation'
    REPORT_BUDGET = 'account.report.budget'
    REPORT_BUDGET_ITEM = 'account.report.budget.item'
    REPORT_COLUMN = 'account.report.column'
    REPORT_CUSTOM_HANDLER = 'account.report.custom.handler'
    REPORT_EXPRESSION = 'account.report.expression'
    REPORT_EXTERNAL_VALUE = 'account.report.external.value'
    REPORT_FILE_DOWNLOAD_ERROR_WIZARD = 'account.report.file.download.error.wizard'
    REPORT_HORIZONTAL_GROUP = 'account.report.horizontal.group'
    REPORT_HORIZONTAL_GROUP_RULE = 'account.report.horizontal.group.rule'
    REPORT_LINE = 'account.report.line'
    REPORT_SEND = 'account.report.send'
    REPORT = 'account.report'
    RESEQUENCE_WIZARD = 'account.resequence.wizard'
    ROOT = 'account.root'
    SECURE_ENTRIES_WIZARD = 'account.secure.entries.wizard'
    SETUP_BANK_MANUAL_CONFIG = 'account.setup.bank.manual.config'
    TAX_GROUP = 'account.tax.group'
    TAX_REPARTITION_LINE = 'account.tax.repartition.line'
    TAX_REPORT_HANDLER = 'account.tax.report.handler'
    TAX_UNIT = 'account.tax.unit'
    TAX = 'account.tax'
    TRANSFER_MODEL = 'account.transfer.model'
    TRANSFER_MODEL_LINE = 'account.transfer.model.line'
    TRIAL_BALANCE_REPORT_HANDLER = 'account.trial.balance.report.handler'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

ACCOUNT = Account()

@dataclass
class AccountFollowUp:
    """Account Follow Up Tables"""
    FOLLOWUP_LINE = 'account_followup.followup.line'
    MANUAL_REMINDER = 'account_followup.manual_reminder'
    MISSING_INFORMATION_WIZARD = 'account_followup.missing.information.wizard'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

ACCOUNT_FOLLOW_UP = AccountFollowUp()

@dataclass
class AccountReports:
    """Account Reports Tables"""
    EXPORT_WIZARD = 'account_reports.export.wizard'
    EXPORT_WIZARD_FORMAT = 'account_reports.export.wizard.format'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

ACCOUNT_REPORTS = AccountReports()

@dataclass
class Bank:
    """Bank Tables"""
    REC_WIDGET = 'bank.rec.widget'
    REC_WIDGET_LINE = 'bank.rec.widget.line'

    def __post_init__(self):
        self.modules = generate_dict(self)
        self.members = inspect.getmembers(type(self))
        self.fields = {k: v for k,v in dict(self.members).items() if not k.startswith('__')}

    def __str__(self):
        return string_class(self)

BANK = Bank()

@dataclass
class Sales:
    """
    Sales Tables
    """
    ADVANCE_PAYMENT_INV = 'sale.advance.payment.inv'
    EDI_COMMON = 'sale.edi.common'
    EDI_XML_UBL_BIS3 = 'sale.edi.xml.ubl_bis3'
    LOYALTY_COUPON_WIZARD = 'sale.loyalty.coupon.wizard'
    LOYALTY_REWARD_WIZARD = 'sale.loyalty.reward.wizard'
    MASS_CANCEL_ORDERS = 'sale.mass.cancel.orders'
    ORDER_ALERT = 'sale.order.alert'
    ORDER_CANCEL = 'sale.order.cancel'
    ORDER_CLOSE_REASON = 'sale.order.close.reason'
    ORDER_COUPON_POINTS = 'sale.order.coupon.points'
    ORDER_DISCOUNT = 'sale.order.discount'
    ORDER_LINE = 'sale.order.line'
    ORDER_LOG = 'sale.order.log'
    ORDER_LOG_REPORT = 'sale.order.log.report'
    ORDER_OPTION = 'sale.order.option'
    ORDER_SPREADSHEET = 'sale.order.spreadsheet'
    ORDER_TEMPLATE = 'sale.order.template'
    ORDER_TEMPLATE_LINE = 'sale.order.template.line'
    ORDER_TEMPLATE_OPTION = 'sale.order.template.option'
    ORDER = 'sale.order'
    PAYMENT_PROVIDER_ONBOARDING_WIZARD = 'sale.payment.provider.onboarding.wizard'
    PDF_FORM_FIELD = 'sale.pdf.form.field'
    REPORT = 'sale.report'
    SUBSCRIPTION_CHANGE_CUSTOMER_WIZARD = 'sale.subscription.change.customer.wizard'
    SUBSCRIPTION_CLOSE_REASON_WIZARD = 'sale.subscription.close.reason.wizard'
    SUBSCRIPTION_PLAN = 'sale.subscription.plan'
    SUBSCRIPTION_PRICING = 'sale.subscription.pricing'
    SUBSCRIPTION_REPORT = 'sale.subscription.report'
    modules = None

    def export_to_dict(self):
        return self.__dict__.copy()
    
SALES = Sales()
SALES.modules = SALES.export_to_dict()

@dataclass
class L10n:
    """
    * fonacot 
    * infonavit 
    * Mexican Account Report Custom Handler (The base model, which is implicitly inherited by all models.)
    * Addenda for Mexican EDI 
    * Mexican documents that needs to transit outside of Odoo 
    * Create a global invoice 
    * Request CFDI Cancellation:
        Model super-class for transient records, meant to be temporarily persistent, and regularly vacuum-cleaned.
        A TransientModel has a simplified access rights management, all users can create new records, and may only access the records they created.
        The superuser has unrestricted access to all TransientModel records.)
    * Payment Method for Mexico from SAT Data:
        Payment Method for Mexico from SAT Data.
        Electronic documents need this information from such data. Here the `xsd <goo.gl/Vk3IF1>`_
        The payment method is an required attribute, to express the payment method of assets or services covered by the voucher.
        It is understood as a payment method legends such as check, credit card or debit card, deposit account, etc.
        Note:
            Odoo have the model payment.method, but this model need fields that we not need in this feature as partner_id, acquirer, etc.,
            and they are there with other purpose, then a new model is necessary in order to avoid lose odoo's features
    * Wizard for the XML Polizas export of Journal Entries
        Model super-class for transient records, meant to be temporarily persistent, and regularly vacuum-cleaned.
        A TransientModel has a simplified access rights management, all users can create new records, and may only access the records they created.
        The superuser has unrestricted access to all TransientModel records.

    """
    MX_HR_FONACOT = 'l10n.mx.hr.fonacot'
    MX_HR_INFONAVIT = 'l10n.mx.hr.infonavit'
    REPORT_HANDLER = 'l10n_mx.report.handler'
    ADDENDA = 'l10n_mx_edi.addenda'
    DOCUMENT = 'l10n_mx_edi.document'
    GLOBAL_INVOICE_CREATE = 'l10n_mx_edi.global_invoice.create'
    INVOICE_CANCEL = 'l10n_mx_edi.invoice.cancel'
    PAYMENT_METHOD = 'l10n_mx_edi.payment.method'
    XML_POLIZAS_WIZARD = 'l10n_mx_xml_polizas.xml_polizas_wizard'
    modules = None
    def export_to_dict(self):
        return self.__dict__.copy()
    
L10N = L10n()
L10N.modules = L10N.export_to_dict()

@dataclass
class Manufactory:
    """
    MRP: Material Requirements Planning
    BOM: Bill of Materials
    """
    ACCOUNT_WIP_ACCOUNTING = 'mrp.account.wip.accounting'
    ACCOUNT_WIP_ACCOUNTING_LINE = 'mrp.account.wip.accounting.line'
    BATCH_PRODUCE = 'mrp.batch.produce'
    BOM_BYPRODUCT = 'mrp.bom.byproduct'
    BOM_LINE = 'mrp.bom.line'
    BOM = 'mrp.bom'
    BILLS = 'mrp.bom'
    MATERIAL_BILLS = 'mrp.bom'
    CONSUMPTION_WARNING = 'mrp.consumption.warning'
    CONSUMPTION_WARNING_LINE = 'mrp.consumption.warning.line'
    PRODUCTION_BACKORDER = 'mrp.production.backorder'
    PRODUCTION_BACKORDER_LINE = 'mrp.production.backorder.line'
    PRODUCTION_SPLIT = 'mrp.production.split'
    PRODUCTION_SPLIT_LINE = 'mrp.production.split.line'
    PRODUCTION_SPLIT_MULTI = 'mrp.production.split.multi'
    PRODUCTION = 'mrp.production'
    REPORT = 'mrp.report'
    ROUTING_WORKCENTER = 'mrp.routing.workcenter'
    UNBUILD = 'mrp.unbuild'
    WORKCENTER_CAPACITY = 'mrp.workcenter.capacity'
    WORKCENTER_PRODUCTIVITY = 'mrp.workcenter.productivity'
    WORKCENTER_PRODUCTIVITY_LOSS = 'mrp.workcenter.productivity.loss'
    WORKCENTER_PRODUCTIVITY_LOSS_TYPE = 'mrp.workcenter.productivity.loss.type'
    WORKCENTER_TAG = 'mrp.workcenter.tag'
    WORKCENTER = 'mrp.workcenter'
    WORKORDER = 'mrp.workorder'
    ADDITIONAL_WORKORDER = 'mrp_production.additional.workorder'
    modules = None
    def export_to_dict(self):
        return self.__dict__.copy()
    
MANUFACTORY = Manufactory()
MANUFACTORY.modules = MANUFACTORY.export_to_dict()
FACTORY = Manufactory()
FACTORY.modules = FACTORY.export_to_dict()
