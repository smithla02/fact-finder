import streamlit as st
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer

Base = declarative_base()


class Facts(Base):
    __tablename__ = "facts"
    topic = Column(String, primary_key=True, index=True)
    persona = Column(String, primary_key=True, index=True)
    facts = Column(Text)
    related_topics = Column(Text)
    num_facts = Column(Integer)


def init_db():
    # Initialize the database connection using st.connection
    conn = st.connection("facts_db", "sql", autocommit=True)
    # Use the engine attribute to bind the Base metadata for creating tables
    Base.metadata.create_all(bind=conn.engine)
    return conn


# Initialize database connection
db_conn = init_db()


def get_facts_from_db(topic: str, persona: str, num_facts: int):
    with db_conn.session as session:
        facts_instance = (
            session.query(Facts)
            .filter_by(topic=topic, persona=persona, num_facts=num_facts)
            .first()
        )
        if facts_instance:
            return (
                json.loads(facts_instance.facts),
                json.loads(facts_instance.related_topics),
            )
        else:
            return None, None


def save_facts_to_db(
    topic: str, persona: str, facts: list, related_topics: list, num_facts: int
):
    with db_conn.session as session:
        existing_fact = (
            session.query(Facts)
            .filter(Facts.topic == topic, Facts.persona == persona)
            .first()
        )
        if existing_fact:
            existing_fact.facts = json.dumps(facts)
            existing_fact.related_topics = json.dumps(related_topics)
            existing_fact.num_facts = num_facts  # Add this line
        else:
            new_facts = Facts(
                topic=topic,
                persona=persona,
                facts=json.dumps(facts),
                related_topics=json.dumps(related_topics),
                num_facts=num_facts,  # Add this line
            )
            session.add(new_facts)
        session.commit()
