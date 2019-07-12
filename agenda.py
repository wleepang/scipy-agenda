import re
import argparse
from datetime import datetime, timedelta
from textwrap import dedent

import arrow
from ics import Calendar, Event
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()

parser.add_argument(
    'infile',
    help='path to input agenda (html file)')

parser.add_argument(
    '-o',
    dest='outfile',
    default='agenda.ics',
    help='path to output .ics file')


def parse_agenda(soup):
    """
    parse an html soup agenda into events
    """
    agenda_rows = (
        soup
        .select_one('.agenda-row.by_date_item')
        .select('.agenda-date, .time-event-row:not(.filtered_out)')
    )
    curdate = None
    events = []
    for row in agenda_rows:
        if 'agenda-date' in row.attrs['class']:
            curdate = row.h4.text
        elif 'time-event-row' in row.attrs['class']:
            event = {
                'date': curdate,
                'times': row.select_one('.time').span.text.strip(),
                'title': row.select_one('.session_name').text.strip(),
                'location': row.select_one('.session_location').text.strip(),
            }

            event['times'] = (
                re.match(
                    '(\d+:\d+\s+[ap]m+).*?(\d+:\d+\s+[ap]m)', 
                    event['times']
                )
                .groups()
            )

            speakers = [
                speaker.text.strip()
                for speaker in row.select('.speaker_name')
            ]
            event.update(speakers=', '.join(speakers))

            if row.select_one('.track_name'):
                event.update(track=row.select_one('.track_name').text.strip())
            
            events += [event]
        else:
            print('skipping row:', row)

    return events


def create_event(event):
    """
    convert event dictionary to Event object
    """
    dtformat = '%m/%d/%Y %I:%M %p'
    dtstart = arrow.get(
        datetime.strptime(f"{event['date']} {event['times'][0]}".upper(), dtformat),
        'US/Central')

    dtend = arrow.get(
        datetime.strptime(f"{event['date']} {event['times'][1]}".upper(), dtformat),
        'US/Central')

    description = [event['title']]

    if event['speakers']:
        description += [event['speakers']]

    if event.get('track'):
        description += [event['track']]
    
    return Event(
        name=event['title'],
        begin=dtstart,
        end=dtend,
        location=event['location'],
        description='\n'.join(description)
    )


def main(args):

    with open(args.infile, 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')

    events = [create_event(event) for event in parse_agenda(soup)]

    from pprint import pprint; pprint(events)
    cal = Calendar(events=events)
    with open(args.outfile, 'w') as f:
        f.writelines(cal)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
