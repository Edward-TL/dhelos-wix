"""
"""
# from copy import copy
from dataclasses import dataclass, field
from typing import Optional, Literal
from copy import copy
from pprint import pprint
from xmlrpc.client import Fault

import pandas as pd
from numpy import nan as np_nan

from odoo_apps.client import OdooClient, RPCHandlerMetaclass
from odoo_apps.models import PRODUCT, POS, STOCK
from odoo_apps.response import Response

from odoo_apps.type_hints.stock import DisplayTypes, CreateVariants
from odoo_apps.utils.cleaning import (
    transform_dict_array_to_dict,
    merge_dictionaries,
    gen_matrix,
    split_id_pair
    )

from odoo_apps.product.objects import ProductTemplate, AttributeLine
from odoo_apps.utils.cleaning import extract_cell_value

product_model = {
    'CATEGORY': PRODUCT.CATEGORY,
    'ATTRIBUTE_VALUE': PRODUCT.ATTRIBUTE_VALUE,
    'ATTRIBUTE': PRODUCT.ATTRIBUTE
}

def reference_clasifier(ref: list):
    """
    """
    if len(ref) == 1:
        return int(ref[0])
    
    if len(ref) == 0:
        return np_nan
    
    return ref

main_tmpl_att_val_fields = [
'id', 'display_name', "product_template_variant_value_ids"
]

@dataclass
class ProductManager(metaclass=RPCHandlerMetaclass):
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
    # Categories related
    stocl_cat_col: str = None
    pos_cat_col: str = None
    stock_pos_cat: Literal['same', 'different'] = 'same'
    categories: Optional[list | dict[str | int]] = None
    pos_categories: Optional[list | dict] = None
    public_categories: Optional[list | dict] = None
    
    # Attributes_related
    attributes: Optional[dict | list] = None
    att_values: Optional[dict[str , list] | list | dict[str , dict]] = None
    
    # Templates related
    templates: Optional[dict[str, dict]] = None
    raw_templates_data: Optional[list[dict]] = None
    template_attributes_value_matrix: Optional[dict[str, list] | pd.DataFrame] = None
    
    # Products related
    products: Optional[dict[str, dict]] = None
    raw_products_data: Optional[list[dict]] = None
    products_matrix: Optional[dict[str, list] | pd.DataFrame] = None

    def __post_init__(self):
        if self.preload:
            # If there is no specific category, it means that we need everything,
            # and if the user hadn't set a category before on some products, this will
            # make that categ_id is False, and using the categ_id reference will cause
            # an error, because the products with categ_id = False, won't be given by
            # Odoo's RPC API

            # ==============[ categories ]==============================
            product_domain = ['id', '>', 0]
            if isinstance(self.categories, (dict, list)):
                if isinstance(self.categories, dict):
                    cat_domain = ['id', 'in', list(self.categories.values())]
                else:
                    if isinstance(self.categories[0], str):
                        cat_domain = ['name', 'in', self.categories]
                    elif isinstance(self.categories[0], int):
                        cat_domain = ['id', 'in', self.categories]
                    else:
                        msg = "Categories list must contain `str` or `int` values"
                        raise ValueError(msg)
                    
                print(f'Getting categories ID for {cat_domain=}')
                self.categories = transform_dict_array_to_dict(
                    dict_array = self.client.search_read(
                        PRODUCT.CATEGORY,
                        domain = [cat_domain],
                        fields = ['id', 'name']
                        )
                )
                pprint(self.categories)
                product_domain = ['categ_id', 'in', list(self.categories.keys())]

            if self.categories is None:
                print('Getting ALL categories ID')
                self.get_all_categories()
            
            print("Total attributes: ",len(self.categories))

            # ==============[ categories ]==============================
            if self.pos_categories is None:
                print('Getting ALL POS categories ID')
                try:
                    self.get_all_pos_categories()
                except Exception as e:
                    if e is Fault:
                        print(type(e), e)
                    pass

            if self.public_categories is None:
                print('Getting ALL PUBLIC categories ID')
                try:
                    self.get_all_public_categories()
                except Exception as e:
                    print(type(e), e)
                    pass
            
            # ==============[ Attributes ]==============================
            if self.attributes is None:
                print('Getting attibutes ID')
                self.get_all_attributes()
                
            if isinstance(self.attributes, list):
                print('Requesting attibutes ID')
                self.attributes = transform_dict_array_to_dict(
                    self.client.search_read(
                            PRODUCT.ATTRIBUTE,
                            domain = [
                                ['name', 'in', self.attributes]
                            ],
                            fields = ['id', 'name']
                        )
                )
            print("Total attributes: ",len(self.attributes))
                
            # ==============[ Values ]==============================
            print('Getting values ID')
            self.get_all_attribute_values()
            print(len(self.id_att_val))

            # ==============[ Product Templates ]==============================
            product_template_domain = ['categ_id', 'in', list(self.categories.keys())]
            if self.templates is None:
                print('Requesting ALL products templates from categories')

            if isinstance(self.templates, list):
                print('Requesting products templates by them given names')
                product_template_domain = ['name', 'in', self.templates]

            self.raw_templates_data = self.client.search_read(
                PRODUCT.TEMPLATE,
                domain = [product_template_domain],
                fields = [
                    'id',
                    'name',
                    'categ_id',
                    'default_code',
                    'attribute_line_ids',
                    'valid_product_template_attribute_line_ids',
                    'product_variant_ids'
                    ]
            )

            self.templates_ids = [
                prod_tmp['id'] for prod_tmp in self.raw_templates_data
            ]

            self.templates_names = [
                prod_tmp['name'] for prod_tmp in self.raw_templates_data
            ]
            print('Creating `product_templates` by merging products_templates_raw with categories')
            self.templates = merge_dictionaries(
                parent = self.categories,
                child = self.raw_templates_data,
                parent_ref = 'categ_id',
            )

            # ==============[ Products ]==============================
            
            if self.products is None:
                print('Requesting ALL products in categories')
            
            if isinstance(self.products, list):
                product_domain = ['name', 'in', self.products]

            product_domain = [product_domain, ['active', '=', True]]
            print(f"{product_domain=}")
            self.raw_products_data = self.client.search_read(
                PRODUCT.PRODUCT,
                domain = product_domain,
                fields = [
                    'id',
                    'categ_id',
                    'display_name',
                    'default_code',
                    'product_tmpl_id',
                    'product_variant_id',
                    'product_template_variant_value_ids',
                    # in case the variant doesn't work because is a unique product
                    # this one can be used.
                    'product_template_attribute_value_ids'
                ]
            )

            self.raw_template_attributes_value_data = self.client.search_read(
                PRODUCT.TEMPLATE_ATTRIBUTE_VALUE,
                domain = [
                    ['product_tmpl_id', 'in', [
                raw_p['product_tmpl_id'][0] for raw_p in self.raw_products_data
            ]]
                ],
                fields = [
                    'id',
                    'attribute_id',
                    'product_attribute_value_id',
                    'product_tmpl_id',
                    'display_name'
                ]
            )

            if len(self.raw_template_attributes_value_data) > 0:
                tav_matrix = gen_matrix(self.raw_template_attributes_value_data)
                tav_matrix = split_id_pair(tav_matrix)
                
                # pprint(self.id_att_val)
                # pprint(self.att_values)
                mixed_ids = {}
                for n, att_val_id in enumerate(tav_matrix['product_attribute_value_id']):
                    try:
                        tav_matrix["product_attribute_value_name"][n] = self.id_att_val[att_val_id]
                    except KeyError:
                        if att_val_id not in mixed_ids:
                            mixed_ids[att_val_id] = self.client.search_read(
                                PRODUCT.ATTRIBUTE_VALUE,
                                [
                                    ['id', '=', att_val_id]
                                ],
                                ['id', 'display_name']
                            )[0]['display_name']

                        tav_matrix["product_attribute_value_name"][n] = mixed_ids[att_val_id]

                if len(mixed_ids):
                    warning_msg = f"WARNING!> attribute_value_ids: {mixed_ids} got lost in gen_matrix.\n"
                    warning_msg += "WARNING!> It's cuase because there is a duplicate attribute_value in "
                    warning_msg += "the same attribute. \n"
                    warning_msg += "WARNING!> Update all products with this id to it's"
                    warning_msg += " new value."
                    print(warning_msg)
                self.template_attributes_value_matrix = tav_matrix

                products_matrix = gen_matrix(self.raw_products_data)

                
                self.products_matrix = split_id_pair(products_matrix)
                del self.products_matrix['product_variant_name']

                self.products_matrix['product_template_variant_value_ids'] = [
                    reference_clasifier(ptvv_ref) for ptvv_ref in self.products_matrix['product_template_variant_value_ids']
                ]

                self.data_available = {
                    'category': self.categories,
                    'attribute': self.attributes,
                    'product_template': set(self.templates_names)
                }

    def get_all_categories(self) -> None:
        """
        Gets all categories stored on Odoo database, and stores it at `self.categories`
        """
        self.categories = transform_dict_array_to_dict(
                dict_array = self.get_all_values(PRODUCT.CATEGORY)
            )

    def get_all_pos_categories(self) -> None:
        """
        Gets all POS categories stored on Odoo database, and stores it at `self.pos_categories`
        """
        self.pos_categories = transform_dict_array_to_dict(
                dict_array = self.get_all_values(
                    POS.CATEGORY, fields = ['id', 'display_name']
                    ),
                    key_ref = 'display_name'
            )
        
    def get_all_public_categories(self) -> None:
        """
        Gets all POS categories stored on Odoo database, and stores it at `self.pos_categories`
        """
        self.public_categories = transform_dict_array_to_dict(
                dict_array = self.get_all_values(
                    PRODUCT.PUBLIC_CATEGORY, fields = ['id', 'display_name']
                    ),
                    key_ref = 'display_name'
            )

    def get_all_attributes(self) -> None:
        """
        Gets all attributes stored on Odoo database, and stores it at `self.attributes`
        """
        self.attributes = transform_dict_array_to_dict(
            self.get_all_values(PRODUCT.ATTRIBUTE)
        )
    def get_all_attribute_values(self) -> None:
        """
        Gets all attribute values stored on Odoo database, and stores it at:
            - self.att_values as {attribute: {value: id}}
            - self.id_att_val as {id: value}
        """
        vals = self.client.search_read(
            PRODUCT.ATTRIBUTE_VALUE,
            domain = [
                ['attribute_id', 'in', list(self.attributes.keys())]
            ],
            fields = ['id', 'name', 'attribute_id']
        )
        print('Merging values with its attributes')

        self.att_values = merge_dictionaries(
            parent = self.attributes,
            child = vals
        )

        self.id_att_val = {}
        for cat, attributes_id in self.att_values.items():
            for att, _id in attributes_id.items():
                self.id_att_val[_id] = att

    def get_ids_from(
            self,
            module: str,
            domain: Optional[list[list[str, str, str]]] = None
            ) -> list:
        """
        Searchs for the objects id, in the given `module` that match the `domain` passed.
        
        Remember that using a list on respected value (domain or arg), it will be the same
        as creating a batch query. For example:
            domain = [
                ['name', 'in', ['name_1', 'name_2']]
            ]
            
            Will return: [1, 2]
        Args:
            module: a PRODUCT module value, like: PRODUCT.ATTRIBUTE_VALUE, or PRODUCT.TEMPLATE.
                Remember to import from odoo_apps.models the PRODUCT object
            domain: a list of list that contains 3 values, like:
                [['id','=',1]] or [['id','>',10], ['category','=','foo']]
        Returns:
            id: int ] list[int]. The id(s) of the attribute value(s).
        """
        return self.client.search(product_model[module], domain)
    
    def get_all_values(self, model:str, fields = ['id', 'display_name']) -> list[dict]:
        """
        Gets all values stored on Odoo's Database.
        Args:
            model: str. value stored on PRODUCT class

        Returns:
            list[dict]: [{'id':1,'name':'foo'},{'id':2,'name':'bar'}]
        """
        return self.client.search_read(
            model,
            domain = [
                ['id', '>', 0]
            ],
            fields = fields
        )
    
    def create_category(self, category_name: str, parent_id: Optional[int | bool] = None) -> Response:
        """
        Crea una nueva categoría de producto en Odoo.

        Args:
            client: Una instancia de la clase OdooClient.
            category_name (str): El nombre de la nueva categoría.
            parent_id (int, optional): El ID de la categoría padre. Defaults to False [this is root]

        Returns:
            int | False: El ID de la nueva categoría creada en Odoo, o False si hubo un error.
        """
        
        category_data = {'name': category_name}
        cat_domain = [
            ['name', '=', category_name]
        ]
        if parent_id is not None: # can be False
            category_data['parent_id'] = parent_id
            cat_domain.append(['parent_id', '=', parent_id])

        category_response = self.client.create(
            model = PRODUCT.CATEGORY,
            vals = category_data,
            domains = cat_domain
        )

        if category_response.status_code in [200, 201]:
            self.categories[category_name] = category_response.object

        return category_response

    def create_pos_category(
            self, category_name: str,
            parent_id: Optional[int] = None,
            hard = False) -> Response:
        """
        Crea una nueva categoría de producto en Odoo.

        Args:
            client: Una instancia de la clase OdooClient.
            category_name (str): El nombre de la nueva categoría.
            parent_id (int, optional): El ID de la categoría padre. Defaults to False [this is root]

        Returns:
            int | False: El ID de la nueva categoría creada en Odoo, o False si hubo un error.
        """
        category_data = {
            'name': category_name
        }
        cat_domain = [
            ['name', '=', category_name]
        ]

        if parent_id is not None:
            category_data['parent_id'] = parent_id
            cat_domain.append(['parent_id', '=', parent_id])

        category_response = self.client.create(
            model = POS.CATEGORY,
            vals = category_data,
            domains = cat_domain,
            hard = hard
        )

        if category_response.status_code in [200, 201]:
            self.pos_categories[category_name] = category_response.object

        return category_response
    
    def create_attribute(self, name: str,
        display_type: DisplayTypes = "select",
        create_variant: CreateVariants = "always"
        ) -> Response:
        """
        Crea un nuevo atributo de producto en Odoo. Sin valores
        """
        
        att_response = self.client.create(
            model = PRODUCT.ATTRIBUTE,
            vals = {
                    'name': name,
                    'display_type': display_type,
                    'create_variant': create_variant,
                }
        )

        if att_response.status_code in [200, 201]:
            self.attributes[name] = att_response.object
            self.att_values[name] = {}
        return att_response

    def append_attribute_value(
        self, attribute_id: int | str, value_name: str,
        default_extra_price: float | None = None,
        html_color: str | None = None,
        image: str | None = None
        ) -> Response:
        """
        Append values to an existing Attribute
        """
        # If it's a string, it's because it's not known the attribute_id
        att_domain = None
        attribute_name = None
        if isinstance(attribute_id, str):
            if attribute_id not in self.attributes:
                att_domain = [('name', '=', attribute_id)]
                attribute_sr = self.client.search_read(
                    model = PRODUCT.ATTRIBUTE,
                    domain = att_domain,
                    fields = ['id','name']
                )

                attribute_id = attribute_sr['id']
                attribute_name = attribute_sr['name']

        if isinstance(attribute_id, int):
            attribute_name = [
                key for key, val in self.attributes.items() \
                if val == attribute_id
            ][0]

        attribute_data = {
                'name': value_name,
                'attribute_id': attribute_id
            }
        if html_color:
            attribute_data['html_color'] = html_color
        
        if default_extra_price:
            attribute_data['default_extra_price'] = default_extra_price

        if image:
            attribute_data['image'] = image

        att_val_response = self.client.create(
                PRODUCT.ATTRIBUTE_VALUE,
                attribute_data,
                domains = [
                    ['name', '=', value_name],
                    ['attribute_id', '=', attribute_id]
                ]
        )

        if att_val_response.status_code in [200, 201]:
            if attribute_name not in self.att_values:
                self.att_values[attribute_name] = {}

            self.att_values[attribute_name][value_name] = att_val_response.object

        return att_val_response

    def gen_attributes_values_ids(self, attribute_values: dict[str, list]) -> None:
        """
        Based on `self.attributes` and `self.att_values`, generates a based dictionary
        that translates, attributes_values dictionary:
        {
            'attribute_1': ['value_1', 'value_2'],
            'attribute_2': ['value_1', 'value_3'],
            'attribute_3': ['value_21', 'value_4']    
        }
        into an attributes_values_ids, ready to use with AttributeLine object and ProductTemplate
        {
            1: [1,2],
            2: [3,5],
            3: [27, 10]
        }
        """
        return {
            self.attributes[k]: [
                self.att_values[k][v] for v in values
                ] for k, values in attribute_values.items()
        }

    def create_product_template(
            self, product_template: ProductTemplate, printer = False) -> None | Response | list:
        """
        This creates a product at `product.product` and at `product.template`,
        and updates `product_template._id` inplace. It also appends all requirded
        attribute stored on `product_template` at `product.template.attribute.line`

        Note:
            * If you want to check the domains used to search and create the product_template, check it with `product_template.domains`.
            * Remember that, if creation fails, response.object is None

        Args:
            - product_template: ProductTemplate
        
        Return:
            - creation_response: Response
        """

        product_vals = product_template.export_to_dict()
        for check_field in ['company_id', 'warehouse_id']:
            if check_field in product_vals:
                if product_vals[check_field] != 1:
                    del product_vals[check_field]

        creation_response = self.client.create(
            PRODUCT.PRODUCT,
            vals = product_vals,
            domains = product_template.domains,
            printer = printer
        )

        if printer:
            print(
                product_template.name,
                'creation code: ', creation_response.status_code
                )
            
        if creation_response.status_code not in [200, 201]:
            print(creation_response.msg)
            return creation_response
        
        product_template._id = self.client.search(
            PRODUCT.TEMPLATE,
            domain = [
                ['name', '=', product_template.name],
                ['categ_id', '=', product_template.categ_id]
            ]
        )[0]

        error_log = []
        n = 0

        correction_vals = {}
        correction_response = None
        correction_check = [
           f"product_template.company_id != 1: {product_template.company_id != 1}",
           f"product_template.warehouse_id != 1: {product_template.warehouse_id != 1}"
        ]
        if product_template.company_id != 1:
            correction_vals['company_id'] = product_template.company_id
        
        if product_template.warehouse_id != 1:
            correction_vals['warehouse_id'] = product_template.warehouse_id
        
        if printer:
            for check in correction_check:
                print(check)
            print(f"{correction_vals=}: {len(correction_vals.keys())}")
        
        if len(correction_vals.keys()) > 0:
            correction_response = self.client.update(
                model = PRODUCT.TEMPLATE,
                records_ids = [creation_response.object],
                new_vals = correction_vals
            )

        if any(
            [
                product_template.attribute_values is None,
                product_template.attribute_values_ids is None
            ]
        ):
            
            return creation_response
        
        for (att_id, vals_ids) , (att_name, vals_names) in zip(
            product_template.attribute_values_ids.items(),
            product_template.attribute_values.items()
            ):
            prod_att_line = AttributeLine(
                attribute_id = att_id,
                values_ids = vals_ids,
                product_tmpl_id = product_template._id,
                # Human data
                attribute_name = att_name,
                values = vals_names
            )

            att_line_response = self.client.create(
                PRODUCT.TEMPLATE_ATTRIBUTE_LINE,
                vals = prod_att_line.export_to_dict(),
                domains = prod_att_line.domains
            )

            prod_att_line._id = att_line_response.object

            product_template.attribute_lines.append(prod_att_line)
            if printer:
                print(
                    "Attribute Line Creation | Status = ",
                    att_line_response.status, ":", att_line_response.status_code,
                    "|",
                    f"Attribute {prod_att_line.attribute_name}: ", prod_att_line.attribute_id, " | ",
                    "Attribute Values ID: ", prod_att_line.values_ids,
                    " Vals: ", prod_att_line.values
                    )
            if att_line_response.status_code not in [200, 201]:
                prod_att_line.error_msg = att_line_response.msg

                error_log.append(f"error at: {att_id=}, att_line_idx: {n}")

            n += 1

        if len(error_log)>0:
            return Response(
                action = 'create',
                model = PRODUCT.PRODUCT,
                msg = error_log,
                object = None,
                status = 'FAIL',
                status_code = 400
            )
        
        if correction_response is not None:

            if correction_response.status_code not in [200,201]:
                creation_response.msg = "Succes on creating, Error while correcting: \n"
                creation_response.msg += correction_response.msg
                creation_response.status_code = 409
                creation_response.status = 'Creation OK, Update FAILED'
                creation_response.action = 'create -> update'
        
        return creation_response
    


    def append_product_template_attribute_line(self, attribute_line: AttributeLine) -> Response:
        """
        """
        att_line_resp = self.client.create(
            PRODUCT.TEMPLATE_ATTRIBUTE_LINE,
            vals = attribute_line.export_to_dict(),
            domains = attribute_line.domains
        )

        attribute_line._id = att_line_resp.object

        return att_line_resp
    
    def get_att_vals_id(
            self, attribute_id: int, fields: Optional[list]=None) -> list:
        """
        Gets all attribute values ids stored in `product.attribute.value`, by the `attribute_id`. If fields are needed, by given the list will change the method from `search` to `search_read`.

        Args:
            - attribute_id [int]: Attribute ID
            - fields Optional[list]: List of fields names required for further analysis.

        Return:
            list: Can contain only integers or dictionaries, according to the scenarios expressed before.
        """
        if fields is None:
            return self.client.search(
                PRODUCT.ATTRIBUTE_VALUE,
                domain = [
                    ['attribute_id', '=', attribute_id]
                ]
            )
        
        return self.client.search_read(
            PRODUCT.ATTRIBUTE_VALUE,
            domain = [
                ['attribute_id', '=', attribute_id]
            ],
            fields = ['id', 'name']
        )

    def update_product(self, template_id: int | list[int], vals:dict, printer=False) -> Response:
        """
        """
 
        return self.client.update(
            PRODUCT.PRODUCT,
            records_ids = template_id,
            new_vals = vals,
            printer = printer
        )
    
    
    def assign_attributes_values_to_products(
            self, products_matrix: pd.DataFrame, attributes_matrix: pd.DataFrame
    ):
        """
        In case you prefered to use pandas, here is a solution I found to get in one table,
        all products with its respective templates and attribute values.
        
        Right now, I'm lazy of thinking with data structures (raw_ values). I know that I'm half way, but I need the visuals for work stuff.
        """
        for att in self.attributes.keys():
            # Creates empty cols for each attributes
            products_matrix[att] = None

        # What can I say? I'm an old fashion man LOL
        r = 0
        # product_template_attribute_value_ids stores all values needed but you need the
        # data from attributes to do the match with its template.
        for att_values in products_matrix['product_template_attribute_value_ids'].to_list():
            for val_id in att_values:
                att_col = extract_cell_value(attributes_matrix, 'id', val_id, 'attribute_name')
                att_val_id = int(extract_cell_value(attributes_matrix, 'id', val_id, 'product_attribute_value_id'))
                
                # This is the main reason that this method is used here, because of
                # this dictionary
                products_matrix.at[r, att_col] = self.id_att_val[att_val_id]
            
            r += 1

    def look_for_missing_data(
        self, db_label: Literal['attribute', 'category', 'product_template', 'attribute_value'],
        values: list[str] | set[str] | pd.Series,
        attribute_name: Optional[str] = None) -> list[str]:
        """
        Looks into `self.data_available`, according to the given `db_label` if
        any of received `values` is not registered.
        Args:
            - db_label:
            - values:
        Returns:
            - list of missing values

        Remember:
            self.data_available = {
                'category': self.categories,
                'attribute': self.id_att_val.values(),
                'product_template': set(self.templates_names)
            }
        """
        if db_label == 'attribute_value':
            if attribute_name is None:
                msg = "Missing `attribute_name`. It's important to consider value contet"
                raise ValueError(msg)
            
            data_to_check = self.att_values[attribute_name]
        else:
            data_to_check = self.data_available[db_label]

        if isinstance(values, (list, pd.Series)):
            values = set(values)

        return [
            val for val in values if all(
                [
                    val not in data_to_check,
                    val != np_nan,
                    str(val) != 'nan',
                    val is not None
                ]
            )
        ]
    
    def melt_product_df(
            self, df: pd.DataFrame, product: str,
            product_col:str = 'product_tmpl_name',
            melt_attribute_name = "TALLA",
            col_name_of_new_values = "DISPONIBILIDAD"
        ) -> pd.DataFrame:
        """
        Melts a product DataFrame to transform product-related columns into a more normalized format.

        This function is typically used to reshape a DataFrame from a wide format (where product attributes
        might be spread across multiple columns) to a long format, making it easier to analyze or
        process product availability or other attribute-specific data.

        Args:
            df (pd.DataFrame): The input DataFrame containing product data.
            product (str): The specific product identifier to filter or process within the DataFrame.
            product_col (str, optional): The name of the column in `df` that contains product template names.
                                         Defaults to 'product_tmpl_name'.
            melt_attribute_name (str, optional): The name of the attribute column that will be created
                                                 after melting. Defaults to "TALLA" (Size).
            col_name_of_new_values (str, optional): The name of the column that will hold the values
                                                    corresponding to the `melt_attribute_name`.
                                                    Defaults to "DISPONIBILIDAD" (Availability).

        Returns:
            pd.DataFrame: A new DataFrame that has been melted according to the specified parameters.
                          The structure will typically include `product_col`, `melt_attribute_name`,
                          and `col_name_of_new_values`.


        Args:
            - df: pd.DataFrame
            - product: str
            - product_col:str = 'product_tmpl_name'
            - melt_attribute_name = "TALLA"
            - col_value_in_new_melt_att_col = "DISPONIBILIDAD"

            Returns:
            - pd.DataFrame
            product_df = df.loc[
                df[product_col] == product
            ]
            pd.melt(
                product_df,
                id_vars = product_info_cols,
                value_vars = tallas_registradas,
                var_name = melt_attribute_name,
                value_name = col_value_in_new_melt_att_col
            )
        """

        product_df = df.loc[
            df[product_col] == product
        ]
        product_df = product_df.loc[:, product_df.notna().any()]
        
        tallas_registradas = [
            col for col in product_df.columns \
                if col in self.att_values[melt_attribute_name].keys()
                ]
        
        product_info_cols = [
            col for col in product_df.columns \
                if col not in tallas_registradas
                ]
        
        return pd.melt(
            product_df,
            id_vars = product_info_cols,
            value_vars = tallas_registradas,
            var_name = melt_attribute_name,
            value_name = col_name_of_new_values
        )

    def unpivot_by_attribute(
            self, stock: pd.DataFrame,
            product_col_ref: str = "product_tmpl_name",
            ref_attribute: str = "TALLA",
            values_name: str = "DISPONIBILIDAD"
    ) -> pd.DataFrame:
        """
            df: pd.DataFrame
            product_col:str = 'product_tmpl_name',
            melt_attribute_name = "TALLA",
            col_value_in_new_melt_att_col = "DISPONIBILIDAD"
        """
        products_received = [
            self.melt_product_df(
                df = stock,
                product = product,
                product_col = product_col_ref,
                melt_attribute_name = ref_attribute,
                col_name_of_new_values = values_name
                ) for product in stock[
                product_col_ref].unique()
            ]

        return pd.concat(products_received, ignore_index=True)
    
    def find_product(self,
        template: Optional[str | int] = None,
        attribute: Optional[str | int] = None,
        value: str | int = None,
        by_id: Optional[int] = None,
        just_id = True, fields: Optional[list] = main_tmpl_att_val_fields,
        all_fields: bool = False
    ) -> list[int] | list[dict]:
        """
        Finds a product variant in Odoo based on template, attribute, and value.
        In case there's zero results, returns all variants of the product template.

        Args:
            template (str | int): The product template ID or name.
            attribute (str | int): The attribute ID or name to filter by.
            value (str | int): The attribute value ID or name to filter by.
            just_id (bool, optional): If True, returns only the product IDs.
                - If False, returns the product with this fields:
                `['id', 'display_name', "product_template_variant_value_ids"]`.
                - Defaults to True.
            fields (Optional[list], optional): List of fields to return for each product.
                - If provided, overrides just_id.
        Returns:
            list[dict]: If a matching product is found, returns the product(s) as a list of dicts (either IDs or full records depending on just_id/fields).
                  If no exact match is found, returns a list of product variants enriched with their attribute values.
        Raises:
            None explicitly. Assumes self.client methods handle exceptions.
        """

        if by_id is not None:
            if just_id:
                return self.client.search(
                    PRODUCT.PRODUCT,
                    [
                        ['id', '=', by_id]
                    ]
                )
        
            if all_fields:            
                return self.client.search_read(
                    PRODUCT.PRODUCT,
                    [
                        ['id', '=', by_id]
                    ]
                )
            
            return self.client.search_read(
                    PRODUCT.PRODUCT,
                    [
                        ['id', '=', by_id]
                    ],
                    fields = fields
                )
        
        tmpl_att_val = self.client.search(
            PRODUCT.TEMPLATE_ATTRIBUTE_VALUE,
            domain = [
                ['product_tmpl_id', '=', template],
                ['attribute_id', '=', attribute],
                ['product_attribute_value_id', '=', value]
            ]
        )

        ptvv_key = "product_template_variant_value_ids"

        if all_fields:
            # This will make client.search_read to bring all fields
            fields = None
            just_id = False
            
        product_search = self.client.search_read(
            PRODUCT.PRODUCT,
            domain = [
                ['product_tmpl_id', '=', template],
                ['product_template_variant_value_ids', '=', tmpl_att_val]
            ],
            fields = fields
        )

        if len(product_search) >= 1:
            found = False
            if len(product_search) == 1:
                found = True
            # There could be a lot of options, with the one attribute value
            # but we need the one that has the same template_attribute_values
            n = 0
            while found is False:
                option = product_search[n]
                # Id's can be unsorted, so lets force them to be in the
                # same order, so they will be the same
                option[ptvv_key].sort()
                tmpl_att_val.sort()
                if option[ptvv_key] == tmpl_att_val:
                    product_search = option
                    found = True

                n += 1

            if just_id:
                return [product_search['id']]

            return [product_search]

        # In case there is no product, instead of returning an empty list,
        # giving the idea that there is no product with that value, returns a list
        # of all the products with it's variants. Because, maybe, the product wasn't
        # created without consider that attribute. So, instead of searching again,
        # returns all the variants so the user search it manually

        product_variants = self.client.search_read(
            PRODUCT.PRODUCT,
            domain = [
                ['product_tmpl_id', '=', template]
            ],
            fields =['id', 'display_name', ptvv_key]
        )

        # the template attribute variant values are not considered in the matrix
        # because other ways can be done to match with it's variant
        raw_variant_values = self.client.search_read(
            PRODUCT.TEMPLATE_ATTRIBUTE_VALUE,
            [
                [
                    'id', 'in', list(
                    {
                        _id for variant_data in product_variants \
                            for _id in variant_data[ptvv_key]
                    }
                )
                ]
            ],
            ['id', 'display_name']
        )

        variant_value = transform_dict_array_to_dict(
            raw_variant_values,
            key_ref = 'id',
            key_val = 'display_name'
            )

        enriched_product_variants = copy(product_variants)
        for n, product in enumerate(product_variants):
            enriched_product_variants[n][ptvv_key] = [
                {
                    "id": variant_id,
                    "display_name": variant_value[variant_id]
                } for variant_id in product[ptvv_key]
            ]

        return enriched_product_variants    
    
    def archive_product(self, id: int | list, by: Literal['variant', 'template'] = 'variant') -> Response:
        """
        Archives, don't deletes, the product by variant or template
        """
        model = None
        if by == 'variant':
            model = PRODUCT.PRODUCT
        elif by == 'template':
            model = PRODUCT.TEMPLATE
        else:
            raise ValueError(f'Choose a `by` option. Received: {by=}')
        
        if isinstance(id, int):
            id = [id]
        print(model, [id])

        return self.client.models.execute_kw(
            self.client.db, self.client.uid, self.client.password,
            # Yes, must be a nested list
            model, 'action_archive', [id]
        )