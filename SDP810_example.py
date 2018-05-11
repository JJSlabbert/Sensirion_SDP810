#Reading the Sensirion SDP810 125PA (or 500PA will need modification) sensor
#Dev by JJ Slabbert
#Code tested with Python 2.7
#Run sudo i2cdetect -y 1 in the terminal, to see if the sensor is connected. it will show address 25
#Check the datasheet at https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/0_Datasheets/Differential_Pressure/Sensirion_Differential_Pressure_Sensors_SDP8xx_Digital_Datasheet.pdf
#The sensor i2c address is 0x25 (Not user Programable).
#I have no formal electronics, physics or programing education, code should be tested before critical applications

import smbus
import time

bus=smbus.SMBus(1) #The default i2c bus
address=0x25
bus.write_i2c_block_data(address, 0x3F, [0xF9]) #Stop any cont measurement of the sensor
time.sleep(0.8)

#Start Continuous Measurement (5.3.1 in Data sheet)
print ("(Start Continuous Measurement (5.3.1 in Data sheet)")

##Command code (Hex)        Temperature compensation            Averaging
##0x3603                    Mass flow                           Average  till read
##0x3608                    Mass flow None                      Update rate 0.5ms
##0x3615                    Differential pressure               Average till read
##0x361E                    Differential pressure None          Update rate 0.5ms

# We will use command code 0x3615
#the smbus write_i2c_block_data function have 3 arguments, addr=the i2c address, cmd and [val]. cmd and val is derived from the Command code in Hex
#We will take 5 readings now
bus.write_i2c_block_data(address, 0x36, [0X03])
print ("Taking 5 readings of 9 bites each. See table in section 5.3.1 of datasheet for meaning of each bite")
for x in range (0, 5):    
    time.sleep(2)
    reading=bus.read_i2c_block_data(address,0,9)
    print (reading)


#We will now take 5 Diffirential Presure readings
print("We will now take 5 Diffirential Pressure readings, Play around, increase the number of readings, blow a fan on throught the pipes")
for x in range (0, 5):    
    time.sleep(2)
    reading=bus.read_i2c_block_data(address,0,9)
    pressure_value=reading[0]+float(reading[1])/255
    if pressure_value>=0 and pressure_value<128:
        diffirential_pressure=pressure_value*240/256 #scale factor adjustment
    elif pressure_value>128 and pressure_value<256:
        diffirential_pressure=-(256-pressure_value)*240/256 #scale factor adjustment
    elif pressure_value==256 or pressure_value==128:
        diffirential_pressure=99999999 #Out of range
    print("Diffirential Pressure: "+str(diffirential_pressure)+" PA")

#We will now take 5 Temperature readings
print("We will now take 5 Temperature readings, Play around, increase the number of readings, Blow a hair dryer on it.")
for x in range (0, 5):    
    time.sleep(2)
    reading=bus.read_i2c_block_data(address,0,9)
    temp_value=reading[3]+float(reading[4])/255
    if temp_value>=0 and temp_value<=100:
        temperature=temp_value*255/200 #scale factor adjustment
    if temp_value<=256 and temp_value>=200:
        temperature=-(256-temp_value)*255/200 #scale factor adjustment
    print("Temperature: "+str(temperature)+" Degrees Celcius")
    
    
    
