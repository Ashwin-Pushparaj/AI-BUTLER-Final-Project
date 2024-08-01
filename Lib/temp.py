import openai
import time
import pandas

# Initialize the client
client = openai.OpenAI(api_key="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")

conversation = {}

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Friday",
    #instructions="You are a personal math tutor. Write and run code to answer math questions.",
    instructions="you are a female assistant",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)

# Step 2: Create a Thread
thread = client.beta.threads.create()
data = {
    "Name": ["FRIDAY"],
    "Instructions": ["you are a female assistant"],
    "Assistat_ID": [assistant.id],
    "Thread_ID": [thread.id]
}
# Make data frame of above data
df = pandas.DataFrame(data)

# append data frame to CSV file
df.to_csv('Assistants_list.csv', mode='a', index=False, header=False)

# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    #content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    content="hello"
)

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    #here speech recognition can be used to adress people differently
    instructions=""
)

#print(run.model_dump_json(indent=4))

time.sleep(10)
# Retrieve the run status
run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
)
#print(run_status.model_dump_json(indent=4))

# If run is completed, get messages
if run_status.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

# Loop through messages and print content based on role
for msg in reversed(messages.data):
    role = msg.role
    content = msg.content[0].text.value
    print(f"{role.capitalize()}: {content}")

