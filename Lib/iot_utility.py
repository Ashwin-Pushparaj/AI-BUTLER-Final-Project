import requests
import GUI
import openai
import tkinter as tk
import customtkinter as ck
import iot_utility
import csv
import pandas

class Functions_iot:
    def __init__(self, app):
        self.app = app
        self.app.geometry("400x400")
        self.app.title("IoT control")

        # Add UI elements for device management
        names = []
        with open("device_list.csv",'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                names.append(row['Name'])
        print(names)
        def switch(value):
            print(value)
            with open("device_list.csv","r") as csvfile:
                reader = csv.DictReader(csvfile)
                df = pandas.read_csv("device_list.csv")
                mask = df['Name'] == value
                nm = df[df.Name == value]
                (str(nm.Webhook_on.iloc[0]))
                webhook_on = (str(nm.Webhook_on.iloc[0]))
                webhook_off = (str(nm.Webhook_off.iloc[0]))
                status = row['Status']
                if status == '0':
                    self.turn_on(webhook_on)
                    if df['Status'].dtype != object:  # Convert the "Status" column to object type (string) if necessary
                        df['Status'] = df['Status'].astype(str)
                    df.loc[mask, 'Status'] = '1'
                    df.to_csv("device_list.csv", index=False)
                    status = '1'
                    csvfile.flush()
                else:
                    self.turn_off(webhook_off)
                    if df['Status'].dtype != object:  # Convert the "Status" column to object type (string) if necessary
                        df['Status'] = df['Status'].astype(str)
                    df.loc[mask, 'Status'] = '0'
                    df.to_csv("device_list.csv", index=False)
                    status = '0'
                    csvfile.flush()
                csvfile.flush()



        self.segemented_button = ck.CTkSegmentedButton(app, values=names, command=switch, dynamic_resizing=True,corner_radius=30)
        self.segemented_button.grid(padx=10, pady=10, row=3, column=0, sticky="nsew")

        self.add_device_label = ck.CTkLabel(app, text="Add Device", font=("Helvetica Bold", 18))
        self.add_device_label.grid(row=4, column=0, padx=10, pady=10)

        self.device_name_label = ck.CTkLabel(app, text="Device Name:")
        self.device_name_label.grid(row=5, column=0, padx=10, pady=5)
        self.device_name_entry = ck.CTkEntry(app)
        self.device_name_entry.grid(row=5, column=1, padx=10, pady=5)

        self.webhook_on_label = ck.CTkLabel(app, text="Webhook ID(ON):")
        self.webhook_on_label.grid(row=6, column=0, padx=10, pady=5)
        self.webhook_on_entry = ck.CTkEntry(app)
        self.webhook_on_entry.grid(row=6, column=1, padx=10, pady=5)

        self.webhook_off_label = ck.CTkLabel(app, text="Webhook ID(OFF):")
        self.webhook_off_label.grid(row=7, column=0, padx=10, pady=5)
        self.webhook_off_entry = ck.CTkEntry(app)
        self.webhook_off_entry.grid(row=7, column=1, padx=10, pady=5)

        self.add_device_button = ck.CTkButton(app, text="Add Device", command=self.add_device)
        self.add_device_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)


    def add_device(self):
        device_name = self.device_name_entry.get()
        webhook_on = self.webhook_on_entry.get()
        webhook_off = self.webhook_off_entry.get()
        if device_name and webhook_on and webhook_off:
            data = {
                "Name": [device_name],
                "Webhook_on": [webhook_on],
                "Webhook_off": [webhook_off],
                "Status": ['0'],
            }
            # Make data frame of above data
            df = pandas.DataFrame(data)

            # append data frame to CSV file
            df.to_csv("device_list.csv", mode='a', index=False, header=False)

    def create_device_control(self, device_name):
        # Create UI elements for controlling the device
        device_control_label = ck.CTkLabel(self.app, text=device_name, font=("Helvetica Bold", 14))
        device_control_label.grid(row=len(self.device_info) + 8, column=0, padx=10, pady=5)

        # Example: Create a button to turn the device on
        on_button = ck.CTkButton(self.app, text="Turn On",
                                 command=lambda: self.handle_device_control(device_name, "on"))
        on_button.grid(row=len(self.device_info) + 8, column=1, padx=10, pady=5)

        # Example: Create a button to turn the device off
        off_button = ck.CTkButton(self.app, text="Turn Off",
                                  command=lambda: self.handle_device_control(device_name, "off"))
        off_button.grid(row=len(self.device_info) + 8, column=2, padx=10, pady=5)

    def handle_device_control(self, device_name, action):
        webhook_id = self.device_info.get(device_name)
        if webhook_id:
            # Call the function to control the device using the provided webhook ID
            status, response = iot_utility.iot_handle(f"{action} {device_name}")
            if status == 1:
                # Display feedback to the user (optional)
                print(response)
        else:
            print(f"No webhook ID found for device '{device_name}'.")

    def turn_on(self,id):

        # Define the webhook URL
        webhook_url = 'http://192.168.43.206:8123/api/webhook/-'+id

        # Define the payload data to be sent to the webhook
        payload = {
            'key1': 'value1',
            'key2': 'value2'
        }

        # Send the POST request to the webhook URL with the payload data
        response = requests.post(webhook_url, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Webhook POST request was successful!")
        else:
            print("Webhook POST request failed with status code:", response.status_code)

    def turn_off(self,id):


        # Define the webhook URL
        webhook_url = 'http://192.168.43.206:8123/api/webhook/-'+id

        # Define the payload data to be sent to the webhook
        payload = {
            'key1': 'value1',
            'key2': 'value2'
        }

        # Send the POST request to the webhook URL with the payload data
        response = requests.post(webhook_url, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Webhook POST request was successful!")
        else:
            print("Webhook POST request failed with status code:", response.status_code)




def iot_handle(query):
    if 'turn on' in query:
        with open("device_list.csv",'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['Name'])
                if row['Name'] in query:
                    print(row["Name"])
                    webhook_on = row['Webhook_on']
                    turn_on(webhook_on)
                    break
        return 1,"Lights have been turned on"

    elif 'turn off' in query:
        with open("device_list.csv",'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['Name'])
                if row['Name'] in query:
                    print(row["Name"])
                    webhook_off = row['Webhook_off']
                    turn_off(webhook_off)
                    break
        return  1,"Lights have been turned off"
    else :
        return 0,''


def turn_off(id):


    # Define the webhook URL
    webhook_url = 'http://192.168.43.206:8123/api/webhook/-'+id

    # Define the payload data to be sent to the webhook
    payload = {
        'key1': 'value1',
        'key2': 'value2'
    }

    # Send the POST request to the webhook URL with the payload data
    response = requests.post(webhook_url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Webhook POST request was successful!")
    else:
        print("Webhook POST request failed with status code:", response.status_code)

def turn_on(id):


    # Define the webhook URL
    webhook_url = 'http://192.168.43.206:8123/api/webhook/-'+id

    # Define the payload data to be sent to the webhook
    payload = {
        'key1': 'value1',
        'key2': 'value2'
    }

    # Send the POST request to the webhook URL with the payload data
    response = requests.post(webhook_url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Webhook POST request was successful!")
    else:
        print("Webhook POST request failed with status code:", response.status_code)