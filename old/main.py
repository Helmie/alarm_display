import fs
import ocr
import repeat

__author__ = 'Christopher'


def task():
    fax = fs.start()
    if fax is not None:
        print fax + " gefunden!"
        ocr.texterkennung(fax)
        fs.finish(fax)
    else:
        print "Nichts gefunden :("


repeat.every(task, seconds=60)
