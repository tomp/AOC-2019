# AOC-2019
Python solutions for the 2019 Advent of Code http://adventofcode.com/2019

The solution for each day's puzzle is in its own folder.

Convenience scripts
-------------------
The "new_day.sh" script will create the directory for a new day's puzzle and
populate it with a starter script that provides ithe boilerplate structure for
a puzzle solution, and a few useful utility functions.  Your input for the
puzzle is also downloaded into that directory and stored as "input.txt".

To download your input file, you'll need to log in to adventofcode.com and
grab the session key from the request headers.  I usually just use the browser's
developer tools to dig that out, but I suspect there's a more elegant way to
get that.  The seesion key should be stored as a single line in a file
name "session_key.txt", in the same directory as this file.

Once you have a session key stored, you can create the folder for a new day
(say, day 23) using the command,

./new_day.sh 23

The folder and files are only created if they don't already exist.

