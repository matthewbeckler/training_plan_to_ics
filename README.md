This tool helps convert a copy-and-pasted running race training plan, into an ICS file that can be imported into a calendar system.

This tool adds assumes that each day of the week has the same type of activity each week, and adds corresponding notes to the ICS event field. It also adds the URL to the bottom of the description.

To use:
1. Set a `start_date` or `end_date` below (but not both).
2. Copy/paste the tab-split training plan table into the `raw_data` string below.
3. Then add `day_of_week_details` entries for each day of the week (if you want).
4. If you want an URL added to the end of the details, add one to the `url` variable below.
5. The output ICS file will be written to the file `output_filename`, change this filename if you like.

Assumptions and limitations:
* Assumes the training plan is full weeks (no partial weeks).
* Assumes the same details for each day of the week, so you'll have to edit the event descriptions for exceptional events (like a race).
