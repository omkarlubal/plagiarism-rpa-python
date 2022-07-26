# plagiarism-rpa-python
A Plagiarism detection bot using RPA, Python and Google Search API

Use UiPath studio to execute the RPA bot (Main.xaml).

Configure the gmail id on which the bot can monitor incoming mail (can be done in studio).
The bot scans for any attachments in the mail. Extracts the text content and passes it to the python script to perform plagiarism checks.
Python script outputs an HTML document (out.html) highlighting the plagiarised content and the sources of the original content from where this was copied.
This document is then mailed to the original sender with a detailed plagiarism report.

Can be highly customized to include more plagiarism detection tools.
Allows configuring of multiple email IDs to monitor.
Bot can carry out specific actions like notifying admin, sending customised mails to sender etc based on the percentage of plagiarism found.
