import os


def is_allowed_file(filename):
    allowed_extensions = {'.bmp', '.png', '.jpg', '.jpeg', ',gif'}
    _, ext = os.path.splitext(filename)
    return ext.lower() in allowed_extensions

