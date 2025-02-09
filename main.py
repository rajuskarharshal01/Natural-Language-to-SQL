from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st


# Initialize the OpenAI Chat model
llm = ChatOpenAI(api_key="Your OpenAI key")


# Function to connect to the MySQL database
def ConnectDatabase(username, port, host, password, database):

     # Construct MySQL URI and use it to initialize SQLDatabase object
    mysql_uri = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    st.session_state.db = SQLDatabase.from_uri(mysql_uri)


# Function to run SQL queries
def runQuery(query):
    return st.session_state.db.run(query) if st.session_state.db else "Please connect to database"


# Function to fetch database schema (tables and columns)
def getDatabaseSchema():
    return st.session_state.db.get_table_info() if st.session_state.db else "please connect to database"


# Function to generate SQL query from the natural language question using LLM (Large Language Model)
def getQueryFromLLM(question):
        
    # Define the template for the LLM prompt
    template = """below is the schema of MYSQL database, please answer user's question in the dorm of SQL query by looking into the schem for best query

    {schema}

    please only provide SQL query and nothing else

    for example:
    question:how many albums we have in the database
    SQL query: SELECT COUNT(*) FROM album;
    question: How many customers are from Brazil in the database ?

    your turn: 
    question: {question}
    SQL query: 


    """
    

    # Initialize prompt and chain the prompt with LLM
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm

    # Invoke the chain with schema and question to get the SQL query
    response = chain.invoke({
        "question": question,
        "schema": getDatabaseSchema()
    })
    return response.content


# Function to generate a response to the query result in natural language
def getResponseForQueryResult(question, query, output):

    # Template to convert SQL query result into natural language
    template2 = """below is the schema of MYSQL database, please answer user's question in the dorm of SQL query by looking into the schem for best query and convert the SQL query into natural language

    {schema}

    please only provide SQL query and nothing else

    for example:
    question:how many albums we have in the database
    SQL query: SELECT COUNT(*) FROM album;
    output: [(347,)]
    Response: There are 347 albums in the database


    your turn to write response in natural language from the given result: 
    question: {question}
    SQL query: {query}
    Output: {output}
    Response: 


    """ 
    # Initialize second prompt and chain it with LLM
    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = prompt2 | llm

    # Invoke the chain with schema, question, query, and output to get the response in natural language
    response = chain2.invoke({
    "question": question,
    "schema": getDatabaseSchema(),
    "query": query,
    "output": output
    })

    return response.content

# Function to capture voice input using speech recognition
import speech_recognition as sr
def capture_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")  # Notify user that voice input is being captured
        try:
            audio = recognizer.listen(source, timeout=5)    # Capture audio input
            query = recognizer.recognize_google(audio)   # Convert audio to text using Google's recognition
            st.success(f"You said: {query}")   # Display the recognized text
            return query          # Return the recognized query text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")    # Handle unrecognized audio
        except sr.RequestError:
            st.error("Error with the Speech Recognition service.")   # Handle errors with speech recognition service
        except Exception as e:
            st.error(f"An error occurred: {e}")     # Handle any other exceptions
        return None
 



# Streamlit UI setup
def get_shareable_link():
    # Replace with your actual Streamlit app's URL
    app_url = "http://localhost:8501/"
    return app_url

# Set up Streamlit page configuration
st.set_page_config(
    page_icon = "🤖",
    page_title = "NL2SQL",
    layout = "centered",
    
)

# Custom styling for social icons
st.markdown(
    """
    <style>
       

        .social-icons img {
            width: 30px; /* Adjust width of icons */
            height: 30px; /* Adjust height of icons */
            margin-right: 10px; /* Space between icons */
            cursor: pointer; /* Pointer cursor for hover effect */
        }
    </style>
    """,
    unsafe_allow_html=True
)



# Display the app title and description
st.title("Natural Language to SQL Interface")
st.write("Chat with your database using natural language. You can also use voice input!")


# Input box for user to enter their question/query
question = st.chat_input('Enter your database query or ask a question.')


# Initialize session state for chat if not already initialized  
if "chat" not in st.session_state:
    st.session_state.chat = []

# Voice Input Button
if st.button("Speak with your Database"):
    voice_query = capture_voice()   # Capture voice input
    if voice_query:
        question = voice_query   # Use voice input as the query


# If a question is provided
if question:

    # Ensure database is connected
    if "db" not in st.session_state:
        st.error('Please connect to database first.')
    else:       
         # Store the user's question in chat history    
        st.session_state.chat.append({
            "role":"user",
            "content":question 
        })


        # Generate SQL query from the question using LLM
        query = getQueryFromLLM(question)
        print(query)

        # Run the query and get the result
        output = runQuery(query)
        print(output)

        # Get the response for the query result in natural language
        response = getResponseForQueryResult(question, query, output)

          # Store the assistant's response in chat history
        st.session_state.chat.append({
            "role":"assistant",
            "content":f"SQL Query: `{query}`\n\nResponse: {response}"
        })
        
# Display the chat history        
for chat in st.session_state.chat:
    st.chat_message(chat['role']).markdown(chat['content'])



# Sidebar for database connection details
with st.sidebar:
    st.title('Database Connection')
    st.text_input(label="Host", key="host", value="localhost")
    st.text_input(label="Port", key="port", value="3306")
    st.text_input(label="Username", key="username", value="root")
    st.text_input(label="Password", key="password", value="", type="password")
    st.text_input(label="Database", key="database", value="chinook")
    connectBtn = st.button("Connect")     # Button to initiate the database connection


# If the connect button is pressed
if connectBtn:
    ConnectDatabase(
        username=st.session_state.username,
        port=st.session_state.port,
        host=st.session_state.host,
        password=st.session_state.password,
        database=st.session_state.database,
    )
    st.success("Database Connected")

with st.sidebar:
    st.title("App Features")
    st.markdown("### Share This App")

    # Display Share Icons
    st.markdown(
        """
        <div class="social-icons">
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://your-streamlit-app-url.com" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" alt="LinkedIn">
            </a>
            <a href="https://www.facebook.com/sharer/sharer.php?u=https://your-streamlit-app-url.com" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/145/145802.png" alt="Facebook">
            </a>
            <a href="https://wa.me/?text=Check%20out%20this%20app:%20https://your-streamlit-app-url.com" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="WhatsApp">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

