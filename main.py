import codecs
import os
import re
from chardet.universaldetector import UniversalDetector
from os import listdir

def detect_encode(filename):
    detector = UniversalDetector()
    with open(filename, 'rb') as textfile:
        for line in textfile:
            detector.feed(line)
            if detector.done:
                break
            detector.close()
    return (detector.result.get('encoding'))


def fix_wrong_strings(array):
    count = 0
    for i,e in enumerate(array):
        if not e[:11].isdigit():
            right_index = int(i)-1
            print('Found error # ', count, '| text: ', e)
            if right_index < 0:
                del array[i]
                continue
            array[right_index] = str(array[right_index]).rstrip() + str(array[i][:])
            del array[i]
            count = count + 1

    return (array)

def fix_destination(array):
    wrong_lines = 0
    for line in array.copy():
        from_number = re.search('OT\d+', line)
        to_number = re.search('K\d+', line)
        if from_number or to_number:
            from_line = re.sub('OT\d+','',line)
            from_and_to_line = re.sub('K\d+','',from_line)
            del array[array.index(line)]
            array.append(from_and_to_line)
            wrong_lines = wrong_lines +1
    print(f'Number of wrong lines: {wrong_lines}')
    return array


if __name__ == '__main__':
    print('''
    Check-script for MTS (RUSSIA) providers`s TXT files.
    Author Anton Pozdnyakov.
    Version 2020.12.03
    --------------------------------''')
    input('Please press Enter to continue...')
    
    files = listdir()

    for file in files:
        if file[-3:] == 'txt':
            print('Found file: ', file)
            abspath = os.path.abspath(file)
            os.path.normpath(abspath)
            filecode = detect_encode(abspath)
            print('Encode is...', filecode)
            old_file = codecs.open(abspath, 'r', filecode)
            array = []
            for line in old_file:
                array.append(line)
            old_file.close()
            print('Fixing file: ', file)
            fixed_strings_array = fix_wrong_strings(array)
            print('--------------------------------')
            print ("Searching for wrong lines. Please wait...")
            fixed_array = fix_destination(fixed_strings_array)
            newfilename = 'Checked_' + file
            newfile = open(newfilename, 'w', encoding='utf-8')
            for e in fixed_array:
                e = e.strip()
                if not e[:11].isdigit():
                    print('Attention! Something was wrong: ', e)
                    print('This file can not be used!')
                    break
                else:
                    newfile.write(str(e) + '\n')
            print('--------------------------------')
            newfile.close()
            print('New file created: ', newfilename)
            print('--------------------------------')
    input('Please press Enter to exit...')
    print('--------------------------------')
