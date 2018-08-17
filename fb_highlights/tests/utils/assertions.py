import json


def assert_highlight_in(item, list):
    if item not in list:
        error = _create_error(item, list, 'NOT IN')
        raise AssertionError(error)


def assert_highlight_not_in(item, list):
    if item in list:
        error = _create_error(item, list, 'IN')
        raise AssertionError(error)


def _create_error(item, list, error):
    title = item['message']['attachment']['payload']['elements'][0]['title']

    message = '\n\n' + title + '\n' + str(item) + '\n\n' + error

    counter = 1

    for i in range(len(list)):

        if not list[i]['message'].get('attachment'):
            continue

        title = list[i]['message']['attachment']['payload']['elements'][0]['title']

        message += '\n\n'
        message += str(counter) + ") " + title + '\n' + str(list[i])

        counter += 1

    return message