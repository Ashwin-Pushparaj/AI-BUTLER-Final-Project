import speech_recognition
import openai
import time
import tkinter as tk
from tkinter import scrolledtext
import speech_utility
import assistants
from GUI_functions import Functions
# # Initialize the client
# client = openai.OpenAI(api_key="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")
#
# assistant.create_assistant()
#
# # Create a Thread
# thread = client.beta.threads.create()

if __name__ == "__main__":

    root = tk.Tk()
    chatbot_gui = Functions(root)
    root.mainloop()

