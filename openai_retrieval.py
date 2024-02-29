"""
openai_retrieval.py: Handles data retrieval from OpenAI based on given prompts.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, GPT_MODEL
from prompts import (
    create_fun_facts_prompt,
    create_related_topics_prompt,
    create_persona_prompt,
)
import logging
from typing import Tuple, List


def fetch_openai_data(
    topic: str, num_fun_facts: int, persona: str
) -> Tuple[List[str], List[str]]:
    """
    Fetches fun facts and related topics from OpenAI based on the given topic and persona.
    """
    try:
        client = OpenAI()
        OpenAI.api_key = OPENAI_API_KEY
        persona_prompt = create_persona_prompt(persona)
        fun_facts_prompt = create_fun_facts_prompt(topic, num_fun_facts)

        # Fetch fun facts
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": fun_facts_prompt},
            ],
        )

        facts_text = response.choices[0].message.content
        facts = facts_text.strip().split("\n")

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

        related_topics_text = response.choices[0].message.content
        related_topics = related_topics_text.strip().split("\n")

        return facts, related_topics
    except Exception as e:
        logging.error(f"Error fetching data from OpenAI: {e}")
        return ["An exception occurred while fetching fun facts."], [
            "An exception occurred while fetching related topics."
        ]
