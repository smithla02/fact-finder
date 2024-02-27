import json

NUM_RELATED_TOPICS = 5
TARGET_TOPIC_LENGTH = "1-4 words"


def create_fun_facts_prompt(topic, num_fun_facts):
    return f"Give me {num_fun_facts} fun fact(s) about {topic}."


def _get_topic_associations():
    with open("topic_associations.json", "r") as f:
        return json.load(f)


def create_related_topics_prompt(source_topic):
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
