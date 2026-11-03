import serial
import time

PORT  = ''
BAUDRATE = 100000

actual_angles = [0,45,90,0]

try:
    pico = serial.Serial(PORT,BAUDRATE)
    time.sleep(2)

    while True:
        com = f"{acutal_angles[0]},{acutal_angles[1]},{acutal_angles[2]},{acutal_angles[3]}\n"

        pico.write(com.encode("ascii"))
        pico.flush()
        print(f"\nActual angles: {actual_angles}")

        in = input("changes: servo_id angle")
        if in = "q":
            break

        data = in.split()

        if len(data) == 2:
            serv_id = int(data[0])
            new_angle = int(data[1])

        if 1 <= serv_id <= 4:
            if 0 <= new_angle <=180:
                actual_angles[serv_id - 1] = new_angle
                else:
                    print("Error: wrong angle")
            else:
                print("Error: wrond servo_id")
        else:
            print("Eror: wrong input")
    except Exception as error:
        print("Connection error")
    finally:
        if 'pico' in locals() and pico.is_open:
            pico.close()



