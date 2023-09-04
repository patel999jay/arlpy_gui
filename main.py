# MIT License

# Copyright (c) 2023 Jay Patel

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# bokeh serve --show main.py

from bokeh.layouts import column, row
from bokeh.models import TextInput, PreText, TextAreaInput, CheckboxGroup, CustomJS
from bokeh.plotting import curdoc, figure
import arlpy.uwapm as pm
import arlpy.plot as plt
from bokeh.models import Select
from bokeh.themes import Theme, built_in_themes
import json
import numpy as np

class BellhopSimulation:
    def __init__(self):
        self.params = {
            'name': 'arlpy',
            'bottom_absorption': 0.1,
            'bottom_density': 1600,
            'bottom_roughness': 0,
            'bottom_soundspeed': 1600,
            'depth': 30,
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
        self.last_command_output = None

    def add_to_command_output(self, text):
        # self.command_output.text += "\n" + text
        if text != self.last_command_output:
            self.command_output.text += "\n" + text
            self.last_command_output = text

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

        p = plt.figure(title=env_params['name'] + ' env', xlabel="depth (m)", ylabel="range (m)", width=600, height=350)
        plt.hold(True)
        pm.plot_env(env)
        p = plt.gcf()
        p.title.align = "center"
        p.title.text_color = "black"

        # Compute and plot rays
        rays = pm.compute_eigenrays(env)
        q = plt.figure(title=env_params['name'] + ' eigen rays', xlabel="depth (m)", ylabel="range (m)", width=600, height=350)
        pm.plot_rays(rays, env=env, width=900)
        q = plt.gcf()
        q.title.align = "center"
        q.title.text_color = "black"

        # Compute Arrivals
        arrivals = pm.compute_arrivals(env)
        r = plt.figure(title=env_params['name'] + ' arrivals', xlabel="amplitude", ylabel="arrival time (s)", width=600, height=350)
        pm.plot_arrivals(arrivals, width=900)
        r = plt.gcf()
        r.title.align = "center"
        r.title.text_color = "black"

        # Compute and plot rays
        rays = pm.compute_rays(env)
        s = plt.figure(title=env_params['name'] + ' rays', xlabel="depth (m)", ylabel="range (m)", width=600, height=350)
        pm.plot_rays(rays, env=env, width=600)
        s = plt.gcf()
        s.title.align = "center"
        s.title.text_color = "black"

        #Plot the SSP
        t = plt.figure(title=env_params['name'] + ' SSP', xlabel="soundspeed (m/s)", ylabel="depth (m)",  width=600, height=350)
        plt.hold(True)
        pm.plot_ssp(env)
        t = plt.gcf()
        t.title.align = "center"
        t.title.text_color = "black"

        # print("Env : ", type(env_params))
        bellhop.add_to_command_output(f"simulation run with default values.")

        return p, q, r, s, t

bellhop = BellhopSimulation()


# Update function for the Bokeh widgets
def update(attr, old, new):

    for key, widget in bellhop.widgets.items():
        if isinstance(widget, TextInput):
            value = widget.value
            # Convert value to the appropriate data type
            if value == 'None':
                bellhop.params[key] = None
            elif key in ['soundspeed', 'depth']:
                try:
                    bellhop.params[key] = json.loads(value)
                except json.JSONDecodeError:
                    bellhop.add_to_command_output(f"Invalid JSON entered for {key}.")
                    print(f"Invalid JSON entered for {key}.")
                continue   
            elif key in ['name', 'depth_interp', 'soundspeed_interp', 'surface_interp', 'tx_directionality', 'type']:
                bellhop.params[key] = value
            elif key == 'rx_range':
                bellhop.params[key] = float(value)
            elif key == 'rx_depth':
                bellhop.params[key] = float(value)    
            else:
                bellhop.params[key] = float(value)
    # try:
    #     bellhop.params[key] = json.loads(value)
    # except json.JSONDecodeError:
    #     bellhop.add_to_command_output(f"Invalid JSON entered for {key}.")
    #     print(f"Invalid JSON entered for {key}.")

    p, q, r, s, t = bellhop.runSimulation()
    bellhop.add_to_command_output(f"simulation updated.")

    # layout.children[1] = p
    layout.children[1].children[0] = p
    layout.children[1].children[1] = q  # Update the second plot
    layout.children[1].children[2] = r  # Update the third plot
    layout.children[2].children[0] = t  # Update the forth plot
    layout.children[2].children[1] = s  # Update the fifth plot

# Create the Bokeh plot
# p = bellhop.runSimulation()
p, q, r, s, t = bellhop.runSimulation()

bellhop.create_widgets()

# Connect the update function to the widget events
for widget in bellhop.widgets.values():
    widget.on_change('value', update)

def switch_theme(value, old, new):
    curdoc().theme = new

theme_select = Select(title='Theme', options=['caliber',
                                              'dark_minimal', 
                                              'light_minimal'])
theme_select.on_change('value', switch_theme)    

# Create the layout
control_widgets = [widget for widget in bellhop.widgets.values()]
controls = column(*control_widgets, width=250)
# layout = row(controls, p, theme_select)
# layout = row(controls, p)
# layout = column(row(controls, column(p, q, r)), row(s,s,s)) # need to change this.
layout = row(controls, column(p, q, r), column(t, s), column(bellhop.command_output)) # checkbox_group

# Add the layout to the current document
# curdoc().theme = './theme.yaml'
curdoc().add_root(layout)
curdoc().title = "Bellhop Simulation"
