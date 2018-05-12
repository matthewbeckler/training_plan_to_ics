#!/usr/bin/env python
#
# This tool helps convert a copy-and-pasted running race training plan,
# into an ICS file that can be imported into a calendar system.
#
# This tool adds assumes that each day of the week has the same type
# of activity each week, and adds corresponding notes to the ICS
# event field. It also adds the URL to the bottom of the description.
#
# To use:
# 1. Set a `start_date` or `end_date` below (but not both).
# 2. Copy/paste the tab-split training plan table into the
#    `raw_data` string below.
# 3. Then add `day_of_week_details` entries for each day of
#    the week (if you want).
# 4. If you want an URL added to the end of the details, add one
#    to the `url` variable below.
# 5. The output ICS file will be written to the file `output_filename`,
#    change this filename if you like.
#
# Assumptions and limitations:
# * Assumes the training plan is full weeks (no partial weeks).
# * Assumes the same details for each day of the week, so you'll have to
#   edit the event descriptions for exceptional events (like a race).
#
# Written by Matthew Beckler - matthew at mbeckler.org
# No rights reserved. Released into the public domain, good luck, have fun.
#
# If you have suggestions for improvements or bug fixes, check out the repo:
# https://github.com/matthewbeckler/training_plan_to_ics

import sys
import os
from datetime import date as Date, datetime as DateTime, timedelta as TimeDelta

# Set either start OR end date (but not both).
# using something like Date(2018,5,7) for May 7, 2018
start_date = Date.today()
end_date = None

# You can add details to each event's description.
# If you want to add a newline, use \\n so that \n ends up in the output file.
# Regardless of which weekday is the start_date, this array starts with Monday.
day_of_week_details = [
    "Monday--Rest: because your body needs rest",
    "Tuesday--Run: one foot in front of the other",
    "Wednesday--Bicycle: turns out there are other muscles",
    "Thursday--Run: yes, more running",
    "Friday--Rest: but don't do anything I wouldn't do",
    "Saturday--Long Run: slow and easy (but long)",
    "Sunday--Cross-Training: bike or swim or row or whatever",
]
assert len(day_of_week_details) == 7, "A week has seven days, silly"

# Copy-paste the training plan table into this multi-line string.
# True HTML tables will paste with tab characters, for easy .split().
# Many training plan websites have the week number in the first column.
# If each row has 7 items, this script assumes they are Mon-Fri.
# If each row has 8 items, this script assumes the first column is week number.
# The entries here will become the calendar entry titles, so feel free to edit.
# Blank lines will be skipped.
raw_data = """
1	Rest	1 m run	Bike 60min	3 m run	Rest	Run 6 mi	Bicycling
2	Rest	2 m run	Bike 60min	3 m run	Rest	Run 7 mi	Bicycling
3	Rest	3 m run	Bike 60min	3 m run	Rest	Run 5 mi	Bicycling
4	Rest	4 m run	Bike 60min	3 m run	Rest	Run 9 mi	Bicycling
5	Rest	3 m run	Bike 60min	3 m run	Rest	Run 10 mi	Bicycling
6	Rest	4 m run	Bike 60min	3 m run	Rest	Run 7 mi	Bicycling
7	Rest	3 m run	Bike 60min	3 m run	Rest	Run 12 mi	Bicycling
8	Rest	4 m run	Bike 60min	3 m run	Rest	Rest	Half Marathon
9	Rest	3 m run	Bike 60min	4 m run	Rest	Run 10 mi	Bicycling
10	Rest	4 m run	Bike 60min	4 m run	Rest	Run 15 mi	Bicycling
11	Rest	4 m run	Bike 60min	4 m run	Rest	Run 16 mi	Bicycling
12	Rest	3 m run	Bike 60min	5 m run	Rest	Run 12 mi	Bicycling
13	Rest	4 m run	Bike 60min	5 m run	Rest	Run 18 mi	Bicycling
14	Rest	5 m run	Bike 60min	5 m run	Rest	Run 14 mi	Bicycling
15	Rest	5 m run	Bike 60min	5 m run	Rest	Run 20 mi	Bicycling
16	Rest	5 m run	Bike 60min	4 m run	Rest	Run 12 mi	Bicycling
17	Rest	4 m run	Bike 60min	3 m run	Rest	Run 8 mi	Bicycling
18	Rest	3 m run	Bike 60min	2 m run	Rest	Rest	Marathon
"""

# If you want to add an URL to the event description, add one here,
# otherwise leave it as `None`.
#url = None
url = "http://example.com/"

# Filename for the ICS output, change it if you want
output_filename = "training_plan.ics"


# END OF THINGS TO CUSTOMIZE

if start_date is not None and end_date is not None:
    print "Please only define one of start_date/end_date, not both."
    sys.exit(1)

data = []
for line in raw_data.split("\n"):
    if line == "":
        # skip blank lines
        continue
    items = line.strip().split("\t")
    #print len(items), items
    if len(items) == 7:
        data.append(items)
    elif len(items) == 8:
        data.append(items[1:])
print "Parsed %d weeks worth of training plan" % len(data)

if not start_date:
    # compute start date based on end_date - training plan length
    start_date = end_date + TimeDelta(weeks = -len(data))
    print "Computed start date %s based on %d training weeks before end date %s" % (start_date, len(data), end_date)


file_header = """BEGIN:VCALENDAR
VERSION:0.1
PRODID:-//training_plan_to_ics_0.1//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""

vevent="""BEGIN:VEVENT
SUMMARY:{}
UID:{}@training_plan_to_ics
STATUS:CONFIRMED
TRANSP:TRANSPARENT
DTSTART:{}
DTEND:{}
DESCRIPTION:{}
END:VEVENT
"""

file_footer="""END:VCALENDAR
"""

print "Writing to output file \"%s\"" % output_filename
with open(output_filename, "w") as fp:
    text = file_header

    count = 0
    today = start_date
    print "Start date: %s" % today
    for week in data:
        for day in week:
            tomorrow = today + TimeDelta(days = 1)
            #print today, today.strftime("%Y%m%d"), tomorrow.strftime("%Y%m%d"), day
            description = day_of_week_details[today.weekday()]
            if url:
                description += "\\n\\n" + url
            text += vevent.format(day, DateTime.now().strftime("%s") + "-" + today.strftime("%s"), today.strftime("%Y%m%d"), tomorrow.strftime("%Y%m%d"), description)
            count += 1
            today = tomorrow
    print "End date: %s" % today

    text += file_footer

    # A random ICS validator online said to use DOS line endings so :shrug:
    fp.write(text.replace("\n", "\r\n"))

    print "Wrote %d events to ICS file" % count

