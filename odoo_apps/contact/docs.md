Contact representation


`account_move_count`: [integer] Account Move Count
`account_represented_company_ids`: [one2many] Account Represented Company
`active`: [boolean] Active
`active_lang_count`: [integer] Active Lang Count
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
`application_statistics`: [json] Stats
`autopost_bills`: [selection] Automatically post bills for this trusted partner
    - `always` -> `Always`
    - `ask` -> `Ask after 3 validations without edits`
    - `never` -> `Never`
`available_invoice_template_pdf_report_ids`: [one2many] Available Invoice Template Pdf Report
`available_peppol_eas`: [json] Available Peppol Eas
`avatar_1024`: [binary] Avatar 1024
`avatar_128`: [binary] Avatar 128
`avatar_1920`: [binary] Avatar
`avatar_256`: [binary] Avatar 256
`avatar_512`: [binary] Avatar 512
`bank_account_count`: [integer] Bank
`bank_ids`: [one2many] Banks
`barcode`: [char] Use a barcode to identify this contact.
`buyer_id`: [many2one] Buyer
`calendar_last_notif_ack`: [datetime] Last notification marked as read from base Calendar
`category_id`: [many2many] Tags
`certifications_company_count`: [integer] Company Certifications Count
`certifications_count`: [integer] Certifications Count
`channel_ids`: [many2many] Channels
`channel_member_ids`: [one2many] Channel Member
`child_ids`: [one2many] Contact
`city`: [char] City
`color`: [integer] Color Index
`comment`: [html] Notes
`commercial_company_name`: [char] Company Name Entity
`commercial_partner_id`: [many2one] Commercial Entity
`company_id`: [many2one] Company
`company_name`: [char] Company Name
`company_registry`: [char] The registry number of the company. Use it if it is different from the Tax ID. It must be unique across all partners of a same country
`company_registry_label`: [char] Company ID Label
`company_registry_placeholder`: [char] Company Registry Placeholder
`company_type`: [selection] Company Type
    - `person` -> `Person`
    - `company` -> `Company`
`complete_name`: [char] Complete Name
`contact_address`: [char] Complete Address
`contact_address_complete`: [char] Contact Address Complete
`contact_address_inline`: [char] Inlined Complete Address
`contract_ids`: [one2many] Partner Contracts
`country_code`: [char] The ISO country code in two chars. 
    You can use this field for quick search.
`country_id`: [many2one] Country
`create_date`: [datetime] Created on
`create_uid`: [many2one] Created by
`credit`: [monetary] Total amount this customer owes you.
`credit_limit`: [float] Credit limit specific to this partner.
`credit_to_invoice`: [monetary] Credit To Invoice
`currency_id`: [many2one] Currency
`customer_rank`: [integer] Customer Rank
`days_sales_outstanding`: [float] [(Total Receivable/Total Revenue) * number of days since the first invoice] for this customer
`debit`: [monetary] Total amount you have to pay to this vendor.
`display_invoice_edi_format`: [boolean] Display Invoice Edi Format
`display_invoice_template_pdf_report_id`: [boolean] Display Invoice Template Pdf Report
`display_name`: [char] Display Name
`duplicate_bank_partner_ids`: [many2many] Duplicate Bank Partner
`duplicated_bank_account_partners_count`: [integer] Duplicated Bank Account Partners Count
`email`: [char] Email
`email_formatted`: [char] Format email address "Name <email@domain>"
`email_normalized`: [char] This field is used to search on email address as the primary email field can contain more than strictly an email address.
`employee`: [boolean] Whether this contact is an Employee.
`employee_ids`: [one2many] Related employees based on their private address
`employees_count`: [integer] Employees Count
`fiscal_country_codes`: [char] Fiscal Country Codes
`followup_line_id`: [many2one] Follow-up Level
`followup_next_action_date`: [date] No follow-up action will be taken before this date.
            Sending a reminder will set this date depending on the levels configuration, and you can change it manually.
`followup_reminder_type`: [selection] Reminders
    - `automatic` -> `Automatic`
    - `manual` -> `Manual`
`followup_responsible_id`: [many2one] The responsible assigned to manual followup activities, if defined in the level.
`followup_status`: [selection] Follow-up Status
    - `in_need_of_action` -> `In need of action`
    - `with_overdue_invoices` -> `With overdue invoices`
    - `no_action_needed` -> `No action needed`
`function`: [char] Job Position
`has_message`: [boolean] Has Message
`has_moves`: [boolean] Has Moves
`id`: [integer] ID
`ignore_abnormal_invoice_amount`: [boolean] Ignore Abnormal Invoice Amount
`ignore_abnormal_invoice_date`: [boolean] Ignore Abnormal Invoice Date
`im_status`: [char] IM Status
`image_1024`: [binary] Image 1024
`image_128`: [binary] Image 128
`image_1920`: [binary] Image
`image_256`: [binary] Image 256
`image_512`: [binary] Image 512
`image_medium`: [binary] Medium-sized image
`industry_id`: [many2one] Industry
`invoice_edi_format`: [selection] eInvoice format
    - `facturx` -> `France (FacturX)`
    - `ubl_bis3` -> `EU Standard (Peppol Bis 3.0)`
    - `xrechnung` -> `Germany (XRechnung)`
    - `nlcius` -> `Netherlands (NLCIUS)`
    - `ubl_a_nz` -> `Australia BIS Billing 3.0 A-NZ`
    - `ubl_sg` -> `Singapore BIS Billing 3.0 SG`
`invoice_edi_format_store`: [char] Invoice Edi Format Store
`invoice_ids`: [one2many] Invoices
`invoice_sending_method`: [selection] Invoice sending
    - `manual` -> `Manual`
    - `email` -> `by Email`
    - `snailmail` -> `by Post`
`invoice_template_pdf_report_id`: [many2one] Invoice report
`is_blacklisted`: [boolean] If the email address is on the blacklist, the contact won't receive mass mailing anymore, from any list
`is_company`: [boolean] Check if the contact is a company, otherwise it is a person
`is_in_call`: [boolean] Is In Call
`is_peppol_edi_format`: [boolean] Is Peppol Edi Format
`is_public`: [boolean] Is Public
`is_ubl_format`: [boolean] Is Ubl Format
`l10n_mx_edi_addenda_ids`: [many2many] Addendas & Complementos
`l10n_mx_edi_fiscal_regime`: [selection] Fiscal Regime is required for all partners (used in CFDI)
    - `601` -> `General de Ley Personas Morales`
    - `603` -> `Personas Morales con Fines no Lucrativos`
    - `605` -> `Sueldos y Salarios e Ingresos Asimilados a Salarios`
    - `606` -> `Arrendamiento`
    - `607` -> `Régimen de Enajenación o Adquisición de Bienes`
    - `608` -> `Demás ingresos`
    - `609` -> `Consolidación`
    - `610` -> `Residentes en el Extranjero sin Establecimiento Permanente en México`
    - `611` -> `Ingresos por Dividendos (socios y accionistas)`
    - `612` -> `Personas Físicas con Actividades Empresariales y Profesionales`
    - `614` -> `Ingresos por intereses`
    - `615` -> `Régimen de los ingresos por obtención de premios`
    - `616` -> `Sin obligaciones fiscales`
    - `620` -> `Sociedades Cooperativas de Producción que optan por diferir sus ingresos`
    - `621` -> `Incorporación Fiscal`
    - `622` -> `Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras`
    - `623` -> `Opcional para Grupos de Sociedades`
    - `624` -> `Coordinados`
    - `625` -> `Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas`
    - `626` -> `Régimen Simplificado de Confianza - RESICO`
    - `628` -> `Hidrocarburos`
    - `629` -> `De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales`
    - `630` -> `Enajenación de acciones en bolsa de valores`
`l10n_mx_edi_ieps_breakdown`: [boolean] IEPS Breakdown
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
`l10n_mx_nationality`: [char] Mexico: Nationality based in the supplier country. Is the seventh column in DIOT report.
`l10n_mx_type_of_operation`: [selection] Type of Operation
    - `02` -> ` 02 - Alienation of Assets`
    - `03` -> ` 03 - Provision of Professional Services`
    - `06` -> ` 06 - Renting of buildings`
    - `07` -> ` 07 - Import of goods or services`
    - `08` -> ` 08 - Import via virtual transfer`
    - `85` -> ` 85 - Others`
    - `87` -> ` 87 - Global Operations`
`l10n_mx_type_of_third`: [char] Mexico: Describes what type of third party the supplier is. This is the first column in DIOT report.
`lang`: [selection] All the emails and documents sent to this contact will be translated in this language.
    - `es_419` -> `Spanish (Latin America) / Español (América Latina)`
    - `es_MX` -> `Spanish (MX) / Español (MX)`
`main_user_id`: [many2one] There can be several users related to the same partner. When a single user is needed, this field attempts to find the most appropriate one.
`meeting_count`: [integer] # Meetings
`meeting_ids`: [many2many] Meetings
`message_attachment_count`: [integer] Attachment Count
`message_bounce`: [integer] Counter of the number of bounced emails for this contact
`message_follower_ids`: [one2many] Followers
`message_has_error`: [boolean] If checked, some messages have a delivery error.
`message_has_error_counter`: [integer] Number of messages with delivery error
`message_has_sms_error`: [boolean] If checked, some messages have a delivery error.
`message_ids`: [one2many] Messages
`message_is_follower`: [boolean] Is Follower
`message_needaction`: [boolean] If checked, new messages require your attention.
`message_needaction_counter`: [integer] Number of messages requiring action
`message_partner_ids`: [many2many] Followers (Partners)
`my_activity_date_deadline`: [date] My Activity Deadline
`name`: [char] Name
`ocn_token`: [char] Used for sending notification to registered devices
`offline_since`: [datetime] Offline since
`on_time_rate`: [float] Over the past x days; the number of products received on time divided by the number of ordered products.x is either the System Parameter purchase_stock.on_time_delivery_days or the default 365
`online_partner_information`: [char] Online Partner Information
`parent_id`: [many2one] Related Company
`parent_name`: [char] Parent name
`partner_company_registry_placeholder`: [char] Partner Company Registry Placeholder
`partner_latitude`: [float] Geo Latitude
`partner_longitude`: [float] Geo Longitude
`partner_share`: [boolean] Either customer (not a user), either shared user. Indicated the current partner is a customer without access or with a limited access created for sharing data.
`partner_vat_placeholder`: [char] Partner Vat Placeholder
`payment_token_count`: [integer] Payment Token Count
`payment_token_ids`: [one2many] Payment Tokens
`peppol_eas`: [selection] Code used to identify the Endpoint for BIS Billing 3.0 and its derivatives.
            List available at https://docs.peppol.eu/poacc/billing/3.0/codelist/eas/
    - `9923` -> `Albania VAT`
    - `9922` -> `Andorra VAT`
    - `0151` -> `Australia ABN`
    - `9914` -> `Austria UID`
    - `9915` -> `Austria VOKZ`
    - `0208` -> `Belgian Company Registry`
    - `9925` -> `Belgian VAT`
    - `9924` -> `Bosnia and Herzegovina VAT`
    - `9926` -> `Bulgaria VAT`
    - `9934` -> `Croatia VAT`
    - `9928` -> `Cyprus VAT`
    - `9929` -> `Czech Republic VAT`
    - `0096` -> `Denmark P`
    - `0184` -> `Denmark CVR`
    - `0198` -> `Denmark SE`
    - `0191` -> `Estonia Company code`
    - `9931` -> `Estonia VAT`
    - `0037` -> `Finland LY-tunnus`
    - `0216` -> `Finland OVT code`
    - `0213` -> `Finland VAT`
    - `0002` -> `France SIRENE`
    - `0009` -> `France SIRET`
    - `9957` -> `France VAT`
    - `0225` -> `France FRCTC Electronic Address`
    - `0240` -> `France Register of legal persons`
    - `0204` -> `Germany Leitweg-ID`
    - `9930` -> `Germany VAT`
    - `9933` -> `Greece VAT`
    - `9910` -> `Hungary VAT`
    - `0196` -> `Iceland Kennitala`
    - `9935` -> `Ireland VAT`
    - `0211` -> `Italia Partita IVA`
    - `0097` -> `Italia FTI`
    - `0188` -> `Japan SST`
    - `0221` -> `Japan IIN`
    - `0218` -> `Latvia Unified registration number`
    - `9939` -> `Latvia VAT`
    - `9936` -> `Liechtenstein VAT`
    - `0200` -> `Lithuania JAK`
    - `9937` -> `Lithuania VAT`
    - `9938` -> `Luxembourg VAT`
    - `9942` -> `Macedonia VAT`
    - `0230` -> `Malaysia`
    - `9943` -> `Malta VAT`
    - `9940` -> `Monaco VAT`
    - `9941` -> `Montenegro VAT`
    - `0106` -> `Netherlands KvK`
    - `0190` -> `Netherlands OIN`
    - `9944` -> `Netherlands VAT`
    - `0192` -> `Norway Org.nr.`
    - `9945` -> `Poland VAT`
    - `9946` -> `Portugal VAT`
    - `9947` -> `Romania VAT`
    - `9948` -> `Serbia VAT`
    - `0195` -> `Singapore UEN`
    - `9949` -> `Slovenia VAT`
    - `9950` -> `Slovakia VAT`
    - `9920` -> `Spain VAT`
    - `0007` -> `Sweden Org.nr.`
    - `9955` -> `Sweden VAT`
    - `9927` -> `Swiss VAT`
    - `0183` -> `Swiss UIDB`
    - `9952` -> `Turkey VAT`
    - `0235` -> `UAE Tax Identification Number (TIN)`
    - `9932` -> `United Kingdom VAT`
    - `9959` -> `USA EIN`
    - `0060` -> `DUNS Number`
    - `0088` -> `EAN Location Code`
    - `0130` -> `Directorates of the European Commission`
    - `0135` -> `SIA Object Identifiers`
    - `0142` -> `SECETI Object Identifiers`
    - `0193` -> `UBL.BE party identifier`
    - `0199` -> `Legal Entity Identifier (LEI)`
    - `0201` -> `Codice Univoco Unità Organizzativa iPA`
    - `0202` -> `Indirizzo di Posta Elettronica Certificata`
    - `0209` -> `GS1 identification keys`
    - `0210` -> `Codice Fiscale`
    - `9913` -> `Business Registers Network`
    - `9918` -> `S.W.I.F.T`
    - `9919` -> `Kennziffer des Unternehmensregisters`
    - `9951` -> `San Marino VAT`
    - `9953` -> `Vatican VAT`
    - `AN` -> `O.F.T.P. (ODETTE File Transfer Protocol)`
    - `AQ` -> `X.400 address for mail text`
    - `AS` -> `AS2 exchange`
    - `AU` -> `File Transfer Protocol`
    - `EM` -> `Electronic mail`
`peppol_endpoint`: [char] Unique identifier used by the BIS Billing 3.0 and its derivatives, also known as 'Endpoint ID'.
`perform_vies_validation`: [boolean] Perform Vies Validation
`phone`: [char] Phone
`phone_blacklisted`: [boolean] Indicates if a blacklisted sanitized phone number is a phone number. Helps distinguish which number is blacklisted             when there is both a mobile and phone field in a model.
`phone_mobile_search`: [char] Phone Number
`phone_sanitized`: [char] Field used to store sanitized phone number. Helps speeding up searches and comparisons.
`phone_sanitized_blacklisted`: [boolean] If the sanitized phone number is on the blacklist, the contact won't receive mass mailing sms anymore, from any list
`picking_warn_msg`: [text] Message for Stock Picking
`project_ids`: [one2many] Projects
`property_account_payable_id`: [many2one] Account Payable
`property_account_position_id`: [many2one] The fiscal position determines the taxes/accounts used for this contact.
`property_account_receivable_id`: [many2one] Account Receivable
`property_inbound_payment_method_line_id`: [many2one] Property Inbound Payment Method Line
`property_outbound_payment_method_line_id`: [many2one] Property Outbound Payment Method Line
`property_payment_term_id`: [many2one] Customer Payment Terms
`property_product_pricelist`: [many2one] Used for sales to the current partner
`property_purchase_currency_id`: [many2one] This currency will be used for purchases from the current partner
`property_stock_customer`: [many2one] The stock location used as destination when sending goods to this contact.
`property_stock_supplier`: [many2one] The stock location used as source when receiving goods from this contact.
`property_supplier_payment_term_id`: [many2one] Vendor Payment Terms
`purchase_line_ids`: [one2many] Purchase Lines
`purchase_order_count`: [integer] Purchase Order Count
`purchase_warn_msg`: [text] Message for Purchase Order
`rating_ids`: [one2many] Ratings
`receipt_reminder_email`: [boolean] Automatically send a confirmation email to the vendor X days before the expected receipt date, asking him to confirm the exact date.
`ref`: [char] Reference
`ref_company_ids`: [one2many] Companies that refers to partner
`reminder_date_before_receipt`: [integer] Number of days to send reminder email before the promised receipt date
`rtc_session_ids`: [one2many] Rtc Session
`sale_order_count`: [integer] Sale Order Count
`sale_order_ids`: [one2many] Sales Order
`sale_warn_msg`: [text] Message for Sales Order
`same_company_registry_partner_id`: [many2one] Partner with same Company Registry
`same_vat_partner_id`: [many2one] Partner with same Tax ID
`self`: [many2one] Self
`show_credit_limit`: [boolean] Show Credit Limit
`signature_count`: [integer] # Signatures
`signup_type`: [char] Signup Token Type
`specific_property_product_pricelist`: [many2one] Specific Property Product Pricelist
`starred_message_ids`: [many2many] Starred Message
`state_id`: [many2one] State
`street`: [char] Street
`street2`: [char] Street2
`supplier_invoice_count`: [integer] # Vendor Bills
`supplier_rank`: [integer] Supplier Rank
`task_count`: [integer] # Tasks
`task_ids`: [one2many] Tasks
`total_all_due`: [monetary] Total All Due
`total_all_overdue`: [monetary] Total All Overdue
`total_due`: [monetary] Total Due
`total_invoiced`: [monetary] Total Invoiced
`total_overdue`: [monetary] Total Overdue
`trust`: [selection] Degree of trust you have in this debtor
    - `good` -> `Good Debtor`
    - `normal` -> `Normal Debtor`
    - `bad` -> `Bad Debtor`
`type`: [selection] Address Type
    - `contact` -> `Contact`
    - `invoice` -> `Invoice`
    - `delivery` -> `Delivery`
    - `other` -> `Other`
`type_address_label`: [char] Address Type Description
`tz`: [selection] When printing documents and exporting/importing data, time values are computed according to this timezone.
    If the timezone is not set, UTC (Coordinated Universal Time) is used.
    Anywhere else, time values are computed according to the time offset of your web client.
    - `Africa/Abidjan` -> `Africa/Abidjan`
    - `Africa/Accra` -> `Africa/Accra`
    - `Africa/Addis_Ababa` -> `Africa/Addis_Ababa`
    - `Africa/Algiers` -> `Africa/Algiers`
    - `Africa/Asmara` -> `Africa/Asmara`
    - `Africa/Asmera` -> `Africa/Asmera`
    - `Africa/Bamako` -> `Africa/Bamako`
    - `Africa/Bangui` -> `Africa/Bangui`
    - `Africa/Banjul` -> `Africa/Banjul`
    - `Africa/Bissau` -> `Africa/Bissau`
    - `Africa/Blantyre` -> `Africa/Blantyre`
    - `Africa/Brazzaville` -> `Africa/Brazzaville`
    - `Africa/Bujumbura` -> `Africa/Bujumbura`
    - `Africa/Cairo` -> `Africa/Cairo`
    - `Africa/Casablanca` -> `Africa/Casablanca`
    - `Africa/Ceuta` -> `Africa/Ceuta`
    - `Africa/Conakry` -> `Africa/Conakry`
    - `Africa/Dakar` -> `Africa/Dakar`
    - `Africa/Dar_es_Salaam` -> `Africa/Dar_es_Salaam`
    - `Africa/Djibouti` -> `Africa/Djibouti`
    - `Africa/Douala` -> `Africa/Douala`
    - `Africa/El_Aaiun` -> `Africa/El_Aaiun`
    - `Africa/Freetown` -> `Africa/Freetown`
    - `Africa/Gaborone` -> `Africa/Gaborone`
    - `Africa/Harare` -> `Africa/Harare`
    - `Africa/Johannesburg` -> `Africa/Johannesburg`
    - `Africa/Juba` -> `Africa/Juba`
    - `Africa/Kampala` -> `Africa/Kampala`
    - `Africa/Khartoum` -> `Africa/Khartoum`
    - `Africa/Kigali` -> `Africa/Kigali`
    - `Africa/Kinshasa` -> `Africa/Kinshasa`
    - `Africa/Lagos` -> `Africa/Lagos`
    - `Africa/Libreville` -> `Africa/Libreville`
    - `Africa/Lome` -> `Africa/Lome`
    - `Africa/Luanda` -> `Africa/Luanda`
    - `Africa/Lubumbashi` -> `Africa/Lubumbashi`
    - `Africa/Lusaka` -> `Africa/Lusaka`
    - `Africa/Malabo` -> `Africa/Malabo`
    - `Africa/Maputo` -> `Africa/Maputo`
    - `Africa/Maseru` -> `Africa/Maseru`
    - `Africa/Mbabane` -> `Africa/Mbabane`
    - `Africa/Mogadishu` -> `Africa/Mogadishu`
    - `Africa/Monrovia` -> `Africa/Monrovia`
    - `Africa/Nairobi` -> `Africa/Nairobi`
    - `Africa/Ndjamena` -> `Africa/Ndjamena`
    - `Africa/Niamey` -> `Africa/Niamey`
    - `Africa/Nouakchott` -> `Africa/Nouakchott`
    - `Africa/Ouagadougou` -> `Africa/Ouagadougou`
    - `Africa/Porto-Novo` -> `Africa/Porto-Novo`
    - `Africa/Sao_Tome` -> `Africa/Sao_Tome`
    - `Africa/Timbuktu` -> `Africa/Timbuktu`
    - `Africa/Tripoli` -> `Africa/Tripoli`
    - `Africa/Tunis` -> `Africa/Tunis`
    - `Africa/Windhoek` -> `Africa/Windhoek`
    - `America/Adak` -> `America/Adak`
    - `America/Anchorage` -> `America/Anchorage`
    - `America/Anguilla` -> `America/Anguilla`
    - `America/Antigua` -> `America/Antigua`
    - `America/Araguaina` -> `America/Araguaina`
    - `America/Argentina/Buenos_Aires` -> `America/Argentina/Buenos_Aires`
    - `America/Argentina/Catamarca` -> `America/Argentina/Catamarca`
    - `America/Argentina/ComodRivadavia` -> `America/Argentina/ComodRivadavia`
    - `America/Argentina/Cordoba` -> `America/Argentina/Cordoba`
    - `America/Argentina/Jujuy` -> `America/Argentina/Jujuy`
    - `America/Argentina/La_Rioja` -> `America/Argentina/La_Rioja`
    - `America/Argentina/Mendoza` -> `America/Argentina/Mendoza`
    - `America/Argentina/Rio_Gallegos` -> `America/Argentina/Rio_Gallegos`
    - `America/Argentina/Salta` -> `America/Argentina/Salta`
    - `America/Argentina/San_Juan` -> `America/Argentina/San_Juan`
    - `America/Argentina/San_Luis` -> `America/Argentina/San_Luis`
    - `America/Argentina/Tucuman` -> `America/Argentina/Tucuman`
    - `America/Argentina/Ushuaia` -> `America/Argentina/Ushuaia`
    - `America/Aruba` -> `America/Aruba`
    - `America/Asuncion` -> `America/Asuncion`
    - `America/Atikokan` -> `America/Atikokan`
    - `America/Atka` -> `America/Atka`
    - `America/Bahia` -> `America/Bahia`
    - `America/Bahia_Banderas` -> `America/Bahia_Banderas`
    - `America/Barbados` -> `America/Barbados`
    - `America/Belem` -> `America/Belem`
    - `America/Belize` -> `America/Belize`
    - `America/Blanc-Sablon` -> `America/Blanc-Sablon`
    - `America/Boa_Vista` -> `America/Boa_Vista`
    - `America/Bogota` -> `America/Bogota`
    - `America/Boise` -> `America/Boise`
    - `America/Buenos_Aires` -> `America/Buenos_Aires`
    - `America/Cambridge_Bay` -> `America/Cambridge_Bay`
    - `America/Campo_Grande` -> `America/Campo_Grande`
    - `America/Cancun` -> `America/Cancun`
    - `America/Caracas` -> `America/Caracas`
    - `America/Catamarca` -> `America/Catamarca`
    - `America/Cayenne` -> `America/Cayenne`
    - `America/Cayman` -> `America/Cayman`
    - `America/Chicago` -> `America/Chicago`
    - `America/Chihuahua` -> `America/Chihuahua`
    - `America/Ciudad_Juarez` -> `America/Ciudad_Juarez`
    - `America/Coral_Harbour` -> `America/Coral_Harbour`
    - `America/Cordoba` -> `America/Cordoba`
    - `America/Costa_Rica` -> `America/Costa_Rica`
    - `America/Coyhaique` -> `America/Coyhaique`
    - `America/Creston` -> `America/Creston`
    - `America/Cuiaba` -> `America/Cuiaba`
    - `America/Curacao` -> `America/Curacao`
    - `America/Danmarkshavn` -> `America/Danmarkshavn`
    - `America/Dawson` -> `America/Dawson`
    - `America/Dawson_Creek` -> `America/Dawson_Creek`
    - `America/Denver` -> `America/Denver`
    - `America/Detroit` -> `America/Detroit`
    - `America/Dominica` -> `America/Dominica`
    - `America/Edmonton` -> `America/Edmonton`
    - `America/Eirunepe` -> `America/Eirunepe`
    - `America/El_Salvador` -> `America/El_Salvador`
    - `America/Ensenada` -> `America/Ensenada`
    - `America/Fort_Nelson` -> `America/Fort_Nelson`
    - `America/Fort_Wayne` -> `America/Fort_Wayne`
    - `America/Fortaleza` -> `America/Fortaleza`
    - `America/Glace_Bay` -> `America/Glace_Bay`
    - `America/Godthab` -> `America/Godthab`
    - `America/Goose_Bay` -> `America/Goose_Bay`
    - `America/Grand_Turk` -> `America/Grand_Turk`
    - `America/Grenada` -> `America/Grenada`
    - `America/Guadeloupe` -> `America/Guadeloupe`
    - `America/Guatemala` -> `America/Guatemala`
    - `America/Guayaquil` -> `America/Guayaquil`
    - `America/Guyana` -> `America/Guyana`
    - `America/Halifax` -> `America/Halifax`
    - `America/Havana` -> `America/Havana`
    - `America/Hermosillo` -> `America/Hermosillo`
    - `America/Indiana/Indianapolis` -> `America/Indiana/Indianapolis`
    - `America/Indiana/Knox` -> `America/Indiana/Knox`
    - `America/Indiana/Marengo` -> `America/Indiana/Marengo`
    - `America/Indiana/Petersburg` -> `America/Indiana/Petersburg`
    - `America/Indiana/Tell_City` -> `America/Indiana/Tell_City`
    - `America/Indiana/Vevay` -> `America/Indiana/Vevay`
    - `America/Indiana/Vincennes` -> `America/Indiana/Vincennes`
    - `America/Indiana/Winamac` -> `America/Indiana/Winamac`
    - `America/Indianapolis` -> `America/Indianapolis`
    - `America/Inuvik` -> `America/Inuvik`
    - `America/Iqaluit` -> `America/Iqaluit`
    - `America/Jamaica` -> `America/Jamaica`
    - `America/Jujuy` -> `America/Jujuy`
    - `America/Juneau` -> `America/Juneau`
    - `America/Kentucky/Louisville` -> `America/Kentucky/Louisville`
    - `America/Kentucky/Monticello` -> `America/Kentucky/Monticello`
    - `America/Knox_IN` -> `America/Knox_IN`
    - `America/Kralendijk` -> `America/Kralendijk`
    - `America/La_Paz` -> `America/La_Paz`
    - `America/Lima` -> `America/Lima`
    - `America/Los_Angeles` -> `America/Los_Angeles`
    - `America/Louisville` -> `America/Louisville`
    - `America/Lower_Princes` -> `America/Lower_Princes`
    - `America/Maceio` -> `America/Maceio`
    - `America/Managua` -> `America/Managua`
    - `America/Manaus` -> `America/Manaus`
    - `America/Marigot` -> `America/Marigot`
    - `America/Martinique` -> `America/Martinique`
    - `America/Matamoros` -> `America/Matamoros`
    - `America/Mazatlan` -> `America/Mazatlan`
    - `America/Mendoza` -> `America/Mendoza`
    - `America/Menominee` -> `America/Menominee`
    - `America/Merida` -> `America/Merida`
    - `America/Metlakatla` -> `America/Metlakatla`
    - `America/Mexico_City` -> `America/Mexico_City`
    - `America/Miquelon` -> `America/Miquelon`
    - `America/Moncton` -> `America/Moncton`
    - `America/Monterrey` -> `America/Monterrey`
    - `America/Montevideo` -> `America/Montevideo`
    - `America/Montreal` -> `America/Montreal`
    - `America/Montserrat` -> `America/Montserrat`
    - `America/Nassau` -> `America/Nassau`
    - `America/New_York` -> `America/New_York`
    - `America/Nipigon` -> `America/Nipigon`
    - `America/Nome` -> `America/Nome`
    - `America/Noronha` -> `America/Noronha`
    - `America/North_Dakota/Beulah` -> `America/North_Dakota/Beulah`
    - `America/North_Dakota/Center` -> `America/North_Dakota/Center`
    - `America/North_Dakota/New_Salem` -> `America/North_Dakota/New_Salem`
    - `America/Nuuk` -> `America/Nuuk`
    - `America/Ojinaga` -> `America/Ojinaga`
    - `America/Panama` -> `America/Panama`
    - `America/Pangnirtung` -> `America/Pangnirtung`
    - `America/Paramaribo` -> `America/Paramaribo`
    - `America/Phoenix` -> `America/Phoenix`
    - `America/Port-au-Prince` -> `America/Port-au-Prince`
    - `America/Port_of_Spain` -> `America/Port_of_Spain`
    - `America/Porto_Acre` -> `America/Porto_Acre`
    - `America/Porto_Velho` -> `America/Porto_Velho`
    - `America/Puerto_Rico` -> `America/Puerto_Rico`
    - `America/Punta_Arenas` -> `America/Punta_Arenas`
    - `America/Rainy_River` -> `America/Rainy_River`
    - `America/Rankin_Inlet` -> `America/Rankin_Inlet`
    - `America/Recife` -> `America/Recife`
    - `America/Regina` -> `America/Regina`
    - `America/Resolute` -> `America/Resolute`
    - `America/Rio_Branco` -> `America/Rio_Branco`
    - `America/Rosario` -> `America/Rosario`
    - `America/Santa_Isabel` -> `America/Santa_Isabel`
    - `America/Santarem` -> `America/Santarem`
    - `America/Santiago` -> `America/Santiago`
    - `America/Santo_Domingo` -> `America/Santo_Domingo`
    - `America/Sao_Paulo` -> `America/Sao_Paulo`
    - `America/Scoresbysund` -> `America/Scoresbysund`
    - `America/Shiprock` -> `America/Shiprock`
    - `America/Sitka` -> `America/Sitka`
    - `America/St_Barthelemy` -> `America/St_Barthelemy`
    - `America/St_Johns` -> `America/St_Johns`
    - `America/St_Kitts` -> `America/St_Kitts`
    - `America/St_Lucia` -> `America/St_Lucia`
    - `America/St_Thomas` -> `America/St_Thomas`
    - `America/St_Vincent` -> `America/St_Vincent`
    - `America/Swift_Current` -> `America/Swift_Current`
    - `America/Tegucigalpa` -> `America/Tegucigalpa`
    - `America/Thule` -> `America/Thule`
    - `America/Thunder_Bay` -> `America/Thunder_Bay`
    - `America/Tijuana` -> `America/Tijuana`
    - `America/Toronto` -> `America/Toronto`
    - `America/Tortola` -> `America/Tortola`
    - `America/Vancouver` -> `America/Vancouver`
    - `America/Virgin` -> `America/Virgin`
    - `America/Whitehorse` -> `America/Whitehorse`
    - `America/Winnipeg` -> `America/Winnipeg`
    - `America/Yakutat` -> `America/Yakutat`
    - `America/Yellowknife` -> `America/Yellowknife`
    - `Antarctica/Casey` -> `Antarctica/Casey`
    - `Antarctica/Davis` -> `Antarctica/Davis`
    - `Antarctica/DumontDUrville` -> `Antarctica/DumontDUrville`
    - `Antarctica/Macquarie` -> `Antarctica/Macquarie`
    - `Antarctica/Mawson` -> `Antarctica/Mawson`
    - `Antarctica/McMurdo` -> `Antarctica/McMurdo`
    - `Antarctica/Palmer` -> `Antarctica/Palmer`
    - `Antarctica/Rothera` -> `Antarctica/Rothera`
    - `Antarctica/South_Pole` -> `Antarctica/South_Pole`
    - `Antarctica/Syowa` -> `Antarctica/Syowa`
    - `Antarctica/Troll` -> `Antarctica/Troll`
    - `Antarctica/Vostok` -> `Antarctica/Vostok`
    - `Arctic/Longyearbyen` -> `Arctic/Longyearbyen`
    - `Asia/Aden` -> `Asia/Aden`
    - `Asia/Almaty` -> `Asia/Almaty`
    - `Asia/Amman` -> `Asia/Amman`
    - `Asia/Anadyr` -> `Asia/Anadyr`
    - `Asia/Aqtau` -> `Asia/Aqtau`
    - `Asia/Aqtobe` -> `Asia/Aqtobe`
    - `Asia/Ashgabat` -> `Asia/Ashgabat`
    - `Asia/Ashkhabad` -> `Asia/Ashkhabad`
    - `Asia/Atyrau` -> `Asia/Atyrau`
    - `Asia/Baghdad` -> `Asia/Baghdad`
    - `Asia/Bahrain` -> `Asia/Bahrain`
    - `Asia/Baku` -> `Asia/Baku`
    - `Asia/Bangkok` -> `Asia/Bangkok`
    - `Asia/Barnaul` -> `Asia/Barnaul`
    - `Asia/Beirut` -> `Asia/Beirut`
    - `Asia/Bishkek` -> `Asia/Bishkek`
    - `Asia/Brunei` -> `Asia/Brunei`
    - `Asia/Calcutta` -> `Asia/Calcutta`
    - `Asia/Chita` -> `Asia/Chita`
    - `Asia/Choibalsan` -> `Asia/Choibalsan`
    - `Asia/Chongqing` -> `Asia/Chongqing`
    - `Asia/Chungking` -> `Asia/Chungking`
    - `Asia/Colombo` -> `Asia/Colombo`
    - `Asia/Dacca` -> `Asia/Dacca`
    - `Asia/Damascus` -> `Asia/Damascus`
    - `Asia/Dhaka` -> `Asia/Dhaka`
    - `Asia/Dili` -> `Asia/Dili`
    - `Asia/Dubai` -> `Asia/Dubai`
    - `Asia/Dushanbe` -> `Asia/Dushanbe`
    - `Asia/Famagusta` -> `Asia/Famagusta`
    - `Asia/Gaza` -> `Asia/Gaza`
    - `Asia/Harbin` -> `Asia/Harbin`
    - `Asia/Hebron` -> `Asia/Hebron`
    - `Asia/Ho_Chi_Minh` -> `Asia/Ho_Chi_Minh`
    - `Asia/Hong_Kong` -> `Asia/Hong_Kong`
    - `Asia/Hovd` -> `Asia/Hovd`
    - `Asia/Irkutsk` -> `Asia/Irkutsk`
    - `Asia/Istanbul` -> `Asia/Istanbul`
    - `Asia/Jakarta` -> `Asia/Jakarta`
    - `Asia/Jayapura` -> `Asia/Jayapura`
    - `Asia/Jerusalem` -> `Asia/Jerusalem`
    - `Asia/Kabul` -> `Asia/Kabul`
    - `Asia/Kamchatka` -> `Asia/Kamchatka`
    - `Asia/Karachi` -> `Asia/Karachi`
    - `Asia/Kashgar` -> `Asia/Kashgar`
    - `Asia/Kathmandu` -> `Asia/Kathmandu`
    - `Asia/Katmandu` -> `Asia/Katmandu`
    - `Asia/Khandyga` -> `Asia/Khandyga`
    - `Asia/Kolkata` -> `Asia/Kolkata`
    - `Asia/Krasnoyarsk` -> `Asia/Krasnoyarsk`
    - `Asia/Kuala_Lumpur` -> `Asia/Kuala_Lumpur`
    - `Asia/Kuching` -> `Asia/Kuching`
    - `Asia/Kuwait` -> `Asia/Kuwait`
    - `Asia/Macao` -> `Asia/Macao`
    - `Asia/Macau` -> `Asia/Macau`
    - `Asia/Magadan` -> `Asia/Magadan`
    - `Asia/Makassar` -> `Asia/Makassar`
    - `Asia/Manila` -> `Asia/Manila`
    - `Asia/Muscat` -> `Asia/Muscat`
    - `Asia/Nicosia` -> `Asia/Nicosia`
    - `Asia/Novokuznetsk` -> `Asia/Novokuznetsk`
    - `Asia/Novosibirsk` -> `Asia/Novosibirsk`
    - `Asia/Omsk` -> `Asia/Omsk`
    - `Asia/Oral` -> `Asia/Oral`
    - `Asia/Phnom_Penh` -> `Asia/Phnom_Penh`
    - `Asia/Pontianak` -> `Asia/Pontianak`
    - `Asia/Pyongyang` -> `Asia/Pyongyang`
    - `Asia/Qatar` -> `Asia/Qatar`
    - `Asia/Qostanay` -> `Asia/Qostanay`
    - `Asia/Qyzylorda` -> `Asia/Qyzylorda`
    - `Asia/Rangoon` -> `Asia/Rangoon`
    - `Asia/Riyadh` -> `Asia/Riyadh`
    - `Asia/Saigon` -> `Asia/Saigon`
    - `Asia/Sakhalin` -> `Asia/Sakhalin`
    - `Asia/Samarkand` -> `Asia/Samarkand`
    - `Asia/Seoul` -> `Asia/Seoul`
    - `Asia/Shanghai` -> `Asia/Shanghai`
    - `Asia/Singapore` -> `Asia/Singapore`
    - `Asia/Srednekolymsk` -> `Asia/Srednekolymsk`
    - `Asia/Taipei` -> `Asia/Taipei`
    - `Asia/Tashkent` -> `Asia/Tashkent`
    - `Asia/Tbilisi` -> `Asia/Tbilisi`
    - `Asia/Tehran` -> `Asia/Tehran`
    - `Asia/Tel_Aviv` -> `Asia/Tel_Aviv`
    - `Asia/Thimbu` -> `Asia/Thimbu`
    - `Asia/Thimphu` -> `Asia/Thimphu`
    - `Asia/Tokyo` -> `Asia/Tokyo`
    - `Asia/Tomsk` -> `Asia/Tomsk`
    - `Asia/Ujung_Pandang` -> `Asia/Ujung_Pandang`
    - `Asia/Ulaanbaatar` -> `Asia/Ulaanbaatar`
    - `Asia/Ulan_Bator` -> `Asia/Ulan_Bator`
    - `Asia/Urumqi` -> `Asia/Urumqi`
    - `Asia/Ust-Nera` -> `Asia/Ust-Nera`
    - `Asia/Vientiane` -> `Asia/Vientiane`
    - `Asia/Vladivostok` -> `Asia/Vladivostok`
    - `Asia/Yakutsk` -> `Asia/Yakutsk`
    - `Asia/Yangon` -> `Asia/Yangon`
    - `Asia/Yekaterinburg` -> `Asia/Yekaterinburg`
    - `Asia/Yerevan` -> `Asia/Yerevan`
    - `Atlantic/Azores` -> `Atlantic/Azores`
    - `Atlantic/Bermuda` -> `Atlantic/Bermuda`
    - `Atlantic/Canary` -> `Atlantic/Canary`
    - `Atlantic/Cape_Verde` -> `Atlantic/Cape_Verde`
    - `Atlantic/Faeroe` -> `Atlantic/Faeroe`
    - `Atlantic/Faroe` -> `Atlantic/Faroe`
    - `Atlantic/Jan_Mayen` -> `Atlantic/Jan_Mayen`
    - `Atlantic/Madeira` -> `Atlantic/Madeira`
    - `Atlantic/Reykjavik` -> `Atlantic/Reykjavik`
    - `Atlantic/South_Georgia` -> `Atlantic/South_Georgia`
    - `Atlantic/St_Helena` -> `Atlantic/St_Helena`
    - `Atlantic/Stanley` -> `Atlantic/Stanley`
    - `Australia/ACT` -> `Australia/ACT`
    - `Australia/Adelaide` -> `Australia/Adelaide`
    - `Australia/Brisbane` -> `Australia/Brisbane`
    - `Australia/Broken_Hill` -> `Australia/Broken_Hill`
    - `Australia/Canberra` -> `Australia/Canberra`
    - `Australia/Currie` -> `Australia/Currie`
    - `Australia/Darwin` -> `Australia/Darwin`
    - `Australia/Eucla` -> `Australia/Eucla`
    - `Australia/Hobart` -> `Australia/Hobart`
    - `Australia/LHI` -> `Australia/LHI`
    - `Australia/Lindeman` -> `Australia/Lindeman`
    - `Australia/Lord_Howe` -> `Australia/Lord_Howe`
    - `Australia/Melbourne` -> `Australia/Melbourne`
    - `Australia/NSW` -> `Australia/NSW`
    - `Australia/North` -> `Australia/North`
    - `Australia/Perth` -> `Australia/Perth`
    - `Australia/Queensland` -> `Australia/Queensland`
    - `Australia/South` -> `Australia/South`
    - `Australia/Sydney` -> `Australia/Sydney`
    - `Australia/Tasmania` -> `Australia/Tasmania`
    - `Australia/Victoria` -> `Australia/Victoria`
    - `Australia/West` -> `Australia/West`
    - `Australia/Yancowinna` -> `Australia/Yancowinna`
    - `Brazil/Acre` -> `Brazil/Acre`
    - `Brazil/DeNoronha` -> `Brazil/DeNoronha`
    - `Brazil/East` -> `Brazil/East`
    - `Brazil/West` -> `Brazil/West`
    - `CET` -> `CET`
    - `CST6CDT` -> `CST6CDT`
    - `Canada/Atlantic` -> `Canada/Atlantic`
    - `Canada/Central` -> `Canada/Central`
    - `Canada/Eastern` -> `Canada/Eastern`
    - `Canada/Mountain` -> `Canada/Mountain`
    - `Canada/Newfoundland` -> `Canada/Newfoundland`
    - `Canada/Pacific` -> `Canada/Pacific`
    - `Canada/Saskatchewan` -> `Canada/Saskatchewan`
    - `Canada/Yukon` -> `Canada/Yukon`
    - `Chile/Continental` -> `Chile/Continental`
    - `Chile/EasterIsland` -> `Chile/EasterIsland`
    - `Cuba` -> `Cuba`
    - `EET` -> `EET`
    - `EST` -> `EST`
    - `EST5EDT` -> `EST5EDT`
    - `Egypt` -> `Egypt`
    - `Eire` -> `Eire`
    - `Europe/Amsterdam` -> `Europe/Amsterdam`
    - `Europe/Andorra` -> `Europe/Andorra`
    - `Europe/Astrakhan` -> `Europe/Astrakhan`
    - `Europe/Athens` -> `Europe/Athens`
    - `Europe/Belfast` -> `Europe/Belfast`
    - `Europe/Belgrade` -> `Europe/Belgrade`
    - `Europe/Berlin` -> `Europe/Berlin`
    - `Europe/Bratislava` -> `Europe/Bratislava`
    - `Europe/Brussels` -> `Europe/Brussels`
    - `Europe/Bucharest` -> `Europe/Bucharest`
    - `Europe/Budapest` -> `Europe/Budapest`
    - `Europe/Busingen` -> `Europe/Busingen`
    - `Europe/Chisinau` -> `Europe/Chisinau`
    - `Europe/Copenhagen` -> `Europe/Copenhagen`
    - `Europe/Dublin` -> `Europe/Dublin`
    - `Europe/Gibraltar` -> `Europe/Gibraltar`
    - `Europe/Guernsey` -> `Europe/Guernsey`
    - `Europe/Helsinki` -> `Europe/Helsinki`
    - `Europe/Isle_of_Man` -> `Europe/Isle_of_Man`
    - `Europe/Istanbul` -> `Europe/Istanbul`
    - `Europe/Jersey` -> `Europe/Jersey`
    - `Europe/Kaliningrad` -> `Europe/Kaliningrad`
    - `Europe/Kiev` -> `Europe/Kiev`
    - `Europe/Kirov` -> `Europe/Kirov`
    - `Europe/Kyiv` -> `Europe/Kyiv`
    - `Europe/Lisbon` -> `Europe/Lisbon`
    - `Europe/Ljubljana` -> `Europe/Ljubljana`
    - `Europe/London` -> `Europe/London`
    - `Europe/Luxembourg` -> `Europe/Luxembourg`
    - `Europe/Madrid` -> `Europe/Madrid`
    - `Europe/Malta` -> `Europe/Malta`
    - `Europe/Mariehamn` -> `Europe/Mariehamn`
    - `Europe/Minsk` -> `Europe/Minsk`
    - `Europe/Monaco` -> `Europe/Monaco`
    - `Europe/Moscow` -> `Europe/Moscow`
    - `Europe/Nicosia` -> `Europe/Nicosia`
    - `Europe/Oslo` -> `Europe/Oslo`
    - `Europe/Paris` -> `Europe/Paris`
    - `Europe/Podgorica` -> `Europe/Podgorica`
    - `Europe/Prague` -> `Europe/Prague`
    - `Europe/Riga` -> `Europe/Riga`
    - `Europe/Rome` -> `Europe/Rome`
    - `Europe/Samara` -> `Europe/Samara`
    - `Europe/San_Marino` -> `Europe/San_Marino`
    - `Europe/Sarajevo` -> `Europe/Sarajevo`
    - `Europe/Saratov` -> `Europe/Saratov`
    - `Europe/Simferopol` -> `Europe/Simferopol`
    - `Europe/Skopje` -> `Europe/Skopje`
    - `Europe/Sofia` -> `Europe/Sofia`
    - `Europe/Stockholm` -> `Europe/Stockholm`
    - `Europe/Tallinn` -> `Europe/Tallinn`
    - `Europe/Tirane` -> `Europe/Tirane`
    - `Europe/Tiraspol` -> `Europe/Tiraspol`
    - `Europe/Ulyanovsk` -> `Europe/Ulyanovsk`
    - `Europe/Uzhgorod` -> `Europe/Uzhgorod`
    - `Europe/Vaduz` -> `Europe/Vaduz`
    - `Europe/Vatican` -> `Europe/Vatican`
    - `Europe/Vienna` -> `Europe/Vienna`
    - `Europe/Vilnius` -> `Europe/Vilnius`
    - `Europe/Volgograd` -> `Europe/Volgograd`
    - `Europe/Warsaw` -> `Europe/Warsaw`
    - `Europe/Zagreb` -> `Europe/Zagreb`
    - `Europe/Zaporozhye` -> `Europe/Zaporozhye`
    - `Europe/Zurich` -> `Europe/Zurich`
    - `GB` -> `GB`
    - `GB-Eire` -> `GB-Eire`
    - `GMT` -> `GMT`
    - `GMT+0` -> `GMT+0`
    - `GMT-0` -> `GMT-0`
    - `GMT0` -> `GMT0`
    - `Greenwich` -> `Greenwich`
    - `HST` -> `HST`
    - `Hongkong` -> `Hongkong`
    - `Iceland` -> `Iceland`
    - `Indian/Antananarivo` -> `Indian/Antananarivo`
    - `Indian/Chagos` -> `Indian/Chagos`
    - `Indian/Christmas` -> `Indian/Christmas`
    - `Indian/Cocos` -> `Indian/Cocos`
    - `Indian/Comoro` -> `Indian/Comoro`
    - `Indian/Kerguelen` -> `Indian/Kerguelen`
    - `Indian/Mahe` -> `Indian/Mahe`
    - `Indian/Maldives` -> `Indian/Maldives`
    - `Indian/Mauritius` -> `Indian/Mauritius`
    - `Indian/Mayotte` -> `Indian/Mayotte`
    - `Indian/Reunion` -> `Indian/Reunion`
    - `Iran` -> `Iran`
    - `Israel` -> `Israel`
    - `Jamaica` -> `Jamaica`
    - `Japan` -> `Japan`
    - `Kwajalein` -> `Kwajalein`
    - `Libya` -> `Libya`
    - `MET` -> `MET`
    - `MST` -> `MST`
    - `MST7MDT` -> `MST7MDT`
    - `Mexico/BajaNorte` -> `Mexico/BajaNorte`
    - `Mexico/BajaSur` -> `Mexico/BajaSur`
    - `Mexico/General` -> `Mexico/General`
    - `NZ` -> `NZ`
    - `NZ-CHAT` -> `NZ-CHAT`
    - `Navajo` -> `Navajo`
    - `PRC` -> `PRC`
    - `PST8PDT` -> `PST8PDT`
    - `Pacific/Apia` -> `Pacific/Apia`
    - `Pacific/Auckland` -> `Pacific/Auckland`
    - `Pacific/Bougainville` -> `Pacific/Bougainville`
    - `Pacific/Chatham` -> `Pacific/Chatham`
    - `Pacific/Chuuk` -> `Pacific/Chuuk`
    - `Pacific/Easter` -> `Pacific/Easter`
    - `Pacific/Efate` -> `Pacific/Efate`
    - `Pacific/Enderbury` -> `Pacific/Enderbury`
    - `Pacific/Fakaofo` -> `Pacific/Fakaofo`
    - `Pacific/Fiji` -> `Pacific/Fiji`
    - `Pacific/Funafuti` -> `Pacific/Funafuti`
    - `Pacific/Galapagos` -> `Pacific/Galapagos`
    - `Pacific/Gambier` -> `Pacific/Gambier`
    - `Pacific/Guadalcanal` -> `Pacific/Guadalcanal`
    - `Pacific/Guam` -> `Pacific/Guam`
    - `Pacific/Honolulu` -> `Pacific/Honolulu`
    - `Pacific/Johnston` -> `Pacific/Johnston`
    - `Pacific/Kanton` -> `Pacific/Kanton`
    - `Pacific/Kiritimati` -> `Pacific/Kiritimati`
    - `Pacific/Kosrae` -> `Pacific/Kosrae`
    - `Pacific/Kwajalein` -> `Pacific/Kwajalein`
    - `Pacific/Majuro` -> `Pacific/Majuro`
    - `Pacific/Marquesas` -> `Pacific/Marquesas`
    - `Pacific/Midway` -> `Pacific/Midway`
    - `Pacific/Nauru` -> `Pacific/Nauru`
    - `Pacific/Niue` -> `Pacific/Niue`
    - `Pacific/Norfolk` -> `Pacific/Norfolk`
    - `Pacific/Noumea` -> `Pacific/Noumea`
    - `Pacific/Pago_Pago` -> `Pacific/Pago_Pago`
    - `Pacific/Palau` -> `Pacific/Palau`
    - `Pacific/Pitcairn` -> `Pacific/Pitcairn`
    - `Pacific/Pohnpei` -> `Pacific/Pohnpei`
    - `Pacific/Ponape` -> `Pacific/Ponape`
    - `Pacific/Port_Moresby` -> `Pacific/Port_Moresby`
    - `Pacific/Rarotonga` -> `Pacific/Rarotonga`
    - `Pacific/Saipan` -> `Pacific/Saipan`
    - `Pacific/Samoa` -> `Pacific/Samoa`
    - `Pacific/Tahiti` -> `Pacific/Tahiti`
    - `Pacific/Tarawa` -> `Pacific/Tarawa`
    - `Pacific/Tongatapu` -> `Pacific/Tongatapu`
    - `Pacific/Truk` -> `Pacific/Truk`
    - `Pacific/Wake` -> `Pacific/Wake`
    - `Pacific/Wallis` -> `Pacific/Wallis`
    - `Pacific/Yap` -> `Pacific/Yap`
    - `Poland` -> `Poland`
    - `Portugal` -> `Portugal`
    - `ROC` -> `ROC`
    - `ROK` -> `ROK`
    - `Singapore` -> `Singapore`
    - `Turkey` -> `Turkey`
    - `UCT` -> `UCT`
    - `US/Alaska` -> `US/Alaska`
    - `US/Aleutian` -> `US/Aleutian`
    - `US/Arizona` -> `US/Arizona`
    - `US/Central` -> `US/Central`
    - `US/East-Indiana` -> `US/East-Indiana`
    - `US/Eastern` -> `US/Eastern`
    - `US/Hawaii` -> `US/Hawaii`
    - `US/Indiana-Starke` -> `US/Indiana-Starke`
    - `US/Michigan` -> `US/Michigan`
    - `US/Mountain` -> `US/Mountain`
    - `US/Pacific` -> `US/Pacific`
    - `US/Samoa` -> `US/Samoa`
    - `UTC` -> `UTC`
    - `Universal` -> `Universal`
    - `W-SU` -> `W-SU`
    - `WET` -> `WET`
    - `Zulu` -> `Zulu`
    - `Etc/GMT` -> `Etc/GMT`
    - `Etc/GMT+0` -> `Etc/GMT+0`
    - `Etc/GMT+1` -> `Etc/GMT+1`
    - `Etc/GMT+10` -> `Etc/GMT+10`
    - `Etc/GMT+11` -> `Etc/GMT+11`
    - `Etc/GMT+12` -> `Etc/GMT+12`
    - `Etc/GMT+2` -> `Etc/GMT+2`
    - `Etc/GMT+3` -> `Etc/GMT+3`
    - `Etc/GMT+4` -> `Etc/GMT+4`
    - `Etc/GMT+5` -> `Etc/GMT+5`
    - `Etc/GMT+6` -> `Etc/GMT+6`
    - `Etc/GMT+7` -> `Etc/GMT+7`
    - `Etc/GMT+8` -> `Etc/GMT+8`
    - `Etc/GMT+9` -> `Etc/GMT+9`
    - `Etc/GMT-0` -> `Etc/GMT-0`
    - `Etc/GMT-1` -> `Etc/GMT-1`
    - `Etc/GMT-10` -> `Etc/GMT-10`
    - `Etc/GMT-11` -> `Etc/GMT-11`
    - `Etc/GMT-12` -> `Etc/GMT-12`
    - `Etc/GMT-13` -> `Etc/GMT-13`
    - `Etc/GMT-14` -> `Etc/GMT-14`
    - `Etc/GMT-2` -> `Etc/GMT-2`
    - `Etc/GMT-3` -> `Etc/GMT-3`
    - `Etc/GMT-4` -> `Etc/GMT-4`
    - `Etc/GMT-5` -> `Etc/GMT-5`
    - `Etc/GMT-6` -> `Etc/GMT-6`
    - `Etc/GMT-7` -> `Etc/GMT-7`
    - `Etc/GMT-8` -> `Etc/GMT-8`
    - `Etc/GMT-9` -> `Etc/GMT-9`
    - `Etc/GMT0` -> `Etc/GMT0`
    - `Etc/Greenwich` -> `Etc/Greenwich`
    - `Etc/UCT` -> `Etc/UCT`
    - `Etc/UTC` -> `Etc/UTC`
    - `Etc/Universal` -> `Etc/Universal`
    - `Etc/Zulu` -> `Etc/Zulu`
`tz_offset`: [char] Timezone offset
`unpaid_invoice_ids`: [one2many] Unpaid Invoice
`unpaid_invoices_count`: [integer] Unpaid Invoices Count
`unreconciled_aml_ids`: [one2many] Unreconciled Aml
`upcoming_appointment_ids`: [many2many] Upcoming Appointments
`use_partner_credit_limit`: [boolean] Set a value greater than 0.0 to activate a credit limit check
`user_id`: [many2one] The internal user in charge of this contact.
`user_ids`: [one2many] Users
`vat`: [char] The Tax Identification Number. Values here will be validated based on the country format. You can use '/' to indicate that the partner is not subject to tax.
`vat_label`: [char] Tax ID Label
`vies_valid`: [boolean] European VAT numbers are automatically checked on the VIES database.
`website`: [char] Website Link
`website_message_ids`: [one2many] Website communication history
`write_date`: [datetime] Last Updated on
`write_uid`: [many2one] Last Updated by
`zip`: [char] Zip