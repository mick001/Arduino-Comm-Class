"""
                     Measuring function. 

 Makes nSamples measurements through an Arduino object
 
 Notes:
 The function loops until it collects the nSamples readings

 This function accepts an object of the Arduino class and if save=True it saves
 the readings into a .txt file in the specified path.
 
 Note that the same number of measurement must be set in the Arduino
 sketch for the program to work properly

"""

def measure(nSamples,arduino,save=False):

    try:
        print('Waiting for measurements...\n')
		
        data = np.array(arduino.readData(nSamples,array=True,Floaters=True))
        
		# Convert microseconds readings into seconds (1 s = 10^6 micro s)
		data = data/1000000
		
        print(str(nSamples) + ' measurements done:',data,'\n')
    except Exception as e:
        print(e)
        
    if save:
        try:
			path = 'C:\\measurements.txt'
            file = open(path,'w')
            for element in data:
                file.write(str(element))
                file.write('\n')
            file.close()
            print('Data saved successfully')
        except Exception as e:
            print(e)

#------------------------------------------------------------------------------
# Run the program and make 1 measurement

measurements = 1

uno = Arduino()

measure(measurements,arduino,save=True)

uno.closeConn()
