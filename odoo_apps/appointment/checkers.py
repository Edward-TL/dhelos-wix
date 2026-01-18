"""
Helper functions to keep code cleaner
"""
# from pprint import pprint
from copy import copy
from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from typing import Literal, Optional

from flask import Response as FlaskResponse

# from odoo_apps.client import OdooClient
from odoo_apps.models import CALENDAR#, APPOINTMENT
from odoo_apps.response import Response, standarize_response

from odoo_apps.utils.time_management import DATE_STR, TIME_STR


DATE_RANGE_RGX = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s"
DATE_RANGE_RGX += r"([01]\d|2[0-3]):[0-5]\d\s-\s([01]\d|2[0-4]):[0-5]\d$"

@dataclass
class DateLimit:
    """
    Add this value to .now() datetime, so it can validates that
    the date is after a valid start point.
    """
    days: int = 0
    hours: int = 0
    minutes: int = 50

    def __post_init__(self):
        self.msg = f"Consider now + {self.days} days, {self.hours} hours and {self.minutes} minutes"

def create_busy_response(object_id) -> Response:
    return Response(
        action = 'create',
        model = CALENDAR.EVENT,
        object = object_id,
        status = 'BUSY',
        status_code = 409,
        msg = "User is busy. Request is OK. Try other time"
    )

def create_bad_request_response(
        msg: str, action: Literal['search', 'update', 'cancel', 'create'] = 'update'
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

def weekdays_requested(
        start_date: str | datetime, end_date: str | datetime,
        date_format = '%Y-%m-%d') -> dict:
    """
    From a `start_date` and `end_date` returns a dictionary with the
    dates that can be managed as a values, and the normalized weekdays (+1)
    as keys. 
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, date_format)
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, date_format)

    date = copy(start_date)
    weekdays_check = {}
    while date <= end_date:
        # print(date)
        str_date = date.strftime(date_format)
        weekday = date.weekday() + 1
        weekdays_check[weekday] = str_date
        date = date + timedelta(days=1)

    return weekdays_check

def gen_range_hours(
        hours_range: Optional[list] = None,
        start: Optional[int] = None, end: Optional[int] = None) -> list:
    """
    Returns a tuple of values between start and end
    """
    if hours_range is None:
        return list(range(start, end+1))

    return list(range(hours_range[0], hours_range[1]+1))

def check_dates_range(dates_range: list[datetime, datetime] | list[str, str]) -> None | FlaskResponse: 
    """
    Checks if dates given are in correct format and time range
    """
    check_start = None
    check_end = None
    error = True
    if isinstance(dates_range, list):
        if len(dates_range) == 2:
            if isinstance(dates_range[0], str):
                error = False
                check_start = datetime.strptime(dates_range[0], DATE_STR)
                check_end = datetime.strptime(dates_range[1], DATE_STR)

            elif isinstance(dates_range[0], datetime):
                error = False
                check_start = dates_range[0]
                check_end = dates_range[1]

            if not error:
                dates_difference = check_start - check_end
                if dates_difference.days >= 7:
                    error = True
            
    if error:
        error_msg = "`dates_range` MUST BE a list of 2 datetimes, or 2 strs with"
        error_msg += f" format: `{DATE_STR}` and not greater than 7 days (a week). \n"
        error_msg += f"Got: {dates_range}"
        return standarize_response(
            request = {'dates_range': dates_range},
            response=Response(
                action = 'search',
                model='calendar.event',
                object=None,
                status = 'BAD REQUEST',
                status_code = 400,
                msg = error_msg
            )
        )
    
def check_hours_range(hours_range: list[int, int]) -> None | FlaskResponse: 
    """
    Checks if dates given are in correct format and time range
    """
    check_start = None
    check_end = None
    error = True
    if isinstance(hours_range, list):
        if len(hours_range) == 2:
            if isinstance(hours_range[0], int) and isinstance(hours_range[1], int):
                error = False
                check_start = hours_range[0]
                check_end = hours_range[1]
    
                dates_difference = check_start - check_end
                if dates_difference >= 12:
                    error = True
            
    if error:
        error_msg = "`hours_range` MUST BE a list of 2 integers"
        error_msg += " and not greater than 12 hours (half day). \n"
        error_msg += f"Got: {hours_range}"
        return standarize_response(
            request = {'hours_range': hours_range},
            response=Response(
                action = 'search',
                model='calendar.event',
                object = None,
                status = 'BAD REQUEST',
                msg = error_msg
            )
        )
    
def after_today_limit(
        check_date: datetime,
        date_limit: DateLimit) -> datetime:
    """
    Datetime validation
    """
    today_limit = datetime.now() + timedelta(
        days=date_limit.days, hours=date_limit.hours, minutes=date_limit.minutes
        )
    return today_limit <= check_date


def validate_dates(
        dt_range:str, start_dt: str | datetime, end_dt: str | datetime, date_limit=DateLimit()
        ):
    """
    Makes two validations:
    1) Validates that the dates given are a valid string or a datetime. In case of a datetime_range
        It will check that fits the format `%Y-%m-%d %H:%M - %H:%M` using Regex, so it can be managed
        if passes it.
    3) Check that end date is greater than start. If not, returns each one in reverse (end as start,
        and start as end).
    2) If everything is OK. Validates that the given date is valid for a time comparission. Adding the
        indicated days to .today(), and in case the range is smaller, returns an error.
    """
    error_msg = "`self.date_time_range`, `self.start_request` and `self.end_request`"
    error_msg += " Are `None`. Please provide one of the following options: \n"
    error_msg += "a) `self.date_time_range` as `str` with format `%Y-%m-%d %H:%M - %H:%M` "
    error_msg += "(`date` `start_time` - `end_time`).\n"
    error_msg += "b) `self.start_request` and `self.end_request` as `datetime | str` values"
    
    if all(
        # No info was given
        [dt_range is None, start_dt is None, end_dt is None]) or all(
            # Partial info
            [dt_range is None, start_dt is not None, end_dt is None]
        ) or all([dt_range is None, start_dt is None, end_dt is not None]):    
        raise ValueError(error_msg)
    
    if all([dt_range is not None, start_dt is None, end_dt is None]):
        dtr_err_val = "`date_time_range` MUST BE a `str` with format `%Y-%m-%d %H:%M - %H:%M`"
        dtr_err_val += "(`date` `start_time` - `end_time`)."
        if not isinstance(dt_range, str):
            raise ValueError(dtr_err_val)

        if not re.match(DATE_RANGE_RGX, dt_range):
            raise ValueError(dtr_err_val)

        date_time_values = dt_range.split(" ")
        date = date_time_values[0]
        start_time = date_time_values[1]
        end_time = date_time_values[-1]

        start_request = f"{date} {start_time}"
        end_request = f"{date} {end_time}"

        
        start_dt = start_request
        end_dt = end_request

    request_start_dt = datetime.strptime(start_dt, TIME_STR)
    request_end_dt = datetime.strptime(end_dt, TIME_STR)

    if request_end_dt < request_start_dt:
        raise ValueError("End date is closer than start. Please check dates")
    
    if not after_today_limit(request_start_dt, date_limit):
        error_msg = "Start Date is not valid due to is not greater than today plus considerations"
        error_msg += f"{date_limit.msg}"
        error_msg += f"Start Date value: {request_start_dt}"
        raise ValueError(error_msg)
    
    if not after_today_limit(request_end_dt, date_limit):
        # Range was not given, but rest of data.
        error_msg = "End date is not valid due to is not greater than today plus considerations"
        error_msg += f"{date_limit.msg} \n"
        error_msg += f"Start Date value: {request_end_dt}"
        raise ValueError(error_msg)
    
    return start_dt, end_dt

def create_next_week_days(date_ref: datetime | str) -> list[str, str]:
    if isinstance(date_ref, str):
        try:
            date_ref = datetime.strptime(date_ref, DATE_STR)
        except ValueError:
            date_ref = datetime.strptime(date_ref, TIME_STR)

    weekday = date_ref.weekday() + 1
    # Check tomorrow
    if weekday <= 4:
        start_pls = 1
        end_pls = 1

    # Check next weekend
    elif weekday == 5:
        start_pls = 6
        end_pls = 8

    # Check next weekend but not match with Monday
    else:
        start_pls = 5
        end_pls = 7
    
    start_range = date_ref + timedelta(days = start_pls)
    end_range = date_ref + timedelta(days = end_pls)

    return [
        start_range.strftime(DATE_STR),
        end_range.strftime(DATE_STR)
    ]