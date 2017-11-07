#!/usr/bin/env python3

import sys, math
try:
    from unidecode import unidecode
except:
    print('Error: unidecode not found. You probably need to apt install python3-unidecode')
    exit(3)

if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
    print(
'''Upstairs lab: seats.py up [options]
Downstairs lab: seats.py down [options]
Who is on a seat: seats.py seat <number> [options]
Find someone: seats.py find <name> [options]

This tool requires a csv file on STDIN:
    cat seats.csv | python3 seats.py down
Or a little easier:
    <seats.csv python3 seats.py down

The csv file is in the format "seat,name\\n" (without header), e.g. 1,Jon Doe

If the output is too wide for your screen, pipe it to less -S and use arrow
keys to pan.

Options:
    -s  Use first names only when displaying the grid
''')
    exit(1)

grids = {}
grids['up'] = ''
grids['down'] = '''
0  0  5  0  ~ Teacher 0  0  0
8  7  6  0  ~ 4       3  2  1
16 15 14 0  13      12 11 10 9
24 23 22 0  21      20 19 18 17
'''.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip()

space = '_'
unassigned = 'unassigned'

# From https://stackoverflow.com/a/17303428/1201863 by Boubakr
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

shortnames = '-s' in sys.argv
highlightSeat = None

seats = {}
for line in sys.stdin:
    seat, name = line.split(',', 1)
    seats[int(seat)] = name.strip()

if len(seats) < 10:
    print('Warning: Something seems wrong with your csv input file. Use --help for help.')

if sys.argv[1] == 'seat':
    if int(sys.argv[2]) not in seats:
        print('Seat not found in csv input.')
    else:
        print('{} is in that seat.'.format(seats[int(sys.argv[2])]))
    highlightSeat = int(sys.argv[2])
    sys.argv[1] = 'down' if highlightSeat <= 25 else 'up'

elif sys.argv[1] == 'find':
    def normalize(s):
        return unidecode(s.lower()).encode('ascii')

    found = False
    for key in seats:
        if normalize(sys.argv[2]) in normalize(seats[key]):
            print('They can be found in seat {}'.format(key))
            found = True
            highlightSeat = key
            sys.argv[1] = 'down' if highlightSeat <= 25 else 'up'
            break

    if not found:
        print('Name not found.')
        exit(2)

if sys.argv[1] in grids:
    if len(grids[sys.argv[1]]) == 0:
        print('Error: this grid is not implemented.')
        exit(2)

    prn = sys.stdout.write
    def center(name, opts=''):
        global maxw, color
        prespacing = space * (maxw - len(name) - math.floor((maxw-len(name))/2))
        postspacing = space * (maxw - len(name) - len(prespacing))
        return prespacing + opts + name + color.END + postspacing

    maxw = len(unassigned)
    for key in seats:
        maxw = max(maxw, len(seats[key] if not shortnames else seats[key].split(' ')[0]))

    startpipe = '|'
    for line in grids[sys.argv[1]].split('\n'):
        for item in line.split(' '):
            if len(item) <= 2: # Assuming <100 seats here, and that no name (first+last) is <3 characters.
                if item == '~':
                    prn(space * math.floor(maxw / 2))
                else:
                    item = int(item)
                    if item == 0:
                        prn(space * (maxw + 1))
                        startpipe = '|'
                    elif item not in seats:
                        prn(startpipe + center(unassigned, color.RED if highlightSeat == item else '') + '|')
                        startpipe = ''
                    else:
                        name = seats[item] if not shortnames else seats[item].split(' ')[0]
                        prn(startpipe + center(name, color.RED if highlightSeat == item else '') + '|')
                        startpipe = ''
            elif type(item) == str:
                prn(startpipe + center(item) + '|')
            else:
                print('Error: invalid grid.')
        prn('\n')
        startpipe = '|'

else:
    print('Command not found. Use --help for help.')
    exit(1)    

