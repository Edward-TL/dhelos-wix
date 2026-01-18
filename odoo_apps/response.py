"""
Standard response
"""

from dataclasses import dataclass
from typing import Literal, Union, Optional
from flask import Flask, make_response
from flask import Response as FlaskResponse

from .request import (
    SearchRequest,
    ReadRequest,
    SearchReadRequest,
    CreateRequest,
    UpdateRequest,
    DeleteRequest
    )
from .utils.cleaning import generate_dict

status_code_idea = {
    201: 'Success on creating',
    200: 'Object found/Action completed',
    400: 'Request does not have all values needed',
    404: 'Request is OK. Object was not found',
    406: 'ValueError type on request values',
    409: 'Request is OK. Object has a conflict (overlaps/busy/taken)'
}

meaning_code = {
    'OK': 200,
    'CREATED': 201,
    'BAD REQUEST': 400,
    'NOT FOUND': 404,
    'NOT ACCEPTABLE': 406,
    'CONFLICT': 409
}

code_meaning = {
    200: 'OK',
    201: 'CREATED',
    400: 'BAD REQUEST',
    404: 'NOT FOUND',
    406: 'NOT ACCEPTABLE',
    409: 'CONFLICT'
}

HttpStatus = Literal[
    200, 201,
    406, 409, 400, 404
    ]

StatusMeaning = Literal[
    'OK', 'CREATED',
    'FAIL', 'CONFLICT', 'BAD REQUEST', 'NOT FOUND'
    ]
Action = Literal['read', 'search', 'create', 'update', 'delete']

# Just an Idea, that will evolve
Request = Union[
    dict,
    SearchRequest,
    ReadRequest,
    SearchReadRequest,
    CreateRequest,
    UpdateRequest,
    DeleteRequest
]

@dataclass
class Response:
    """
    Body for response data
    """
    action: Action
    model: str
    msg: Optional[str] = None
    object: Optional[int | list[int] | list[list[int, str]] | bool] = None
    status: Optional[StatusMeaning] = None
    status_code: Optional[HttpStatus] = None

    def __post_init__(self):
        if self.status_code is not None and self.status is None:
            self.status = code_meaning[self.status_code]

        if self.status_code is None and self.status is not None:
            self.status_code = meaning_code[self.status]


        if self.msg is None and self.status_code is not None:
            self.msg = status_code_idea[self.status_code]

        self.data = generate_dict(self)

    def update_message(self, error_message="") -> str:
        message = ""
        message += f"{self.status} | "
        if self.status != 'FAIL':
            message += f"Message: {status_code_idea[self.status_code]} | "
        else:
            message += f"Error: {error_message}"
        message += f"Action: {self.action} | "
        message += f"Model: {self.model} | "
        message += f"[ID]: {self.object}"

        self.msg = message

    def print(self):
        """
        Print the message based on the action and status.
        """
        print(self.msg)

    def complete_response(
        self, obj_id: int | bool, status: HttpStatus, msg = "",
        printer = False
        ):

        self.object = obj_id
        self.status = code_meaning[status]
        self.status_code = status
        if msg != "":
            self.msg = msg
        else:
            self.update_message()

        if printer:
            self.print()

    def get_data(self):
        self.data = generate_dict(self)
        return {
            "action": self.action,
            "model": self.model,
            "object": self.object,
            "status": self.status,
            "status_code": self.status_code,
            "msg": self.msg
        }


def report_fail(
        action: Action,
        model: str,
        http_status: HttpStatus,
        msg: str
    ) -> Response:
    """
    Returns a Response error
    """
    return Response(
        action = action,
        model = model,
        object = None,
        status = meaning_code[http_status],
        status_code = http_status,
        msg = msg
    )

def standarize_response(request: Request, response: Response) -> FlaskResponse:
    """
    Function to simplifys the reponse generation
    """
    app = Flask(__name__)
    response_status = int(response.status_code)

    data = {
        "message": response.msg,
        "success": response_status in {200, 201},
        "status": response_status, 
        "body": response.get_data(),
        "metadata": {
            "requested": request.data if not isinstance(request, dict) else request,
            }
    }

    # print(type(data['request']))
    # print(type(data['response']))
    # print(data)
    with app.app_context():
        response = make_response(
            data, response_status
        )
        return response
