import win32com.client as wincl

if __name__ == '__main__':
    while True:
        a = input("Please enter the text you want me to speak out loud")
        if a == 'Quit':
            break
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(a)
