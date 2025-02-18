import streamlit as st
from dotenv import dotenv_values
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

config = dotenv_values('.env')
astra_or_chroma = config['ASTRA_OR_CHROMA']
openai_key = config['OPENAI_API_KEY']

### Load Tools #########
if astra_or_chroma == "astra":
    from tools.tools_astra import TotalRevenueReaderTool, ClientSimilarityTool, GetClientInformationTool
    tools = [TotalRevenueReaderTool(), ClientSimilarityTool(), GetClientInformationTool()]
else:
    from tools.tools_chroma import ClientSimilarityTool
    tools = [ClientSimilarityTool()]


### Initialize the LangChain Agent #########
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    ai_prefix='AI',
    k=5,
    return_messages=True
)

llm = ChatOpenAI(
    openai_api_key=openai_key,
    temperature=0,
    model_name="gpt-3.5-turbo"
)

agent = initialize_agent(
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    max_iterations=5,
    verbose=True,
    memory=conversational_memory,
    handle_parsing_errors=True,
    early_stopping_method='generate'
)

# set title
st.title('🏦 BankFlix Chatbot')

# set header
st.header("Welcome dear bank employee!")

user_question = st.text_input('Ask a question here:')
# if the question has more than 5 characters, run the agent
if len(user_question) > 5:
    with st.spinner(text="In progress..."):
        response = agent.run('{}, {}'.format(user_question, user_question))
        st.write(response)

