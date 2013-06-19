import pytesser

content = pytesser.image_file_to_string('depesche.tiff')

if "ALARMDEPESCHE" in content:
    print "ALARM!"


