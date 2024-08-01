import pandas
import openai
from openai_utility import FilesManager, AssistantManager
import speech_utility
import elevenlabs
from pydub import AudioSegment
from pydub.playback import play
import requests
"""
assistants_info = {
    "Name" :["Name generator","JARVIS"],
    "Instructions" : ["you are name generator","You are a personal assistant like the one on the Iron man movies and marvel comics , you have British accent , you must be technologically well informed and know about different engineering and scientific principles and methods . you must behave just like the jarvis from iron man"],
    "Assistant_ID"  :["asst_CHYj3ppVTKIRN63OgVayai9f","asst_M8DCHGTjgegFy1H6c8c04JUc"],
    "Thread_ID" :["thread_oaCIPHytP4GUZHGDmXIzoFfy","thread_RVXXFHvxa93OUr2ztmrRVlVS"]
}

assitants_list = pandas.DataFrame(assistants_info)
assitants_list.to_csv('Assistants_list.csv', mode='a', index=False, header=True)

file1 = open("Assistant_id.txt", "r")
file2 = open("Thread_id.txt", "r")

thread_id=file2.readline().strip()
print(thread_id)
openai_api_key = "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"
openai_client = openai.OpenAI(api_key=openai_api_key)
files_manager = FilesManager(openai_client)
assistant_manager = AssistantManager(openai_client)

files_df = files_manager.list_files_df()
assistants_df = assistant_manager.list_assistants_df()
print(files_manager.upload_file("Mrs.AshwiniShethResearchPaperonCyberSecurity.pdf"))

data = pandas.read_csv("Assistants_list.csv")
n1 = data[data.Name == "JARVIS"]
instruction = str(n1.Instructions.iloc[0])  # Retrieve the string value from the DataFrame
print(instruction)

from tkinter import *
from tkinter import font

root = Tk()
root.title('Font Families')
fonts=list(font.families())
fonts.sort()

def populate(frame):
    '''Put in the fonts'''
    listnumber = 1
    for item in fonts:
        label = "listlabel" + str(listnumber)
        label = Label(frame,text=item,font=(item, 16)).pack()
        listnumber += 1

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(root, borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

populate(frame)

root.mainloop()

client = openai.OpenAI(api_key="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")
assistant = client.beta.assistants.create(
        name="Advaith",
        # instructions="You are a personal math tutor. Write and run code to answer math questions.",
        instructions="Casual Conversations",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
        model="gpt-3.5-turbo-1106"  # ,  #gpt-4-1106-preview
        # file_ids=

    )
thread = client.beta.threads.create()
data = {
        "Name": ["Advaith"],
        "Instructions":["Casual conversations"] ,
        "Assistat_ID": [assistant.id],
        "Thread_ID": [thread.id]
    }
# Make data frame of above data
df = pandas.DataFrame(data)

# append data frame to CSV file
df.to_csv('Assistants_list.csv', mode='a', index=False, header=False)
print("Done")
"""

"""
elevenlabs.set_api_key("786caecee1209ef2f344680f1a9d1b5c")
audio = elevenlabs.generate(
    text="Hello everyone",
    voice = "Daniel"
)

elevenlabs.play(audio)

"""

#speech_utility.text_to_speech("I am Jarvis")

# openai_api_key = "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"
# openai_client = openai.OpenAI(api_key=openai_api_key)
# files_manager = FilesManager(openai_client)
# print(files_manager.list_files())
import requests
"""
# Define the webhook URL
# webhook_url = 'http://192.168.1.10:8123/api/webhook/-nO-hW1ikD-f8z9eLJWwX3bmY'
# 
# # Define the payload data to be sent to the webhook
# payload = {
#     'key1': 'value1',
#     'key2': 'value2'
# }
# 
# # Send the POST request to the webhook URL with the payload data
# response = requests.post(webhook_url, json=payload)
# 
# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     print("Webhook POST request was successful!")
# else:
#     print("Webhook POST request failed with status code:", response.status_code)

# Import necessary libraries
assistants_info = {
    "Name" :["lights"],
    "Webhook_on"  :["nO-hW1ikD-f8z9eLJWwX3bmY"],
    "Webhook_off"  :["c0suVrQnI6m4NDrE3fi4Q9IO"]
}

device_list = pandas.DataFrame(assistants_info)
device_list.to_csv('device_list.csv', mode='a', index=False, header=True)
"""
