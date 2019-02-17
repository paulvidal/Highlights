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


def format_matchat_link(link):
    link = format_link(link)
    link = link.split('?')[0]
    return link.replace('/html/', '/').replace('/player/', '/embed/')


def format_ok_ru_link(link):
    link = format_link(link)
    return link.replace('/video/', '/videoembed/')


def format_link(link):
    link = link.replace("\"", "").replace("\\", "")

    # remove double // at start if present
    if link[:2] == '//':
        link = link[2:]

    # remove http
    link = 'https://' + link.replace('http://', '') if not 'https://' in link else link

    return link


if __name__ == "__main__":
    print(format_matchat_link('https://footy11.videostreamlet.net/player/html/WlsUWPSKVd?popup=yes&autoplay=1'))