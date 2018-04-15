class ClientWrapper:

    def __init__(self):
        self.client_send = True

messages = []


def client_test(func):
    def func_wrapper(url, message):
        if CLIENT_SEND:
            func(url, message)
        else:
            messages.append(message)

    return func_wrapper