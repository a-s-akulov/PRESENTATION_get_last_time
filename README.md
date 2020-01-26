# PRESENTATION_get_last_time

This is my 6th task on Python. This is a script for the Zabbix monitoring system.
The camera must be recorded on a memory card.
Get date and time
The last successful record on the memory card in some format.

The task of the script is to check how long the production record on the memory card
and issue a specific code.

My script has 4 output options:

"TimeGood": 0, - in case of successful passing of verification
"TimeBad": 1, - in case the last record was too long
"ConnFailed": 2, - Could not connect to camera
"ExecError": 3, - We were able to connect to the camera, but could not correctly decrypt the response from it


It was assumed that Zabbix will run a script for each of these cameras, passing the IP address of the camera as a parameter

used modules:

  sys,
  paramiko
