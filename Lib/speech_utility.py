import speech_recognition as sr
import elevenlabs
import pyttsx3
from gtts import gTTS
import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
# This module is imported so that we can
# play the converted audio
import os
def speechtotext():
    # create a speech recognition object
    r = sr.Recognizer()

    # open the microphone and start listening
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google's speech recognition API
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error with speech recognition service; {0}".format(e))
    return text

# audio = elevenlabs.generate(
#     text= "Hi , I am Jarvis",
#     voice = 'Rachel',
#     model="eleven_multilingual_v2"
#
# )
#
# elevenlabs.play(audio)

#voices = elevenlabs.voices()
#print(voices)

# Initialize the pyttsx3 engine
# engine = pyttsx3.init()
#
# # Convert text to speech
# engine.say("I love Python for text to speech, and you?")
# engine.runAndWait()

async def text_to_speech(response):
    # VOICES = [
    #     'en-US-GuyNeural',
    #     'en-US-JennyNeural',
    #     'af-ZA-AdriNeural',
    #     'am-ET-MekdesNeural',
    #     'ar-EG-SalmaNeural',
    #     'ar-SA-ZariyahNeural',
    #     # Add other voices as needed
    # ]
    with open("voice.txt",'r') as voice:
        value = voice.read()
    TEXT = response.replace("Assistant:", "").strip()
    VOICE = value
    OUTPUT_FILE = "test.mp3"

    # async def amain():
    #     communicate = edge_tts.Communicate(TEXT, VOICE)
    #     await communicate.save(OUTPUT_FILE)
    #
    # loop = asyncio.get_event_loop_policy().get_event_loop()
    # try:
    #     loop.run_until_complete(amain())
    # finally:
    #     loop.close()
    # audio = AudioSegment.from_mp3("test.mp3")
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

    audio = AudioSegment.from_mp3("test.mp3")
    play(audio)
    # Play the audio
    #play(audio)