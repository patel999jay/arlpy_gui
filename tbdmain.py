import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import arlpy.uwapm as pm
import arlpy.plot as plt
from bokeh.models import TextInput, PreText, TextAreaInput, Select
from bokeh.layouts import column, row
from bokeh.plotting import curdoc

class BellhopSimulation:
    def __init__(self):
        self.params = {
            'name': 'arlpy',
            'bottom_absorption': 0.1,
            'bottom_density': 1600,
            'bottom_roughness': 0,
            'bottom_soundspeed': 1600,
            'depth': 25,
            'depth_interp': 'linear',
            'frequency': 25000,
            'max_angle': 80,
            'min_angle': -80,
            'rx_depth': 10,
            'rx_range': 1000,
            'soundspeed': 1500,
            'soundspeed_interp': 'spline',
            'surface': None,
            'surface_interp': 'linear',
            'tx_depth': 5,
            'tx_directionality': None,
            'type': '2D'
        }
        self.command_output = PreText(text="Command output:", width=400, height=200)
        self.command_input = TextAreaInput(title="Enter command:", rows=5, width=400)

    def create_widgets(self):
        self.widgets = {}
        for key, value in self.params.items():
            if isinstance(value, str):
                widget = TextInput(value=value, title=key)
            else:
                widget = TextInput(value=str(value), title=key)
            self.widgets[key] = widget

    def get_simulation_params(self):
        params = {}
        for key, widget in self.widgets.items():
            if isinstance(widget, TextInput):
                params[key] = widget.value
        return params    

    def runSimulation(self):
        env_params = {}
        env_params['name'] = self.params['name']
        env_params['bottom_absorption'] = self.params['bottom_absorption']
        env_params['bottom_density'] = self.params['bottom_density']
        env_params['bottom_roughness'] = self.params['bottom_roughness']
        env_params['bottom_soundspeed'] = self.params['bottom_soundspeed']
        env_params['depth'] = self.params['depth']
        env_params['depth_interp'] = self.params['depth_interp']
        env_params['frequency'] = self.params['frequency']
        env_params['max_angle'] = self.params['max_angle']
        env_params['min_angle'] = self.params['min_angle']
        env_params['rx_depth'] = self.params['rx_depth']
        env_params['rx_range'] = self.params['rx_range']
        env_params['soundspeed'] = self.params['soundspeed']
        env_params['soundspeed_interp'] = self.params['soundspeed_interp']
        env_params['surface'] = self.params['surface']
        env_params['surface_interp'] = self.params['surface_interp']
        env_params['tx_depth'] = self.params['tx_depth']
        env_params['tx_directionality'] = self.params['tx_directionality']

        # Run simulation and generate plot using your Bellhop code
        # Replace the following code with your Bellhop simulation code and plot generation
        env = pm.create_env2d(**env_params)

        fig = plt.figure(title=env_params['name'], width=600, height=350)
        plt.hold(True)
        pm.plot_env(env)
        fig = plt.gcf()

        return fig

bellhop = BellhopSimulation()

# Update function for the Bokeh widgets
def update(attr, old, new):
    for key, widget in bellhop.widgets.items():
        if isinstance(widget, TextInput):
            value = widget.value
            # Convert value to the appropriate data type
            if value == 'None':
                bellhop.params[key] = None
            elif key in ['name', 'depth_interp', 'soundspeed_interp', 'surface_interp', 'tx_directionality', 'type']:
                bellhop.params[key] = value
            else:
                bellhop.params[key] = float(value)
    fig = bellhop.runSimulation()
    layout.children[1] = dcc.Graph(figure=fig)

def switch_theme(value, old, new):
    curdoc().theme = new

theme_select = Select(title='Theme', options=['caliber', 'dark_minimal', 'light_minimal'])
theme_select.on_change('value', switch_theme)

# Button callbacks
def plot_rays():
    # Implement your code to plot rays here
    pass

def plot_eigenrays():
    # Implement your code to plot eigenrays here
    pass

def plot_arrivals():
    # Implement your code to plot arrivals here
    pass

# Create the Bokeh plot
fig = bellhop.runSimulation()
graph = dcc.Graph(figure=fig)

bellhop.create_widgets()

# Connect the update function to the widget events
for widget in bellhop.widgets.values():
    widget.on_change('value', update)

# Create the layout
control_widgets = [widget for widget in bellhop.widgets.values()]
controls = column(*control_widgets, width=250)
button_row = html.Div([
    html.Button('Plot Rays', id='plot-rays-btn', n_clicks=0),
    html.Button('Plot Eigenrays', id='plot-eigenrays-btn', n_clicks=0),
    html.Button('Plot Arrivals', id='plot-arrivals-btn', n_clicks=0)
])
layout = row(controls, column(graph, button_row))

app = dash.Dash(__name__)
app.layout = layout

# Button callbacks
@app.callback(
    Output('plot-rays-btn', 'n_clicks'),
    Output('plot-eigenrays-btn', 'n_clicks'),
    Output('plot-arrivals-btn', 'n_clicks'),
    [Input('plot-rays-btn', 'n_clicks'),
     Input('plot-eigenrays-btn', 'n_clicks'),
     Input('plot-arrivals-btn', 'n_clicks')]
)
def update_plots(ray_btn_clicks, eigenrays_btn_clicks, arrivals_btn_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'plot-rays-btn':
        plot_rays()
        return ray_btn_clicks + 1, eigenrays_btn_clicks, arrivals_btn_clicks
    elif button_id == 'plot-eigenrays-btn':
        plot_eigenrays()
        return ray_btn_clicks, eigenrays_btn_clicks + 1, arrivals_btn_clicks
    elif button_id == 'plot-arrivals-btn':
        plot_arrivals()
        return ray_btn_clicks, eigenrays_btn_clicks, arrivals_btn_clicks + 1
    else:
        return ray_btn_clicks, eigenrays_btn_clicks, arrivals_btn_clicks

if __name__ == '__main__':
    app.run_server(debug=True)
