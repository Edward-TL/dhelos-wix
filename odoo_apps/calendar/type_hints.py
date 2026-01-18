"""
"""

from typing import Literal

Privacy = Literal[
    'public',
    'private',
    'confidential'
]

ShowAs = Literal[
    'busy',
    'free'
]

Frequency = Literal[
    'daily',
    'weekly',
    'monthly',
    'yearly'
]

AlarmType = Literal[
    'notification',
    'email',
    'sms'
]

Interval = Literal[
    'minutes',
    'hours', 
    'days'
]

AppointmentTz = Literal[
    'America/Mexico_City',
    'America/Monterrey',
    'UTC'
]