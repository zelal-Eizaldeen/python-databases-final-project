# **Leading Universities in Data Science with Their Top Faculty and Publications**

## Purpose

### Application Scenario
The application aims to provide insights into the leading universities in Data Science, showcasing their top faculty members and their publications. It allows users to explore keywords, trends, and detailed professor information from the Academic World dataset.

### Target Users
- Academic researchers
- University administrators
- Students interested in Data Science
- Data Science enthusiasts

### Objectives
- To display the top faculty members based on citations in Data Science.
- To visualize the distribution and trends of keywords in publications.
- To compare the number of faculty members specializing in Data Science across leading universities.
- To provide detailed information about selected professors and their publications.
- Allow users to favorite the publications they like and find more information about the faculty that published them.

## Demo

[Link to video demo](https://mediaspace.illinois.edu/media/t/1_eybctuw8)

## Installation

1. Clone the repository.
2. Switch to python version 3.12.3
   ```bash
   pyenv install
   ```
   Or install and configure python 3.12 manually.
3. Install the required Python packages:
    ```bash
    pipenv install
    pipenv shell
    ```
    Or use generated `requirements.txt` with `pip install -r requirements.txt`
4. Set up environment variables
   - Create a `.env` file in the root directory and add the following:
      ```plaintext
      PASSWORD=<your_database_password>
      ```
   - This password should be the same for MySQL and Neo4j.
5. Ensure databases are running and accessible

## Usage
1. Run
    ```bash
        python app.py
    ```
2. Copy the link provided by Dash which would be: http://127.0.0.1:8050/
3. Paste it into your favourite browser and hit enter.
4. Interact with the dashboard:
   - View the top faculty members by accumulated citations.
   - Explore the top universities by the number of faculty members.
   - Analyze the distribution and trends of keywords in publications.
   - Get detailed information about professors and their publications.
   - Manage your favorite publications and view associated professor details.

## Design
The Application is designed with ten Widgets that manipulate the database and arranged in a rectangular space with:

- Querying widgets: It has seven widgets that retrieve data based on the user input.
- Updating widgets: It has three widgets one that perform INSERT favourite publications into fav_pub table and one that performs a DELETE operation publications From fav_pub. As well as an extra-credit widget that allows users to update faculty research interests.
- Visual Layout: The widgets are arranged in a rectangular shape with Rows and Columns, and the data starts from general data (overview) to more specific results. It follows the [Schneiderman's Mantra ](https://hampdatavisualization.wordpress.com/2016/02/26/schneidermans-mantra/).

In terms of colors: The dashboard used the same colors provided by Dash Plotly library to have Color Consistency.<br />
For the Style: Used dash_bootstrap_components, and CSS.
The Querying Widgets are:
1. First Row contains the Card element that gives the Top Five Faculty based on Accumulated_Citation, and the Card colors are the same colors that used in Dash Plotly charts.
2. Second Row contains two widgets in two columns, the first widget is a Bar graph in which the user can see Top Five Universities by Data Science Faculties number, and the second widget is a Pie graph in which the user can see Top Five Keywords containing data.
3. Third Row contains two widgets in one column, the first one is a DropDown showing only data Keywords to select from, and the second one is a Line graph which responds to the user selecttion.
4. Forth Row contains two widgets in one column in order to show Top Ten Universities in Data Science Publications by using a DropDown to select the University and a Datatable responds to the user selection.
5. Fifth Row contains two widgets, a datatable, where the user can INSERT from Publication table and add his/her favourite ones, and a Button that shows the total number of favourite publications. The user can INSERT or Delete from the favourite table.
6. Sixth Row contains one widget,a datatable, where the user can see the details of his/her favourite professor.
7. Seventh Row contains one widget, which allows the user to update a faculy members research interests.


## Implementation

### Frameworks and Libraries
- Dash Plotly: For building interactive web applications.
- Dash Bootstrap Components: For styling and layout.
- Pandas: For data manipulation.
- MySQL Connector: For connecting and querying MySQL database.
- Pymongo: For connecting and querying MongoDB database.
- Neo4j: For connecting and querying Neo4j database.

### Functionalities
- Top Faculty Members: Fetch and display top faculty members by citations.
- Keyword Distribution: Visualize the distribution of keywords in publications.
- Trendy Keywords: Show trends of keywords over time.
- Top Universities: Compare universities based on faculty count.
- Favorite Publications: Manage and view favorite publications.
- Professor Details: Display detailed information about selected professors.

## Database Techniques
1. Indexing: Indexed the keyword collection in MongoDB to speed up the query. As well as an index on the `materialized_ds_faculty_count` to speed up the query for the Top 5 Universities by Number of Faulty.
2. View: Created uiuc view to filter out the UIUC among other universities, top_ten_universities view to show top ten universities based on accumulated citations. Also created a materialized view for data science faculty count to preprocess the query results and speed up the dashboard.
3. Constraint:
    - Created Unique node property constraints on Keyword property to ensure that Keyword values are unique for all nodes with a specific label.
    - Created Primary Key with Professor name and Title publication for the favourite publication table to ensure not saving multi records for the same professor with same publications, which means save space in the memory.

4. Trigger: Created a trigger after INSERT on the favourite publications table to update the total number of favourite publications stored in the database automatically.

## Contributions

| NetID          | Contributions                    | Time Spent            |
| ---------------| ---------------------------------| ----------------------|
| zelalae2       | Connected to MySQL using Python   | 2 hours               |
| zelalae2       | Connected to Neo4j using Python   | 2 hours               |
| zelalae2       | Added search bar for trends in data keyword and sorted them by year using Plotly Express line | 3 hours |
| zelalae2       | Added constraint by Neo4j, added CSS files, added bar graph by MySQL | 4 hours |
| zelalae2       | Added View (uiuc) using MySQL | 2 hours |
| jg70       | Added MongoDB support | 3 hours |
| zelalae2       | Retrieved top 10 universities in ML by MySQL | 3 hours |
| zelalae2       | Added Dash Bootstrap Components, and finished the dropdown top ten universities with the table showing its publication info | 4 hours |
| zelalae2       | Solved GitHub branches issue, added bootstrap components | 2 hours |
| zelalae2       | Added insert command using MySQL | 2 hours |
| zelalae2       | Delete rows from fav_table | 2 hours |
| jg70       | Added support for Pipenv, cleaned code, and fixed typo. And a WIP pie chart. | 4 hours |
| zelalae2       | Added a Deck of Cards using Neo4j query. Styling the colors to be consistent. | 3 hours |
| jg70       | Added initial README text and structure | 2 hours |
| zelalae2       | Added Primary Key constraint in the fav_pub table to avoid duplication in INSERT INTO. Added Trigger on the fav_pub AFTER INSERT | 3 hours |
| jg70       | Added another widget for professor information | 3 hours |
| jg70       | Went through code and dashboard, added improvements, and made all widgets consistent with the data science theme | 4 hours |
| jg70       | Add final touches to README report | 2 hours |
| zelalae2   | Added A Button to show the total_fav_pub, and an interval to update every 1000ms | 4 hours |
| jg70 | Add extra functionality for updating the faculty research interests | 2 hours |
| jg70 | Added video demo | 2 hours |
