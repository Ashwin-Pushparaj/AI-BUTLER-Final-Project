import tkinter as tk
import customtkinter as ck
from customtkinter import StringVar
from tkinter import scrolledtext, Menu,messagebox, filedialog
import speech_recognition as sr
import assistants
import pandas
import openai
from openai_utility import FilesManager, AssistantManager
from PIL import Image
from customtkinter import CTkImage
from speech_utility import *
import iot_utility

openai_api_key = "<API KEY>"
openai_client = openai.OpenAI(api_key=openai_api_key)
files_manager = FilesManager(openai_client)
assistant_manager = AssistantManager(openai_client)
class Functions:
    def __init__(self, app):
        # App Frame
        self.app = app
        self.app.geometry("900x600")
        self.app.title("AI Butler")

        self.send_img = Image.open("send_icon.png")
        self.mic_img = Image.open("microphone-black-shape.png")
        #system settings
        ck.set_appearance_mode("dark")
        ck.set_default_color_theme("blue")

        self.recognizer = sr.Recognizer()

        #Adding UI Elements
        with open("Name.txt", "r") as name_file:
            assistant_name = name_file.read().strip()

        self.title = ck.CTkLabel(app,text=assistant_name,font=("Helvetica Bold", 24),height=50,width=100)
        self.title.grid(padx = 100,pady = 10,row = 0,column = 0,sticky = "nsew")

        #Chat log
        self.chat_log = ck.CTkTextbox(app,state = "disabled",corner_radius=16,border_color="#FFCC70",border_width=1,height=400,width=400)
        self.chat_log.grid(padx = 8,pady = 10,row = 1,column = 0,sticky = "nsew")

        with open("Thread_id.txt", "r") as name_file:
            thread_id = name_file.read().strip()
            self.chat_log.configure(state='normal')
            assistants.print_conversation(thread_id)
            with open ("chat_log.txt","r") as file:
                for line in file :
                    self.chat_log.insert(tk.END,line +"\n" )
            self.chat_log.configure(state='disabled')
            self.chat_log.see(tk.END)
            with open("chat_log.txt", "w") as file:
                pass
        #user text input
        self.query = tk.StringVar()
        self.user_input = ck.CTkEntry(app,corner_radius=16,height=50,width=500,font=("Helvetica Bold", 15),placeholder_text='type somethig...',placeholder_text_color="#FFCC70",textvariable=self.query)
        self.user_input.grid(padx = 10,pady = 10,row = 2,column = 0,sticky = "nsew")

        #send button
        self.send_button = ck.CTkButton(app ,width = 2, corner_radius= 32,image=CTkImage(dark_image=self.send_img, light_image=self.send_img),text="",command=self.handle_user_input)
        self.send_button.grid(padx = 10,pady = 10,row = 2,column = 1,sticky = "nsew")

        #Segmented button to switch assistants
        def switch(value):
            # create the assistant in openAI playground
            with open("Name.txt", "w") as name_file:
                name_file.write(value)
            with open("Assistant_id.txt", "w") as asid:
                data = pandas.read_csv("Assistants_list.csv")
                nm = data[data.Name == value]
                asid.write(str(nm.Assistant_ID.iloc[0]))
            with open("Thread_id.txt", "w") as thid:
                data = pandas.read_csv("Assistants_list.csv")
                nm = data[data.Name == value]
                thid.write(str(nm.Thread_ID.iloc[0]))
            with open("instruction.txt", "w") as thid:
                data = pandas.read_csv("Assistants_list.csv")
                nm = data[data.Name == value]
                thid.write(str(nm.Instructions.iloc[0]))
            with open("voice.txt", "w") as thid:
                data = pandas.read_csv("Assistants_list.csv")
                nm = data[data.Name == value]
                thid.write(str(nm.Voice.iloc[0]))
            self.title.configure(text = value)
            self.chat_log.configure(state='normal')
            self.chat_log.delete("1.0", "end")
            with open("Thread_id.txt", "r") as name_file:
                thread_id = name_file.read().strip()
                self.chat_log.configure(state='normal')
                assistants.print_conversation(thread_id)
                with open("chat_log.txt", "r") as file:
                    for line in file:
                        self.chat_log.insert(tk.END, line + "\n")
                self.chat_log.configure(state='disabled')
                self.chat_log.see(tk.END)
                with open("chat_log.txt", "w") as file:
                    pass


        with open("name_list.txt", 'r') as file:
            my_list = file.readlines()
        my_list = [item.strip() for item in my_list]  # Removing newline characters

        self.segemented_button = ck.CTkSegmentedButton(app, values=my_list, command=switch,dynamic_resizing=True,corner_radius=30)
        self.segemented_button.grid(padx = 10,pady = 10,row = 3,column = 0,sticky = "nsew")

        #mic button
        self.mic_button = ck.CTkButton(app ,width = 2,height = 35, corner_radius= 32,image=CTkImage(dark_image=self.mic_img, light_image=self.mic_img),text="",command=self.handle_voice_input)
        self.mic_button.grid(padx = 10,pady = 10,row = 3,column = 1,sticky = "nsew")

        def switch_event():
            print("switch toggled, current value:", self.switch_var.get())

        self.switch_var = ck.StringVar(value="on")
        self.switch = ck.CTkSwitch(app, text="", command=switch_event,variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(padx=10, pady=10, row=3, column=2, sticky="nsew")

        class MyFrame(ck.CTkScrollableFrame):

            def __init__(self, master,parent, **kwargs):
                super().__init__(master, **kwargs)
                self.parent = parent
                # add widgets onto the frame
                self.img = Image.open("upload_3097412.png")
                # self.label = ck.CTkLabel(self,text="Settings",font=("Helvetica Bold", 18))
                # self.label.pack( padx=60)
                self.voices = ['en-CA-ClaraNeural', 'en-CA-LiamNeural','en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-MX-DaliaNeural', 'fr-CA-SylvieNeural', 'fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'ja-JP-NanamiNeural', 'nl-NL-ColetteNeural', 'pt-BR-FranciscaNeural', 'zh-CN-XiaoxiaoNeural', 'zh-CN-YunyangNeural'
]
                self.devices = ck.CTkButton(self, text="Devices", font=("Helvetica Bold", 13),command=self.iot_control)
                self.devices.pack(pady=10)

                self.create_new = ck.CTkButton(self,text="Create new Assistant", font=("Helvetica Bold", 13),command=self.create_new_assistant)
                self.create_new.pack(pady = 10)

                self.files = ck.CTkButton(self,text="File upload", font=("Helvetica Bold", 13) ,command=self.open_files_window)
                self.files.pack()

                self.label = ck.CTkLabel(self, text="Voice :", font=("Helvetica Bold", 13))
                self.label.pack(pady = 10)

                self.combobox = ck.CTkComboBox(self, values=self.voices,command=self.combobox_callback)
                self.combobox.pack()
                with open ("voice.txt",'r') as voice :
                    self.combobox.set(value=voice.read())

                self.model = ck.CTkLabel(self, text="Model :", font=("Helvetica Bold", 13))
                self.model.pack(pady = 10)

                self.model_drop = ck.CTkComboBox(self, values=["gpt-3.5-turbo-1106","gpt-4-0125-preview"], command=self.change_model)
                self.model_drop.pack()

                self.delete = ck.CTkButton(self, text="Remove Assistant", font=("Helvetica Bold", 13), command=self.delete_assistant)
                self.delete.pack(pady = 10)


            def change_model(self,choice):
                assistant_manager.change_model(choice)

            def combobox_callback(self,choice):
                with open ("voice.txt",'w') as voice :
                    voice.write(choice)
                    voice.flush()
                asyncio.run(text_to_speech("Hello, how may I assist you"))#speech_utility.text_to_speech("Hello , how may I assist you")
                with open("Name.txt",'r') as name_file:
                    name = name_file.read()
                    # Read the CSV file into a DataFrame
                    df = pandas.read_csv("Assistants_list.csv")
                    # Locate the row corresponding to the assistant with the specified name
                    mask = df['Name'] == name
                    if mask.any():
                        if df['Voice'].dtype != object:         # Convert the "Voice" column to object type (string) if necessary
                            df['Voice'] = df['Voice'].astype(str)
                        # Update the "Voice" field in that row
                        df.loc[mask, 'Voice'] = choice
                        # Write the updated DataFrame back to the CSV file
                        df.to_csv("Assistants_list.csv", index=False)
                        print(f"Voice for assistant '{name}' changed to '{choice}' successfully.")
                    else:
                        print(f"No assistant found with the name '{name}'.")



            def create_new_assistant(self):
                create_window = ck.CTkToplevel(self.master)
                create_window.title("Create New Assistant")
                create_window.geometry("400x350")
                create_window.lift()

                ck.CTkLabel(create_window, text="Name: ").grid(row=0, column=0, padx=10, pady=10)
                name = tk.StringVar()
                name_entry = ck.CTkEntry(create_window,textvariable=name)
                name_entry.grid(row=0, column=1, padx=10, pady=10)

                ck.CTkLabel(create_window, text="Instruction: ").grid(row=1, column=0, padx=10, pady=10)
                instruction_entry = ck.CTkTextbox(create_window, width=200, height=200)
                instruction_entry.grid(row=1, column=1, padx=10, pady=10)

                def save_and_close():

                    self.save_assistant(name_entry.get(), instruction_entry.get("1.0", tk.END), create_window)

                save_button = ck.CTkButton(create_window, text="Save", command=save_and_close,corner_radius=16)
                save_button.grid(row=2, column = 1, padx=10, pady=10)

            def save_assistant(self, name, instruction, window_to_close):
                with open("name_list.txt", "a") as name_list:
                    name_list.write(f"{name}\n")
                    name_list.flush()
                self.parent.update_segmented_buttons()
                assistants.create_assistant(name, instruction)  # create the assistant in openAI playground
                self.parent.update(name)
                window_to_close.destroy()

            def open_files_window(self):
                create_window = ck.CTkToplevel(self.master)
                create_window.title("File Upload")
                create_window.geometry("400x200")
                create_window.lift
                create_window.focus_set()

                ck.CTkLabel(create_window, text="File name/Path: ").grid(row=0, column=0, padx=10, pady=10)
                file_entry = ck.CTkEntry(create_window)
                file_entry.grid(row=0, column=1, padx=10, pady=10)

                upload_button = ck.CTkButton(create_window, text="Upload", command=lambda: upload_file(file_entry.get()))
                upload_button.grid(row=1, column=1, padx=10, pady=10)

                def open_file_dialog():
                    # Open a file dialog and get the selected file path
                    file_path = filedialog.askopenfilename()
                    # Display the selected file path in a label or print it
                    file_entry.insert(index=0,string=file_path)

                explore = ck.CTkButton(create_window, text="",command=lambda:open_file_dialog() ,height=30,width =30,image=CTkImage(dark_image=self.img, light_image=self.img))
                explore.grid(row=1, column=2, padx=10, pady=10)

                status_label = ck.CTkLabel(create_window, text="")
                status_label.grid(row=2, column = 1)

                def upload_file(path):
                    file_path = path
                    if not file_path:
                        status_label.configure(text="Enter the Path")  # Provide feedback to the user
                        return

                    try:
                        files_manager.upload_file(file_path)
                    except FileNotFoundError as e:
                        status_label.configure(text="")  # Provide feedback to the user
                    with open("Assistant_id.txt",'r') as name :
                        id = name.read()
                        file_list = files_manager.list_files()
                        file_id = file_list[0]
                    with open ("Vector_id.txt","r") as vc:
                        vecid = vc.read()
                        assistant_manager.update_assistant(id,vecid,file_id)

            def iot_control(self):
                root_new = ck.CTk()
                iot_gui = iot_utility.Functions_iot(root_new)
                root_new.mainloop()

            def delete_assistant(self):
                create_window = ck.CTkToplevel(self.master)
                create_window.title("File Upload")
                create_window.geometry("400x200")
                create_window.lift()

                ck.CTkLabel(create_window, text="Do you want to permenently delete this assistant").pack()

                def delete():
                    print("delete1")
                    with open("Assistant_id.txt", "r") as as_file:
                        as_id = as_file.read()
                    assistant_manager.delete_assistant(as_id)
                    print("delete1")
                    with open ("Name.txt","r") as name_file:
                        name = name_file.read()
                    with open("name_list.txt", 'r') as file:
                        my_list = file.readlines()
                    my_list = [item.strip() for item in my_list ]
                    my_list.remove(name)
                    print(my_list)
                    with open("name_list.txt" , "w") as file:
                        for item in my_list:
                            file.write(item+"\n")

                    self.parent.update_segmented_buttons()
                    self.parent.update(my_list[0])

                button = ck.CTkButton(create_window, text="Delete", command=delete).pack()




        self.my_frame = MyFrame(master=app,parent = self,border_color="#8B8378",border_width=5,corner_radius=16,height=250,width = 150)
        self.my_frame.grid(row=1, column=2, padx=10, pady=10,sticky ="ew")
        app.columnconfigure(0, weight=1)
        app.rowconfigure(0, weight=1)


    def update_segmented_buttons(self):
        with open("name_list.txt", 'r') as file:
            my_list = file.readlines()
            file.flush()
        my_list = [item.strip() for item in my_list]  # Removing newline characters
        self.segemented_button.configure(values=my_list)
    def handle_user_input(self,event = None):
        user_input_text = self.user_input.get().strip()  # Get text from Text widget

        if user_input_text:

            self.display_message(user_input_text, is_user=True)
            # Call your chatbot logic here and get the response
            status,response = iot_utility.iot_handle(user_input_text)
            if status == 1:
                self.display_message(response)
                self.user_input.delete(0, 'end')
                self.app.update()
                if self.switch_var.get() == "on":
                    asyncio.run(text_to_speech(response))  # speech_utility.text_to_speech(response)
                return

            bot_response = self.get_bot_response(user_input_text)
            self.display_message(bot_response)
            self.user_input.delete(0,'end')
            self.app.update()
            if self.switch_var.get() == "on":
                asyncio.run(text_to_speech(bot_response))#speech_utility.text_to_speech(bot_response)


    def handle_voice_input(self):
            self.display_message("Listening...")
            self.app.update()  # Update the GUI immediately
            self.app.after(10)  # Wait a bit to ensure the message is displayed before capturing audio
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            try:
                user_input_text = self.recognizer.recognize_google(audio)
                self.display_message(user_input_text, is_user=True)
                # Call your chatbot logic here and get the response
                status, response = iot_utility.iot_handle(user_input_text)
                if status == 1:
                    self.display_message(response)
                    self.user_input.delete(0, 'end')
                    self.app.update()
                    if self.switch_var.get() == "on":
                        asyncio.run(text_to_speech(response))  # speech_utility.text_to_speech(response)
                    return
                bot_response = self.get_bot_response(user_input_text)

                self.display_message(bot_response)
                self.app.update()
                if self.switch_var.get() == "on":
                    asyncio.run(text_to_speech(bot_response))  # speech_utility.text_to_speech(bot_response)

            except sr.UnknownValueError:
                self.display_message("Could not understand audio")
            except sr.RequestError as e:
                self.display_message("Error fetching results; {0}".format(e))
    def get_bot_response(self, user_input):
            # Here you can implement your chatbot logic
            file1 = open("Assistant_id.txt", "r")
            file2 = open("Thread_id.txt", "r")
            threadid = file2.readline().strip()
            assistantid = file1.readline().strip()
            return "Assistant: " + assistants.run_assistant(user_input,threadid,assistantid)

    def display_message(self, message, is_user=False):
            self.chat_log.configure(state='normal')
            if is_user:
                self.chat_log.insert(tk.END, "User: " + message + "\n\n")
            else:
                self.chat_log.insert(tk.END, message + "\n\n")
            self.chat_log.configure(state='disabled')
            self.chat_log.see(tk.END)

    def update(self,value):
        # create the assistant in openAI playground
        with open("Name.txt", "w") as name_file:
            name_file.write(value)
            name_file.flush()
        with open("Assistant_id.txt", "w") as asid:
            data = pandas.read_csv("Assistants_list.csv")
            nm = data[data.Name == value]
            asid.write(str(nm.Assistant_ID.iloc[0]))
            asid.flush()
        with open("Thread_id.txt", "w") as thid:
            data = pandas.read_csv("Assistants_list.csv")
            nm = data[data.Name == value]
            thid.write(str(nm.Thread_ID.iloc[0]))
            thid.flush()
        with open("instruction.txt", "w") as thid:
            data = pandas.read_csv("Assistants_list.csv")
            nm = data[data.Name == value]
            thid.write(str(nm.Instructions.iloc[0]))
            thid.flush()
        with open("voice.txt", "w") as thid:
            data = pandas.read_csv("Assistants_list.csv")
            nm = data[data.Name == value]
            thid.write(str(nm.Voice.iloc[0]))
            thid.flush()

        with open("Vector_id.txt", "w") as thid:
            data = pandas.read_csv("Assistants_list.csv")
            nm = data[data.Name == value]
            thid.write(str(nm.Vector_ID.iloc[0]))
            thid.flush()
        self.title.configure(text=value)


if __name__ == "__main__":

    root = ck.CTk()
    chatbot_gui = Functions(root)
    root.mainloop()