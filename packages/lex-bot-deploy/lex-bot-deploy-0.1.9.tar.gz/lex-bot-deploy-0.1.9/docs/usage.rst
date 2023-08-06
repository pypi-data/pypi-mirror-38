=====
Usage
=====

Deploy
------

lex_bot_deploy.lex_deploy(lex_schema_file='path to file')
To use lex-bot-deploy in a project::

    from lex_bot_deploy import lex_bot_deploy

    lex_bot_deploy.lex_deploy(lex_schema_file='path to Lex Schema file')

To use the command line::

    lex-bot-deploy -e 'path to Lex Schema file'

Get Schema
----------

To export a schema::

    lex-bot-get-schema --lex-bot-name ScheduleAppointment

Will export the standard Schedule Appointment demo Lex bot to the local file system as a JSON file.
Keep in mind that the export requires a version to exist, so you need to have published at least once. Default version is 1



