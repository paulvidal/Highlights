def format_dailymotion_link(link):
    link = format_link(link)

    # add the embed option
    if not '/embed/' in link:
        link = link.replace('/video/', '/embed/video/')

    return link

def format_streamable_link(link):
    link = format_link(link)

    if '/s/' in link:
        resource_id = link.split('/s/')[1].split('/')[0]
    elif '/e/' in link:
        resource_id = link.split('/e/')[1].split('/')[0]
    else:
        resource_id = link.split('/')[-1]

    # Return streamable link in the format 'https://streamable.com/e/ioz1l'
    return 'https://streamable.com/e/' + resource_id


def format_link(link):
    # remove double // if present
    link = link.replace('//', '')

    # remove http
    if not 'https://':
        link = link.replace('http://', '')

    return 'https://' + link