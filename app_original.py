from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
import streamlit as st


def main():
    
    # Load the OpenAI API key from the environment variable
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")
    
    user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your openAI API key, sk-",
    type="password")



    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=user_api_key)
        agent = create_csv_agent(llm,csv_file,agent_type="openai-tools",verbose=True, allow_dangerous_code=True)

        user_question = st.text_input("Ask a question about the LPs: ")

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))


if __name__ == "__main__":
    main()