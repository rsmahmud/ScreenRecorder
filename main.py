from multiprocessing import freeze_support
freeze_support()
import os
import PySimpleGUI as sg
import time
from datetime import datetime
from screen_recorder_sdk import screen_recorder
import threading


IS_RECORDING = False
REC_START_TIME = datetime.now()


def get_duration(window):
    while IS_RECORDING:
        time.sleep(1)
        total_seconds = int(datetime.now().timestamp() - REC_START_TIME.timestamp())
        hours, remainder = divmod(total_seconds, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        window.write_event_value('-DURATION-', duration)
    window.write_event_value('-DURATION-', '00:00:00')


class PySCR:
    def __init__(self):
        self.filename = ''
        self.create_recordings_folder()
        self.init_recorder()

    def create_recordings_folder(self):
        if not os.path.exists('./Recordings'):
            print("Recordings folder created!")
            os.mkdir('Recordings')

    def init_recorder(self):
        try:
            screen_recorder.enable_log()
            params = screen_recorder.RecorderParams()
            screen_recorder.init_resources(params)
        except Exception as e:
            print(f"Could not start!\nClose all Py Screen Windows and run again!\n{str(e)}")
            raise

    def start_recording(self):
        global IS_RECORDING, REC_START_TIME
        REC_START_TIME = datetime.now()
        IS_RECORDING = True

        self.filename = f"Recordings/{REC_START_TIME.strftime('%Y_%b_%d_%H_%M_%S')}.mp4"

        screen_recorder.start_video_recording(
            filename=self.filename,
            frame_rate=30,
            bit_rate=8000000,
            use_hw_transfowrms=True
        )

        print(f"[+] recording started: {self.filename}")

    def stop_recording(self):
        global IS_RECORDING
        if IS_RECORDING:
            print(f"[#] recording stopped: {self.filename}")
            print("Saving recording...")
            screen_recorder.stop_video_recording()
            IS_RECORDING = False


if __name__ == '__main__':
    window = sg.Window(
        'PyScreen Recorder (-.-) by Rasel Mahmud © BitByteLab',
        titlebar_icon="icon.ico",
        icon="icon.ico",
        size=(240, 150),
        no_titlebar=True, alpha_channel=.8, grab_anywhere=True
    ).Layout(
        [
            [sg.T("PyScreen Recorder [ ] by Rasel Mahmud", font='Gabriola 12', text_color='yellow')],
            [sg.B("Start", key="start", button_color='red', size=(8, 2)),
             sg.B("Stop", key="stop", button_color='gray', size=(8, 2), disabled=True),
             sg.B("Exit", key="Exit", size=(4, 2))],
            [sg.T("00:00:00", key="status", size=(30,2), font='Consolas 30', justification='center')],
        ]
    ).Finalize()

    pyscr = PySCR()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == sg.WIN_CLOSED or event == 'Exit':
            print("WINDOW_CLOSED > Exit")
            window.perform_long_operation(pyscr.stop_recording, '-EXIT-')
        elif event.startswith('start'):
            window['start'].update(disabled=True, button_color='gray')
            window['stop'].update(disabled=False, button_color='red')
            window.perform_long_operation(pyscr.start_recording, '-START-')
        elif event.startswith('stop'):
            window['start'].update(disabled=False, button_color='red')
            window['stop'].update(disabled=True, button_color='gray')
            window.perform_long_operation(pyscr.stop_recording, '-STOP-')
        elif event == '-START-':
            threading.Thread(target=get_duration, args=(window,), daemon=True).start()
        elif event == '-DURATION-':
            window['status'].update(values[event])
        elif event == '-EXIT-':
            break

    screen_recorder.free_resources()
    window.close()
