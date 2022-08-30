# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtCore import QRunnable, Slot, Signal, QObject


import speech_recognition
import pyttsx3


class CarlaSignals(QObject):
    result = Signal(str)
    process = Signal(int)

class CarlaListener(QRunnable):
    def __init__(self):
        super(CarlaListener, self).__init__()
        self.recognizer = speech_recognition.Recognizer()
        self.signals = CarlaSignals()

#Slots#
    @Slot()
    def run(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    print("running...")
                    self.signals.process.emit(1)
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    print("emitting signal")
                    self.signals.process.emit(2)
                    self.signals.result.emit(text)
                    #will send text with signal#
                    break

#            except  speech_recognition.UnknownValueError():
#                self.recognizer = speech_recognition.Recognizer()
#                self.signals.process.emit(3)
#                continue

            except Exception as e:
                print("some error occured")
                print(e)
                self.signals.process.emit(3)
                continue
        self.signals.process.emit(4)
        print("start the function over")
    #_Slots_#

