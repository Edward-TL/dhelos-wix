"""
# odoo_rpc.py
This module provides a class to interact with Odoo's XML-RPC API.
It allows for searching, reading, creating, updating, and deleting records in Odoo models.
It also provides a function to create a CSV file with the models and their descriptions.
It uses the xmlrpc.client library to communicate with the Odoo server.

Author: EdwardTL
"""
import csv
import io
import re
from pathlib import Path
from dataclasses import dataclass
import functools
from typing import OrderedDict, Optional, Union
import xmlrpc.client
from xmlrpc.client import Fault
from pprint import pprint

import pandas as pd

from .utils.cleaning import check_domains
from .utils.operators import Operator
from .response import Response

InterestFields = tuple(['string', 'help', 'type', 'selection'])

PROJECT_PATH = str(
    Path(__file__).resolve().parent.parent
    )

TABLES_DIR = 'tables_files'

output = io.StringIO()
DEFAULT_CSV_FILE = f'{PROJECT_PATH}/{TABLES_DIR}/odoo_tables.csv'
DEFAULT_XLSX_FILE = f'{PROJECT_PATH}/{TABLES_DIR}/xodoo_tables.xlsx'


def handle_xmlrpc_fault(func):
    """
    A decorator that catches xmlrpc.client.Fault, extracts the faultString,
    and raises a new RuntimeError with the fault message.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Fault as e:
            # Extract the faultString from the Fault object
            fault_message = e.faultString
            # Raise a new exception with the extracted message
            raise RuntimeError(f"XML-RPC Fault: {fault_message}") from e
        
        except ConnectionError as e:
            # Optionally, handle other xmlrpc-related errors like connection issues
            raise RuntimeError(f"XML-RPC Connection Error: {e}") from e
    
    return wrapper

class RPCHandlerMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                attrs[attr_name] = handle_xmlrpc_fault(attr_value)
        return super().__new__(mcs, name, bases, attrs)

@dataclass
class OdooClient(metaclass=RPCHandlerMetaclass):
    """
    Odoo client server class to interact with Odoo XML-RPC API.
    """

    user_info: Optional[OrderedDict[str, str]] = None
    url: Optional[str] = None
    db: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self):
        if all([
          self.user_info is None,
          self.url is None,
          self.db is None,
          self.username is None,
          self.password is None
        ]):
            no_data = "No data was given. Please give: \n"
            no_data += "a) host, db, username and password. \n"
            no_data += "b) user_info as a dictionary, with the keys "
            no_data += "in uppercase `URL`, `DB`, `USERNAME`, `PASSWORD` on it's keys. \n"
            no_data += "more info at: https://www.odoo.com/documentation/18.0"
            no_data += "/es_419/developer/reference/external_api.html"
            raise ValueError(no_data)
        if self.user_info is not None:
            self.url = self.user_info['URL']
            self.db = self.user_info['DB']
            self.username = self.user_info['USERNAME']
            self.password = self.user_info['PASSWORD']
        
        self.create_conection_with_server()


    
    def create_conection_with_server(self) -> xmlrpc.client.ServerProxy:
        """
        Creates the uid and models from Odoo ServerProxy Autentication
        """
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def search(self, model: str, domain: list[tuple[str,str,str]]) -> list[int]:
        #request: SearchRequest):
        '''
        Search for records in the specified model that match the given domain.
        :param model: The name of the model to search in.
        :param domain: A list of tuples representing the search criteria.
                       Each tuple should be in the format (field_name, operator, value).
        :return: A list of record IDs that match the search criteria.
        '''
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, "search",
            [domain]
        )
        # return self.models.execute_kw(
        #     self.db, self.uid, self.password,
        #     request.model, request.action,
        #     [request.domains]
        # )


    def execute_kw(self, model: str, kw: str, data: list | str | dict):
        """
        Executes kw on model
        """
        if not isinstance(data, list):
            data = [data]
        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password,
                model, kw,
                data
            )
        except Fault as f:
            fault = f.faultString
            raise ConnectionError(fault)


    def read(self, model: str, ids: list[int], fields: list[str] = ['name']):
             #: ReadRequest):
    # model: str, ids: list[int], fields: list[str]):
        '''
        Read records from the specified model.
        :param model: The name of the model to read from.
        :param ids: A list of record IDs to read.
        :param fields: A list of field names to retrieve.
        :return: A list of dictionaries representing the records.
        '''

        # data = models.execute_kw(
        #           db, uid, password, 'res.partner', 'read',
        #           [ids],
        #           {'fields': ['name', 'email']}
        # )

        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'read',
            [ids], {'fields': fields}
            )
        # Esto es de Gemini
        # data = models.execute_kw(
        #   db, uid, password, 'res.partner', 'read', [ids, ['name', 'email']]
        #)

    def search_read(self,
            model: str,
            domain: list[tuple[str,str,str]] = [('id', '>', 0)],
            fields: Optional[list[str]] = None,
            limit: Optional[int] = None,
            order: Optional[str] = None
        ):#request: SearchReadRequest):
        # domain: list[tuple[str, str, str]] = None, fields: list[str] = None):
        '''
        Search and read records from the specified model.
            - model (str): The name of the Odoo model to query.
            - domain (list[tuple[str, str, str]] | None): The domain filter for the search.
            - fields (list[str]): The list of fields to retrieve from the model.
            - limit (int | None): The maximum number of records to return.
            - order (str | None): The order in which to return the records.
        :return: A list of dictionaries representing the records that match the search criteria.
        '''
        # Ejemplo de Gemini:
        # partners = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        #     [[('customer_rank', '>', 0)]],
        #     {'fields': ['name', 'phone'], 'limit': 10, 'order': 'name asc'}
        # )
        if fields is None:
            fields = self.get_models_fields(model)
            
        query_structure = {'fields': fields}

        if limit is not None:
            query_structure['limit'] = limit
        if order is not None:
            query_structure['order'] = order

        query = query_structure

        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'search_read',
            [domain], query
            )

    def create(
        self,
        model: str,
        vals: Union[list[dict], dict],
        domain_fields: Union[list[str], str] = 'name',
        domain_operators: Operator | list[Operator] = '=',
        domains: Optional[ list[tuple[str, Operator, str]] ] = None,
        hard: bool = False,
        printer = False
        ) -> Response:
        '''
        Create a new record in the specified model.
            - model (str): The name of the Odoo model to create a record in.
            - vals (dict | list[dict]): The values for the new record(s).
            - domain_fields (str | list[str], optional): Field(s) to use for domain checking.
                If the field is a date(time) field, you can also specify a part of the date using
                'field_name.granularity'. The supported granularities are 'year_number',
                'quarter_number', 'month_number', 'iso_week_number', 'day_of_week', 'day_of_month',
                'day_of_year', 'hour_number', 'minute_number', 'second_number'. They all use an integer as value.
                
                Defaults to 'name'.
            - domain_comp (Operator | list[Operator], optional): Comparison operator(s)
                for domain checking. Defaults to '='.
            - search_request (SearchRequest | None, optional): Associated search request
                for pre-creation checks. Defaults to None.
            - domains (list[tuple[field, Operator, value]], optional): Computed domain tuples
                for searching existing records. Defaults to None.
        '''

        response = Response(
            action = 'create',
            model = model
            )
        
        # Confirms the existense of all given fields (trough vals) in Clients Odoo DB
        # A set is used due to speed
        avialable_fields = set(self.get_models_fields(model = model))
        vals_check = vals.copy()
        
        if hard is False:
            for field in vals_check:
                if field not in avialable_fields:
                    del vals[field]
        
        if hard:
            exists = False

        else:
            if domains is None:
                domains = check_domains(
                    domain_fields = domain_fields,
                    domain_operators = domain_operators,
                    vals = vals
                )

            exists = self.search(
                model = model,
                domain = domains
            )
            
            if printer:
                print("DOMAINS: ", domains)
                print("Exist: ", exists)
                pprint(f"{vals=}")
        
        if not exists:
            # print('Creando en', model, vals)
            try:
                # CORE ACTIVITY
                object_id = self.models.execute(
                    self.db, self.uid, self.password,
                    model, 'create', vals
                )
                response.complete_response(
                    obj_id = object_id,
                    status = 201,
                    printer = printer
                )
                return response

            except Exception as e:
                # print(e)
                response.complete_response(
                    obj_id = False,
                    status = 406,
                    msg = str(e),
                    printer = printer
                )
                return response
        
        # IF EXISTS
        if isinstance(exists,list):
            object_id = exists[0]
        else:
            object_id = exists

        response.complete_response(
            obj_id = object_id,
            status = 200,
            printer = printer
        )

        return response

    def update(self,
        model: str,
        records_ids: Union[list[int], int],
        new_vals: dict,
        printer = False):
        '''
        Update existing records in the specified model.
        :param model: The name of the model to update records in.
        :param records_ids:
            if int: The ID of the record to update.
            if list: A list of record IDs to update with the given value.
        :param vals: A dictionary of field names and values to update.
        :return: List like [[id, new_val]].
        '''
        if isinstance(records_ids, int):
            records_ids = [records_ids]

        response = Response(
            action = 'update',
            model = model,
            )
        try:
            object_vals = self.models.execute_kw(
                self.db, self.uid, self.password,
                model, "write",
                [records_ids, new_vals]
            )
            if object_vals:
                response.complete_response(
                        obj_id = records_ids,
                        status = 201,
                        printer = printer
                    )
                return response

        except Exception as e:
            response.complete_response(
                obj_id = False,
                status = 406,
                msg = str(e),
                printer = printer
            )
            return response
    

    def delete(self,
        model: str,
        ids: Union[list[int], int],
        printer = False) -> None:
        '''
        Delete records from the specified model.
        :param model: The name of the model to delete records from.
        :param ids: A list of record IDs to delete.
        :return: True if the deletion was successful, False otherwise.
        '''
        response = Response(
            action = 'delete',
            model = model,
            )
        if isinstance(ids, int):
            ids = [ids]
        try:
            delete_status = self.models.execute_kw(
                self.db, self.uid, self.password,
                model, "unlink", [ids]
            )
            delete_msg = f'Success deleting obj with ID(s): {ids}'
            response.complete_response(
                obj_id = delete_status,
                status = 200,
                msg = delete_msg,
                printer = printer
            )
            return response

        except Exception as e:
            response.complete_response(
                obj_id = False,
                status = 406,
                msg = str(e),
                printer = printer
            )
            return response

    def get_record_names(self, model: str, ids: list[int]):
        '''
        Get the names (textual representation) of records in the specified model.
        :param model: The name of the model to get names from.
        :param ids: A list of record IDs to get names for.
        :return: A list of tuples containing record IDs and their corresponding names.
        '''
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'name_get', [ids]
            )

    def get_models_fields(self, model: str, attributes = False) -> tuple | dict:
        '''
        Get the fields of a specified model.
        :param model: The name of the model to get fields from.
        :return: A dictionary of field names and their corresponding attributes.
        '''
        # fields_info = models.execute_kw(
        #   db, uid, password, 'res.partner', 'fields_get', [], 
        # {'attributes': ['string', 'type']}
        #)
        fields_data = self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'fields_get', []
            )
        if not attributes:
            fields = [field for field in fields_data.keys()]
            return tuple(fields)
            
        return fields_data

    def reference_field_data(
        self, model,
        interest_fields: list | tuple = InterestFields,
        get_values=False,
        help_data = False,
        get_interest_data = False,
        fields_ref = ['string', 'help', 'type'],
        printer = True
    ) -> None | list:
        """
        Print fields from a model
        :param model: Model name
        :param fields: Fields to get
        :return: Dictionary of fields
        """
        attribute_fields = self.get_models_fields(
            model,
            {
                'attributes': fields_ref
                }
                )
        clean_fields = {}
        for field, props in attribute_fields.items():
            # print(props)
            # print(field)
            if field not in clean_fields:
                clean_fields[field] = {}
            for k, v in props.items():
                if k in interest_fields:
                    clean_fields[field][k] = v
        
        if printer:
            pprint(
                clean_fields
            )

        if get_interest_data:
            return clean_fields
        
        if get_values:
            return list(clean_fields.keys())
        
        if help_data:
            return {
                k:v for k,v in clean_fields.items() if 'help' in v
            }


def create_models_file(
    self,
    csv_file = DEFAULT_CSV_FILE,
    xlsx_file = DEFAULT_XLSX_FILE) -> None:
    """
    Create a CSV file with the models and their descriptions.
    :param client: OdooClient instance
    :return: None
    """

    odoo_tables_file = open(csv_file, 'w', encoding='utf-8')
    writer = csv.writer(odoo_tables_file)
    writer.writerow(['app', 'module', 'component', 'model_name', 'description'])

    models_info = self.search_read("ir.model", fields = ['model', 'name', 'info'])

    for model_info in models_info:
        model_name = model_info.get('model', 'N/A')
        # Odoo nombra las tablas de la base de datos a partir del nombre técnico del modelo,
        # reemplazando los puntos por guiones bajos.
        # Ej: res.partner -> res_partner
        model_comp = model_name.split('.')
        app = model_comp[0]
        if len(model_comp) == 1:
            module = ''
            component = ''
        elif len(model_comp) == 2:
            module = model_comp[1]
            component = ''
        else:
            module = model_comp[1]
            component = '.'.join(model_comp[2:])

        # table_name = model_name.replace('.', '_') if model_name != 'N/A' else 'N/A'

        description = model_info.get('name', 'Sin descripción') # 'name' es el nombre visible
        # 'info' a veces contiene una descripción más detallada, podemos usarla si está disponible
        detailed_info = model_info.get('info', '').strip()
        if detailed_info:
            description += f" ({detailed_info})"


        # Limpiar la descripción para evitar problemas con caracteres especiales en CSV
        description = description.replace('"', '""').replace('\n', ' ').replace('\r', '')
        description = re.sub(r'\s+', ' ', description)  # Eliminar espacios adicionales
        description = re.sub(r'=+', ' ', description)  # Eliminar espacios adicionales
        writer.writerow([app, module, component, model_name, description])

    odoo_tables_file.close()

    pd.read_csv(csv_file, encoding='utf-8').to_excel(xlsx_file, index=False)
