import re
import argparse
from datetime import datetime, timedelta

import arrow
from ics import Calendar, Event

parser = argparse.ArgumentParser()

parser.add_argument(
    'infile',
    help='path to input agenda (plain text)')

parser.add_argument(
    '-o',
    dest='outfile',
    default='agenda.ics',
    help='path to output .ics file')


def parse_agenda(filepath):
    """
    parse a plaintext agenda into events
    """
    # get a whitespace cleaned list of lines
    lines = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]

    # agenda items are in sets of lines with a rough hierarchy
    # [date]
    # .. [timestart] - [timeend]
    # .. [title]
    # .. [details...]
    # .. "Add to My Agenda"
    events = []
    curdate = None
    event = []
    for line in lines:
        if re.search('\d+/\d+/\d+', line):
            curdate = line

        elif re.search('add to my agenda', line, re.I):
            # wrap up the event
            # add to list of events
            event.insert(0, curdate)
            events += [event]
            event = []

        else:
            rex = re.match('.*\t(.*)', line)
            if rex:
                line = rex.groups(1)[0]
            
            event += [line]

    return events

def parse_event(event):
    """
    parse lines for an event into a dictionary
    """

    date, times, title, *details = event

    times = re.match('(\d+:\d+\s+[ap]m+).*?(\d+:\d+\s+[ap]m)', times).groups()

    dtformat = '%m/%d/%Y %I:%M %p'
    dtstart = arrow.get(
        datetime.strptime(f"{date} {times[0]}".upper(), dtformat),
        'US/Central')

    dtend = arrow.get(
        datetime.strptime(f"{date} {times[1]}".upper(), dtformat),
        'US/Central')

    location = details[-1]
    description = details[:-1] if len(details) > 1 else details

    return Event(
        name=title,
        begin=dtstart,
        end=dtend,
        location=location,
        description=', '.join(description)
    )

def main(args):
    events = [parse_event(event) for event in parse_agenda(args.infile)]

    from pprint import pprint; pprint(events)
    cal = Calendar(events=events)
    with open(args.outfile, 'w') as f:
        f.writelines(cal)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
