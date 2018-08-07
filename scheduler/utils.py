from django.core.management import call_command


def create_command(action, arg=None):
    def command():
        if arg:
            call_command(action, arg)
        else:
            call_command(action)

    return command