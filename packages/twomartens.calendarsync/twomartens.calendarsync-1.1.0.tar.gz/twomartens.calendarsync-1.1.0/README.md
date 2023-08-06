# Calendar synchronization

This is a small tool that can be used to synchronize a Jekyll event collection
with a remote calendar.

## Installation

Use Python package manager

``pip install twomartens.calendarsync``

Afterwards you can use ``tm-calendarsync`` to access the CLI interface. If you installed
the package into a virtual environment, this environment needs to be activated. Otherwise
the ``tm-calendarsync`` command will not be known.

## Usage

``tm-calendarsync calendar_url event_collection_path``

The CLI interface validates the input and guarantees that the URL is valid and the directory
of the event collection exists. It however does not make logical checks. So you need to
make sure that the directory is actually the correct one. The URL for the calendar must be
readable without authentication and point to an ICS file.

If the input is correct the tool will go through ALL events of the calendar and create files
in the event collection directory. The filename of these is as follows:

``YYYY-MM-DD-title.markdown`` where all spaces in the title are replaced by underscores (``_``).

The content of these files follows this structure:

```markdown
# preamble for Jekyll event (this line is not actually written)
---
layout: event
title:  <name>
date: <created>
start_date: <begin>
end_date: <end>
location: <location>
---
```

The full usage of this tool becomes obvious if you create a cronjob or something similar that executes this code
every x amount of time. 

Note: Even if you run this as a cronjob it will not yet result in any visible changes to the Jekyll-powered website.
You will need to trigger the build yourself in whatever way makes sense to you. 
