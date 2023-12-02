import serial
# Define the serial port and baud rate
uid=''
cv=0
ci=0
dv=0
di=0
iv=0
ii=0     
ser = serial.Serial('COM13', 9600)  # Update 'COM1' with your specific port and 9600 with your baud rate
def read_serial_data(serial_port):
    try:
        while True:
            # Read a line from the serial port
            line = serial_port.readline().decode('utf-8').strip()
            
            # Print the received data
            print(f"Received: {line}")
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
        
            # Print the received data
            print(f"Received: {line}")
            parts = line.split(':')
            label = parts[0].strip()
            value = parts[1].strip()
            if(label =='uid'):
                uid = value
                print(f"UID:{uid}")
            elif(label == 'cv'):
                cv=float(value)
                print(f"cv:{cv}")
            elif(label=='ci'):
                ci =float(value)
                print(f"ci:{ci}")
            elif(label=='dv'):
                dv =float(value)
                print(f"dv:{dv}")
            elif(label=='di'):
                di =float(value)
                print(f"di:{di}")
            elif(label=='iv'):
                iv=float(value)
                print(f"iv:{iv}")
            elif(label=='ii'):
                ii =float(value)
                print(f"ii:{ii}")
            elif(label=='show'):
                pass
            elif(label=="start"):
                pass
            # Check if the user wants to stop
           # user_input = input("Enter 'stop' to close the serial port: ")
           # if user_input.lower() == 'stop':
             #   break

    finally:
        # Close the serial port when the loop is terminated
        serial_port.close()
        print("Serial port closed.")

def main():
    # Define the serial port and baud rate

    
    try:
        read_serial_data(ser)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the serial port is closed even in case of an exception
        ser.close()

if __name__ == "__main__":
    main()