from openai import OpenAI
from config import OPENAI_API_KEY, GPT_MODEL
from prompts import (
    create_fun_facts_prompt,
    create_related_topics_prompt,
    create_persona_prompt,
)
import logging


def fetch_openai_data(topic, num_fun_facts, persona):
    try:
        client = OpenAI()
        OpenAI.api_key = OPENAI_API_KEY
        persona_prompt = create_persona_prompt(persona)
        user_prompt = create_fun_facts_prompt(topic, num_fun_facts)

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        facts_text = response.choices[0].message.content
        facts = facts_text.strip().split("\n")

        user_prompt = create_related_topics_prompt(topic)

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides related topics similar to a reference topic.",
                },
                {"role": "user", "content": user_prompt},
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
