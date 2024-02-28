from sqlalchemy import create_engine, Table, Column, String, MetaData, select, and_
from sqlalchemy.orm import sessionmaker
from config import DATABASE_NAME
import json
import logging

engine = create_engine(f"sqlite:///{DATABASE_NAME}")
metadata = MetaData()
facts_table = Table(
    "facts",
    metadata,
    Column("topic", String, primary_key=True),
    Column("persona", String, primary_key=True),
    Column("facts", String),
    Column("related_topics", String),
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def save_facts_to_db(topic, persona, facts, related_topics):
    try:
        with Session() as session:
            existing_entry = (
                session.query(facts_table)
                .filter_by(topic=topic, persona=persona)
                .first()
            )
            if existing_entry:
                existing_entry.facts = json.dumps(facts)
                existing_entry.related_topics = json.dumps(related_topics)
            else:
                # Corrected insertion process
                new_entry = facts_table.insert().values(
                    topic=topic,
                    persona=persona,
                    facts=json.dumps(facts),
                    related_topics=json.dumps(related_topics),
                )
                session.execute(new_entry)
            session.commit()
    except Exception as e:
        logging.error(f"Error saving facts to database: {e}")


def get_facts_from_db(topic, persona):
    with Session() as session:
        query = select(facts_table).where(
            and_(facts_table.c.topic == topic, facts_table.c.persona == persona)
        )
        result = session.execute(query).fetchone()
        if result:
            return json.loads(result.facts), json.loads(result.related_topics)
        else:
            return None, None
