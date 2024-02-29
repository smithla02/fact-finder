# Fun Facts Streamlit App

Welcome to the Fun Facts Streamlit App repository. This app fetches and displays fun facts based on user-selected topics and personas, leveraging OpenAI's GPT models for content generation and SQLAlchemy for data persistence.

## Using the deployed app

The app is deployed using Streamlit cloud here: https://funfacts.streamlit.app/

## Features

- Fetch fun facts from OpenAI based on selected topics and personas.
- Cache fun facts in a SQLite database for quick retrieval.
- User interface built with Streamlit for an interactive experience.

## Project Structure

- `streamlit_app.py`: The main Streamlit application file.
- `database.py`: Contains SQLAlchemy database operations for storing and retrieving fun facts.
- `config.py`: Configuration settings for the application, including environment variables.
- `openai_retrieval.py`: Handles fetching data from OpenAI.
- `prompts.py`: Constructs prompts for querying OpenAI.
- `.streamlit/secrets.toml`: (Not included in the repository for security reasons) Contains sensitive information like database credentials and API keys.

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## Setting Up the Environment

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment:
   - **Linux/macOS**: `python3 -m venv venv`
   - **Windows**: `py -m venv venv`
4. Activate the virtual environment:
   - **Linux/macOS**: `source venv/bin/activate`
   - **Windows**: `.\venv\Scripts\activate`
5. Install the required dependencies: `pip install -r requirements.txt`

## Running the Streamlit App Locally

With the environment set up and activated, run the Streamlit app using:

```bash
streamlit run streamlit_app.py
```

## Configuring `.streamlit/secrets.toml`

To run the app, you need to create a `.streamlit/secrets.toml` file in the root of your project with your database credentials and OpenAI API key. Here's a template:

```toml
[database]
url = "sqlite:///your_database_path.db"

[openai]
api_key = "your_openai_api_key"
```

Replace `your_database_path.db` with the path to your SQLite database file and `your_openai_api_key` with your actual OpenAI API key.

## Environment Variables

The `config.py` file loads environment variables for configuration. You can set these variables in a `.env` file at the root of the project. Here's an example `.env` file:

```env
LOG_LEVEL=DEBUG
DATABASE_NAME=facts.db
OPENAI_API_KEY=your_openai_api_key
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.
