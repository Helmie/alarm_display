import fuzzy
import re
import pytesser


def run(filename):
    content = pytesser.image_file_to_string(filename)
    minimum_ratio = 80

    def find_match(line, word):
        ratio, word = fuzzy.partial(line, word)

        if ratio >= minimum_ratio:
            return word

        return None

    def find_alarm(lines):
        for line in lines:
            match = find_match(line, 'ALARMDEPESCHE')
            if match is not None:
                return match
        return None

    dictionary = {}
    lines = content.splitlines()
    alarm = find_alarm(lines)
    print alarm
    if alarm is not None:
        i = content.index(alarm)
        content = content[i:]

        for line in content.splitlines():
            if line.strip() == '':
                continue

            keys = ["Einsatzstichwort", "Sachverhalt", "Sondersignal", "Einsatzbeginn(Soll)", "Auftragsnummer",
                    "Objekttyp",
                    "Objekt",
                    "Strasse / Hausnummer", "Strasse", "Zusatz Strasse", "Segment", "PLZ / Ort", "Stadt", "Region",
                    "Info",
                    "Telefon"]

            for key in keys:
                match = find_match(line, key)
                if match is not None:
                    print key + ':',
                    rest = line.replace(match, '').strip()
                    rest = re.sub(r'^[.:]?', '', rest).strip()
                    dictionary[key] = rest
                    break

    return dictionary