"""
Escenarios for data cleaning
"""

from copy import copy
import pandas as pd
from odoo_apps.client import OdooClient
# from odoo_apps.models import PRODUCT


def fill_missing_unique_atts(
        odoo: OdooClient, products_matrix: pd.DataFrame, attributes_matrix:pd.DataFrame
        ) -> pd.DataFrame:
    """
    """
    key_attributes = attributes_matrix.attribute_id.unique().tolist()
    unique_products = products_matrix[
        # Condition
        products_matrix['product_template_variant_value_ids'] == 0
        ]['product_tmpl_id'].to_list()
    

def gen_attributes_values_dict(
        products_data: pd.DataFrame, product: str,
        cols_ref: set | list | tuple,
        product_col: str = 'product_tmpl_name') -> dict:
    """
    """
    product_attribute_values = {
            col : [
                str(val) for val in products_data[col][
                products_data[product_col] == product
            ].unique().tolist() if str(val) != 'nan'
            ] for col in cols_ref
        }
    
    safe_lines = copy(product_attribute_values)
    for k, val in safe_lines.items():
        if val == []:
            del product_attribute_values[k]

    return product_attribute_values

