# pyinstaller --onefile --paths D:\Personal\PyCharm\ScreenRecorder\venv\Lib\site-packages --noconsole --icon=icon.ico cv_recorder.py
import os
import PySimpleGUI as sg
import time
from datetime import datetime
import pyautogui
import numpy as np
import cv2


IS_RECORDING = False
IS_PAUSED = False
REC_START_TIME = datetime.now()
PAUSED_TIME = 0


# webcam = cv2.VideoCapture(0)  # specifying we will be using the primary camera of our laptop
#
# while True:
#     img = ImageGrab.grab(bbox=(0, 0, width, height)) # Declaring a variable called img and call ImageGrab to take a picture of our screen
#     img_ny = ny.array(img)  # convert our image to a numpy array in order to pass it to open cv
#     img_final = cv2.cvtColor(img_ny, cv2.COLOR_BGR2RGB)  # cv2 will take our image and convert it to RGB color
#     _, frame = webcam.read()  # opening the webcam
#     fr_height, fr_width, _ = frame . shape  # Finding the width, height and shape of our webcam image
#     img_final[0:fr_height, 0: fr_width, :] = frame[0:fr_height, 0: fr_width, :]  # setting the width and height properties
#     cv2.imshow('Section screen capture', img_final)  # Calling cv2 to display our converted image
#
#     final_video.write(img_final)  # Writing our converted image
#     if cv2.waitKey(10) == ord('t'):  # waiting for any key that the user will press. If t is pressed the program terminates.
#         break


class PySCR:
    def __init__(self, window):
        self.window = window
        self.filename = ''
        self.final_video = None
        self.create_recordings_folder()

    def create_recordings_folder(self):
        if not os.path.exists('./Recordings'):
            print("Recordings folder created!")
            os.mkdir('Recordings')

    def start_recording(self):
        global IS_RECORDING, REC_START_TIME, IS_PAUSED, PAUSED_TIME
        REC_START_TIME = datetime.now()
        PAUSED_TIME = 0
        IS_PAUSED = False
        IS_RECORDING = True

        self.filename = f"./Recordings/{REC_START_TIME.strftime('%Y_%b_%d_%H_%M_%S')}_cv.mp4"

        SCREEN_SIZE = tuple(pyautogui.size())
        fps = 12.0
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # cv2.VideoWriter_fourcc(*"XVID")
        self.final_video = cv2.VideoWriter(self.filename, fourcc, fps, SCREEN_SIZE)

        print(f"[+] recording started: {self.filename}")
        frame_count = 0
        process_time = 0
        try:
            while IS_RECORDING:
                sleep_time = (1/fps)-process_time
                if sleep_time > 0:time.sleep(sleep_time)

                if IS_PAUSED:continue

                process_st = datetime.now().timestamp()

                img = pyautogui.screenshot()
                frame = np.array(img)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.final_video.write(frame)

                frame_count += 1
                duration = int(frame_count/fps)

                hours, remainder = divmod(duration, 60 * 60)
                minutes, seconds = divmod(remainder, 60)
                duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                self.window.write_event_value('-DURATION-', duration)
                # self.window['info'].update(f"Resolution: {SCREEN_SIZE[0]}x{SCREEN_SIZE[1]} | FPS:{fps}")

                process_time = datetime.now().timestamp() - process_st
                # print(f"Process time: {process_time:.5f}")

        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            cv2.destroyAllWindows()
            self.final_video.release()

    def stop_recording(self):
        global IS_RECORDING
        if IS_RECORDING:
            print(f"[#] recording stopped: {self.filename}")
            print("Saving recording...")
            IS_RECORDING = False
        try:
            cv2.destroyAllWindows()
            self.final_video.release()
        except:pass
        self.window.write_event_value('-DURATION-', '00:00:00')


if __name__ == '__main__':
    window = sg.Window(
        'PyScreen Recorder (-.-) by Rasel Mahmud © BitByteLab',
        titlebar_icon="icon.ico",
        icon="icon.ico",
        # size=(260, 200),
        no_titlebar=True, alpha_channel=.8, grab_anywhere=True
    ).Layout(
        [
            [sg.Push(), sg.T("PyScreen Recorder [o] by Rasel Mahmud", font='Gabriola 12', text_color='yellow'), sg.Push()],
            [sg.B("Start", key="start", button_color='red', size=(4, 1), expand_x=True),
             sg.B("Pause", key="pause", button_color='gray', size=(8, 1), disabled=True, expand_x=True),
             sg.B("Stop", key="stop", button_color='gray', size=(4, 1), disabled=True, expand_x=True),
             sg.B("Exit", key="Exit", size=(4, 1), expand_x=True)],
            [sg.T("", key="info", text_color='yellow', justification='center')],
            [sg.Push(), sg.T("00:00:00", key="status", font='Consolas 30', expand_x=True), sg.Push()],
        ]
    ).Finalize()

    pyscr = PySCR(window)

    while True:
        event, values = window.read()

        total_seconds = int(datetime.now().timestamp() - REC_START_TIME.timestamp())
        hours, remainder = divmod(total_seconds - PAUSED_TIME, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        print(f'EVENT: {event}\tDuration: {duration}')
        if event == sg.WINDOW_CLOSED or event == sg.WIN_CLOSED or event == 'Exit':
            print("WINDOW_CLOSED > Exit")
            # threading.Thread(target=pyscr.stop_recording, daemon=True).start()
            window.perform_long_operation(pyscr.stop_recording, '-EXIT-')
            # window.write_event_value('-EXIT-', 'exit')
        elif event.startswith('start'):
            window['start'].update(disabled=True, button_color='gray')
            window['stop'].update(disabled=False, button_color='red')
            window['pause'].update(disabled=False, button_color='green')
            # threading.Thread(target=pyscr.start_recording, daemon=True).start()
            window.perform_long_operation(pyscr.start_recording, '-START-')
            # window.write_event_value('-START-', True)
        elif event.startswith('stop'):
            window['start'].update(disabled=False, button_color='red')
            window['stop'].update(disabled=True, button_color='gray')
            window['pause'].update(disabled=True, button_color='gray')
            window.perform_long_operation(pyscr.stop_recording, '-STOP-')
            # threading.Thread(target=pyscr.stop_recording, daemon=True).start()
        elif event.startswith('pause'):
            txt = window['pause'].get_text()
            print(f"Text: {txt}")
            if txt == 'Pause':
                window['pause'].update(text="Resume")
                # threading.Thread(target=pyscr.pause_recording, daemon=True).start()
                # window.perform_long_operation(pyscr.pause_recording, '-PAUSE-')
                IS_PAUSED = True
            elif txt == 'Resume':
                window['pause'].update(text="Pause")
                # threading.Thread(target=pyscr.resume_recording, daemon=True).start()
                # window.perform_long_operation(pyscr.resume_recording, '-RESUME-')
                IS_PAUSED = False

        elif event == '-START-':
            pass
            # threading.Thread(target=get_duration, args=(window,), daemon=True).start()
        elif event == '-DURATION-':
            window['status'].update(values[event])
        elif event == '-EXIT-':
            break

    window.close()
