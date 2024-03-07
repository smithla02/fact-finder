"""
openai_retrieval.py: Handles data retrieval from OpenAI based on given prompts.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, GPT_MODEL
from prompts import (
    create_facts_prompt,
    create_related_topics_prompt,
    create_persona_prompt,
)
import logging
from typing import List, Tuple


def process_response(response: dict) -> List[str]:
    """
    Processes the response from OpenAI and returns the output as a list of strings.
    """
    output_text = response.choices[0].message.content
    output = output_text.strip().split("\n")
    return output


def fetch_facts(client: OpenAI, topic: str, persona: str, num_facts: int) -> List[str]:
    """
    Fetches facts from OpenAI based on the given topic and persona.
    """
    try:
        persona_prompt = create_persona_prompt(persona)
        facts_prompt = create_facts_prompt(topic, num_facts)

        # Fetch facts
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": facts_prompt},
            ],
        )

        facts = process_response(response)
        return facts
    except Exception as e:
        logging.error(f"Error fetching facts from OpenAI: {e}")
        return ["An exception occurred while fetching facts."]


def fetch_related_topics(client: OpenAI, topic: str) -> List[str]:
    """
    Fetches related topics from OpenAI based on the given topic.
    """
    try:
        related_topics_prompt = create_related_topics_prompt(topic)

        # Fetch related topics
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides related topics similar to a reference topic.",
                },
                {"role": "user", "content": related_topics_prompt},
            ],
        )

        related_topics = process_response(response)
        return related_topics
    except Exception as e:
        logging.error(f"Error fetching related topics from OpenAI: {e}")
        return ["An exception occurred while fetching related topics."]


def fetch_openai_data(
    topic: str, persona: str, num_facts: int
) -> Tuple[List[str], List[str]]:
    """
    Fetches facts and related topics from OpenAI based on the given topic and persona.
    """
    try:
        client = OpenAI()
        OpenAI.api_key = OPENAI_API_KEY
        facts = fetch_facts(client, topic, persona, num_facts)
        related_topics = fetch_related_topics(client, topic)
        return facts, related_topics
    except Exception as e:
        logging.error(f"Error fetching data from OpenAI: {e}")
        return ["An exception occurred while fetching facts."], [
            "An exception occurred while fetching related topics."
        ]
