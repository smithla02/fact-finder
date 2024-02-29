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

# Database configuration
DATABASE_NAME = os.getenv("DATABASE_NAME", "facts.db")  # Default database name

# OpenAI API configuration
# Check for OPENAI_API_KEY in environment variables, otherwise use st.secrets
OPENAI_API_KEY = (
    os.getenv("OPENAI_API_KEY")
    if os.getenv("OPENAI_API_KEY")
    else st.secrets["OPENAI_API_KEY"]
)

# File paths for topic associations and topics
TOPIC_ASSOCIATIONS_FILE = os.getenv(
    "TOPIC_ASSOCIATIONS_FILE", "topic_associations.json"
)
TOPICS_FILE = os.getenv("TOPICS_FILE", "topics.json")

# OpenAI model configuration
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")  # Default GPT model

# Fun facts configuration
MINIMUM_FUN_FACTS = 1
MAXIMUM_FUN_FACTS = 10
DEFAULT_FUN_FACTS = 3

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

# TODO: Add Fun Fact Categories
# FUN_FACT_CATEGORIES = ['All', 'Nature', 'Internet', 'Business', 'Spooky', 'Psychology',
# 'Movies', 'Love', 'Funny', 'Animals', 'Universe', 'Celebrities', 'For Kids', 'World', 'Science',
# 'Life Hacks', 'Technology', 'Human Body', 'Food', 'Sex', 'United States', 'Trivia', 'Sports',
# 'Language', 'History']
