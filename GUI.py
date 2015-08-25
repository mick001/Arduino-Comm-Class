#------------------------------------------------------------------------------
# Name:        Arduino GUI
# Purpose:     Educational
#
# Created:     14/08/2014
# Copyright:   (c) Copyright Mic 2014
# Licence:     GNU GPL
#
#
#     This software is distributed under the GNU GPL license
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    If you need to contact the author of this program, please fill in the
#    contact form at http://firsttimeprogrammer.blogspot.com/p/contacts.html
#
#    This script assumes that you have available somewhere in your script the
#    Arduino class available at: https://github.com/mick001/ArduinoCommClass
#------------------------------------------------------------------------------

import sys
from PyQt4 import QtGui, QtCore
import serial
import time
import struct

def toList(string):
    
    """ This function converts a string such as [1,2,3] into a list of integers """

    final =[]
    for i in string:
        if i == "[" or i == "]" or i == "," or i == " ":
            pass
        else:
            final.append(int(i))
    return final

class Arduino(object):

    def __init__(self,port='com3',speed=9600):

        """ CLASS CONSTRUCTOR """
        
        self.port = port
        self.speed = speed
        self.conn = serial.Serial(port,speed)

    def __repr__(self):

        """ How the object is representing itself when printed/called """        
        
        return "Arduino object:\n\nArduino connected to: %s\nspeed: %s" %(self.port,self.speed)
    
    
    def sendChar(self,char):
        
        """ SEND A CHARACTER (CHAR) TO ARDUINO through serial port"""
        
        if len(str(char))>1 or char == "":
            raise ValueError('Only a single character is allowed')
        
        valueToWrite = bytes(str(char).encode())
        
        try:
            send = self.conn.write(valueToWrite)
        except Exception as e:
            pass


    def sendInteger(self, integer,printR=False):
        
        """ 
            SEND AN INTEGER (INT) TO ARDUINO through serial port
            Optionally a report is printed if printR = True

            Note that integers are converted into raw binary code readable 
            from Arduino through the module struct.
        
            Special thanks to Ignacio Vazquez-Abrams for the suggestion on 
            StackOverflow.
        """
        
        try:
            integer = int(integer)
        except Exception as e:
            pass
        try:
            dataToSend = struct.pack('>B',integer)
            send = self.conn.write(dataToSend)
            if printR:
                print("Sent the integer %s succesfully" %integer)
        except Exception as e:
            pass

    
    def sendIntArray(self,array,delay=2,printR=False):
        
        """            
            SEND AN ARRAY OF INTEGERS (INT) TO ARDUINO through serial port
            Optionally a report is printed if printR = True
            
            Note that the array is sent as a sequence of integers
        """
        
        try:
            for i in array:
                self.sendInteger(i)
                time.sleep(delay)
                if printR:
                    print("Sent integer %s" %i)
            if printR:
                print("Sent the array %s succesfully" %array)
        except Exception as e:
            pass

   
    def readData(self,nlines,printData=False,array=True,integers=False,Floaters=False):
        
        """
            READ DATA FROM ARDUINO through serial port.
            
            The function reads the first nlines and returns an array of 
            strings by default.
            If printData is true it prints the data to the console.
            If array is True it returns an array.
            If integers or Floaters are either True, it returns an array of 
            either integers or float.
            
            Use the Serial.print() function on Arduino to send data
            Serial port on Arduino should be initialized at 9600 baud.
            Example:
                    void setup()
                    {
                        Serial.begin(9600);                    
                    }
                    
                    void loop()
                    {
                        // Sending integer 1 each second 
                        Serial.print(1);
                        delay(1000);                        
                    }
                    
            Carefully note that the function will loop until it collects
            exactly nlines readings or exceptions.
        """
        
        data = []
        
        i = 0
        
        while i <= nlines:
            
            try:
                value = self.conn.readline().decode('ascii').strip()
                data.append(value)
                i += 1
            except Exception as e:
                pass
                i += 1
                
        if printData:
            for k in data:
                print(k)
                
        if array and not integers and not Floaters:
            return data
        elif array and integers and not Floaters:
            dataToReturn = []
            for j in data:
                try:
                    dataToReturn.append(int(j))
                except:
                    dataToReturn.append("None")
            return dataToReturn
        elif array and not integers and Floaters:
            dataToReturn = []
            for j in data:
                try:
                    dataToReturn.append(float(j))
                except:
                    dataToReturn.append("None")
            return dataToReturn
        else:
            pass


    def closeConn(self):

        """ CLOSE THE USB CONNECTION """
        
        self.conn.close()
        

class ArduinoGUI(QtGui.QMainWindow):
    
    """ A GUI FOR THE ARDUINO CLASS """

    is_connected = False    # BOOL: is Arduino connected?
    uno = 0                 # Arduino object will be initialized here
    portt = 'com3'          # Default port
    speedd = 9600           # Default speed

    def __init__(self):

        """ Constructor """
        
        super(ArduinoGUI,self).__init__()
        self.initUI()

    def initUI(self):
        
        """ Basic UI settings """
        
        self.setGeometry(400,200,400,400)
        self.setWindowTitle('Arduino GUI 1.0')

        # menuBar
        menubar = self.menuBar()

        # Fill the menuBar

        # File Menu and functions
        fileMenu = menubar.addMenu('&File')

        passCharAction = QtGui.QAction('&Send character',self)
        passCharAction.triggered.connect(self.senderFun)
        passCharAction.setShortcut('Ctrl+I')
        fileMenu.addAction(passCharAction)

        passIntAction = QtGui.QAction('&Send Integer',self)
        passIntAction.triggered.connect(self.senderFun)
        passIntAction.setShortcut('Ctrl+I')
        fileMenu.addAction(passIntAction)

        passArrAction = QtGui.QAction('&Send array of integers',self)
        passArrAction.triggered.connect(self.senderFun)
        passArrAction.setShortcut('Ctrl+A')
        fileMenu.addAction(passArrAction)

        readAction = QtGui.QAction('&Read data from Arduino',self)
        readAction.triggered.connect(self.readArduino)
        readAction.setShortcut('Ctrl+R')
        fileMenu.addAction(readAction)

        # Connection Menu
        connectionMenu = menubar.addMenu('&Connection')

        setConnAction = QtGui.QAction('&Set up connection',self)
        setConnAction.triggered.connect(self.setupConnection)
        connectionMenu.addAction(setConnAction)

        showConnAction = QtGui.QAction('&Show connection info',self)
        showConnAction.triggered.connect(self.showConnInfo)
        connectionMenu.addAction(showConnAction)

        closeConnAction = QtGui.QAction('&Close connection',self)
        closeConnAction.triggered.connect(self.closeC)
        connectionMenu.addAction(closeConnAction)

        restoreSpeed = QtGui.QAction('&Restore speed to 9600 (default)',self)
        restoreSpeed.triggered.connect(self.speedDefault)
        connectionMenu.addAction(restoreSpeed)

        changeCSAction48 = QtGui.QAction('&Change connection speed to 4800',self)
        changeCSAction48.triggered.connect(self.changeCSA48)
        connectionMenu.addAction(changeCSAction48)

        changeCSAction192 = QtGui.QAction('&Change connection speed to 19200',self)
        changeCSAction192.triggered.connect(self.changeCSA192)
        connectionMenu.addAction(changeCSAction192)

        changeCSAction576 = QtGui.QAction('&Change connection speed to 4800',self)
        changeCSAction576.triggered.connect(self.changeCSA576)
        connectionMenu.addAction(changeCSAction576)

        usbDefault = QtGui.QAction('&Restore USB port to com3 (default)',self)
        usbDefault.triggered.connect(self.USBdefault)
        connectionMenu.addAction(usbDefault)

        changePort2 = QtGui.QAction('&Change USB port to com2',self)
        changePort2.triggered.connect(self.changeUSB2)
        connectionMenu.addAction(changePort2)

        changePort4 = QtGui.QAction('&Change USB port to com4',self)
        changePort4.triggered.connect(self.changeUSB4)
        connectionMenu.addAction(changePort4)



        # About Menu
        aboutMenu = menubar.addMenu('&About')
        showInfoAction = QtGui.QAction('&About',self)
        showInfoAction.setStatusTip('Info on the program')
        showInfoAction.triggered.connect(self.showAbout)
        aboutMenu.addAction(showInfoAction)

        # Help Menu
        helpMenu = menubar.addMenu('&Help')
        showHelpAction = QtGui.QAction('&Help',self)
        showHelpAction.setStatusTip('Help and tips')
        showHelpAction.triggered.connect(self.showHelp)
        helpMenu.addAction(showHelpAction)

        # Buttons
        self.sendBut = QtGui.QPushButton('Send to Arduino',self)
        self.sendBut.move(20,350)
        self.sendBut.clicked.connect(self.senderFun)
        self.readBut = QtGui.QPushButton('Read from Arduino',self)
        self.readBut.move(150,350)
        self.readBut.clicked.connect(self.readArduino)
        self.sendReadBut = QtGui.QPushButton('Send/read data',self)
        self.sendReadBut.move(280,350)
        self.sendReadBut.clicked.connect(self.sendRead)

        # Table
        self.table = QtGui.QTextBrowser(self)
        self.table.setGeometry(10,60,380,270)

        self.show()
        
    def sendRead(self):
        if not self.is_connected:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")
        else:
            self.senderFun()
            self.readArduino()


    def senderFun(self):
        
        """ Sender helping function """
        
        if not self.is_connected:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")
        else:
            data, ver = QtGui.QInputDialog.getText(self,'Enter data to send','Allowed data types:\n1.Integers\n2.characters\n3.Lists (arrays)')
            if data == "" and ver:
                text = "Nothing Entered, enter data again"
                QtGui.QMessageBox.about(self, "About",text)
                self.senderFun()
            try:
                # If this block does not throw exceptions then data is an int (or can be coerced into an int)
                data = int(data)
                self.passInt(data)
            except:
                # If this block does not throw exceptions then data is a char
                try:
                    verify = ord(data)
                    self.passChar(data)
                except:
                    # Data is a list
                    data = toList(data)
                    self.passArray(data)

    def USBdefault(self):
        self.portt = 'com3'

    def changeUSB2(self):
        """ Change usb port """
        self.portt = 'com2'

    def changeUSB4(self):
        self.portt = 'com4'

    def speedDefault(self):
        self.speedd = 9600

    def changeCSA48(self):
        """ Change speed """
        self.speedd = 4800

    def changeCSA192(self):
        self.speedd = 19200

    def changeCSA576(self):
        self.speedd = 57600

    def showAbout(self):
        
        """ Show about """

        aboutText = "A simple GUI application to send and read data from Arduino Uno.\nCreated by Mic.\nNot for commercial use."
        QtGui.QMessageBox.about(self, "About",aboutText)

    def showHelp(self):

        """ Show help """
        
        helpText = "Some help text which will be provided later,\nor a link to my site, whatever!"
        QtGui.QMessageBox.about(self, "Help", helpText)

    def setupConnection(self):

        """ Setup the connection with Arduino uno """        
        
        try:
            self.uno = Arduino(self.portt,self.speedd)
            self.is_connected = True
            text = "Arduino connected succesfully:\n" + str(self.uno)
            QtGui.QMessageBox.about(self, "Connection status", text)
        except Exception as e:
            text = "Could not connect, please check:\nIs the USB port available?\nIs Arduino uno connected to the USB?\nIs the connection already established?\nException: "+ str(e)
            QtGui.QMessageBox.about(self, "Connection status", text)


    def showConnInfo(self):

        """ Show information on the connection status """        
        
        if self.is_connected:
            data = str(self.uno)
            QtGui.QMessageBox.about(self, "Connection status", data)
        else:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")

    def passChar(self,char):
    
        """ Helper function for sending a character to Arduino """        
        
        if not self.is_connected:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")
        else:
            try:
                self.uno.sendChar(char)
                self.statusBar().showMessage('Character sent succesfully')
                QtGui.QMessageBox.about(self, "Data sent", "Character sent succesfully")
                return True
            except Exception as e:
                text = "Some error occurred, please check connection!\n"+str(e)
                QtGui.QMessageBox.about(self, "Error!", text)

    def passInt(self,integer):
        
        """ Helper function for sending an integer to Arduino """           
        
        if not self.is_connected:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")
        else:
            try:
                self.uno.sendInteger(integer)
                self.statusBar().showMessage('Integer sent succesfully')
                QtGui.QMessageBox.about(self, "Data sent", "Integer sent succesfully")
            except Exception as e:
                text = "Some error occurred, please check connection!\n"+str(e)
                QtGui.QMessageBox.about(self, "Error!", text)

    def passArray(self,data):
        
        """ Helper function for sending an array to Arduino """   
        
        if not self.is_connected:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")
        else:
            try:
                self.uno.sendIntArray(data)
                self.statusBar().showMessage('List sent succesfully')
                QtGui.QMessageBox.about(self, "Data sent", "List sent succesfully")
            except Exception as e:
                text = "Some error occurred, please check connection!\n"+str(e)
                QtGui.QMessageBox.about(self, "Error!", text)

    def readArduino(self):
    
        """ Helper function for reading data from Arduino """           
        
        if not self.is_connected:
            QtGui.QMessageBox.about(self, "Connection status", "Arduino not connected.")
        else:
            try:
                linesToRead = self.numberLines()
                dataRead = self.uno.readData(linesToRead)
                for i in dataRead:
                    self.table.append(i)
            except Exception as e:
                text = "Some error occurred, please check connection!\n"+str(e)
                QtGui.QMessageBox.about(self, "Error!", text)


    def closeC(self):

        """ Helper function for closing connection """           
        
        try:
            self.uno.closeConn()
            self.is_connected = False
            text = "Connection closed succesfully!"
            QtGui.QMessageBox.about(self, "Connection status", text)
        except Exception as e:
            text = "Could not close connection!\n\nIs Arduino even connected? Check it.\nHere is the exception:\n"+ str(e)
            QtGui.QMessageBox.about(self, "Connection status", text)

    def numberLines(self):

        """ Helper function for gathering the number of lines to read """           
        
        nlines, ver = QtGui.QInputDialog.getText(self,'Enter number of lines to read: ','Enter an integer: ')
        try:
            nlines = int(nlines)
            return nlines
        except Exception as e:
            text = "Please enter only numbers"
            QtGui.QMessageBox.about(self, "Only integers allowed", text)
            self.numberLines()
        




#------------------------------------------------------------------------------
# Run the program

def main():
    
    """ MAIN: INITIALIZE THE GUI """  
    
    app = QtGui.QApplication(sys.argv)
    ex = ArduinoGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
