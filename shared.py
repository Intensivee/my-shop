"""Contains values and functions used in many modules."""

my_id = -1
bgg = 'SkyBlue1'
lgg = 'LightSkyBlue1'
xgg = 'DeepSkyBlue4'


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
