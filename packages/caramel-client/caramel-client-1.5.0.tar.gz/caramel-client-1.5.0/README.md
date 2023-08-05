Caramel client README
==============

What is Caramel Client?
----------------

Caramel Client is a python client for the Caramel CA system. The Python
implementation is under the GPL3 license, but there is a shell script version
under a more permissive license.


What's in the shell/ directory?
------------------

There's a small automatic refresh client, suitable for running via cron.
There's also a small shellscript implementation of the caramel client.

Both require sha256sum to be installed, and curl to be built with TLS support.


License
-------
We have chosen the GNU Affero GPL v3 license for the project. We see no need
for others to keep modification to this software a secret, and we welcome
outside providers. Just because the code is GPLv3, doesn't prevent you from
keeping your keys & certificates private.

For the organizations using this, there should be no additional gain to be
had from keeping the source code secret, and if you think there is any such
gain, please contact us.
