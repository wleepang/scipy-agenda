# SciPy 2018 Agenda Maker

Creates an iCalendar (`*.ics`) file from the "build your own agenda" page created by the 
SciPy 2018 conference schedule tool that you can import into your calendar app of choice\*

__(\* tested with iCalendar and MS Outlook on a Mac)__

## Dependencies

* python 3.6+
* ics - package for reading / writing `*.ics` files

## Usage

1. Create your agenda
2. Highlight the agenda created and <kbd>ctrl/cmd-c</kbd> and <kbd>ctrl/cmd-v</kbd> the contents
   into a plain text file.
3. run `agenda.py`:

```
python agenda.py path/to/plaintext/agenda.txt
```

The above will create a `agenda.ics` file that you can import into your calendar app of choice.



