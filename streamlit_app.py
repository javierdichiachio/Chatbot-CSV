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
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    if 'user_question' not in st.session_state:
        st.session_state['user_question'] = ''
    
    if csv_file is not None and user_api_key:
        llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=user_api_key)
        
        agent = create_csv_agent(llm,csv_file,agent_type="openai-tools",verbose=True, allow_dangerous_code=True)

        user_question = st.text_input("Ask a question about the LPs:", value=st.session_state['user_question'])

        if user_question:
            with st.spinner(text="In progress..."):
                answer = agent.run(user_question)
                st.session_state.chat_history.append((user_question, answer))
        
        if st.session_state['chat_history']:
            st.write("### Chat History:")
            for question, response in st.session_state['chat_history']:
                st.write(f"**You:** {question}")
                st.write(f"**RebelBot:** {response}")



if __name__ == "__main__":
    main()