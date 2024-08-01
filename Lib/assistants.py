import openai
import time
import speech_recognition
import speech_utility
import pandas


def create_assistant(name1 , instruction1):
    # Step 1: Create an Assistant
    client = openai.OpenAI(api_key="<API Key>")
    assistant = client.beta.assistants.create(
        name=name1,
        # instructions="You are a personal math tutor. Write and run code to answer math questions.",
        instructions=instruction1 + "reply in a natural manner as if you are a person,make the conversations as lifelike as possible",
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
        model="gpt-3.5-turbo-1106"  # ,  #gpt-4-0125-preview
        # file_ids=

    )

    thread = client.beta.threads.create()
    vector_store = client.beta.vector_stores.create()
    data = {
        "Name": [name1],
        "Instructions": [instruction1],
        "Assistat_ID": [assistant.id],
        "Thread_ID": [thread.id],
        "Voice":['en-CA-LiamNeural'],
        "Vector_ID": [vector_store.id]

    }
    # Make data frame of above data
    df = pandas.DataFrame(data)

    # append data frame to CSV file
    df.to_csv('Assistants_list.csv', mode='a', index=False, header=False)
    print("Done")
    with open("Name.txt", "w") as name_file:
        name_file.write(name1)
    with open("Assistant_id.txt", "w") as as_id:
        as_id.write(assistant.id)
    with open("Thread_id.txt", "w") as threadid:
        threadid.write(thread.id)
    with open("Vector_id.txt","w") as vid:
        vid.write(vector_store.id)
    print("done")

 #######################################################################################################################

def run_assistant(query,threadid,assistantid):
    client = openai.OpenAI(api_key="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")
    user_query = query

    # Step 3: Add a Message to a Thread
    with open("instruction.txt" ,"r") as inst:
        intruc = inst.readline()
    message = client.beta.threads.messages.create(
        #thread_id=file2.readline().strip(),
        thread_id= threadid,
        role="user",
        #content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
        content=user_query
    )

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
        #thread_id=file2.readline().strip(),
        thread_id=threadid,
        assistant_id=assistantid,
        #here speech recognition can be used to adress people differently
        instructions=intruc+" Please address the user as Ashwin.reply in a natural manner as if you are a person. The user has a premium account.limit the response to 1000 characters.know that you are part of a bigger code which also has a IoT integration , so if you get a query which has something related to controlling a device (like lights) of some sort reply accordingly "
    )

    # time.sleep(10)
    # # Retrieve the run status
    # run_status = client.beta.threads.runs.retrieve(
    #         thread_id=thread.id,
    #         run_id=run.id
    # )

    # If run is completed, get messages
    # if run_status.status == 'completed':
    #     messages = client.beta.threads.messages.list(
    #         thread_id=thread.id
    #     )
    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=threadid,
            run_id = run.id
        )

    messages = client.beta.threads.messages.list(
            thread_id=threadid
        )
    #speech_utility.text_to_speech(messages.data[0].content[0].text.value)
    return messages.data[0].content[0].text.value
########################################################################################################################

def print_conversation(threadid):
    #To print whole conversation Loop through messages and print content based on role
    client = openai.OpenAI(api_key="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")

    messages = client.beta.threads.messages.list(
        thread_id=threadid
    )
    with open("chat_log.txt","a") as file:
        for msg in reversed(messages.data):
            role = msg.role
            content = msg.content[0].text.value
            file.write(f"{role.capitalize()}: {content} \n")
