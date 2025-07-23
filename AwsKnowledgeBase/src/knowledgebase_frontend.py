import streamlit as st
import requests
import json

# API URL (your GET endpoint)
api_url = "https://qlmkqrx9pi.execute-api.us-east-1.amazonaws.com/DEV"

# Streamlit App Layout
st.title("Bedrock Knowledge Base API Interaction")
st.write("Enter your query to interact with the Bedrock Knowledge Base!")

# User input field
user_input = st.text_area("Enter your question:", "")

# Button to trigger the API call
if st.button("Submit"):
    if user_input.strip():
        # Encode the user input to be part of the URL query string
        params = {
            "prompt": user_input
        }
        try:
            # Send GET request with the query string
            response = requests.get(api_url, params=params)
            
            # Check if the API call was successful
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract the body content from the response
                if "body" in response_data:
                    answer = response_data["body"]
                    # Display the answer content in a clean answer box
                    st.subheader("Answer:")
                    st.text_area("Response from Knowledge Base", answer, height=200)
                else:
                    st.warning("No answer found in the response.")
            
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question before submitting.")
