from sqlalchemy import Table, Column, String, MetaData, select, and_
import streamlit as st
import json
import logging

# Assuming the connection name 'facts_db' is defined in your .streamlit/secrets.toml
conn = st.connection("facts_db", type="sql")

metadata = MetaData()
facts_table = Table(
    "facts",
    metadata,
    Column("topic", String, primary_key=True),
    Column("persona", String, primary_key=True),
    Column("facts", String),
    Column("related_topics", String),
)


def standardize_primary_key(topic, persona):
    return str.lower(topic), str.lower(persona)


def save_facts_to_db(topic, persona, facts, related_topics):
    try:
        # Use the connection's managed session for database operations
        with conn.session as session:
            # Assuming facts_table is reflected or otherwise available
            topic, persona = standardize_primary_key(topic, persona)
            existing_entry = (
                session.query(facts_table)
                .filter_by(topic=topic, persona=persona)
                .first()
            )
            if existing_entry:
                existing_entry.facts = json.dumps(facts)
                existing_entry.related_topics = json.dumps(related_topics)
            else:
                # Assuming facts_table is mapped correctly for insertions
                new_entry = {
                    "topic": topic,
                    "persona": persona,
                    "facts": json.dumps(facts),
                    "related_topics": json.dumps(related_topics),
                }
                session.execute(facts_table.insert(), new_entry)
            session.commit()
    except Exception as e:
        logging.error(f"Error saving facts to database: {e}")


def get_facts_from_db(topic, persona):
    topic, persona = standardize_primary_key(topic, persona)
    with conn.session as session:
        query = select(facts_table).where(
            and_(facts_table.c.topic == topic, facts_table.c.persona == persona)
        )
        result = session.execute(query).fetchone()
        if result:
            return json.loads(result.facts), json.loads(result.related_topics)
        else:
            return None, None
