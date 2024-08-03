from dash import Dash, html, dcc, callback, Output, Input,State, dash_table, ctx
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd
import mysql_utils
import mongodb_utils
import neo4j_utils


# ------MySQL Queries-----
# ------------------------
#------Creating New Tables--
mysql_utils.create_fav_table()
mysql_utils.create_total_fav_pub()

#------Creating New Triggers--
mysql_utils.trigger_after_insert_fav_pub()

# ---------VIEWS----------
mysql_utils.create_views()
top_ten_uni=mysql_utils.get_top_uni()
top_ten_uni=((top_ten_uni[0].values))

# ------SELECTIONS--------
#Get counts of faculty members in each university
faculty_counts=mysql_utils.compare_universities_ds_faculty_count()
# ------Neo4j Queries-----
# ------------------------
# Initializing Constraints using Neo4j
neo4j_utils.create_kw_constraint()
# Get each keyword names contains data
keywords=neo4j_utils.get_data_keywords()
keywords=((keywords[0].values)) #store keywords in array
trendy_keywords=neo4j_utils.get_trendy_keywords()
# Get the top five faculty members who are ranked highest by the keyword-relevant citation in data science
top_five_faculty_ds=neo4j_utils.get_top_faculty_DS()
top_faculty_ds = top_five_faculty_ds['Faculty'].values #get the names as array
acc_citation=top_five_faculty_ds['Accumulated_Citation'].values #get the accumulated_citation as array

# -------MongoDB Queries -------
# ------------------------------

mongodb_utils.create_kw_index()

# Fetch keyword data
df_keywords = mongodb_utils.get_data_keywords()

#---------------------------------
#------ Dash Plotly --------------
#---------------------------------

#-------------Using Dash bootstrap Components ------
app = Dash(external_stylesheets=[dbc.themes.SOLAR])
app.css.append_css({'external_url': '/assets/styles.css'})
#------------- Variables --------------------

# --------- Bar Graph For Comparing Top Five Universities ----------
fig_top_uni = px.bar(faculty_counts, x="University", y="Faculty", color="University")

# ---------- Pie chart for Keyword Distribution ----------
fig_keyword_dist = px.pie(df_keywords, values='Count', names='Keyword', title='Distribution of Keywords')

#-------- Layout---------------
app.layout = html.Div(children=[
    html.H1(children='Leading Universities in Data Science with Their Top Faculty and Publications'),
    dbc.Row([
       html.Div(children='Top 5 Faculty Members by Accumulated Citations in Data Science'),

       dbc.Col([
           html.Br(),
           dbc.Card([
               html.H4(top_faculty_ds[0]),
               html.H5(f'{round(acc_citation[0],1)}')
           ],
                    body=True,
                    style={'textAlign':'center','color':'white'},
                    color='rgb(81,82,249)'),
       ]),
         dbc.Col([
           html.Br(),
           dbc.Card([
               html.H4(top_faculty_ds[1]),
               html.H5(f'{round(acc_citation[1],1)}')
           ],
                    body=True,
                    style={'textAlign':'center','color':'white'},
                    color='rgb(233,61,46)'),
       ]),
         dbc.Col([
           html.Br(),
           dbc.Card([
               html.H4(top_faculty_ds[2]),
               html.H5(f'{round(acc_citation[2],1)}')
           ],
                    body=True,
                    style={'textAlign':'center','color':'white'},
                    color='rgb(25,188,126)'),
       ]),
          dbc.Col([
           html.Br(),
           dbc.Card([
               html.H4(top_faculty_ds[3]),
               html.H5(f'{round(acc_citation[3],1)}')
           ],
                    body=True,
                    style={'textAlign':'center','color':'white'},
                    color='rgb(153,67,249)'),
       ]),
           dbc.Col([
           html.Br(),
           dbc.Card([
               html.H4(top_faculty_ds[4]),
               html.H5(f'{round(acc_citation[4],1)}')
           ],
                    body=True,
                    style={'textAlign':'center','color':'white'},
                    color='rgb(253,143,73)'),
       ]),
    ]),#end of row0
    html.Br(),
    dbc.Row([
        dbc.Col([
        html.Div(children='Top 5 Universities by Number of Faculty with Data Science publications'),
        dcc.Graph(id='faculty_counts_bg',figure=fig_top_uni),
        ]),
         dbc.Col([
            html.Div(children='Top 5 Keywords containing data'),
            dcc.Graph(
                id='keyword-pie-chart',
                figure=fig_keyword_dist)
        ]),

    ]),#end of row1
    html.Br(),
    dbc.Row([
        dbc.Col([
        html.Div(className="app-header",children='Trends in Keywords containing data'),
        dcc.Dropdown(options=keywords, id='keywords-dd',placeholder="Select a keyword"),
        dcc.Graph(id='line-trendy-kw'),
        ]),
        html.Br(),
        html.Br(),
    ]),#end row2
    html.Br(),
    dbc.Row([
        dbc.Col([
        html.Div(
            className="app-header",
            children='Top 10 Universities in Data Science and Their Publications',
        ),
        dcc.Dropdown(options=top_ten_uni, id='top-ten-uni-dd', placeholder="Select University",value='University of Illinois at Urbana Champaign'),
        dash_table.DataTable(
        id='top-publication-tb',
        editable=True,
        column_selectable="single",
        row_selectable="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        # active_cell=initial_active_cell,
        page_size=10,
        style_cell={'textAlign': 'left', 'marginBottom':'30px'},
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px',
        })
        ]),
    ]),#end row3
    dbc.Row([
        dbc.Col([
            html.Div(className="app-header", children='Your Favourite Publications'),
            html.Button(children='Total', id='total-fav-pub',
                n_clicks=0,
                style={'textAlign':'center','color':'white','width':'100%','backgroundColor':'rgb(81,82,249)'},
            ),
            dash_table.DataTable(
                id='fav-publication-tb',
                columns=[
                    {"name": "Professor", "id": "Professor"},
                    {"name": "Title", "id": "Title"},
                    {"name": "Venue", "id": "Venue"},
                    {"name": "Year", "id": "Year"}
                ],
                selected_rows=[],
                column_selectable="single",
                row_selectable="multi",
                page_size=10,
                row_deletable=True,
                style_cell={'textAlign': 'left'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px',
                },
                data=[]  # Initialize with an empty list
            ),
        ]),
    ]),  # end row4
    dbc.Row([
        dbc.Col([
            html.Div(
                className="app-header",
                children='Details of Professors for Selected Favorite Publications',
            ),
            dash_table.DataTable(
                id='professor-details',
                columns=[
                    {
                        "name": "Image",
                        "id": "photoUrl",
                        "type": "text",
                        # Display markdown formatted image string
                        "presentation": "markdown",
                    },
                    {"name": "Name", "id": "name"},
                    {"name": "Email", "id": "email"},
                    {"name": "Research Interest(s)", "id": "researchInterest"},
                    {"name": "Affiliation", "id": "affiliation"}
                ],
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px',
                }
            ),
            html.Br(),
            html.Br(),
        ]),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ]),  # end row5

    dbc.Row([
        dbc.Col([
            dbc.Alert(id='update-result', is_open=False, duration=4000, color="info"),
            html.Div(className='app-header', children='Manually Update Faculty Research Interest'),
            dcc.Input(id='professor-name-input', type='text', placeholder='Enter Professor Name'),
            dcc.Input(id='research-interest-input', type='text', placeholder='Enter New Research Interest'),
            html.Button('Update', id='update-button', n_clicks=0),
        ]),
    ]), # end row6

]),

@callback(
    [Output('update-result', 'children'),
     Output('update-result', 'is_open'),
     Output('professor-name-input', 'value'),
     Output('research-interest-input', 'value')],
    Input('update-button', 'n_clicks'),
    State('professor-name-input', 'value'),
    State('research-interest-input', 'value'),
    prevent_initial_call=True
)
def update_research_interest(n_clicks, professor_name, new_research_interest):
    if not professor_name or not new_research_interest:
        return "Please provide both professor name and new research interest.", True, professor_name, new_research_interest

    result = mongodb_utils.update_professor_research_interest(professor_name, new_research_interest)

    if result.matched_count > 0:
        return f"Successfully updated research interest for {professor_name}.", True, '', ''
    else:
        return f"Professor {professor_name} not found.", True, '', ''

#Callback for the line chart
@callback(
    Output('line-trendy-kw', 'figure'),
    Input('keywords-dd', 'value')
)
def update_graph(value):
     dff = trendy_keywords[trendy_keywords['Keywords']==value]
     dff = dff.sort_values(by="Year")
     fig=px.line(dff, x='Year', y='Publication')
     return fig.update_layout(xaxis_type='category')

# Callback to update the top-publication-tb when a university is selected
@callback(
    Output('top-publication-tb', 'data'),
    Input('top-ten-uni-dd', 'value'),
    prevent_initial_call=True
)
def update_datatable(selected_university):
    """
    This function updates the data displayed in the 'top-publication-tb' DataTable based on the selected university.

    Parameters:
    selected_university (str): The name of the selected university. If no university is selected, this parameter will be None.

    Returns:
    list: A list of dictionaries representing the updated data in the 'top-publication-tb' DataTable. Each dictionary contains information about a publication, excluding the 'University' and 'id' columns.
    """
    if not selected_university:
        return []

    top_pub = mysql_utils.get_publication_DS(selected_university)
    if top_pub.empty:
        return []

    # Drop unnecessary columns
    top_pub = top_pub.drop(['University', 'id'], axis=1)
    return top_pub.to_dict('records')

@callback(
    Output('professor-details', 'data'),
    Input('fav-publication-tb', 'selected_rows'),
    State('fav-publication-tb', 'data')
)
def display_professor_details(selected_rows, data):
    """
    This function retrieves and displays detailed information about professors associated with selected publications.

    Parameters:
    selected_rows (list): A list of indices representing the selected rows in the 'fav-publication-tb' DataTable.
    data (list): A list of dictionaries representing the data in the 'fav-publication-tb' DataTable. Each dictionary contains information about a publication, including the professor's name.

    Returns:
    list: A list of dictionaries containing detailed information about the selected professors. Each dictionary has the following keys: 'photoUrl', 'name', 'email', 'researchInterest', and 'affiliation'.
    """
    if not selected_rows or not data:
        return []

    unique_professors = set(data[i]['Professor'] for i in selected_rows)
    all_details = []

    for prof in unique_professors:
        details = mongodb_utils.get_professor_details(prof)
        if details:
            details['photoUrl'] = (
                f"![Professor Image]({details['photoUrl']})" if details['photoUrl'] else 'No photo available'
            )
            if isinstance(details['affiliation'], dict):
                details['affiliation'] = details['affiliation'].get('name', 'Unknown affiliation')
            all_details.append(details)

    return all_details

# Callback to handle loading and updating favorite publications
@callback(
    Output('fav-publication-tb', 'data'),
    Input('top-publication-tb', "data"),
    Input('top-publication-tb', "selected_rows"),
    Input('fav-publication-tb', "data"),
)
def manage_fav_publications(top_pub_data, selected_rows, fav_data):
    """
    This function manages the favorite publications in the Dash application. It handles adding and deleting favorite publications based on user interactions.

    Parameters:
    top_pub_data (list): A list of dictionaries representing the data from the 'top-publication-tb' DataTable. Each dictionary contains information about a publication.
    selected_rows (list): A list of indices representing the selected rows in the 'top-publication-tb' DataTable.
    fav_data (list): A list of dictionaries representing the data in the 'fav-publication-tb' DataTable. Each dictionary contains information about a favorite publication.

    Returns:
    list: A list of dictionaries representing the updated data in the 'fav-publication-tb' DataTable.
    """
    triggered_id = ctx.triggered_id
    if triggered_id == 'top-publication-tb' and selected_rows:
        return add_fav_pub(top_pub_data, selected_rows)
    elif triggered_id == 'fav-publication-tb':
        return delete_fav_pub(fav_data)
    # Initial load if no trigger and data is empty
    if not fav_data:
        df = mysql_utils.get_fav_pub()
        return df.to_dict('records')
    return fav_data

def add_fav_pub(rows, selected_rows):
     dff = df if rows is None else pd.DataFrame(rows)
     if dff.empty:
        return[]
     filtered_df=dff.iloc[selected_rows]
     filtered_df=filtered_df.drop(['Num_Citations'], axis=1)
     mysql_utils.insert_fav_pub(filtered_df)
     df=mysql_utils.get_fav_pub()

     return df.to_dict('records')
def delete_fav_pub(fav_data):
     dff = fav_data if fav_data is None else pd.DataFrame(fav_data)
     mysql_utils.delete_fav_pub()
     mysql_utils.insert_fav_pub(dff)
     return dff.to_dict('records')

#callback to update the total number of favorite publications
@callback(
    Output('total-fav-pub', 'children'),
    Input('total-fav-pub', 'n_clicks'),
    State('fav-publication-tb', "data"),
    Input('interval-component', 'n_intervals'),
    prevent_initial_call=True
)
def update_total_fav_pub(n_clicks,fav_data,n):
    return f'Total Favorites: {len(fav_data)}'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)