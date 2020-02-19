import serial
import struct

ser = serial.Serial("COM13", 115200, timeout=10)  # baud rate = 115200

# set parameter
ser.write(bytes("MessageId = 475\r\n", 'utf-8'))  # 459 = Acc, Gyro, GPS, euler angles, Time, Status, Velocity
print(ser.readline())

ser.write(b'State = 1\r\n')
print(ser.read(3))

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
if MessageId == 475:
    Acc_x = struct.unpack('f', ser.read(4))
    Acc_y = struct.unpack('f', ser.read(4))
    Acc_z = struct.unpack('f', ser.read(4))
    Gyro_x = struct.unpack('f', ser.read(4))
    Gyro_y = struct.unpack('f', ser.read(4))
    Gyro_z = struct.unpack('f', ser.read(4))
    GPS_x = struct.unpack('f', ser.read(4))
    GPS_y = struct.unpack('f', ser.read(4))
    GPS_z = struct.unpack('f', ser.read(4))
    roll = struct.unpack('f', ser.read(4))
    pitch = struct.unpack('f', ser.read(4))
    yaw = struct.unpack('f', ser.read(4))
    Time = struct.unpack('f', ser.read(4))
    Status = int.from_bytes(ser.read(1), byteorder='big')
    Velocity_x = struct.unpack('f', ser.read(4))
    Velocity_y = struct.unpack('f', ser.read(4))
    Velocity_z = struct.unpack('f', ser.read(4))
else:
    print("Incorrect MessageId received")

Checksum = ser.read(2)  # Checksum 2 bytes

ser.write(b'State = 0\r\n')
print(ser.readline())
ser.close()