import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
password=os.getenv('PASSWORD')

# ------Connection with MySQL-------------
def get_connection():
    connection = mysql.connector.connect(user='root', password=password,
                                host='127.0.0.1',
                                database='academicworld')

    cursor = connection.cursor(buffered=True)
    return connection, cursor
# ------ Creating fav_pub table in the academicworld-------------
def create_fav_table():
    (connection, cursor)=get_connection()
    cursor.execute("CREATE TABLE IF NOT EXISTS fav_pub(\
                    id INT,\
                    Professor varchar(250),\
                    Title varchar(250),\
                    Venue varchar(250),\
                    Year varchar(250),\
                    PRIMARY KEY(Professor,Title))")

def create_total_fav_pub():
    (connection, cursor)=get_connection()
    cursor.execute("CREATE TABLE IF NOT EXISTS total_fav_pub(\
                      total_favs INT)")

# ------Creating VIEWS-------------
def create_views():
    (connection, cursor)=get_connection()
    cursor.execute("CREATE OR REPLACE VIEW uiuc  AS SELECT * FROM university \
    U WHERE U.name = 'University of Illinois at Urbana Champaign';")
    cursor.execute('''
        CREATE OR REPLACE VIEW top_ten_universities AS
            SELECT
                U.name,
                SUM(PK.score*P.num_citations) AS KRC
            FROM
                university U,
                faculty F,
                publication_keyword PK,
                publication P,
                faculty_publication FP,
                keyword K
            WHERE
                F.id=FP.faculty_id
                AND P.id=PK.publication_id
                AND K.id=PK.keyword_id
                AND FP.publication_id=P.id
                AND U.id=F.university_id
                AND K.name='data science'
            GROUP BY U.name
            ORDER BY KRC DESC
            LIMIT 10
    ''')
    cursor.execute("CREATE OR REPLACE VIEW fav_pub_view AS\
                   SELECT * FROM fav_pub")

    # This materialized view is required for speed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materialized_ds_faculty_count AS
        SELECT
            u.name AS university_name,
            COUNT(DISTINCT f.id) AS faculty_count
        FROM
            faculty f,
            university u,
            publication p,
            Publication_Keyword pk,
            faculty_publication fp,
            keyword k
        WHERE
            u.id = f.university_id
            AND f.id = fp.faculty_Id
            AND fp.publication_Id = p.ID
            AND p.ID = pk.publication_id
            AND pk.keyword_id = k.id
            AND LOWER(k.name) LIKE '%data science%'
        GROUP BY university_name;
        -- Add index
        CREATE INDEX idx_materialized_keyword_counts ON materialized_ds_faculty_count(university_name, faculty_count);
    """, multi=True)

# ------TRIGGERS-------------
def trigger_after_insert_fav_pub():
    (connection, cursor) = get_connection()
    sql = """
    CREATE TRIGGER IF NOT EXISTS pub_trigger
    AFTER INSERT ON fav_pub
    FOR EACH ROW
    BEGIN
        UPDATE total_fav_pub
        SET total_favs = (
            SELECT COUNT(*)
            FROM fav_pub
        );
    END;
    """

    cursor.execute(sql)
    # save changes
    connection.commit()
    # disconnect from server
    connection.close()

# Get the UIUC (using view uiuc)
def get_uiuc_uni():
    (connection,cursor)=get_connection()
    cursor.execute("SELECT U.name FROM UIUC U")
    result=cursor.fetchall()
    df=pd.DataFrame(result)
    return df

#-------TOP 10 Universities by KRC (using top_ten_universities view) ---
def get_top_uni():
    (connection,cursor)=get_connection()
    cursor.execute("SELECT * FROM top_ten_universities")
    result=cursor.fetchall()
    df=pd.DataFrame(result)
    return df

# Get Favourite Publications ---
def get_fav_pub():
    (connection,cursor)=get_connection()
    cursor.execute("SELECT DISTINCT Professor,Title,Venue,Year FROM fav_pub")
    result=cursor.fetchall()
    df=pd.DataFrame(result)
    df = df.rename(columns={0: 'Professor',1: 'Title',2: 'Venue', 3:'Year'})
    df['id']=df.index # add an id column and set it as the index
    df=df.iloc[:,:4]
    return df
#------Add new favourite publications to the table
def insert_fav_pub(df_pub):
    if(df_pub.empty):
        return []
    (connection,cursor)=get_connection()
    # row created
    sql = "INSERT INTO fav_pub(Professor, Title, Venue, Year)\
        VALUES(%s,%s,%s,%s) ON DUPLICATE KEY\
            UPDATE  Professor=Professor, Title=Title, Venue=Venue, Year=Year"
    for row in df_pub.values.tolist():
         cursor.execute(sql, tuple(row))
    # save changes
    connection.commit()
    # disconnect from server
    connection.close()

#Clean the favorite publications table
def delete_fav_pub():
    (connection,cursor)=get_connection()
    sql = "DELETE FROM fav_pub"
    cursor.execute(sql)
    # save changes
    connection.commit()
    # disconnect from server
    connection.close()

#Save the total number of facourite publications
def total_fav_pub():
    (connection,cursor)=get_connection()
    cursor.execute("DELETE FROM total_fav_pub")
    sql = "INSERT INTO total_fav_pub (total_favs)\
        SELECT COUNT(*) FROM fav_pub"
    cursor.execute(sql)
    # save changes
    connection.commit()
    # disconnect from server
    connection.close()
    
# Get total favourite publications from total_fav_pub table
def get_total_fav_pub():
    (connection,cursor)=get_connection()
    cursor.execute("SELECT * FROM total_fav_pub")
    result=cursor.fetchall()
    df=pd.DataFrame(result)
    return df

# --------------- Publications of the selected university from Top tens---
def get_publication_DS(selected_university):
    """
    Retrieves publications related to 'data science' from a specified university.

    Parameters:
    selected_university (str): The name of the university to retrieve publications from.

    Returns:
    pandas.DataFrame: A DataFrame containing the following columns:
        - Professor: The name of the professor who published the paper.
        - Title: The title of the publication.
        - Venue: The venue where the publication was published.
        - Year: The year of publication.
        - Num_Citations: The number of citations the publication has received.
        - University: The name of the university where the professor is affiliated.
    """
    (connection,cursor) = get_connection()
    cursor.execute(
        """
        SELECT
            DISTINCT F.name AS Professor,
            P.title AS Title,
            P.venue AS Venue,
            P.year AS Year,
            P.num_citations AS Num_Citations,
            U.name AS University
        FROM
            university U, faculty F,publication_keyword PK,
            publication P, faculty_publication FP, keyword K
        WHERE
            F.id=FP.faculty_id AND P.id=PK.publication_id
            AND K.id=PK.keyword_id AND FP.publication_id=P.id
            AND U.id = F.university_id
            AND U.name=%s AND K.name='data science'
        ORDER BY
            P.num_citations DESC;
        """,
        (selected_university,)
    )
    result=cursor.fetchall()
    df=pd.DataFrame(result)
    df = df.rename(
        columns={
            0: 'Professor',
            1: "Title",
            2: 'Venue',
            3:'Year',
            4:'Num_Citations',
            5:'University'
        }
    )
    df['id']=df.index # add an id column and set it as the index
    return df

# Compare #Faculty between UIUC and Stanford
def compare_universities_ds_faculty_count():
    (connection,cursor)=get_connection()
    cursor.execute('''
        SELECT
            university_name,
            faculty_count
        FROM
            materialized_ds_faculty_count
        ORDER BY
            faculty_count DESC
        LIMIT 5;
    ''')
    result=cursor.fetchall()
    df=pd.DataFrame(result)
    df = df.rename(columns={0: 'University',1:'Faculty'})
    return df


