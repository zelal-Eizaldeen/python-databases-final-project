from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

password=os.getenv('PASSWORD')
URI = "neo4j://localhost:7687/academicworld"
AUTH = ("neo4j", password)

# Get data keywords
def get_data_keywords():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    # Get the name of KEYWORDS
    records, summary, keys = driver.execute_query(
        "MATCH(k:KEYWORD) WHERE k.name CONTAINS 'data' RETURN k.name AS keyword",
        database_="academicworld"
    )
    driver.close()
    df = pd.DataFrame(records)
    return df

# Get Trendy keywords
def get_trendy_keywords():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    records, summary, keys = driver.execute_query(
        "MATCH(p:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD) WHERE k.name CONTAINS 'data' AND p.year > 2016 RETURN  COUNT(DISTINCT p.id) AS total_pb, p.year AS year, k.name as name",
        database_="academicworld"
    )
    df = pd.DataFrame(records)
    df = df.rename(columns={0: 'Publication', 1: 'Year',2:'Keywords'})
    return df

# Create constraint on keywords
def create_kw_constraint():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    records, summary, keys = driver.execute_query(
        "CREATE CONSTRAINT kw_name  IF NOT EXISTS FOR (k:KEYWORD) REQUIRE k.name IS UNIQUE",
        database_="academicworld"
    )
    driver.close()

    df = pd.DataFrame(records)

    return df

# Find the top five faculty members who are ranked highest by the keyword-relevant citation in data science
def get_top_faculty_DS():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    records, summary, keys = driver.execute_query(
        "MATCH(u:INSTITUTE)<-[:AFFILIATION_WITH]-(faculty:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[l:LABEL_BY]->(:KEYWORD{name:'data science'}) RETURN faculty.name, sum(l.score*p.numCitations) AS accumulated_citation ORDER BY accumulated_citation DESC LIMIT 5",
        database_="academicworld"
    )
    driver.close()

    df = pd.DataFrame(records)
    df = df.rename(columns={0: 'Faculty', 1: 'Accumulated_Citation'})
    return df

