# coding=utf-8
from __future__ import unicode_literals
import json
from itertools import tee, islice, izip_longest

import fuzzy
import re
import pytesser


def peek(some_iterable, window=1):
    items, nexts = tee(some_iterable, 2)
    nexts = islice(nexts, window, None)
    return izip_longest(items, nexts)


def group(match):
    '' if match is None else match.group(0).strip()


def run(filename, debug=False):
    content = pytesser.image_file_to_string(filename)

    def find_match(text, pattern, minimum=None):
        minimum = minimum if minimum else 0.7
        score, match, start, end = fuzzy.bitap(text, pattern)

        if not match or score <= minimum:
            return None, None, None, None

        return score, match, start, end

    content = unicode(content, 'utf-8')

    _, alarm, _, end = find_match(content, 'ALARMDEPESCHE')

    keys = json.loads(file('ocr/keywords.json').read())
    keys = dict(sorted(keys.items(), key=lambda (n, _): len(n), reverse=True))

    if alarm is not None:
        content = content[end:]

        if debug:
            print content

        original = content

        for name, key in keys.items():
            threshold = key.get('threshold')
            score, match, start, end = find_match(content, name, threshold)

            if match:
                skip = False
                for exclude in key.get('exclude', []):
                    alt, _, _, _ = find_match(match, exclude, keys[exclude].get('threshold'))
                    if alt > score:
                        skip = True

                if skip:
                    continue

                newline = content[:start].rfind('\n')

                if newline == -1 or (start - newline) <= 10:
                    key['score'] = score
                    key['match'] = match
                    key['start'] = start
                    key['end'] = end

                    content = content[:start] + re.sub(r'[^\n]', ' ', match) + content[end:]

        tokens = sorted(filter(lambda (_, k): k.get('match') is not None, keys.items()),
                        key=lambda (_, k): k['start'])

        previous = None
        for current, next in peek(tokens):
            _, token = current

            start = token['end']

            if next:
                _, next_token = next
                end = next_token['start']
            else:
                end = len(original)

            def trim(s):
                return re.sub(r'^[ .:‘]+', '', s.strip()).strip()

            s = trim(original[start:end])

            if previous and token.get('previousLine', False):
                _, previous_token = previous
                previous_content = previous_token['content']
                original_find = original.find(previous_content) + len(previous_content)
                s = trim(original[original_find:token['start']]) + s

            if token.get('singleLine', False):
                rows = s.splitlines()
                token['content'] = rows[0]
            elif token.get('table', False):
                rows = filter(None, s.splitlines())
                token['content'] = filter(None, [group(re.search(r'^(.{10,}?) ?', row)) for row in rows[1:]])
            else:
                token['content'] = s

            previous = current

        tokens = filter(lambda (_, k): not k.get('ignore', False), tokens)

        if debug:
            import pprint

            pprint.PrettyPrinter(indent=4).pprint(tokens)

        return {name: token['content'] for name, token in tokens}

    return []