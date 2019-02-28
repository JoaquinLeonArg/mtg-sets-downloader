from requests import get, post
import os
import errno
from PIL import Image


def save_file(path, content):
    if os.path.isfile(path):
        return
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(path, 'wb') as f:
        f.write(content)

def convert_filename(name):
    return "".join(x for x in name if x.isalnum())

sets = [(i['released_at'], i['code'], i['name'], i['search_uri']) for i in get('https://api.scryfall.com/sets').json()['data']]

while True:
    cmd = input(' > ')
    cmd_download = cmd == 'download'
    cmd_sets = cmd == 'sets'
    cmd_close = cmd == 'close'
    if cmd_download:
        set_name = input('   Set short name: ')
        set_url = [s[3] for s in sets if s[1] == set_name]
        if set_url:
            r = get(set_url[0]).json()
            for c in r['data']:
                print('   SAVING {}'.format(c['name']))
                if 'image_uris' in c:
                    filename = 'dl/{}/{}.png'.format(set_name, convert_filename(c['name']))
                    if os.path.isfile(filename):
                        continue
                    card_image = get(c['image_uris']['png'])
                    save_file(filename, card_image.content)
                else:
                    print('   >>> Image not available for download. Continuing. <<')
    elif cmd_sets:
        print('   DATE            CODE     NAME\n')
        for s in reversed(sets):
            extra_spaces = ' '
            if len(s[1]) == 4:
                extra_spaces = ''
            print('   ' + s[0] + '      ' + s[1] + extra_spaces + '     ' + s[2])
    elif cmd_close:
        exit()
    else:
        print('   Unknown command {}. Usage:\n\n   download  --downloads a card set\n   sets  --lists all available sets\n   close  --exits the program'.format(cmd))