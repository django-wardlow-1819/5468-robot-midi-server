# 5468-robot-midi-server

A python program that runs on a frc driver station an uses FRC networktables (and sin) to transmit limited midi data (badly) to the robot. 
this code was designed to work with the x-touch compact and our robot code (https://github.com/SummitRobotics/FRC2020, midi branch is probably the most up to date with midi stuff)
it is only capable of of sending ccs and notes (only on/off, no velocity values) to the robot and receiving ccs and note ons (with velocity values) from the robot to send to the device, 
however, it is possible to adapt it to send/receive any data with some work. it dose not send the data in a "reasonable" way, so be sure to reference (copy) our robot code to get it to work on your robot.

## Requirements
to run the code, you will need to install
* windows (it should be able to run on other oses but not tested)
* python 3, with all default library's including threading, tkinter, and sys
* pynetworktables (https://robotpy.readthedocs.io/en/stable/install/pynetworktables.html)
* python-rtmidi (https://pypi.org/project/python-rtmidi/)

## Installing
download the 3 python files, put them in a folder or on the desktop and run main.py (rename it to .pyw to make the terminal window not show up)
i will hopefully get around to compiling it into a exe when it gets more finished, but don't count on it

## Usage
once opened, the program will show a error message if there are no midi devices connected to your computer.
when this happens, close the program, connect the device, and restart the program (the device must be both a input and output for it wo work).
once the program opens fully, a window will open. in this window there is the input and output selection dropdown, ip entry box and connect button.
make sure you are connected to a robot running compatible code, the correct input and output are selected and the ip in the ip entry box 
(defaults to 10.45.68.2, go into GUI.py to change default) you have the ip of your roborio. once you have all that press the red connect button.
it will turn blue if no ip is entered (does not check for a valid ip,only if there is anything in the box), yellow while connecting, and green once connected.
if a incorrect ip has been entered or the robot is off the program will freezes and will have to be force closed. 
it will also automatically re-connect if it gets disconnected form the robot
once connected, midi data will be sent from the device to the robot and back.
to disconnect, close the program.

## Testing without a robot/code
to test the program without comparable code:
 pull the midi branch from our github
 open it in frc vs code
 use the simulate robot code on desktop option and then put the robot in telyop mode
 set the ip of the program to 127.0.0.1 and connect
 try to understand how the robot code works so you can use it (the main file is src\main\java\frc\robot\oi\Midi.java but 
 everything in the oi folder that starts with midi is a good reference)

## How does it work
short answer: badly

medium answer: go look at the comments

long answer:

* the gui: a new thread is made and 2 lambdas are passed in. the thread makes all tkinter stuff then runs mainloop. 
the lambdas are startAction and stopAction and they allow the tkinter thread to start and stop network tables.

* midi: when connect is pressed on the gui a thread is started that continually requests new midi data from python-rtmidi. 
if there is new data the data is possessed in MidiInterface.py to remove the timestamp and separate the chanel, data type and data byte 1 and 2. 
that data is then possessed by  MidiInterfaceWrapper.py and if the data is a note on/off or cc then it calls a corresponding function from NetworkTablesWrapper.py to send the data to the robot
when data needs to be sent to the robot NetworkTablesWrapper.py calls a the function corresponding to the data type in MidiInterfaceWrapper.py witch then uses MidiInterface.py to put the data in a valid format and use python-rtmidi to send it to the device

* networktables: when NetworkTablesWrapper.py is inited it makes a connection to the robot with the ip passed in from the gui. once connected 4 tables are made 
(ccTable, noteTable, CCReturn, NoteReturn) the first 2 tables contain get dynamically populated with values based on what is received from the controller, 
each new cc or note from the controller make or updates a entry with the key being the first byte and the data in the entry being true/false for notes or the second data byte for ccs.
on connection the 2 return tables get a listener added to every entry from 0-127. the listeners listed for updates and when one is detected it calls to MidiInterfaceWrapper.py to send the midi data to the device.


## Warnings

* ALL OF THIS CODE IS BAD, ITS PROBABLY BEST TO RE-DO IT ALL USING rtpMIDI OR SOMETHING IF YOU WANT TO USE IT
* all the lambdas everywhere are dumb
* using network tables for this project was a bad idea, we thought it would be simple because its supported by the robot natively but it ended up making everything bad.

## Making it better
we hope to continue to make the code better but if you go in and fix it all then please fork this project, fix it all, then make a pull request.
also provide working robot code with the project if you change how networktables works (witch you should).

## License

This project is licensed under the GNU General Public License License - see the [LICENSE.md](LICENSE.md) file for details