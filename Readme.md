
# Natural Language to SQL Interface with Voice Integration

This project provides a web application that allows users to interact with a MySQL database using natural language. The application converts natural language queries into SQL queries, executes them against the database, and provides the results in a human-readable format. It also includes voice input functionality, allowing users to speak their queries.

## Features

- **Natural Language Processing**: Converts natural language queries into SQL queries using deep learning models.
- **Database Interaction**: Connects to a MySQL database, executes queries, and retrieves results.
- **Voice Input**: Users can ask questions via voice using Google's Speech-to-Text API.
- **Human-readable Responses**: SQL query results are converted into natural language responses.
- **Streamlit Interface**: A simple web-based interface for easy interaction with the database.

## Requirements

Before running the application, make sure you have the following installed:

- Python 3.7 or higher
- Libraries:
  - `streamlit`
  - `speechrecognition` (for voice input)
  - `mysql-connector-python` (for MySQL database interaction)
  - `langchain` (for generating SQL queries using language models)
  - `openai` (for using OpenAI’s language models)

You can install the required dependencies by running the following command:


!pip install streamlit
!pip install speechrecognition
!pip install mysql-connector-python
!pip install langchain
!pip install openai


## API Key
You need an OpenAI API key to use the ChatOpenAI language model for SQL query generation.

Replace the API key in the code with your own:
- llm = ChatOpenAI(api_key="your-openai-api-key")


## MySQL Database setup
You need access to a MySQL database
Modify the database connection details in the Streamlit sidebar with your database credentials:
Host: localhost or your MySQL server address
Port: Default is 3306
Username: Your MySQL username (e.g., root)
Password: Your MySQL password
Database: The name of your database (e.g., chinook)


## Run the application
To run the application, open a terminal, navigate to the project directory, and execute:
- streamlit run app.py


## How to use
1. Connect to Database
In the Streamlit sidebar, enter your MySQL connection details: host, port, username, password, and database name.
Press the "Connect" button to establish a connection to the database.
2. Text-based Queries
Type your natural language question in the input box. For example:
"How many albums are there in the database?"
"Which customers are from Brazil?"
The system will convert your question into an SQL query and fetch the result from the database.
The SQL query and the corresponding natural language response will be displayed below the input box.
3. Voice Input
Press the "Speak with your Database" button to speak your query.
The system will listen to your voice input, convert it into text, generate the SQL query, and retrieve the result from the database.
Example queries you can ask via voice:
"How many albums are in the database?"
"How many customers are from Brazil?"




