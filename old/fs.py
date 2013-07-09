import os
import datetime
import glob

__author__ = 'Christopher'

def start():
    neu = os.path.join('Alarmfax', 'Neu')
    bearbeitung = os.path.join('Alarmfax', 'Bearbeitung')
    #Sieht nach, ob ein neues Fax da ist
    faxs = glob.glob(os.path.join(neu, '*.tiff'))
    if faxs:
        fax = faxs[0]
    else:
        return None

    print fax, 'vorhanden'
    #Bennennt das Fax um und verschiebt es in den Ordner Alarmfax
    time = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    ziel = os.path.join(bearbeitung, time + '.tiff')
    os.rename(fax, ziel)
    fax = ziel


    return fax



def finish(fax):
    alt = os.path.join('Alarmfax', 'Alt')
    os.rename(fax, os.path.join(alt, os.path.basename(fax)))
