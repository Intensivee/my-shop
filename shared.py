my_id = -1
bgg = 'SkyBlue1'
lgg = 'LightSkyBlue1'
xgg = 'DeepSkyBlue4'


# check whether is int or float but also not throw error when it's string
def is_integer(value):
    try:
        if isinstance(int(value), int):
            return True
        else:
            return False
    except ValueError:
        return False


def is_float(value):
    try:
        if isinstance(float(value), float):
            return True
        else:
            return False
    except ValueError:
        return False