# Odoo Apps - Python RPC Client Library

A comprehensive Python library that provides an elegant, object-oriented interface to interact with Odoo's XML-RPC API. This library translates Odoo's RPC methods into intuitive Python classes, making it easier to manage products, inventory, appointments, contacts, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)

## 🚀 Features

- **Intuitive OOP Interface**: Work with Odoo models using clean, Pythonic classes
- **Comprehensive Model Coverage**: Support for Products, Stock, Appointments, Calendar, Contacts, POS, Sales, Accounting, and more
- **Automatic Error Handling**: Built-in XML-RPC fault handling with the `RPCHandlerMetaclass`
- **Smart CRUD Operations**: Create, Read, Update, Delete operations with automatic domain checking
- **Product Management**: Advanced product template and variant management with attributes
- **Stock Management**: Complete inventory and warehouse operations
- **Calendar & Appointments**: Schedule and manage events and appointments
- **Type Safety**: Comprehensive type hints for better IDE support
- **Response Objects**: Structured response objects with status codes and error messages

## 📦 Installation

### Using pip (from source)

```bash
git clone https://github.com/Edward-TL/odoo_apps.git
cd odoo_apps
pip install -e .
```

### Using Poetry

```bash
poetry add git+https://github.com/Edward-TL/odoo_apps.git
```

### Requirements

- Python >= 3.13
- requests >= 2.32.3
- pandas >= 2.2.3
- openpyxl >= 3.1.5
- python-dotenv >= 1.1.0
- pydantic >= 2.11.4
- pytest >= 8.3.5
- pytz >= 2025.2
- flask >= 3.1.1

## 🔧 Quick Start

### Basic Connection

```python
from odoo_apps.client import OdooClient

# Method 1: Direct credentials
client = OdooClient(
    url="https://your-odoo-instance.com",
    db="your_database",
    username="your_username",
    password="your_password"
)

# Method 2: Using environment variables
from collections import OrderedDict
import os

user_info = OrderedDict({
    'URL': os.getenv('ODOO_URL'),
    'DB': os.getenv('ODOO_DB'),
    'USERNAME': os.getenv('ODOO_USERNAME'),
    'PASSWORD': os.getenv('ODOO_PASSWORD')
})

client = OdooClient(user_info=user_info)
```

### Basic CRUD Operations

```python
from odoo_apps.models import PRODUCT

# Search for products
product_ids = client.search(
    model=PRODUCT.PRODUCT,
    domain=[('name', 'ilike', 'laptop')]
)

# Read product data
products = client.read(
    model=PRODUCT.PRODUCT,
    ids=product_ids,
    fields=['name', 'list_price', 'qty_available']
)

# Create a new product
response = client.create(
    model=PRODUCT.PRODUCT,
    vals={
        'name': 'New Product',
        'list_price': 99.99,
        'type': 'product'
    }
)

# Update product
client.update(
    model=PRODUCT.PRODUCT,
    records_ids=[product_ids[0]],
    new_vals={'list_price': 89.99}
)

# Delete product
client.delete(
    model=PRODUCT.PRODUCT,
    ids=[product_ids[0]]
)
```

### Search and Read Combined

```python
# Search and read in one operation
products = client.search_read(
    model=PRODUCT.PRODUCT,
    domain=[('categ_id', '=', 1)],
    fields=['name', 'default_code', 'list_price'],
    limit=10,
    order='name asc'
)
```

## 📚 Advanced Usage

### Product Management

```python
from odoo_apps.product.manager import ProductManager
from odoo_apps.product.objects import ProductTemplate, AttributeLine

# Initialize Product Manager
pm = ProductManager(
    client=client,
    preload=True,  # Preload categories, attributes, and values
    categories=['Electronics', 'Accessories']
)

# Create a product with attributes
product_template = ProductTemplate(
    name="Laptop Pro",
    categ_id=pm.categories['Electronics'],
    list_price=1299.99,
    attribute_values={
        'Color': ['Black', 'Silver'],
        'Storage': ['256GB', '512GB']
    },
    attribute_values_ids=pm.gen_attributes_values_ids({
        'Color': ['Black', 'Silver'],
        'Storage': ['256GB', '512GB']
    })
)

response = pm.create_product_template(product_template, printer=True)
```

### Stock Management

```python
from odoo_apps.stock.manager import StockManager
from odoo_apps.models import STOCK

sm = StockManager(client=client)

# Get stock quantities
stock_info = client.search_read(
    model=STOCK.QUANT,
    domain=[('product_id', '=', product_id)],
    fields=['location_id', 'quantity', 'reserved_quantity']
)

# Create stock picking
picking_response = client.create(
    model=STOCK.PICKING,
    vals={
        'picking_type_id': 1,
        'location_id': 8,
        'location_dest_id': 9,
        'move_ids_without_package': [(0, 0, {
            'name': 'Product Move',
            'product_id': product_id,
            'product_uom_qty': 10,
            'product_uom': 1,
            'location_id': 8,
            'location_dest_id': 9,
        })]
    }
)
```

### Calendar & Appointments

```python
from odoo_apps.calendar.scheduler import Scheduler
from odoo_apps.calendar.objects import Event, Alarm

# Create a calendar event
event = Event(
    name="Team Meeting",
    start="2025-12-15 10:00:00",
    stop="2025-12-15 11:00:00",
    partner_ids=[1, 2, 3],
    alarm_ids=[1]  # Notification alarm
)

scheduler = Scheduler(client=client)
event_response = scheduler.create_event(event)
```

### Contact Management

```python
from odoo_apps.contact.book import ContactBook
from odoo_apps.models import CONTACTS

cb = ContactBook(client=client)

# Create a contact
contact_response = client.create(
    model=CONTACTS.PARTNER,
    vals={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'is_company': False
    }
)
```

## 🗂️ Available Models

The library provides access to numerous Odoo models organized by module:

- **PRODUCT**: Products, Categories, Attributes, Templates, Variants
- **STOCK**: Inventory, Warehouses, Pickings, Moves, Quants
- **CALENDAR**: Events, Alarms, Attendees, Recurrences
- **APPOINTMENT**: Appointments, Slots, Resources
- **CONTACTS**: Partners, Companies, Users
- **POS**: Point of Sale Orders, Sessions, Payments
- **SALES**: Sales Orders, Order Lines, Subscriptions
- **ACCOUNT**: Invoices, Payments, Journal Entries
- **MANUFACTORY**: Manufacturing Orders, Bills of Materials, Work Centers

See `odoo_apps/models.py` for the complete list of available models.

## 🛠️ Utilities

### Operators

```python
from odoo_apps.utils.operators import Operator

# Available operators for domain filters
# '=', '!=', '>', '>=', '<', '<=', 'like', 'ilike', 'in', 'not in', etc.
```

### Response Handling

```python
from odoo_apps.response import Response

# All create/update/delete operations return Response objects
response = client.create(model=PRODUCT.PRODUCT, vals={...})

print(response.status_code)  # 200, 201, 400, 406, etc.
print(response.status)       # 'OK', 'CREATED', 'FAIL', etc.
print(response.object)       # Created object ID or None
print(response.msg)          # Success or error message
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run with coverage
pytest --cov=odoo_apps tests/
```

## 📖 Documentation

### Environment Variables

Create a `.env` file in your project root:

```env
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_database
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
```

### Error Handling

The library uses the `RPCHandlerMetaclass` to automatically handle XML-RPC faults:

```python
from odoo_apps.client import handle_xmlrpc_fault

# All manager classes automatically have error handling
# Errors are caught and raised as RuntimeError with descriptive messages
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Edward Toledo Lopez** (EdwardTL)
- Email: edward_tl@hotmail.com
- GitHub: [@Edward-TL](https://github.com/Edward-TL)

## 🙏 Acknowledgments

- Built for Odoo ERP system
- Inspired by the need for a more Pythonic interface to Odoo's XML-RPC API
- Thanks to the Odoo community for comprehensive documentation

## 📚 Additional Resources

- [Odoo External API Documentation](https://www.odoo.com/documentation/18.0/developer/reference/external_api.html)
- [Odoo XML-RPC Guide](https://www.odoo.com/documentation/18.0/developer/reference/external_api.html#xml-rpc)

## 🔄 Version History

- **0.5.0** - Current version with comprehensive model support
- **0.4.0** - Added Product Manager and enhanced CRUD operations
- Earlier versions - Initial development and core functionality

---

**Note**: This library requires an active Odoo instance to connect to. Make sure you have proper credentials and network access to your Odoo server.