from linechatter.constants import LEFT_PERS
from linechatter.constants import RIGHT_PERS


def insert_every_n(raw_string, group=13, char='\n'):
    return char.join(raw_string[i:i+group] for i in range(0, len(raw_string), group))


def is_line_msg(line):
    if line_startswith(line, LEFT_PERS):
        return True
    elif line_startswith(line, RIGHT_PERS):
        return True
    else:
        return False


def line_startswith(line, cmpstr):
    if line[0].strip().startswith(cmpstr):
        return True
    else:
        return False


def set_line_len(raw_msg):
    msg = ""
    if len(raw_msg) > 13:
        msg = insert_every_n(raw_msg)
    else:
        msg = raw_msg
    return msg
