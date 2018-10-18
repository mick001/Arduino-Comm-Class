## Arduino-Comm-Class

Arduino Communication Class is a high level interface based on the serial module for faster communication with your Arduino board.

Included functions:

- Send a character to Arduino UNO through the serial port.
- Send an integer value to Arduino UNO through the serial port.
- Send an array of integer values to Arduino UNO through the serial port.
- Read the first n lines written by Arduino UNO to the serial port.

A GUI is available but by no means necessary to use the module.
The article presenting the GUI can be found [here](http://firsttimeprogrammer.blogspot.com/2014/08/arduino-module-gui-beta-version.html).

## Supported boards
So far I have tested only Arduino UNO but the program should work with other boards too. Feel free to let me know if you made any test and/or would like to contribute.

## Installation
No need to install anything, just make sure to have Python and all the dependency installed and run the script using your favourite IDE.

## Examples
A simple [example of application](https://firsttimeprogrammer.blogspot.com/2015/08/using-arduino-to-measure-friction.html) is provided at [The Beginner Programmer](http://firsttimeprogrammer.blogspot.com). The example explains how to measure friction coefficient using Arduino and this project.

Other articles are available at [The Beginner Programmer](http://firsttimeprogrammer.blogspot.com).

## Notes
Note that when using the reading function, the script will loop until a "\n" character is written to the serial port by Arduino. For instance, if you as Arduino to read the first 2 value written to the serial port, the corresponding program on the board must include in the main loop:

Serial.print(value)
Serial.print("\n")

so that the output on the serial port should look like this:

1
2
...

otherwise the program will loop indefinitely.

## License
See the LICENSE file for license rights and limitations (GPL 3.0).

