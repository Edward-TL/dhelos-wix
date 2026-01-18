"""
"""

from dataclasses import dataclass
from typing import Literal, Optional
from pprint import pprint

from flask import Response as FlaskResponse

from odoo_apps.client import OdooClient
from odoo_apps.models import CALENDAR
from odoo_apps.response import Response
from .objects import Event

def create_busy_response(object_id) -> Response:
    return Response(
        action = 'create',
        model = CALENDAR.EVENT,
        object = object_id,
        status = 'PASS',
        status_code = 409,
        msg = "User is busy. Request is OK. Try other time"
    )

def create_bad_request_response(
        msg: str, action: Literal['update', 'cancel', 'create'] = 'update'
        ) -> Response:
    return Response(
        action = action,
        model = CALENDAR.EVENT,
        object = None,
        status = 'BAD REQUEST',
        status_code = 400,
        msg = msg
    )

def create_error_response(
    msg: str, action: Literal['update', 'cancel', 'create'] = 'update'
    ) -> Response:
    return Response(
        action = action,
        model = CALENDAR.EVENT,
        object = None,
        status = 'NOT ACCEPTABLE',
        status_code = 406,
        msg = msg
    )


@dataclass
class Scheduler:
    """
    Schedule activities
    """
    client: OdooClient

 # Para manejar zonas horarias
    def search_events_in_range(
            self, start: str, stop: str,
            fields = ('id', 'start', 'stop','name')) -> list[dict]:
        """
        Returns a list of dictionaries, each one contains as keys the fields
        requested if there is any registered event on Calendar.
        """
        return self.client.search_read(
            model = CALENDAR.EVENT,
            domain = [
                ['start', '>=', start],
                ['stop', '<=', stop]
            ],
            fields = fields
        )

    def create_calendar_event(self, event: Event, printer=False) -> FlaskResponse:
        """
        Crea un nuevo evento en el calendario de Odoo utilizando RPC.
        Args:
            event (Event): Objeto Event que contiene la información del evento a crear.
        Returns:
            int or False: El ID del evento creado en Odoo si la creación fue exitosa,
                        False si ocurrió un error.
        """
        if printer:
            print('calendar event creation')
            pprint(event.data)
        event_domains = [
            ['start', '>=', event.data['start']],
            ['stop', '<=', event.data['stop']]
        ]

        # Esto igual y se puede revisar con alguna comparacion de los documentos y logica
        # a la o hardcodeada, despues de la consulta.
        for field in ['partner_ids', 'resource_ids']:
            if field in event.data:
                event_domains.append([field, 'in', event.data[field]])

        try:
            # Probablemente sea requerido hacer una funcion especial para esto,
            # ya que luego podria entrar el tema del lugar o los partners. Pero como
            # esto se esta considerando para una sola persona, no es necesario por ahora.
            #  
            event_response = self.client.create(
                model = CALENDAR.EVENT,
                vals = event.data,
                domains = event_domains,
                printer=printer
            )
            print(event_response)
            event.odoo_id = event_response.object

            if printer:
                print(f"Evento de calendario '{event.name}' creado con ID: {event.odoo_id}")
            return event_response

        except Exception as e:
            exception_msg = f"Error al crear el event de calendario '{event.name}': {e}"
            print(exception_msg)
            return create_error_response(
                msg = exception_msg
            )
    
    def move_calendar_event(
            self,
            event_id: int|list[int],
            new_start: str,
            new_stop: str,
            update_name: Optional[str] = None,
        printer = False) -> FlaskResponse:
        """
        Moves an event on time. All validations must be done before.
        Args:
            - event_id: Odoo's event id at `calendar.event`
            - start: Datetime str with timezone.
            - stop: Datetime str with timezone.
        """
        reschedule_vals = {
            'start': new_start,
            'stop': new_stop
        }
        if update_name:
            reschedule_vals['name'] = update_name
        try:
            update_response = self.client.update(
                model = CALENDAR.EVENT,
                records_ids= event_id,
                new_vals = reschedule_vals,
                printer=printer
            )

            if printer:
                print(f"Evento de calendario '{update_name}' ACTUALIZADO con ID: {event_id}")
            return update_response

        except Exception as e:
            exception_msg = f"Error al actualizar el event de calendario ID `{event_id}`: {e}"
            print(exception_msg)
            return create_error_response(
                msg = exception_msg
            )
        
    def cancel(self, event_id: int | list[int], printer = False) -> FlaskResponse:
        """
        If exists, delets an given Event by it's ID.
        Args:
            - event_id: int | list[int]. If int, turns it into a list[int]. Must be an
                existing event's ID

        Returns:
            Standarize Response with the given Request and Result 
        """
        if printer:
            print('Checking if event exists')

        if isinstance(event_id, int):
            event_id = [event_id]

        event_exists = self.client.search(
            model = CALENDAR.EVENT,
            domain = [
                ['id', '=', event_id]
            ]
        )
        
        if event_exists in ([], [None]): # Event DOES NOT exist
            return create_bad_request_response(
                msg = 'Missing `calendar_event_id` HAS NEVER BEEN SCHEDULED.',
                action = 'cancel'
            )

        try:
            delete_response = self.client.delete(
                model = CALENDAR.EVENT,
                ids = event_id
            )

            if printer:
                print(f"Evento de calendario con ID: {event_id} ELIMINADO")
            return delete_response

        except Exception as e:
            exception_msg = f"Error al eliminar el event de calendario '{event_id}': {e}"
            print(exception_msg)
            return create_error_response(
                msg = exception_msg,
                action = 'cancel'
            )
