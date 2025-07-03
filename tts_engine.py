import pyttsx3
import threading
import queue

engine = pyttsx3.init()
engine.setProperty('rate', 150)

voice_queue = queue.Queue()

def tts_worker():
    while True:
        text = voice_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        voice_queue.task_done()

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text):
    voice_queue.put(text)