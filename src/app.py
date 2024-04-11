import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
 
import xml.etree.ElementTree as ET
from shapely.geometry import LineString
import pandas as pd
import base64
import os
 
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    '/assets/style.css'
]
 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
 
df = pd.read_csv('src/50_trails 3.csv', encoding='utf-8')
 
def load_trail_names():
    return [{'label': name, 'value': name} for name in df['trail_name'].unique()]
 
'''def gpx_to_points(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    namespaces = {'default': 'http://www.topografix.com/GPX/1/1'}
    route_points = [(float(pt.attrib['lat']), float(pt.attrib['lon'])) for pt in root.findall('.//default:trkpt', namespaces)]
    return LineString(route_points)

def create_trail_card(trail_number, trail_name, duration, elevation_gain, distance):
    return dbc.Card(
        dbc.CardBody([
            html.H3(style={'display': 'inline'}, children=[
                html.Span(f"{trail_number}. ", style={'font-weight': 'bold'}),  # Display the trail number
                html.A(trail_name, href=f'/{trail_name.replace(" ", "-")}',
                    style={'color': '#112434', 'text-decoration': 'none', 'margin-bottom': '8px'}),
                html.A(html.I(className="fas fa-external-link-alt",
                              style={'color': '#112434', 'text-decoration': 'none', 'margin-bottom': '8px', 'margin-left':'8px', 'font-size': '13px'}),
                      href=f'/{trail_name.replace(" ", "-")}')
            ]),
            html.Div([
                html.I(className="fas fa-clock", style={'color': '#808080', 'margin-right': '5px'}),
                html.Span(f"Duration: {duration} hours", style={'color': '#808080'}),
                html.I(className="fas fa-mountain", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '10px'}),
                html.Span(f"Elevation Gain: {elevation_gain} m", style={'color': '#808080'}),
                html.I(className="fas fa-route", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '10px'}),
                html.Span(f"Distance: {distance} km", style={'color': '#808080'}),
            ], style={'font-size': '14px', 'margin-bottom': '30px'})
        ])
    )''' 

def create_species_card(species_name):
    image_filename = species_name.replace(" ", "_") + '.jpg'
    image_path = os.path.join('assets', image_filename)  # Make sure this path is correct
    return dbc.Card(
        [
            dbc.CardImg(src=image_path, top=True, alt=f"Image of {species_name}"),
            dbc.CardBody([
                html.H5(species_name, className="card-title"),
                dcc.Link('View Trails', href=f'/species/{species_name.replace(" ", "-")}')
            ]),
        ],
        style={"width": "18rem", "margin": "10px"}
    )

def load_species_names():
    species_set = set()
    for species_list in df['trail_species'].str.split(','):
        species_set.update([species.strip() for species in species_list])
    return [{'label': species, 'value': species} for species in sorted(species_set)]


def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
 
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
        html.H2('Trails in Victoria', style={'font-size': '3em', 'color':'#fff', 'margin-bottom': '10px', 'margin-top':'10px', 'margin-left':'40px'}),
        html.H4('Explore the diverse trails of Victoria with our carefully curated selection.', style={'font-size': '1em', 'color':'#112434', 'margin-left':'40px'}),
        html.P('Our trails span across Victoria and offer a variety of terrains and difficulty levels. We provide average estimates of trail details to help you choose the perfect trail for your adventure.', style={'margin-right':'150px', 'margin-left':'40px'}),
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
            id='trail-search-dropdown',
            options=load_trail_names(),
            searchable=True,
            placeholder='Search for trails...',
            style={
                'width':'600px',
                'padding': '12px',
                'margin-top': '10px',
                'margin-right': '16px',
                'font-size': '16px',
                'border-radius': '30px',
                'vertical-align':'center'
            }
        ),
        html.Div(id='trail-cards-row'),  # This is where the trail cards will be displayed
    ], style={'padding-top': '20px', 'margin-left': '20px'}),
    html.Div(id='trail-info'),
    #html.Div(id='mountain-backgrounds')
 
])
 
'''@app.callback(
    Output('mountain-backgrounds', 'children'),
    [Input('url', 'pathname')]
)
def update_background_images(pathname):
    if pathname == '/' or pathname == '/all-trails':
        return html.Div([
            html.Img(src=b64_image('src/assets/monutain_03.png'),
                style={
                'position': 'fixed',
                'bottom': '0',
                'right': '0',
                'width': '80%',
                'height': '100%',
                'background-size': 'cover',
                'background-attachment': 'fixed',
                'z-index': '-1',
            }),
            html.Img(src=b64_image('src/assets/monutain_02.png'),
                style={
                'position': 'fixed',
                'bottom': '0',
                'right': '0',
                'width': '80%',
                'height': '100%',
                'background-size': 'cover',
                'background-attachment': 'fixed',
                'z-index': '-1',
            }),
        ])
    else:
        return None'''
 
@app.callback(
    Output('trail-search-dropdown', 'style'),
    [Input('url', 'pathname')]
)
def toggle_search_visibility(pathname):
    if pathname == '/' or pathname == '/all-trails':
        return {
                'width':'600px',
                'padding': '12px',
                'margin-top': '10px',
                'margin-right': '16px',
                'font-size': '16px',
                'border-radius': '30px',
                'vertical-align':'center'
                }
    else:
        return {'display': 'none'}
   
@app.callback(
    [Output('trail-cards-row', 'children'),
     Output('trail-info', 'children')],
    [Input('url', 'pathname'),
     Input('trail-search-dropdown', 'value')]
)
def update_trail_info(pathname, search_input):
    url = pathname[1:]
    if len(url) == 0:
        if search_input is None or search_input == '':
            species_to_display = load_species_names()
        else:
            species_to_display = [{'label': search_input, 'value': search_input}]
 
        cards = [
            dbc.Col(create_species_card(species['value']))
            for species in species_to_display
        ]
        return html.Div(className='trail-cards', children=[
            dbc.Row(id='trail-cards-row', children=cards)
        ]), None
    else:
        splitname = [x.split('-') for x in url.split('---')]
        species_name = ' - '.join([' '.join(x) for x in splitname])
        trail = df[df['trail_species'].str.contains(species_name, case=False)]
        trail_name=trail['trail_name'].values[0]
        description = trail['trail_desc'].values[0]
        duration = trail['trail_duration'].values[0]
        elevation_gain = trail['trail_ele_gain'].values[0]
        distance = trail['trail_distance'].values[0]
        dist_mel = trail['trail_dist_mel'].values[0]
        time_mel = trail['trail_time_mel'].values[0]
        loop = trail['trail_loop'].values[0]
   
        return None, html.Div([
            dbc.Row([
                dcc.Link(html.I(className="fas fa-arrow-left", style={'margin-right': '5px'}), href='/'),
                dcc.Link('View all trails', href='/', className='active')
                ], style={'margin': '0 auto', 'padding': '40px'}),
            dbc.Row(html.H2(trail_name, style={'color': '#112434', 'text-decoration': 'none', 'margin-bottom': '15px',
                                               'margin-left':'40px'})),
            dbc.Row([
                dbc.Col(html.Img(src=b64_image(f"src/data/trail_img/{trail_name}.jpg"),
                                 style={'max-width': '100%', 'height': 'auto', 'max-height': '1000px', 'display': 'block'}), width=4),
                dbc.Col([
                    html.P(description, style={'margin-left': '30px', 'text-align': 'justify'}),
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.I(className="fas fa-clock", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '20px', 'margin-left':'30px'}),
                                html.Span(f"Duration: {duration}hours", style={'color': '#808080'}),
                                html.Div(""),
                                html.I(className="fas fa-mountain", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '30px', 'margin-top':'15px'}),  # Mountain icon
                                html.Span(f"Elevation Gain: {elevation_gain}m", style={'color': '#808080'}),
                                html.Div(""),
                                html.I(className="fas fa-route", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '30px', 'margin-top':'15px'}),  # Route icon
                                html.Span(f" Distance: {distance}km", style={'color': '#808080'}),
                            ], width=3),
                            dbc.Col([
                                html.I(className="fas fa-solid fa-car", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '20px', 'margin-left':'200px'}),
                                html.Span(f"Drive from Melbourne: {time_mel}hours", style={'color': '#808080'}),
                                html.Div(""),
                                html.I(className="fas fa-map-pin", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '15px', 'margin-left':'200px'}),
                                html.Span(f"Distance from Melbourne: {dist_mel}km", style={'color': '#808080'}),
                                html.Div(""),
                                html.I(className="fas fa-redo", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '15px', 'margin-left':'200px'}),
                                html.Span(f"Trail route: {loop}", style={'color': '#808080'}),
                            ], width=3),
                        ], style={'display': 'flex'}),
                ])], width=4)
            ], style={'margin': '0 30px', 'padding': '40px', 'display': 'flex', 'border': '1px solid', 'border-color': 'rgba(0, 0, 0, 0.2)', 'border-radius': '50px', 'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',})
      ])
       

 
 
 
if __name__ == '__main__':
    app.run_server(debug=True)