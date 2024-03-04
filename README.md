# Fun Facts Streamlit App

Welcome to the Fun Facts Streamlit App repository. This app fetches and displays fun facts based on user-selected topics and personas, leveraging OpenAI's GPT models for content generation and [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) for data persistence, and [Streamlit](https://github.com/streamlit/streamlit) as a front end.

## Using the deployed app

The app is deployed using Streamlit cloud, and can be accessed here: https://funfacts.streamlit.app/

## Features

- Fetch fun facts from OpenAI based on selected topics and personas.
- Cache fun facts in a SQLite database for quick retrieval.
- User interface built with Streamlit for an interactive experience.

## Project Structure

The project has the following structure:

- `streamlit_app.py`: The main Streamlit application file.
- `database.py`: Contains SQLAlchemy database operations for storing and retrieving fun facts.
- `config.py`: Configuration settings for the application, including environment variables.
- `openai_retrieval.py`: Handles fetching data from OpenAI.
- `prompts.py`: Constructs prompts for querying OpenAI.
- `Dockefile`: Contains information about building a Docker image for the repository.
- `.pre-commit-config.yaml`: Contains linting and formatting commit hooks for maintaining consistency in this repository
- `data/`: Contains information about topics and topic associations.

## Prerequisites

To run in Docker:
- [Docker](https://docs.docker.com/get-docker/)

To run locally:
- Python 3.8+
- pip
- Virtual environment (recommended)
- Docker (for containerization)

### Exporting `OPENAI_API_KEY` as an environment variable

**To run this app in Docker or locally, you must have your own `OPENAI_API_KEY`.**

Instructions for setting up an `OPENAI_API_KEY` can be found [here](https://platform.openai.com/docs/quickstart).

To export your `OPENAI_API_KEY` to your `.zshrc` or `.bashrc` file to have them available for any terminal session, you can use the following commands.

#### Exporting to `.zshrc` or `.bashrc` File:

1. **Exporting the Environment Variable**:
   - For `.zshrc` (Zsh shell):
     ```bash
     echo 'export OPENAI_API_KEY=your_openai_api_key_here' >> ~/.zshrc
     ```
   - For `.bashrc` (Bash shell):
     ```bash
     echo 'export OPENAI_API_KEY=your_openai_api_key_here' >> ~/.bashrc
     ```

2. **Reloading the Shell Configuration**:
   - For Zsh:
     ```bash
     source ~/.zshrc
     ```
   - For Bash:
     ```bash
     source ~/.bashrc
     ```

#### Exporting in a Single Terminal Session:

If you want to export the `OPENAI_API_KEY` in a single terminal session without modifying the shell configuration files, you can do it directly in the terminal:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

This command sets the `OPENAI_API_KEY` environment variable for the current terminal session. Remember that this approach will only persist for the duration of that terminal session.

## Running the App with Docker

To run the Fun Facts Streamlit App using Docker, you can pull the pre-built image from Docker Hub and run it in a container.

### Pulling the Docker Image

Pull the latest version of the Fun Facts Streamlit App image from Docker Hub:

```bash
docker pull smithla02/funfactsapp
```

### Running the Docker Container

To run the Docker container and open in your browser, pass the `OPENAI_API_KEY` as an environment variable and map port 8501 for access:

```bash
docker run -e OPENAI_API_KEY -p 8501:8501 smithla02/funfactsapp & sleep 2 && open http://localhost:8501
```

### Accessing the App

After starting the container, open your web browser and navigate to `http://localhost:8501` to view the app.

### Stopping the Container

To stop the running container, find the container using `docker ps | grep 'funfactsapp'`, then stop it using `docker stop <container_id>`.

## Running the App Locally

### Setting Up the Environment

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment:
   - **Linux/macOS**: `python3 -m venv venv`
   - **Windows**: `py -m venv venv`
4. Activate the virtual environment:
   - **Linux/macOS**: `source venv/bin/activate`
   - **Windows**: `.\venv\Scripts\activate`
5. Install the required dependencies: `pip install -r requirements.txt`

### Running the Streamlit App

With the environment set up and activated, run the Streamlit app using:

```bash
streamlit run streamlit_app.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.
