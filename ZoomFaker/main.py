import numpy as np
import cv2, time, pyvirtualcam
import keyboard as kb


frames = []

if __name__ == "__main__":
    with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
        while True:
            print("Starting...")
            cap = cv2.VideoCapture(0)
            if (cap.isOpened()== False):
                print("Error opening video stream or file")
            going = False
            print("Ready to Record...")

            while(cap.isOpened()):
                ret, frame = cap.read()
                frame = RGB_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cam.send(frame)
                if ret == True:
                    if going:
                        frames.append(frame)

                    if kb.is_pressed("b"):
                        if not going:
                            print("Beginning Recording...")
                        going = True
                    elif kb.is_pressed("s"):
                        if going:
                            print("Recording Ended...")
                            break
            cap.release()

            print(f'Using virtual camera: {cam.device}')
            counter = 0
            back_and_forth = False
            adder = 1
            down_flip = False
            restart = False
            while True:
                try:
                    cam.send(frames[(counter if counter >= 0 else 0)])
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(1)
                cam.sleep_until_next_frame()
                counter += adder
                if counter >= len(frames):
                    if not back_and_forth:
                        counter = 0
                    else:
                        adder = -1
                        counter -= 1
                elif counter < 0:
                    adder = 1
                if kb.is_pressed("q"):
                    print("Quitting...")
                    quit()
                elif kb.is_pressed("f"):
                    if not down_flip:
                        down_flip = True
                        back_and_forth = not back_and_forth
                        if not back_and_forth:
                            adder = 1
                elif kb.is_pressed("p"):
                    restart = True
                    break
                elif kb.is_pressed("r"):
                    restart = True
                    frames = []
                    break
                if not kb.is_pressed("f"):
                    down_flip = False
            if restart:
                continue
