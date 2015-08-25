#------------------------------------------------------------------------------
# Name:        Arduino class module
# Purpose:     
#
# Created:     12/08/2014
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
#------------------------------------------------------------------------------



import serial
import time
import struct

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
        
        # Optional print
        # print(bytes(str(char).encode()))
        
        valueToWrite = bytes(str(char).encode())
        
        try:
            send = self.conn.write(valueToWrite)
            print(
            """
            Data sent succesfully.
            Data sent: %s
            Immediate response: %s
            """ 
            %(char,send))
        except Exception as e:
            print("Some error occurred, here is the exception:",e,sep=" ")


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
            print(e)
        try:
            dataToSend = struct.pack('>B',integer)
            send = self.conn.write(dataToSend)
            if printR:
                print("Sent the integer %s succesfully" %integer)
        except Exception as e:
            print("Some error occurred, here is the exception:",e,sep=" ")

    
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
            print("Some error occurred, here is the exception:",e,sep=" ")

   
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
                print(e)
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
            print("Nothing to return since array = False")


    def closeConn(self):

        """ CLOSE THE USB CONNECTION """
        
        self.conn.close()
        print("Arduino connection to "+str(self.port)+" closed!")
