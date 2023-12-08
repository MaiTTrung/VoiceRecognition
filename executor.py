import subprocess
import datetime
from playsound import playsound

def say_hello():
    print ("Xin chào anh trung")

def return_time():
    print(datetime.datetime.now().strftime("%H:%M %p"))

def return_date():
    print(datetime.datetime.now().strftime("%Y-%m-%d"))

def play_music():
    soundfile_path = "C:/Users/maith/Desktop/MyVirtualAssistant/music.mp3"
    try: 
        playsound(soundfile_path)
    except :
        print("Lỗi")


def play_game():
    try:
        application_path = "C:/Users/maith/AppData/Local/Programs/Microsoft VS Code/Code.exe"
        subprocess.Popen(application_path)
        print("Khởi động ứng dụng thành công")
    except OSError as e:
        print(e)

#play_music()


