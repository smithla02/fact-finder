"""
prompts.py: Constructs prompts for querying OpenAI based on the application's needs.
"""

import json
import logging
from config import (
    RESPONSE_PERSONAS,
    NUM_RELATED_TOPICS,
    TARGET_TOPIC_LENGTH,
    TOPIC_ASSOCIATIONS_FILE,
)


def create_persona_prompt(persona):
    """
    Creates a persona-specific prompt for querying OpenAI.
    """
    prompt = ""
    if persona not in RESPONSE_PERSONAS:
        logging.error("Persona not found")
    else:
        if persona == "Default":
            prompt = "You are a helpful assistant that provides fun facts."
        elif persona == "Comedian":
            prompt = "The delivery for each fun fact will be in a joking manner."
        elif persona == "History Buff":
            prompt = "You are a history buff, who looks at fun facts using a history approach."
        elif persona == "Super Geek":
            prompt = (
                "You are a super technical geek, who uses a geeky style of speaking."
            )
        elif persona == "Cheeky and Clever":
            prompt = "You are a cheeky and clever person, who uses a a cheeky and clever style of speaking."
        elif persona == "Gen Z":
            prompt = "You are a Gen Z kid, who uses a typical Gen Z style of speaking, with slang."
        elif persona == "Hippie":
            prompt = "You are a hippie, who uses a typical hippie style of speaking."
        elif persona == "California Valley Girl":
            prompt = (
                "You are a California valley girl, who uses a typical a California "
                "valley girl style of speaking."
            )
    return prompt


def create_facts_prompt(topic, num_facts):
    """
    Creates a prompt for fetching  facts about a specific topic.
    """
    return f"Give me {num_facts} fun fact(s) about {topic}."


def _get_topic_associations():
    """
    Helper function to load topic associations from a file.
    """
    with open(TOPIC_ASSOCIATIONS_FILE, "r") as f:
        return json.load(f)


def create_related_topics_prompt(source_topic):
    """
    Creates a prompt for fetching related topics based on a source topic.
    """
    output = "I will provide some examples of an original topic and related topics."
    for topic, related_topics in _get_topic_associations().items():
        output += f"Original topic: {topic}, Related topics: {related_topics}"

    output += (
        f"Please note the structure of the original topic and related topics. "
        f"The length of each related topic is typically only {TARGET_TOPIC_LENGTH} words long. "
        f"Now please give me {NUM_RELATED_TOPICS} interesting topics that are related "
        f"to the original topic of {source_topic}. "
        f"Each related topic should only be {TARGET_TOPIC_LENGTH} words long. "
        f"Do not give any introduction in your response, "
        f"please directly just give me the related topics in numbered format."
    )
    return output
