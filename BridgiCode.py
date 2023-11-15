import streamlit as st
import time
from openai import OpenAI

client = OpenAI(api_key='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')
assistantid = 'asst_bLywg5QHHveOLBgE9eBsGmzM'

# Streamlit UI
st.title('BridgiCode')
user_input = st.text_input("Enter your message:")

# Function to interact with OpenAI using threads and runs
def ask_gpt(question):
    try:
        # Create a new thread with initial message
        thread = client.beta.threads.create(
            messages=[f
                {"role": "user", "content": question}
            ]
        )
        thread_id = thread.id

        # Run the thread with your assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistantid
        )

        # Polling for Run status updates
        while True:
            run_update = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_update.status not in ["queued", "in_progress"]:
                break
            time.sleep(0.5)  # Adding a short delay to reduce API calls

        # Retrieve and return the messages after run completion
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Invoke the function and display the response
if st.button("Ask Bridgi"):
    response = ask_gpt(user_input)
    if response:
        for message in response.data:
            if message.role == "assistant":
                st.write(message.content[0].text.value)