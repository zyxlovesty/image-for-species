import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import os
import base64
# Setup Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css', 'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap', '/src/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "Species and Trails"

# Load the dataset
df = pd.read_csv('src/50_trails 3.csv')  # Adjust path as necessary

# Helper function to load species names
def load_species_names():
    species_set = set()
    for species_list in df['trail_species'].str.split(','):
        species_set.update([species.strip() for species in species_list])
    return [{'label': species, 'value': species} for species in sorted(species_set)]

def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
    
# Create species card
def create_species_card(species_name):
    image_filename = species_name.replace(" ", "_") + '.jpg'
    image_path = os.path.join('assets', image_filename)  
    return dbc.Card(
        [
            dbc.CardImg(src=image_path, top=True, alt=f"Image of {species_name}",style={'width': '100%', 'height': '200px', 'object-fit': 'cover'}),
            dbc.CardBody([
                html.H5(species_name, className="card-title"),
                dcc.Link('View Trails', href=f'/species/{species_name.replace(" ", "-")}',style={'color':'#140c1f'})
            ]),
        ],
        style={"width": "18rem", "margin": "10px","background-color": "#b4ded5"}
    )

@app.callback(
    Output('dynamic-content', 'children'),
    [Input('url', 'pathname'),
     Input('species-search-dropdown', 'value')]
)
def update_dynamic_content(pathname, selected_species):
    ctx = dash.callback_context

    if not ctx.triggered or pathname == '/' or pathname == '/all-species':
        if selected_species:
            species_to_display = [{'label': selected_species, 'value': selected_species}]
        else:
            species_to_display = load_species_names()

        species_cards = [create_species_card(species['value']) for species in species_to_display]
        return dbc.Row(species_cards, className="row-cols-1 row-cols-md-3 justify-content-center g-4")
    
    elif pathname.startswith('/species/'):
        species_name = pathname.split('/')[-1].replace('-', ' ')
        filtered_trails = df[df['trail_species'].str.contains(species_name, case=False)]
        
        trails_content = []  
        
        for _, trail in filtered_trails.iterrows():
            trail_name = trail['trail_name']
            description = trail['trail_desc']
            duration = trail['trail_duration']
            elevation_gain = trail['trail_ele_gain']
            distance = trail['trail_distance']
            dist_mel = trail['trail_dist_mel']
            time_mel = trail['trail_time_mel']
            loop = trail['trail_loop']
            
            
            trail_card = dbc.Card(
                [
                    dbc.CardImg(src=b64_image(f'src/data/trail_img/{trail_name}.jpg'), top=True, style={'width': '300px', 'height': '200px'}),  # Adjust the path as needed
                    dbc.CardBody([
                        html.H5(trail_name, className='card-title'),
                        html.P([html.I(className="fas fa-info-circle"), f" Description: {description}"]),
                        html.P([html.I(className="fas fa-clock"), f" Duration: {duration} hours"]),
                        html.P([html.I(className="fas fa-mountain"), f" Elevation Gain: {elevation_gain} m"]),
                        html.P([html.I(className="fas fa-ruler-horizontal"), f" Distance: {distance} km"]),
                        html.P([html.I(className="fas fa-car"), f" Drive from Melbourne: {time_mel} hours"]),
                        html.P([html.I(className="fas fa-map-marker-alt"), f" Distance from Melbourne: {dist_mel} km"]),
                        html.P([html.I(className="fas fa-route"), f" Trail Type: {'Loop' if loop else 'One-way'}"]),
                    ])
                ],
                style={"width": "77rem", "margin": "10px"}
            )
            
            trails_content.append(trail_card)
        
        
        return dbc.Row(trails_content, className="row-cols-1 row-cols-md-3 g-4 justify-content-around")
    
    return "Select a species to see the trails."


# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(
            html.Header([
                html.A('InSync', href='#', className='logo'),
                html.Ul([
                    html.Li(dcc.Link('Home', href='/')),
                    html.Li(dcc.Link('My Trail', href='/my-trail')),
                    html.Li(dcc.Link('All Trails', href='/all-trails', className='active')),
                ], className='navigation')
            ])
        )
    ]),
    html.Div([
        html.H2('Species in Victoria', style={'font-size': '3em', 'color':'#fff', 'margin-bottom': '10px', 'margin-top':'10px', 'margin-left':'40px'}),
        html.H4('Explore the diverse Species of Victoria with our carefully curated selection.', style={'font-size': '1em', 'color':'#112434', 'margin-left':'40px'}),
        html.P('This is where you can find them on our trails, to enhance your nature exploration and help you discover the unique wildlife of the region.', style={'margin-right':'150px', 'margin-left':'40px'}),
        html.P("    "),
        html.H4('Happy Hiking!', style={'margin-top': '20px', 'margin-left':'40px', 'margin-bottom':'10px'})
    ], style={
    'background-color': '#112434',
    'border': '2px solid white',
    'padding': '20px',
    'margin': '40px',
    'margin-top':'100px',
    'border-radius': '15px',
    'color': 'white'
    }),
    # html.Div(id='trail-cards-row'),
    html.Div([
        dcc.Dropdown(
            id='species-search-dropdown',
            options=load_species_names(),
            searchable=True,
            placeholder='Search for species...',
            style={
                            'width': '70%',  # Use 100% to make it responsive within the column
                            'margin': '0 auto',  # Keep it centered
                            'borderRadius': '20px',
                            'fontFamily': '"Poppins", sans-serif',
                            'fontSize': '16px',
                            'margin-bottom': '30px'
                        }
        ),
    ]),
    html.Div(id='dynamic-content', style={'padding': '20px'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
