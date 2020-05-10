"""
Filters for templates
"""


def split(value, arg):
    # Tach string thanh list
    try:
        return value.split(arg)
    except Exception as e:
        return []
