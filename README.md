# Fine-tuning-LLMs-for-Multi-Agent-Collaboration
Built a swarm-based multi-agent system using LangGraph to integrate fine-tuned LLMs (LLaMA 3.1, Falcon 7B, Mistral 7B, CodeT5). Automated SDLC tasks—code generation, QA, deployment, and documentation—with real-time collaboration, RAG, Airflow, and Snowflake.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for different roles, including Project Management, Software Engineering, QA Testing, Data Engineering, and Deployment.
- **Task Distribution**: Intelligent task routing based on query content.
- **Code Generation**: Automatic Python code generation based on user requirements.
- **SQL Query Processing**: Generate and execute SQL queries on the Snowflake database.
- **Test Case Generation**: Automated generation of test cases for code validation.
- **Documentation Generation**: Automatic documentation for code deployments.
- **GitHub Integration**: Push documentation and project artifacts directly to GitHub.
- **User Authentication**: Secure login system with session management.
- **Responsive UI**: Modern web interface for interacting with the agents.

## 🛠️ Technical Stack

- **Backend**: Flask with Python 3.x
- **AI Models**: Integration with Hugging Face models
- **Database**: Snowflake for SQL operations
- **UI**: HTML, CSS, and JavaScript
- **Authentication**: Flask session management
- **Agent Communication**: LangGraph/LangChain framework
- **Version Control**: GitHub API integration

## 📋 System Architecture

The system follows a modular architecture with the following main components:

### 1. Agent System:
   - **Project Manager**: Breaks down tasks into manageable components.
   - **Software Engineer**: Generates Python code based on requirements.
   - **QA Tester**: Creates test cases for code validation.
   - **Data Engineer**: Generates and executes SQL queries.
   - **Deployment Engineer**: Produces documentation for deployments.

### 2. Core Services:
   - **Swarm Management**: Coordinates communication between agents.
   - **Database Utilities**: Interfaces with Snowflake for query execution.
   - **GitHub Integration**: Pushes documentation to repositories.

### 3. Web Interface:
   - **Authentication**: User registration and login.
   - **Chat Interface**: Real-time communication with agents.
   - **Response Display**: Formatted display of agent responses including code highlighting.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Hugging Face API access
- Snowflake account
- GitHub account with access token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multi-agent-chatbot.git
   cd multi-agent-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following environment variables:
   ```
   # Hugging Face API settings
   HF_API_KEY=your_huggingface_api_key
   
   # Agent model endpoints
   PROJECT_MANAGER_ENDPOINT=your_project_manager_endpoint
   SOFTWARE_ENGINEER_ENDPOINT=your_software_engineer_endpoint
   DATA_ENGINEER_ENDPOINT=your_data_engineer_endpoint
   QA_TESTER_ENDPOINT=your_qa_tester_endpoint
   DEPLOYMENT_ENGINEER_ENDPOINT=your_deployment_engineer_endpoint
   
   # Snowflake configuration
   SF_USER=your_snowflake_username
   SF_PASSWORD=your_snowflake_password
   SF_ACCOUNT=your_snowflake_account
   SF_DATABASE=your_snowflake_database
   SF_SCHEMA=your_snowflake_schema
   SF_WAREHOUSE=your_snowflake_warehouse
   
   # GitHub configuration
   GITHUB_TOKEN=your_github_token
   GITHUB_REPO=your_username/your_repo
   GITHUB_BRANCH=main
   
   # Flask settings
   SECRET_KEY=your_secret_key
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://localhost:5000`

### Deployment to Production

For production deployment, consider:

1. Using a WSGI server like Gunicorn:
   ```bash
   gunicorn -w 4 app:application
   ```

2. Setting up Nginx as a reverse proxy
3. Implementing proper SSL/TLS encryption
4. Setting up monitoring and logging

## 🔧 Usage Examples

### Python Code Generation

Input:
```
I need a Python function to calculate the factorial of a number
```

The system will:
1. Route to the Software Engineer agent
2. Generate the appropriate Python code
3. Optionally route to the QA Tester for test cases
4. Optionally route to the Deployment Engineer for documentation

### SQL Query Generation

Input:
```
Show me the top 5 customers by total order amount
```

The system will:
1. Route to the Data Engineer agent
2. Generate SQL query
3. Execute the query against Snowflake
4. Return formatted results

### Project Planning

Input:
```
I need to build a web scraper for e-commerce sites
```

The system will:
1. Route to the Project Manager agent
2. Break down the task into components
3. Recommend a development approach
4. Optionally route to other agents for implementation details

## 📚 Project Structure

```
multi-agent-chatbot/
├── server/                 # Backend server code
│   ├── agents/             # Agent implementations
│   │   ├── __init__.py     # Package initialization
│   │   ├── project_manager.py
│   │   ├── software_engineer.py
│   │   ├── data_engineer.py
│   │   ├── qa_tester.py
│   │   ├── deployment_engineer.py
│   │   └── huggingface_agent.py
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── database_utils.py
│   │   ├── format_utils.py
│   │   └── github_utils.py
│   └── multi_agent_system.py
├── static/                 # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/              # HTML templates
│   ├── index.html
│   ├── login.html
│   └── register.html
├── .env                    # Environment variables
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🔒 Security Considerations

- All API keys and credentials are stored in environment variables
- User passwords should be hashed in a production environment
- Session management with proper timeout
- Input validation for all user inputs
- SQL injection protection in database utilities
