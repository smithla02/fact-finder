"""
config.py: Configuration file for setting up environment variables and default values.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Default log level

# OpenAI API configuration
# Check for OPENAI_API_KEY in environment variables, otherwise use st.secrets
OPENAI_API_KEY = (
    os.getenv("OPENAI_API_KEY")
    if os.getenv("OPENAI_API_KEY")
    else st.secrets["OPENAI_API_KEY"]
)

# File paths for topic associations and topics
TOPIC_ASSOCIATIONS_FILE = os.getenv(
    "TOPIC_ASSOCIATIONS_FILE", "data/topic_associations.json"
)
TOPICS_FILE = os.getenv("TOPICS_FILE", "data/topics.json")

# OpenAI model configuration
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")  # Default GPT model

# Facts configuration
MINIMUM_FACTS = 1
MAXIMUM_FACTS = 10
DEFAULT_FACTS = 3

# Topics configuration
TARGET_TOPIC_LENGTH = "1-4 words"
NUM_RELATED_TOPICS = 5

# Response personas
RESPONSE_PERSONAS = [
    "Default",
    "Comedian",
    "History Buff",
    "Super Geek",
    "Cheeky and Clever",
    "Gen Z",
    "Hippie",
    "California Valley Girl",
]
