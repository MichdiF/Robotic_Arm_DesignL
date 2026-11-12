import serial
import time

PORT  = ""
BAUDRATE = 100000

actual_angles = [0,45,90,0]

def send_angles(pico):
    com = ",".join(map(str, actual_angles)) + "\n"
    pico.write(com.encode("ascii"))
    pico.flush()
    print(f"Actual angles: {actual_angles}")

try:
    pico = serial.Serial(PORT,BAUDRATE, timeout=1)
    time.sleep(2)

    send_angles(pico)
    
    while True:
        user_in = input("changes: (servo_id angle, q = quit): ").strip
        if user_in.lower() == "q":
            break
         data = user_in.split()

        if len(data) != 2:
            print(" Error: wrong input")
            continue
        try:
            serv_id = int(data[0])
            new_angle = int(data[1])
        except ValueError:
            print("Error: not integers")
            continue
        if not 1 <= serv_id <= 4:
            print("Error: wrong servo_id")
            continue
        if not 0 <= new_angle <= 180:
            print("Error: wrond angle")
            continue

        actual_angles[serv_id - 1] = new_angle
        send_angles(pico)
        
except Exception as error:
    print("Connection error")
finally:
    if "pico" in locals() and pico.is_open:
            pico.close()



