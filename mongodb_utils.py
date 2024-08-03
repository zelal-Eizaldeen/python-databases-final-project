from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

uri = f"mongodb://localhost:27017/"
database_name = "academicworld"

client = MongoClient(uri)
db = client[database_name]


def get_professors():
    # Get the name of FACULTIES whose position is Professor
    professors = db.faculty.find({"position": "Professor"}, {"name": 1, "_id": 0})
    professor_list = [prof["name"] for prof in professors]

    # Loop through results and print them
    for name in professor_list:
        print(name)

    # Summary information
    print(f"The query returned {len(professor_list)} records.")

def get_professor_details(professor_name):
    """
    Fetch professor details from MongoDB based on the given professor name.

    Parameters:
    professor_name (str): The name of the professor whose details are to be fetched.

    Returns:
    dict: A dictionary containing the professor's details. The dictionary will have the following keys:
          - name: The name of the professor.
          - email: The email address of the professor.
          - researchInterest: The research interests of the professor.
          - affiliation: The affiliation of the professor.
          - photoUrl: The URL of the professor's photo.

    Note:
    This function assumes that a MongoDB database named 'academicworld' is accessible,
    and the 'faculty' collection contains the professor details.
    """
    details = db.faculty.find_one(
        {"name": professor_name},
        {
            "_id": 0,
            "name": 1,
            "email": 1,
            "researchInterest": 1,
            "affiliation": 1,
            "photoUrl": 1,
        },
    )
    return details

def get_data_keywords():
    keywords_count = db.publications.aggregate([
        { "$unwind": "$keywords" },
        # contains the word _data_
        { "$match": { "keywords.name": { "$regex": "data", "$options": "i" } } },
        # Remove all plural keywords
        { "$match": { "keywords.name": { "$not": { "$regex": ".*s$", "$options": "i" } } } },
        { "$group": { "_id": "$keywords.name", "count": { "$sum": 1 } } },
        { "$sort": { "count": -1 } },
        { "$limit": 5 },
    ])
     # Convert the result to a list and then to a DataFrame
    keyword_list = list(keywords_count)
    df = pd.DataFrame(keyword_list, columns=['_id', 'count'])
    df = df.rename(columns={'_id': 'Keyword', 'count': 'Count'})
    return df

def create_kw_index():
    # Create unique index on keyword name
    result = db.keyword.create_index([("name", 1)], unique=True)
    return result

def update_professor_research_interest(professor_name, new_research_interest):
    """
    Update the research interests of a professor in the MongoDB database.

    Parameters:
    professor_name (str): The name of the professor.
    new_research_interest (str): The new research interest to be added.

    Returns:
    dict: The updated professor details.
    """
    result = db.faculty.update_one(
        {"name": professor_name},
        {"$set": {"researchInterest": new_research_interest}}
    )
    return result

# Example usage:
if __name__ == "__main__":
    # print(get_data_keywords())
    create_kw_index()
