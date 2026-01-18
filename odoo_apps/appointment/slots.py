"""
Slots file made for simplicity and store slots functions
related
"""
from datetime import datetime
from typing import Optional

from odoo_apps.utils.time_management import adapt_datetime, TIME_STR
from .objects import SlotEvent
from .checkers import weekdays_requested, gen_range_hours

def clean_slots_info(slots_info: list[dict]) -> dict:
    """
    Transform a list of dictionaries, that represents slots_info,
    into a dictionary, that contains weekdays_info.
    """
    return {
        int(slot['weekday']) : {
            'start_hour': slot['start_hour'],
            'end_hour': slot['end_hour']
        } for slot in slots_info
    }

def add_weekdays_range_avialability(slots_info: dict, range_hours: list) -> None:
    """
    """
    for wd, hours in slots_info.items():
        slot_start_hour = hours['start_hour']
        if slot_start_hour >= range_hours[0]:
            start_hour = slot_start_hour
        else:
            start_hour = range_hours[0]

        slot_end_hour = hours['end_hour']
        if slot_end_hour <= range_hours[-1]:
            end_hour = slot_end_hour
        else:
            end_hour = range_hours[-1]

        slot_range_hours = [n for n in range(int(start_hour), int(end_hour))]

        slots_info[wd]['range_hours'] = slot_range_hours
        slots_info[wd]['is_free'] = [True] * len(slot_range_hours)

def slots_search_info(slots_info: dict, weekdays_dates: dict) -> None:
    """
    Updates inplace slots_info, adding:
        - day_start:
        - day_stop: 
        - slot_datetime_range:
        - slots_starts:
        - slots_stops:
    """
    for wd, slot_info in slots_info.items():
        # print(slot_range)
        slot_range = slot_info['range_hours']
        date_slots = {
            'slot_datetime_range': [f"{weekdays_dates[wd]} {h}:00 - {h+1}:00" for h in slot_range],
            "start": [adapt_datetime(f"{weekdays_dates[wd]} {h}:00") for h in slot_range] ,
            "stop": [adapt_datetime(f"{weekdays_dates[wd]} {h+1}:00") for h in slot_range]
            }
        
        slots_info[wd]['day_start'] = adapt_datetime(f"{weekdays_dates[wd]} 00:00")
        slots_info[wd]['day_stop'] = adapt_datetime(f"{weekdays_dates[wd]} 23:59")

        
        slots_info[wd]['slot_datetime_range'] = date_slots['slot_datetime_range']
        slots_info[wd]['slots_starts'] = date_slots['start']
        slots_info[wd]['slots_stops'] = date_slots['stop']


def events_overlaps(slot: SlotEvent, event: SlotEvent, printer=False) -> bool:
    """
    Check if a slot is free of a event.
    Consider that:
    1. All three objects are standarized datetimes, in same timezones.
    """

    # Event is before slot
    if event.start_dt <= slot.start_dt and event.stop_dt <= slot.start_dt:
        if printer:
            print('Event is before')
        return False

    if printer:
        print('Event IS NOT BEFORE, checking if is AFTER')
    # Event is after slot
    if slot.stop_dt <= event.start_dt:
        if printer:
            print('Event is after')
        return False

    if printer:
        print("Event is NOT AFTER the slot")
    return True

def confirm_slots_availability(slots_info: dict, events: list[dict]) -> None:
    """
    Updates inplaces slots_info, updating:
        - is_free    
    """
    for o_event in events:    
        o_event['weekday'] = datetime.strptime(
            o_event['start'], TIME_STR
            ).weekday()+1

        n = 0
        for slot_start, slot_stop in zip(
            slots_info[o_event['weekday']]['slots_starts'],
            slots_info[o_event['weekday']]['slots_stops']):

            slot = SlotEvent(slot_start, slot_stop)
            event = SlotEvent(o_event['start'], o_event['stop'])

            is_free = True
            overlaps = events_overlaps(slot, event)
            # print("Events overlaps: ", overlaps)
            if overlaps is True:
                is_free = False

            # print(weekday_slots[o_event['weekday']]['is_free'][n])
            # print("So event is Free:", is_free)
            if slots_info[o_event['weekday']]['is_free'][n]:
                slots_info[o_event['weekday']]['is_free'][n] = is_free

            # print("Weekday:", o_event['weekday'], o_event['name'],n, "IS FREE: ", weekday_slots[o_event['weekday']]['is_free'][n])
            # print(slot_start, o_event['start'])
            # print(slot_stop, o_event['stop'])
            n += 1

def get_slots_available(slots_info: dict[int: dict]) -> tuple:
    """
    Checking in the Slots Info the free space accoding to the weekdays
    """
    availables = []
    for sinfo in slots_info.values():
        slots_availability = sinfo['is_free']
        slot_dt_range = sinfo['slot_datetime_range']
        for is_free, dt_range in zip(slots_availability, slot_dt_range):
            # print(is_free)
            if is_free:
                availables.append(dt_range)

    return tuple(availables)