from __future__ import unicode_literals

import fuzzy
import re
import pytesser

keys = [
    'Einsatzstichwort',
    'Sachverhalt',
    'Sondersignal',
    'Einsatzbeginn(Soll)',
    'Auftragsnummer',
    'Objekttyp',
    'Objekt',
    'Strasse / Hausnummer',
    'Zusatz Strasse',
    'Strasse',
    'Segment',
    'PLZ / Ort',
    'Stadt', 
    'Region',
    'Info',
    'Telefon'
]


def run(filename, debug=False):
    content = pytesser.image_file_to_string(filename)
    minimum_ratio = .75

    def find_match(string, substring):
        ratio, word, start, end = fuzzy.substring(string, substring)

        if ratio >= minimum_ratio:
            return word, start, end

        return None, None, None

    dictionary = {}

    content = unicode(content, 'utf-8')

    alarm, _, end = find_match(content, 'ALARMDEPESCHE')

    if alarm is not None:
        content = content[end:]

        engines, start, _ = find_match(content, 'Einsatzmittelliste')
        content = content[:start]

        if debug:
            print content

        for line in content.splitlines():
            if not line.strip():
                continue

            for key in keys:
                match, start, end = find_match(line, key)
                if match is not None:
                    rest = line[end:].strip()
                    rest = re.sub(r'^[.:]?', '', rest).strip()
                    dictionary[key] = rest
                    break

    return dictionary