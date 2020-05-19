"""Contains values and functions used in many modules."""

my_id = -1

APP_NAME = "Mendiona bytes"

BACKGROUND = 'SkyBlue1'
FOREGROUND = 'LightSkyBlue1'

CUSTOMER_WINDOW_SIZE = "650x600"
ADMIN_WINDOW_SIZE = "1000x500"
LOGIN_WINDOW_SIZE = "300x200"


def is_float(value):
    """check whether it's float but also not throw error when it's string"""
    try:
        return isinstance(float(value), float)
    except ValueError:
        return False


def is_integer(value):
    """check whether it can be an int but also not throw error when it's string"""
    try:
        return isinstance(int(value), int)
    except ValueError:
        return False
