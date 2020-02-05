import numpy as np
import serial

ser = serial.Serial("COM13", 115200, timeout=10)  # baud rate = 115200

# set parameter
ser.write(bytes("MessageId = 459\r\n", 'utf-8'))  # 459 = Acc, Gyro, GPS, Velocity, Time, Status
print(ser.readline())

ser.write(b'State = 1\r\n')
print(ser.readline())

while True:
    if ser.read() != b'\x3D':  # wait for Preamble 1 byte
        #        print("Preamble not received")
        continue
    # x = ser.read()  # MessageId[1] 1 byte
    # y = ser.read()  # MessageId[2] 1 byte
    # MessageId = (x << 8) | y
    MessageId = int.from_bytes(ser.read(2), byteorder='big')
    if ser.read() != b'\x00':  # Message[3] 1 byte
        print("byte zero not received")
        continue
    break
if MessageId == 459:
    # Data = "Acc, Gyro, GPS, Velocity, Time, Status"
    # a = ser.read(12 + 12 + 12 + 12 + 4 + 1)  # Data 53 bytes
    # Acc_x = ser.read(4)
    # Acc_y = ser.read(4)
    # Acc_z = ser.read(4)
    # Gyro_x = ser.read(4)
    # Gyro_y = ser.read(4)
    # Gyro_z = ser.read(4)
    # GPS_x = ser.read(4)
    # GPS_y = ser.read(4)
    # GPS_z = ser.read(4)
    # Velocity_x = ser.read(4)
    # Velocity_y = ser.read(4)
    # Velocity_z = ser.read(4)
    # Time = ser.read(4)
    # Status = ser.read(1)
    Acc_x = int.from_bytes(ser.read(4), byteorder='big')
    Acc_y = int.from_bytes(ser.read(4), byteorder='big')
    Acc_z = int.from_bytes(ser.read(4), byteorder='big')
    Gyro_x = int.from_bytes(ser.read(4), byteorder='big')
    Gyro_y = int.from_bytes(ser.read(4), byteorder='big')
    Gyro_z = int.from_bytes(ser.read(4), byteorder='big')
    GPS_x = int.from_bytes(ser.read(4), byteorder='big')
    GPS_y = int.from_bytes(ser.read(4), byteorder='big')
    GPS_z = int.from_bytes(ser.read(4), byteorder='big')
    Velocity_x = int.from_bytes(ser.read(4), byteorder='big')
    Velocity_y = int.from_bytes(ser.read(4), byteorder='big')
    Velocity_z = int.from_bytes(ser.read(4), byteorder='big')
    Time = int.from_bytes(ser.read(4), byteorder='big')
    Status = int.from_bytes(ser.read(1), byteorder='big')
else:
    print("Incorrect MessageId received")
# elif MessageId == 211:
#     Data = "Acc, Gyro, Euler, Time, Status"
#     a = str(ser.read(12 + 12 + 12 + 4 + 1))  # Data 41 bytes
# elif MessageId == 199:
#     Data = "Acc, Gyro, Magn, Time, Status"
#     b = str(ser.read(12 + 12 + 12 + 4 + 1))  # Data 41 bytes
# elif MessageId == 248:
#     Data = "Euler, Latitude Longitude Altitude, Pressure, Time, Status"
#     c = str(ser.read(12 + 12 + 4 + 4 + 1))  # Data 33 bytes
Checksum = ser.read(2)  # Checksum 2 bytes

ser.write(b'State = 0\r\n')
print(ser.readline())
ser.close()