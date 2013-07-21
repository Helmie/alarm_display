import fs
import repeat

from ocr import ocr


def task():
    fax = fs.start()
    if fax is not None:
        print fax + " gefunden!"
        ocr.run(fax)
        fs.finish(fax)
    else:
        print "Nichts gefunden :("


repeat.every(task, seconds=60)
