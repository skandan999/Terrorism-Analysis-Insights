
#importing the libraries
import pandas as pd
import webbrowser

import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
external_stylesheets=[dbc.themes.BOOTSTRAP])
TAB_STYLE = {
    #'width': 'inherit',
    'border': 'none',
    'boxShadow': 'inset 0px -1px 0px 0px lightgrey',
   # 'background': 'black',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '42px',
    'font-style': 'Ubuntu', 
    'font-weight': 'bold',
    'color': 'black',
    
}

SELECTED_STYLE = {
    'boxShadow': 'none',
    'borderLeft': 'none',
    'borderRight': 'none',
    'borderTop': 'none',
    'borderBottom': '2px #004A96 solid',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '42px',
    'font-style': 'Ubuntu', 
    'font-weight': 'bold',
    'color': 'black',
}
dropdown = { 
    'width' : '700px', 
   'text-align' : 'center', 
    'vertical-align' : 'center', 
    'margin-left' : '210px' }

# Global variables
app = dash.Dash()


def load_data():
  dataset_name = "global_terror.csv"

  #this line we use to hide some warnings which gives by pandas
  pd.options.mode.chained_assignment = None
  
  global df
  df = pd.read_csv(dataset_name)
  
  #pd.set_option("display.max_rows", None)
  #pd.set_option('display.max_columns', None)
  print(df.head(5))
  print(df.tail(5))

  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [x for x in range(1, 32)]


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  #region_list.insert(0, {"label":"All", "value":"All"} )

  #print(region_list)  
  # Total 12 Regions

  global country_list
  #country_list = [{"label": str(i), "value": str(i)}  for i in sorted(df['country_txt'].unique().tolist())]
  #print(country_list)
  # Total 205 Countries
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()


  global state_list
  #state_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
  #print(state_list)
  # Total 2580 states
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()


  global city_list
  #city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
  #print(city_list)
  # Total 39489 cities
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()


  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  #print(attack_type_list)


  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  #print(year_dict)
  
  #chart dropdown options
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app8_ui():
  # Create the UI of the Webpage here
  main_layout = html.Div(
      style={"background-color": "#f6f6f6"},
      children=[
  html.H1(style={'textAlign': 'center', 'color': 'black', 'font-family': 'Montserrat', 'font-weight': "900","background-color": "#111d56","margin":"0","padding-top": "7px","padding-bottom": "7px", "color": "#d6e0f0","padding-bottom": "10px",
                "padding-top": "10px",}, children = 'Terrorism Analysis with Insights', id='Main_title'),
  dcc.Tabs(id="Tabs", value="Map",children=[
      dcc.Tab(label="Map tool" ,id="Map Tool",value="Map", className='tab-style',
                selected_className='selected-tab-style', children=[
          dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap", style=TAB_STYLE,
                selected_style=SELECTED_STYLE,),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap", style=TAB_STYLE,
                selected_style=SELECTED_STYLE,)
              ]),
          dcc.Dropdown(
              id='month', 
                options=month_list,
                placeholder='Select Month',
                multi = True,
                style = dropdown,
                  ),
          dcc.Dropdown(
                id='date', 
                placeholder='Select Day',
                multi = True,
                style = dropdown,
                  ),
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='Select Region',
                multi = True,
                style = dropdown,
                  ),
          dcc.Dropdown(
                id='country-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select Country',
                multi = True,
                style = dropdown
                  ),
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True,
                style = dropdown,
                  ),
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True,
                style = dropdown
                  ),
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                placeholder='Select Attack Type',
                multi = True,
                style = dropdown
                  ),
           
          html.H5('Select the Year in the Slider',
             style={'textAlign': 'left',
            'color': '#d6e0f0',
            'background-color': '#192b81',
            'padding': '10px',
            'font-family': 'Fira Sans',
            'font-weight':'bold',
            }, id='year_title'),
          dcc.RangeSlider(
                    id='year-slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None,
                    
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart",className='tab-style',
                selected_className='selected-tab-style' ,children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
            dcc.Tab(label="World Chart Tool", id="WorldC",  value="WorldChart", style=TAB_STYLE,
                ),          
            dcc.Tab(label="India Chart Tool", id="IndiaC", value="IndiaChart",style=TAB_STYLE,
                )
            
              ]
              ),
            html.H5('Pick the desired filter ', id='filters',style={
            'textAlign': 'left',
            'color': '#d6e0f0',
            'background-color': '#192b81',
            'padding': '10px',
            'font-family': 'Fira Sans',
            'font-weight':'bold',
            }),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
            html.Br(),
            html.Br(),
            html.Hr(),
            html.Center( dcc.Input(id="search", placeholder="Search Filter",style={
                "width":"95%",
                "padding-bottom": "10px",
                "padding-top": "10px",
               
                }
                ) 
            ),                                               
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
              ]),
         ]),
  html.Div(id = "graph-object", children ="Graph will be shown here"),
  
  html.Footer(id= "copyright",
        style={"padding-bottom": "1px", 'background-color': '#192b81'},
        children=[
            html.H3(style={"text-align": "center"},
                    children=[
                            html.H3(children="© 2020 Skandan.",style={"display": "inline", "color": "#EAF6F6", "font-size": "0.75rem"}),
                ]) 
            ])
  ])
  
        
  return main_layout


# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('cyear_slider', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )

def update_app9_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        
         # You should always set the figure for blank, since this callback 
         # is called once when it is drawing for first time        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(
          
          
          
        mapbox_style="white-bg",
        mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }

      ])
        mapFigure.update_layout(margin={"r":0,"t":25,"l":0,"b":25}) 
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)



@app.callback(
  Output("date", "options"),
  [Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of your Project
def main8():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app8_ui()
  app.title = "Terrorism Analysis with Insights"
  # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
  app.run_server() # debug=True

  print("This would be executed only after the script is closed")
  df = None
  app = None

app.css.config.serve_locally = True

if __name__ == '__main__':
    main8()
