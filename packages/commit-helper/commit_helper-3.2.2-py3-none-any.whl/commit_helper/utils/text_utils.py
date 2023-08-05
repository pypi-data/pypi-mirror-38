from commit_helper.utils.colors import RESET
from commit_helper.utils.colors import DEBUG_COLOR
from commit_helper.utils.colors import INPUT_COLOR
from commit_helper.utils.colors import NOTIFY_COLOR


def get_text():
    tag = str(input(INPUT_COLOR + 'type the tag: ' + RESET))
    msg = str(input(INPUT_COLOR + 'type the commit message: ' + RESET)).lower()
    return tag, msg


def get_context():
    context = str(input(INPUT_COLOR + 'type the context: ' + RESET) or '')
    context.lower()
    return context


def sanitize_as_empty_string(string):
    if string is None:
        return ''
    return string


def notify(message):
    print(NOTIFY_COLOR + str(message) + RESET)


def debug(message, value, show=False):
    if show:
        mid = 'DEBUG: ' + str(message) + ' ~> ' + str(value)
        print(DEBUG_COLOR + mid + RESET)
