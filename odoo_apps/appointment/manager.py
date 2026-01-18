"""
apps/appointment/appt_manager.py
Appointment Manager file
"""
from copy import copy
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from typing import Optional

from flask import Response as FlaskResponse

from odoo_apps.client import OdooClient, RPCHandlerMetaclass
from odoo_apps.models import APPOINTMENT, CALENDAR
from odoo_apps.response import (
    Response,
    standarize_response,
    report_fail,
    Action,
    Request,
    StatusMeaning
    )
from odoo_apps.utils.cleaning import flat_list

from odoo_apps.calendar.scheduler import Scheduler

from .checkers import (
    create_bad_request_response,
    create_busy_response,
    create_error_response,
    check_dates_range,
    check_hours_range
)
from .objects import Appointment

from .slots import(
    weekdays_requested,
    gen_range_hours,
    clean_slots_info,
    add_weekdays_range_avialability,
    slots_search_info,
    confirm_slots_availability,
    get_slots_available
)

@dataclass
class AppointmentManager(metaclass=RPCHandlerMetaclass):
    """
    Manages interactions with Odoo's appointment.appointment model via RPC.
    """
    client: OdooClient
    request_fields = tuple([
        'start',
        'stop',
        'name',
        'appointment_resource_id',
        'appointment_type_id',
        'timezone_str',
        'partner_id',
        'client_reference_field',
        'client_reference_value'
    ])
    def __post_init__(self):
        self.scheduler = Scheduler(self.client)

    def get_booking_url(self, appointment_type_id: int | str, as_response=False) -> str | Response:
        """
        Returns the webpage url to schedule and appointment by website
        """
        if isinstance(appointment_type_id, str):
            if not appointment_type_id.isdigit():
                return create_bad_request_response(
                    msg = 'If str, `appointment_type_id` must be a digit',
                    action = 'search'
                )
            appointment_type_id = int(appointment_type_id)
            
        booking_url_response = self.client.search_read(
            model = APPOINTMENT.INVITE,
            domain = [['appointment_type_ids','=', appointment_type_id]],
            fields = ['book_url']
        )
        print(booking_url_response)
        booking_url = booking_url_response[0]['book_url']

        if as_response:
            return Response(
                action = "search",
                model = APPOINTMENT.INVITE,
                object = booking_url,
                status_code = 200,
                status = "OK"
            )
        
        return booking_url
    
    def check_weekday_slots(
            self,
            appointment_type_id: int,
            weekdays: list[int]
            ) -> list[dict]:
        """
        Check if there's a worktime slot available for the given weekdays.
        This does not mean that there's a free space on calendar or
        appointments booking line.
        Args:
            - appointment_type_id: int value of the appointment_type required
            - weekday: list[int] value of weekday. Monday is 1, Sunday is 7. 0 Does not exist
        
        Validation:
        domains = [
            ['appointment_type_id', '=', 4],
            ['weekday', 'in', list(weekdays_check.keys())]
        ]
        Returns:
            A list of slots ids that matches with the fields:
            'weekday', 'display_name'.
        """
        return self.client.search_read(
            model = APPOINTMENT.SLOT,
            domain = [
                    ['appointment_type_id', '=', appointment_type_id],
                    ['weekday', 'in', weekdays]
                ],
            fields = ['weekday', 'display_name']
        )
    def busy_response(
            self,
            appointment: Optional[Appointment] = None,
            appointment_type_id: Optional[int] = None,
            requested_data: Optional[Request] = None,
            model = CALENDAR.EVENT,
            action: Action = 'update',
            cause: StatusMeaning = 'CONFLICT') -> FlaskResponse:
        """
        Returns a standard response for busy spaces, includes booking_url
        """
        # Validations
        if appointment is None:
            if appointment_type_id is None:
                if requested_data is None:
                    msng_err = "Missing `appointment`, `appointemnt_type_id` and `requested_data`"
                    msng_err += "Please, provide such info."
                    raise ValueError(msng_err)
                
                raise ValueError("Missing `appointment`, `appointemnt_type_id`. Please provide one")
            
            if requested_data is None:
                raise ValueError("Miising `requested_data` to complete de standarized response.")
        
        # Real Logic
        appointment_type = None
        if appointment is not None:
            appointment_type = appointment.type_id

        if appointment_type_id is not None:
            appointment_type = appointment_type_id

        booking_url = self.get_booking_url(appointment_type)
        object_data = {
            'booking_url': booking_url,
            'weekday_slots': self.check_weekday_slots(
                appointment_type_id= appointment_type,
                weekdays = requested_data['weekdays']
            )
            }

        busy_msg = f'There is not Slot available. You can check availability here {booking_url}.'
        return standarize_response(
            request = requested_data,
            response = Response(
                action = action,
                model = model,
                object = object_data,
                status = cause,
                msg = busy_msg
            )
        )
    def check_slots_conditions(
            self,
            appointment_type_id: int,
            weekdays: list,
            range_hours: list
            ) -> list[dict]:
        """
        Check if there's a worktime slot available for the given time
        range. This does not mean that there's a free space on calendar or
        appointments booking line.
        Args:
            - appointment_type_id: int value of the appointment_type required
            - weekday: int value of weekday. Monday is 1, Sunday is 7. 0 Does not exist
            - start_hour: INT value
            - end_hour: INT value
        
        Validation:
        domains = [
            ['appointment_type_id', '=', 4],
            ['weekday', 'in', list(weekdays_check.keys())],
            "|",
            ['start_hour', 'in', range_hours],
            ['end_hour', 'in', range_hours ]
        ]
        Returns:
            A list of slots ids that matches with the fields:
            'weekday', 'start_hour', 'end_hour', 'duration'.
        """
        print('start_hour', range_hours[:-1])
        print('end_hour', range_hours[1:])
        print(weekdays)
        return self.client.search_read(
            model = APPOINTMENT.SLOT,
            domain = [
                    ['appointment_type_id', '=', appointment_type_id],
                    ['weekday', 'in', weekdays],
                    "|",
                    ['start_hour', 'in', range_hours[:-1]],
                    ['start_hour', "<=", range_hours[0]],
                    ['end_hour', '>', range_hours[0]],
                    '|',
                    ['end_hour', '>=', range_hours[-1]],
                    ['end_hour', 'in', range_hours[1:]]
                ],
            fields = ['weekday', 'start_hour', 'end_hour', 'duration']
        )
    
    def look_for_slots(
        self,
        appointment_type_id: Optional[int] = None,
        dates_range: Optional[list[datetime, datetime] | list[str, str]] = None,
        hours_range: Optional[list[int, int]] = None,
        request_body: Optional[dict] = None
    ) -> list[dict]:
        """
        According to the type of appointment, a range of dates (no greater than a week)
        and a range of hours, looks for an Appointment Slot that matches with the values,
        checks in the calendar if there is any event, and if there is no event/appointment
        overlaping with the posible slots, will a return FlaskResponse, where the object is an
        dictionary with the next structure:
            response = {
                "message": response.msg,
                "success": True | False,
                "status": , 
                'body' = {
                    "object" : {
                        "booking_url" : booking_url,
                        "available_slots" : [slot, slot, ... , slot]
                    }
                }
            }
        if there is no "available_slots" in response['object'], it means that there is no
        available slots, but you can check on the booking_url for every need
        """
        if request_body is not None:
            dates_range = request_body['optional_date_range']
            hours_range = request_body['prefered_hours']
            appointment_type_id = request_body['appointment_type_id']

        if all(
            [appointment_type_id is None, dates_range is None,
             hours_range is None, request_body is None]):

            error_msg = "No data provided to search for slots. Please provide:\n"
            error_msg += "  a) appointment_type_id, optional_date_range and prefered_hours \n"
            error_msg += "  b) Request Body with previous options inside" \

            raise ValueError(error_msg)

        dates_range_error = check_dates_range(dates_range)
        if dates_range_error:
            return dates_range_error

        hours_range_error = check_hours_range(hours_range)
        if hours_range_error:
            return hours_range_error
        
        weekdays_check = weekdays_requested(
            start_date = dates_range[0],
            end_date = dates_range[1]
        )
        or_hours_range = copy(hours_range)
        hours_range = gen_range_hours(hours_range)

        slots_search = self.check_slots_conditions(
            appointment_type_id = appointment_type_id,
            weekdays = list(weekdays_check.keys()),
            range_hours = hours_range
        )
        print(slots_search)

        if len(slots_search) == 0:
            # return None
            if request_body is None:
                request_data = {
                    'appointment_type_id': appointment_type_id,
                    'weekdays': list(weekdays_check.keys()),
                    'dates_range': dates_range,
                    'hours_range': or_hours_range
                }
            else:
                request_data = request_body

            return self.busy_response(
                requested_data = request_data,
                appointment_type_id = appointment_type_id,
                model = APPOINTMENT.SLOT,
                action='search',
                cause = "NOT FOUND"
            )

        weekday_slots = clean_slots_info(slots_search)
        add_weekdays_range_avialability(
            slots_info = weekday_slots,
            range_hours = hours_range
        )
        slots_search_info(
            slots_info = weekday_slots,
            weekdays_dates = weekdays_check
        )
        odoo_events = [
            self.scheduler.search_events_in_range(
                start = slots_info['day_start'],
                stop = slots_info['day_stop']
                ) for slots_info in weekday_slots.values()
        ]

        odoo_events = flat_list(odoo_events)
        for o_event in odoo_events:
            o_event['start'] = o_event['start'][:16]
            o_event['stop'] = o_event['stop'][:16]

        
        confirm_slots_availability(
            slots_info = weekday_slots,
            events = odoo_events
        )
        
        available_slots = get_slots_available(weekday_slots)
        if len(available_slots) == 0:
            return self.busy_response(
                requested_data = {
                    'appointment_type_id': appointment_type_id,
                    'weekdays': list(weekdays_check.keys()),
                    'dates_range': dates_range,
                    'hours_range': or_hours_range
                },
                appointment_type_id = appointment_type_id,
                model = CALENDAR.EVENT,
                action='search',
                cause = "CONFLICT"
            )
        
        booking_url = self.get_booking_url(appointment_type_id=appointment_type_id)
        availability_msg = f"The available slots are: {available_slots}.\n"
        availability_msg += f"Remember that you can check availability on our site: {booking_url}"
        return standarize_response(
                request = {
                    'appointment_type_id': appointment_type_id,
                    'dates_range': dates_range,
                    'hours_range': or_hours_range
                },
                response= Response(
                    action = 'search',
                    model = 'appointment.slots',
                    object = {
                        "booking_url": booking_url,
                        "available_slots": available_slots
                        },
                    status = "OK",
                    msg = availability_msg
                )
            )
    


    def extract_appointment_data(self, request: dict) -> Appointment:
        """
        Generates an Appointment object from a request dictionary.

        Args:
            request (dict): Dictionary containing appointment data.

        Returns:
            Appointment: An Appointment object populated with the provided data.
        """
        # Assuming request contains all necessary fields for Appointment


        if request['appointment_type_id'] is None and request['name_type'] is None:

            return standarize_response(
                request = request,
                response = Response(
                    action = 'create',
                    model = APPOINTMENT.TYPE,
                    status_code = 400,
                    msg = "Neither appointment type nor name type is set."
                )
            )
        if request['appointment_type_id'] is None:
            existing_ids = self.client.search(
                model = APPOINTMENT.TYPE,
                domain = [
                    ('active', '=', True),
                    ('name', '=', request['name_type'])
                ]
            )
            if len(existing_ids) > 1:
                request['appointment_type_id'] = existing_ids
            else:
                request['appointment_type_id'] = existing_ids[0]

        appointment = Appointment(
            start_request = request['start'],
            end_request = request['stop'],
            name = request['name'],
            resource_ids = request['appointment_resource_id'],
            type_id = request['appointment_type_id'],
            timezone_str = request['timezone_str'],
            partner_ids = request['partner_ids']
        )

        if 'calendar_event_id' in request:
            appointment.calendar_event_id = request['calendar_event_id']
            appointment.event.odoo_id = request['calendar_event_id']
            appointment.event.data['calendar_event_id'] = request['calendar_event_id']

        return appointment

    def book_appointment(self, appointment: Appointment, printer=False) -> FlaskResponse:
        """
        Creates a new appointment in Odoo using RPC.

        Args:
            appointment (Appointment): Appointment object containing the data for the new appointment.

        Returns:
            int or list[int] or None: The ID(s) of the created appointment(s) if successful,
                                      or the ID(s) of existing appointment(s) if found (PASS),
                                      or None if an error occurred (FAIL).
        """
        if printer:
            pprint(appointment.extract_booking_data())
        
        if appointment.calendar_event_id is not None:
            # In real world situation, you just copy de appointment
            # object after you make the request. There sholud not be
            # another way to know the calendar_event_id. Also, if you
            # are looking to book over an specific calendar_event, it's
            # know that the slot is not available. You should consider
            # to make an "update" or "reschedule"
            return self.look_for_slots(
                appointment_type_id = appointment.type_id,
                dates_range = appointment.optional_dates_range,
                hours_range = appointment.optional_hours_range
            )
    
        if printer:
            print('appointment.event.data')
            pprint(appointment.event.data)

        calendar_response = self.scheduler.create_calendar_event(
            event = appointment.event,
            printer=printer
        )
        if printer:
            print("CALENDAR RESPONSE")
            calendar_response.print()
            info = f"STATUS {calendar_response.status_code} = ", calendar_response.status
            print(info)

        appointment.calendar_event_id = calendar_response.object

        if printer:
            pprint(appointment.extract_booking_data())

        if calendar_response.status_code == 200:
            # There was an event, so it's busy
            return self.look_for_slots(
                appointment_type_id = appointment.type_id,
                dates_range = appointment.optional_dates_range,
                hours_range = appointment.optional_hours_range,
                request_body = appointment.requested_data()
            )
        
        if calendar_response.status_code != 201:
            # IT's not created, there was an error
            # One of: 406, 409, 400, 404
            return standarize_response(
                request = appointment.requested_data(),
                response = calendar_response
            )
    
        try:
            # Use the client.create method which includes built-in printing
            # We don't need domain_check here because we did the check manually above.
            # Pass printer=True to enable the printing from the client method.
            appt_response = self.client.create(
                model = APPOINTMENT.BOOKING_LINE,
                vals = appointment.requested_data(),
                domains = (
                        ['event_start', '>=', appointment.start_request],
                        ['event_stop', '<=', appointment.end_request],
                ),
                printer=printer
                # domain_check and domain_comp are not needed due to manual check
            )

            if appt_response.status == 'OK':
                return standarize_response(
                    request = appointment.requested_data(),
                    response = create_busy_response(appt_response.object)
                )
            
            return standarize_response(
                request = appointment.requested_data(),
                response = appt_response
            )

        except Exception as e:
            # The client.create method should handle printing the error,
            # but we can add an extra layer here if needed, or just return None.
            # Let's rely on client.create's printer.
            error_msg = f"An unexpected error occurred during appointment creation: {e}"
            print(error_msg)
            return standarize_response(
                request = appointment.requested_data(),
                response = report_fail(
                    action = 'create',
                    model = APPOINTMENT.BOOKING_LINE,
                    http_status = 400,
                    msg = error_msg
                )
            )


    def reschedule(
            self, appointment: Appointment, printer = False) -> FlaskResponse:
        """
        Reschedules an existing calendar event after performing validation and conflict checks.
        
        Request Args:
            - appointment_type_id: Int value that represents the type of appointment
            - client_id: Int value of the clients refference.
            - calendar_event_id: Int value of the event that wants to be
            - name: Optional[String] value with that specify that is an Reschedule
            - start: Datetime STRING value with the format `%Y-%m-%d %H:%M %z` of the
                tentative new datetime start schedule. 
            - stop: Datetime STRING value with the format `%Y-%m-%d %H:%M %z` of the
                tentative new datetime stop schedule.

        Returns:
            - response: FlaskResponse, where the response['response'] object contains the data
                of action succes. Remember that does can be (but not exclusively):

                SUCCESS, FAIL, PASS, BAD REQUEST, NOT ACEPTABLE, CONFLICT

                From odoo_apps.response check `meaning` and `http_meaning` for more context.
        """

        can_modify = self.client.search(
            model = CALENDAR.EVENT,
            domain = [
                ['id', '=', appointment.calendar_event_id],
                ['partner_ids', '=', appointment.partner_ids]
            ]
        )

        # "One" is added because in Odoo Monday is 1,
        # and weekday(), starts with Monday as a 0 (sunday = 6).
        # slot_weekday = datetime.strptime(appointment.start_utc_str, TIME_STR).weekday() + 1
        # slots = self.check_slots_available(
        #     appointment_type_id = appointment.type_id,
        #     weekday = slot_weekday,
        #     start_hour = extract_hour(appointment.start_utc_str),
        #     end_hour = extract_hour(appointment.end_utc_str)
        # )

        # if slots in ([], [None]):
        #     return self.busy_msg(appointment)
        

        # Hay que verificar si el update checa los eventos en el lugar que
        # apunta
        if not can_modify:
            return standarize_response(
                request = appointment.requested_data(),
                response = Response(
                    action = 'update',
                    model = CALENDAR.EVENT,
                    object = appointment.event.odoo_id,
                    status = 'CONFLICT',
                    status_code = 409,
                    msg = 'There is no calendar_event with this partner.'
                )
            )
        try:
            return standarize_response(
                request = appointment.requested_data(),
                response = self.scheduler.move_calendar_event(
                    event_id = appointment.calendar_event_id,
                    new_start = appointment.start_utc_str,
                    new_stop = appointment.end_utc_str,
                    update_name = appointment.name,
                    printer=printer
                )
            )
        
        except Exception as e:
            exception_msg = f"Error al actualizar la cita del calendario '{appointment.name}': {e}"
            print(exception_msg)
            return create_error_response(
                msg = exception_msg,
                action = 'cancel'
            )

    def cancel(self, request_body: dict, printer = False) -> FlaskResponse:
        """
        Cancels (deletes) a calendar event based on its ID.

        This method attempts to delete a calendar event identified by
        `calendar_event_id` via `odoo.client`. It first validates the presence of
        `calendar_event_id` in the event data and checks if the event actually exists
        before attempting deletion.
        Optional debug information can be printed during the process.

        Args:
            calendar_event_id: The Int value of calendar event in odoo db, that is.
                attempt to be deleted. It only requires calendar_event_id because, it's the
                real reference of the appointment. Once is deleted from calendar, the appointment
                it's deleted from appointments.booking_line

        Returns:
            FlaskResponse: An object suitable for an HTTP response in a Flask application.
                - If `calendar_event_id` is missing or the event does not exist,
                it returns a "bad request" response generated by
                `create_bad_request_response`.
                - If the deletion is successful, it returns the response from
                `self.client.delete`.
                - If an error occurs during deletion, it returns an error
                response generated by `create_error_response`.
        """
        if printer:
            print('Checking if `calendar_event_id` was given')
        
        if 'calendar_event_id' not in request_body:
            print(request_body)
            return create_bad_request_response(
                msg = f'Missing `calendar_event_id` on request. Keys given: {request_body.keys()}',
                action = 'cancel'
            )
        
        if 'partner_ids' not in request_body:
            return create_bad_request_response(
                msg = f'Missing `partner_ids` on request. Keys given: {request_body.keys()}',
                action = 'cancel'
            )
        
        can_cancel = self.client.search(
            model = CALENDAR.EVENT,
            domain = [
                ['id', '=', request_body['calendar_event_id']],
                ['partner_ids', '=', request_body['partner_ids']]
            ]
        )
        if not can_cancel:
            return standarize_response(
                request = request_body,
                response = Response(
                    action = 'update',
                    model = CALENDAR.EVENT,
                    object = request_body['calendar_event_id'],
                    status = 'CONFLICT',
                    status_code = 409,
                    msg = 'There is no calendar_event with this partner.'
                )
            )

        try:
            return standarize_response(
                request = request_body,
                response = self.scheduler.cancel(
                    request_body['calendar_event_id']
                    )
            )
        
        except Exception as e:
            ceid = request_body['calendar_event_id']
            exception_msg = f"Error al cancelar la cita del calendario '{ceid}': {e}"
            print(exception_msg)
            return create_error_response(
                msg = exception_msg,
                action = 'cancel'
            )
