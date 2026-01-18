"""
Block Request types
This is made to make it more difficult to use an
action that wasn't mean to be done. So you will need dublicate the 
action that you want to do. For example:
odoo.search(
    SearchRequest
)
"""
from dataclasses import dataclass, field
from typing import Literal, Optional, Union

from .utils.cleaning import check_domains
from .utils.operators import Operator

RequestAction = Literal[
    'search',
    'read',
    'search_read',
    'create',
    'write',
    'unlink'
]

# Just an idea that I'm thinking around
# @dataclass
# class Request:
#     json_data: dict
#     model: str
#     domains: list[str, Operator, str] | list[list[str, Operator, str]]
#     action: RequestAction
#     ids: list[int]
#     fields: list[str] = field(default_factory = ['name'])
#     limit: Optional[int] = None
#     order: Optional[str] = None
#     vals: Union[list[dict], dict]
#     domain_check: Union[list[str], str] = 'name'
#     domain_comp: Operator | list[Operator] = '='
    
#     domains: Optional[ list[tuple[str, Operator, str]] ] = None

#     # search_request: Optional[SearchRequest] = None

#     def __post_init__(self):
#         if isinstance(self.domains[0], str):
#             self.domains = [self.domains]

#         query_structure = {'fields': self.fields}

#         if self.limit is not None:
#             query_structure['limit'] = self.limit
#         if self.order is not None:
#             query_structure['order'] = self.order

#         self.query = query_structure

#         self.domains = check_domains(
#             domain_check = self.domain_check,
#             domain_comp = self.domain_comp,
#             vals = self.vals
#         )

#         self.search_request = SearchRequest(
#             model = self.model,
#             domains = self.domains
#         )

@dataclass
class SearchRequest:
    """
    Represents an Odoo RPC search request.
    Attributes:
        * model (str): The name of the Odoo model to search
        (e.g., 'res.partner').
        * domains (list[str, str, str] | list[list[str, str, str]]):
            The search domain. Can be a single tuple like
            `['field', 'operator', 'value']` or a list of such tuples
            representing a complex domain.
    """
    model: str
    domains: list[str, Operator, str] | list[list[str, Operator, str]]
    action: RequestAction = 'search'

    def __post_init__(self):
        if isinstance(self.domains[0], str):
            self.domains = [self.domains]


@dataclass
class ReadRequest:
    """
    Represents a request to read records from a specific Odoo model.
    Attributes:
        - model (str): The name of the Odoo model to read from.
        - ids (list[int]): A list of record IDs to retrieve.
        - fields (list[str]): The list of fields to retrieve for each record.
            Defaults to ['name'].
    """

    model: str
    ids: list[int]
    action = 'read'
    fields: list[str] = field(default_factory = ['name'])

@dataclass
class SearchReadRequest:
    """
    Represents a search_read request for an Odoo model.
    Attributes:
        - model (str): The name of the Odoo model to query.
        - domain (list[tuple[str, str, str]] | None): The domain filter for the search.
        - fields (list[str]): The list of fields to retrieve from the model.
        - limit (int | None): The maximum number of records to return.
        - order (str | None): The order in which to return the records.
    Methods:
        __post_init__():
            Initializes the query structure based on the provided attributes.
    """

    model: str
    domain: Optional[ list[tuple[str,str,str]] ] = None
    fields: list[str] = field(default_factory = ['name'])
    action = 'search_read'
    limit: Optional[int] = None
    order: Optional[str] = None

    def __post_init__(self):
        query_structure = {'fields': self.fields}

        if self.limit is not None:
            query_structure['limit'] = self.limit
        if self.order is not None:
            query_structure['order'] = self.order

        self.query = query_structure

@dataclass
class CreateRequest:
    """
    CreateRequest encapsulates the data and logic required to create a new record
    in an Odoo model, with optional pre-creation domain checks.
    Attributes:
        - model (str): The name of the Odoo model to create a record in.
        - vals (dict | list[dict]): The values for the new record(s).
        - domain_check (str | list[str], optional): Field(s) to use for domain checking.
            Defaults to 'name'.
        - domain_comp (CompDomain | list[CompDomain], optional): Comparison operator(s)
            for domain checking. Defaults to '='.
        - search_request (SearchRequest | None, optional): Associated search request
            for pre-creation checks. Defaults to None.
        - domains (list[tuple[str, str, str]] | None, optional): Computed domain tuples
            for searching existing records. Defaults to None.
    Methods:
        __post_init__():
            Initializes domains and search_request based on provided attributes.
    """

    model: str
    vals: Union[list[dict], dict]
    domain_check: Union[list[str], str] = 'name'
    domain_comp: Operator | list[Operator] = '='
    search_request: Optional[SearchRequest] = None
    domains: Optional[ list[tuple[str, Operator, str]] ] = None
    action = 'create'

    def __post_init__(self):
        self.domains = check_domains(
            domain_fields = self.domain_check,
            domain_operators = self.domain_comp,
            vals = self.vals
        )

        self.search_request = SearchRequest(
            model = self.model,
            domains = self.domains
        )

@dataclass
class UpdateRequest:
    """
    Represents a request to update records in an Odoo model.
    Attributes:
        - model (str): The name of the Odoo model to update.
        - record_id (int | list[int]): The ID or list of IDs of the records to update.
        - new_val (dict): A dictionary of field names and their new values.
    """

    model: str
    record_id: Union[list[int], int]
    new_val: dict
    action = 'write'

@dataclass
class DeleteRequest:
    """
    Represents a request to delete one or more records from a specified Odoo model.
    Attributes:
        - model (str): The name of the Odoo model from which records will be deleted.
        - ids (int | list[int]): The ID or list of IDs of the records to delete.
    Methods:
        __post_init__():
            Ensures that 'ids' is always a list of integers, even if a single int is provided.
    """

    model: str
    ids: Union[list[int], int]
    action: RequestAction = 'unlink'

    def __post_init__(self):
        if isinstance(self.ids, int):
            self.ids = [self.ids]
