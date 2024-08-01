import tkinter as tk
from tkinter import scrolledtext, Menu,messagebox
import speech_recognition as sr
import assistants
import pandas
import openai
from openai_utility import FilesManager, AssistantManager

openai_api_key = "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"
openai_client = openai.OpenAI(api_key=openai_api_key)
files_manager = FilesManager(openai_client)
assistant_manager = AssistantManager(openai_client)

class Functions:
    def __init__(self, master):
        self.master = master
        master.title("AI Butler")

        # Dark mode colors
        background_color = "#FFEFDB"
        text_color = "#000000"
        button_color = "#3e3e3e"
        button_text_color = "#FFFFFF"


        master.configure(bg=background_color)

        self.chat_history = ""

        # Display assistant name at the top center
        with open("Name.txt", "r") as name_file:
            assistant_name = name_file.read().strip()
        self.assistant_name_label = tk.Label(master, text=assistant_name, font=("Helvetica Bold", 24), height=5,width=6,bg=background_color,fg=text_color)
        self.assistant_name_label.grid(row=0, column=0, pady=0,sticky="nw")

        self.chat_log = scrolledtext.ScrolledText(master, state='disabled', width=55, height=20, bg=background_color,fg=text_color)
        self.chat_log.grid(row=1, column=0, columnspan=2, padx=2, pady=2,sticky="nsew")

        # Voice Input button
        self.voice_input_button = tk.Button(master, text="Voice Input", command=self.handle_voice_input, width=10,height=4, bg=button_color, fg=button_text_color)
        self.voice_input_button.grid(row=1, column=2, padx=0,pady=0,sticky="sew")

        # User Input Text widget
        self.user_input = tk.Text(master, width=50, height=2, bg=background_color, fg=text_color,font=("Helvetica", 10))
        self.user_input.grid(row=2, column=0, padx=10, pady=0,sticky="nsew",columnspan=2)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.handle_user_input, width=10, bg=button_color,fg=button_text_color)
        self.send_button.grid(row=2, column=2, padx=10, pady=10,sticky="nsew")


        self.settings_button = tk.Menubutton(master, text="Settings", width=10,height=4, bg=button_color, fg=button_text_color)
        self.settings_button.grid(row=1, column=2, padx=10, pady=10, sticky="new")
        self.settings_menu = Menu(self.settings_button, tearoff=0)
        self.settings_button.config(menu=self.settings_menu)

        self.settings_menu.add_command(label="Edit Assistant", command=self.edit_assistant)
        self.settings_menu.add_command(label="Switch Assistants", command=self.switch_assistants)
        self.settings_menu.add_command(label="Create New Assistant", command=self.create_new_assistant)
        self.settings_menu.add_command(label="API Keys", command=self.api_keys)

        # Files button
        self.files_button = tk.Button(master, text="Files", command=self.open_files_window,width=10, height=4,bg=button_color, fg=button_text_color)
        self.files_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.recognizer = sr.Recognizer()


        # Disable resizing of widgets
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

    def handle_user_input(self, event=None):
        user_input_text = self.user_input.get("1.0", tk.END).strip()  # Get text from Text widget
        if user_input_text:
            self.display_message(user_input_text, is_user=True)
            # Call your chatbot logic here and get the response
            bot_response = self.get_bot_response(user_input_text)
            self.display_message(bot_response)
            self.user_input.delete("1.0", tk.END)  # Clear the input area

    def handle_voice_input(self):
        self.display_message("Listening...")
        self.master.update()  # Update the GUI immediately
        self.master.after(10)  # Wait a bit to ensure the message is displayed before capturing audio
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            user_input_text = self.recognizer.recognize_google(audio)
            self.display_message(user_input_text, is_user=True)
            # Call your chatbot logic here and get the response
            bot_response = self.get_bot_response(user_input_text)
            self.display_message(bot_response)
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
        return "Bot: " + assistants.run_assistant(user_input,threadid,assistantid)

    def display_message(self, message, is_user=False):
        self.chat_log.configure(state='normal')
        if is_user:
            self.chat_log.insert(tk.END, "You: " + message + "\n")
        else:
            self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.configure(state='disabled')
        self.chat_log.see(tk.END)

    def edit_assistant(self):
        # Action for "Edit Assistant" menu option
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Assistant")

        # Function to fetch current values from text files
        def fetch_current_values():
            name = ""
            with open("Name.txt", "r") as name_file:
                name_entry.delete(0, tk.END)
                name = name_file.read()
                name_entry.insert(0, name)
            with open("Assistants_list.csv", "r") as instruction_file:
                instruction_entry.delete("1.0", tk.END)
                data = pandas.read_csv("Assistants_list.csv")
                n1 = data[data.Name == name]
                instruction = str(n1.Instructions.iloc[0])  # Retrieve the string value from the DataFrame
                instruction_entry.insert(tk.END, instruction)

        tk.Label(edit_window, text="Name: ").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(edit_window, text="Instruction: ").grid(row=1, column=0, padx=10, pady=10)
        instruction_entry = tk.Text(edit_window, width=40, height=10)
        instruction_entry.grid(row=1, column=1, padx=10, pady=10)

        # Populate entry fields with current values
        fetch_current_values()

        # Save function to save the edited values
        def save_edited_values(name_entry):
            with open("Name.txt", "w") as name_file:
                name_file.write(name_entry.get())


        # Save button to save the edited values and close the window
        save_button = tk.Button(edit_window, text="Save", command=lambda: save_edited_values(name_entry))
        save_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def switch_assistants(self):
        # Action for "Switch Assistants" menu option
        create_window = tk.Toplevel(self.master)
        create_window.title("Switch Assistant")
        tk.Label(create_window, text="Name: ").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(create_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        switch_button = tk.Button(create_window, text="Switch", command=lambda: self.switch(name_entry.get(), create_window))
        switch_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def switch(self, name, window_to_close):
        # create the assistant in openAI playground
        with open("Name.txt", "w") as name_file:
            name_file.write(name)
        with open("Assistant_id.txt", "w") as asid:
             data = pandas.read_csv("Assistants_list.csv")
             nm = data[data.Name == name]
             asid.write(str(nm.Assistant_ID.iloc[0]))
        with open("Thread_id.txt", "w") as thid:
             data = pandas.read_csv("Assistants_list.csv")
             nm = data[data.Name == name]
             thid.write(str(nm.Thread_ID.iloc[0]))
        self.assistant_name_label.config(text = name)
        window_to_close.destroy()


    def create_new_assistant(self):
        create_window = tk.Toplevel(self.master)
        create_window.title("Create New Assistant")

        tk.Label(create_window, text="Name: ").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(create_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(create_window, text="Instruction: ").grid(row=1, column=0, padx=10, pady=10)
        instruction_entry = tk.Text(create_window, width=30, height=10)
        instruction_entry.grid(row=1, column=1, padx=10, pady=10)

        status_label = tk.Label(create_window, text="", fg="green")
        status_label.grid(row=2, columnspan=2)

        def save_and_close():
            nonlocal status_label  # Ensure that status_label is accessed from the outer scope
            self.save_api(name_entry.get(), instruction_entry.get("1.0", tk.END), create_window)
            status_label.config(text="Saved successfully!")  # Provide feedback to the user

        save_button = tk.Button(create_window, text="Save", command=save_and_close)
        save_button.grid(row=2, columnspan=2, padx=10, pady=10)


    def save_assistant(self, name, instruction, window_to_close):
        assistants.create_assistant(name,instruction)  # create the assistant in openAI playground

        window_to_close.destroy()
    def api_keys(self):
        # Action for "API Keys" menu option
        create_window = tk.Toplevel(self.master)
        create_window.title("API Keys")

        tk.Label(create_window, text="OpenAI API: ").grid(row=0, column=0, padx=10, pady=10)
        open_entry = tk.Entry(create_window)
        open_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(create_window, text="ElevenLabs API: ").grid(row=1, column=0, padx=10, pady=10)
        eleven_entry = tk.Entry(create_window)
        eleven_entry.grid(row=1, column=1, padx=10, pady=10)

        status_label = tk.Label(create_window, text="", fg="green")
        status_label.grid(row=2, columnspan=2)

        def save_and_close():
            nonlocal status_label  # Ensure that status_label is accessed from the outer scope
            self.save_api(open_entry.get(), eleven_entry.get(), create_window)
            status_label.config(text="API keys saved successfully!")  # Provide feedback to the user

        save_button = tk.Button(create_window, text="Save", command=save_and_close)
        save_button.grid(row=3, columnspan=2, padx=10, pady=10)

        pass

    def save_api (self,openai_api_key,elevenlabs_api_key,window_to_close):
        with open("api_keys.txt", "w") as f:
            f.write(f"OpenAI API Key: {openai_api_key}\n")
            f.write(f"Elevenlabs API Key: {elevenlabs_api_key}\n")
        # window_to_close.destroy()

    def open_files_window(self):
        create_window = tk.Toplevel(self.master)
        create_window.title("File Upload")

        tk.Label(create_window, text="File name/Path: ").grid(row=0, column=0, padx=10, pady=10)
        file_entry = tk.Entry(create_window)
        file_entry.grid(row=0, column=1, padx=10, pady=10)

        upload_button = tk.Button(create_window, text="Upload", command=lambda:upload_file(file_entry.get()))
        upload_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        status_label = tk.Label(create_window, text="", fg="green")
        status_label.grid(row=2, columnspan=2)

        def upload_file(path):
            file_path = path
            if not file_path:
                status_label.config(text="Enter the Path",fg='red')  # Provide feedback to the user
                return

            try:
                files_manager.upload_file(file_path)
            except FileNotFoundError as e:
                status_label.config(text="Error",fg='red')  # Provide feedback to the user
