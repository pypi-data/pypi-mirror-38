# Copy Over Keeping Ownership (coko)
Tool to overwrite directories using files from a different owners but keeping original owners and permissions.
____
Sometimes you have a directory full of files you want to overwrite periodically. 

You may not want to edit those files directly but let other users edit their own copy of those files to sync them over original ones afterwards. 

Problem there is that local copies may have changed their owners or permissions after being edited by user so those metadata are carried over original directory overwriting them.

This tools let you take an snapshot of your files metadata in a particular directory in order to restore those metadata after files have been overwritten by others version.

## An use case
One use case we're using coko for is to let or development team to fine tune configuration files of development containers. They have their own copy of configuration files and we let them upload to a transient folder inside container. Then a cron job copy files from that transient folder into application folder using coko. If we weren't using coko, application folder would end having files with the users, our developers have to upload changes, as owners.

Theorically docker has a flag (-a) that lets you get more or less the same effect but we haven't got it work and we feel it can be a docker bug. So, while that bug is fixed, we use coko. 
