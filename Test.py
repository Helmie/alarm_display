import re
import pytesser
import difflib

#read the paper 'depesche.tff',make ocr and put it into content
content = pytesser.image_file_to_string('05.tiff')

#starts the programm

minimum_ratio = 0.8

def find_match(line, word):
    def substrings(line):
        for i in range(len(line), 0, -1):
            yield line[0:i]

    matches = map(lambda w: {'word': w, 'ratio':difflib.SequenceMatcher(None, word, w).ratio()}, substrings(line))
    if len(matches) == 0:
        return None

    matches = sorted(matches, key=lambda match:match['ratio'], reverse=True)

    match = matches[0]
    if match['ratio'] >= minimum_ratio:
        return match
    return None

def find_alarm(lines):
    for line in lines:
        match = find_match(line, 'ALARMDEPESCHE')
        if match is not None:
            return match
    return None

lines = content.splitlines()               #teilt den String content in Zeilen
alarm = find_alarm(lines)
if alarm is not None:
    i = content.index(alarm['word'])
    content = content[i:]

    for line in content.splitlines():
        if line.strip() == '':
            continue

        keys = ["Einsatzstichwort", "Sachverhalt", "Sondersignal", "Einsatzbeginn(Soll)", "Auftragsnummer", "Objekttyp", "Objekt",
                "Strasse / Hausnummer", "Strasse", "Zusatz Strasse", "Segment", "PLZ / Ort", "Stadt", "Region", "Info", "Telefon"]

        for key in keys:
            match = find_match(line, key)
            if match is not None and match['ratio'] >= minimum_ratio:
                print key + ':',
                rest = line.replace(match['word'], '').strip()
                rest = re.sub(r'^[.:]?', '', rest).strip()
                print rest
                break
