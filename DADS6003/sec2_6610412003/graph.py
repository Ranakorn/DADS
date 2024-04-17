#Reference: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash%20Components/Graph/dash-graph.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import random
import pandas as pd

df = px.data.gapminder()
def generate_random_hex_colors(num_colors):
    random_colors = []
    for _ in range(num_colors):        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        random_colors.append(hex_color)
    
    return random_colors

unique_countries = df['country'].unique()
random_color_list = generate_random_hex_colors(len(unique_countries))
country_colors = {country: random_color_list[i % len(random_color_list)] for i, country in enumerate(unique_countries)}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['Germany','Brazil'], multi=True, options=[{'label': x, 'value': x} for x in df.country.unique()]),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  ),
        dcc.Graph(id='bar-graph', figure={}, className='six columns')
    ])
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(country_chosen):
    dff = df[df.country.isin(country_chosen)]    
    fig = px.line(data_frame=dff, x='year', y='gdpPercap', color='country', hover_data=["lifeExp", "pop", "iso_alpha"],color_discrete_map=country_colors)
    fig.update_traces(mode='lines+markers')    

    return fig

# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')  
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen):
    if hov_data is None:
        dff2 = df[df.country.isin(country_chosen)]
        dff2 = dff2[dff2.year == 1952]        
        fig2 = px.pie(data_frame=dff2, values='pop', names='country',color='country', title='Population for 1952',color_discrete_map=country_colors)

        return fig2

    else:
        #print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        #print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = df[df.country.isin(country_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        fig2 = px.pie(data_frame=dff2, values='pop', names='country',color='country', title=f'Population for: {hov_year}',color_discrete_map=country_colors)
   
        return fig2

@app.callback(
    Output(component_id='bar-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_bar_chart(selected_data, country_chosen):
    if selected_data is not None:
        selected_countries = [point['customdata'][2] for point in selected_data['points']]
        selected_years = [point['x'] for point in selected_data['points']]
        print('data row',selected_countries)
        print('year:',selected_years)

        selected_data_df = pd.DataFrame({
            'country': [df.loc[df['iso_alpha'] == country, 'country'].iloc[0] for country in selected_countries],
            'year': selected_years,
            'gdpPercap': [df.loc[(df['iso_alpha'] == country) & (df['year'] == year), 'gdpPercap'].iloc[0] for
                          country, year in zip(selected_countries, selected_years)]
        })
        print('selected_data_df:', selected_data_df)

        fig_bar = px.bar(
            data_frame=selected_data_df,
            x='year',
            y='gdpPercap',
            color='country',
            barmode='group',
            title='GDP per Capita for Selected Countries',
            color_discrete_map=country_colors
        )

        return fig_bar

    # Return an empty figure if no data is selected
    return {}

if __name__ == '__main__':
    app.run_server(debug=True)

'''
GDP Per Capita คือ ผลิตภัณฑ์มวลรวมในประเทศต่อหัว หรือ GDP ต่อหัว 
เป็นตัวเลขที่บอกว่าค่าเฉลี่ยของ GDP เมื่อเทียบกับคนในประเทศแล้ว โดยเฉลี่ยคนหนึ่งคนสามารถสร้างมูลค่า GDP ขึ้นมาเท่าไหร่ 
และแน่นอนว่า GDP per capita คือ ตัวเลขที่คำนวณมาจาก ค่า GDP ÷ จำนวนประชากร

iso_alpha
The 3-letter ISO 3166-1 alpha-3 code.

iso_num
The 3-digit ISO 3166-1 numeric-3 code.

อายุคาดเฉลี่ย (Life Expectancy) : LE หรือ Life Expectancy หมายถึง
การคาดประมาณจำนวนปีโดยเฉลี่ยของการมีชีวิตอยู่ของประชากร
'''

