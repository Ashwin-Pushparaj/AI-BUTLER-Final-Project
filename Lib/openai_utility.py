import os
import pandas as pd
import openai
# display all columns
pd.set_option('display.max_columns', None)


class FilesManager:
    def __init__(self, client):
        self.client = client

    def list_files(self):
        file_list = self.client.files.list()

        if file_list is None:
            return
        output = file_list.data
        file_ids = [file_obj.id for file_obj in output]
        return file_ids

    def list_files_df(self):
        file_list = self.list_files()
        if file_list is None:
            return
        return pd.DataFrame([file.model_dump() for file in file_list])

    def upload_file(self, file_path, purpose='assistants'):
        if not os.path.exists(file_path):
            raise FileExistsError(f'{file_path} not found.')
        response = self.client.files.create(
            purpose=purpose,
            file=open(file_path, 'rb')
        )
        file = open(file_path, 'rb')
        with open("Assistant_id.txt",'r') as asd:
            id = asd.read()
        with open ("Vector_id","r") as vsd:
            vec_id = vsd.read()
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        # file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
        #     vector_store_id=vec_id, files=file
        # )
        # print(file_batch.status)
        # print(file_batch.file_counts)

        assistant = self.client.beta.assistants.update(
            assistant_id=id,
            tool_resources={"file_search": {"vector_store_ids": [vec_id]}},
        )
        return response


class AssistantManager:
    def __init__(self, client):
        self.client = client

    def list_assistants(self):
        assistant_list = self.client.beta.assistants.list()
        if assistant_list is None:
            return
        return assistant_list.data

    def list_assistants_df(self):
        assistant_list = self.list_assistants()
        if assistant_list is None:
            return
        return pd.DataFrame([assistant.model_dump() for assistant in assistant_list])

    def delete_assistant(self, assistant_id):

        # response = self.client.beta.assistants.delete(assistant_id)
        # # Read the CSV file into a DataFrame
        # df = pd.read_csv("Assistants_list.csv")
        #
        # # Remove the rows where the 'Assistant_ID' column matches the given assistant_id
        # df = df[df['Assistant_ID'] != assistant_id]
        #
        # # Write the modified DataFrame back to the CSV file
        # df.to_csv("Assistants_list.csv", index=False)
        # print("deleted")
        return 1
    def update_assistant(self,assistant_id,vec_id,file_id):
        response = self.client.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={"file_search": {"vector_store_ids": [vec_id]}},
        )
        file = self.client.beta.vector_stores.files.create_and_poll(
            vector_store_id=vec_id,
            file_id=file_id
        )
        return response
    def change_model(self,model):
        with open("Assistant_id.txt", 'r') as name:
            id = name.read()
        response = self.client.beta.assistants.update(assistant_id = id ,model = model)

        return response