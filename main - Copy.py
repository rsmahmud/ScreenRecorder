
import os
import PySimpleGUI as sg
import time
import keyboard
from datetime import datetime
from screen_recorder_sdk import screen_recorder
from win10toast import ToastNotifier


# def on_exit(signal_type):
#    print('caught signal:', str(signal_type))
#    raise Exception("Signal caught")
#
# import win32api
# win32api.SetConsoleCtrlHandler(on_exit, True)

# class GracefulKiller:
#     kill_now = False
#     def __init__(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)

#     def exit_gracefully(self, *args):
#         self.kill_now = True


def main():
    toast = ToastNotifier()
    if not os.path.exists('./Recordings'):
        toast.show_toast(
            "Py Screen Recorder",
            "Recordings folder created!",
            duration=5,
        )
        os.mkdir('Recordings')

    try:
        screen_recorder.enable_log()
        params = screen_recorder.RecorderParams()
        screen_recorder.init_resources(params)
    except Exception as e:
        toast.show_toast(
            "Py Screen Recorder",
            f"Could not start!\nClose all Py Screen Windows and run again!\n{str(e)}",
            duration=5,
        )
        raise
    else:
        toast.show_toast(
            "Py Screen Recorder",
            "Press [CTRL+SHIFT+S] to start/stop recording!",
            duration=5,
        )

    # screen_recorder.get_screenshot(5).save('screenshot.png')
    # print('Screenshot taken')

    # killer = GracefulKiller()
    while True:
        # start recording
        try:
            print("Press [CTRL+SHIFT+S] to start/stop recording!")
            keyboard.wait('ctrl+shift+s')
            filename = f"Recordings/{datetime.now().strftime('%Y_%b_%d_%H_%M_%S')}.mp4"

            screen_recorder.start_video_recording(
                filename=filename,
                frame_rate=30,
                bit_rate=8000000,
                use_hw_transfowrms=True
            )

            print(f"[+] recording started: {filename}")
            toast.show_toast(
                "Py Screen Recorder",
                "Recording Started!\nPress [CTRL+SHIFT+S] to stop recording!",
                duration=5,
            )

            # if killer.kill_now:raise Exception("GracefulExit")

            # stop recording
            keyboard.wait('ctrl+shift+s')

            print(f"[#] recording stopped: {filename}")
            toast.show_toast(
                "Py Screen Recorder",
                "Recording Stopped!\nPress [CTRL+SHIFT+S] to start again!",
                duration=5,
            )
            
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print("Saving recording...")
            screen_recorder.stop_video_recording()
            time.sleep(5)


if __name__ == '__main__':
    main()

