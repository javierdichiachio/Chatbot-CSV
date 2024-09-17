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
    
    if 'input_question' not in st.session_state:
        st.session_state['input_question'] = ''
    
    if csv_file is not None and user_api_key:
        llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=user_api_key)
        
        agent = create_csv_agent(llm,csv_file,agent_type="openai-tools",verbose=True, allow_dangerous_code=True)

        user_question = st.text_input("Ask a question about the LPs:", value=st.session_state['input_question'], key='input_question')

        if st.button("Send"):
            if user_question:
                if csv_file and user_api_key:
                    try:
                        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=user_api_key)
                        agent = create_csv_agent(llm, csv_file, agent_type="openai-tools", verbose=True, allow_dangerous_code=True)
                        
                        with st.spinner(text="In progress..."):
                            answer = agent.run(user_question)
                            st.session_state['chat_history'].append((user_question, answer))
                            
                            # Limpiar el campo de pregunta después de enviar
                            st.session_state['input_question'] = ''
                            st.experimental_rerun()  # Actualiza la aplicación para limpiar el campo de texto
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        
        if st.session_state['chat_history']:
            st.write("### Chat History:")
            for question, response in st.session_state['chat_history']:
                st.write(f"**You:** {question}")
                st.write(f"**RebelBot:** {response}")



if __name__ == "__main__":
    main()