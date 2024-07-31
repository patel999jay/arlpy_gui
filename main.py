# MIT License

# Copyright (c) 2023 Jay Patel

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# bokeh serve --show main.py

from bokeh.layouts import column, row
from bokeh.models import TextInput, PreText, TextAreaInput, Select, Button, Div
from bokeh.plotting import curdoc, figure
from bokeh.themes import built_in_themes  # Add this line
import arlpy.uwapm as pm
import arlpy.plot as plt
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

    def run_simulation(self):
        env_params = {}
        for key, val in self.params.items():
            if val == 'None' or val is None:
                env_params[key] = None
            elif key not in ['name', 'depth_interp', 'soundspeed_interp', 'surface_interp', 'tx_directionality', 'type']:
                env_params[key] = float(val)
            else:
                env_params[key] = val

        # Debugging: Print the environment parameters
        print("Environment parameters:", env_params)

        # Run simulation and generate plot using your Bellhop code
        try:
            env = pm.create_env2d(**env_params)
        except Exception as e:
            self.add_to_command_output(f"Error creating environment: {e}")
            return None, None, None, None, None

        try:
            p = plt.figure(title=env_params['name'] + ' env', xlabel="depth (m)", ylabel="range (m)", width=600, height=350)
            plt.hold(True)
            pm.plot_env(env)
            p = plt.gcf()
            p.title.align = "center"
            p.title.text_color = "black"
        except Exception as e:
            self.add_to_command_output(f"Error plotting environment: {e}")
            p = figure(title="Error plotting environment", width=600, height=350)

        try:
            rays = pm.compute_eigenrays(env)
            q = plt.figure(title=env_params['name'] + ' eigen rays', xlabel="depth (m)", ylabel="range (m)", width=600, height=350)
            pm.plot_rays(rays, env=env, width=900)
            q = plt.gcf()
            q.title.align = "center"
            q.title.text_color = "black"
        except Exception as e:
            self.add_to_command_output(f"Error computing or plotting eigenrays: {e}")
            q = figure(title="Error plotting eigen rays", width=600, height=350)

        try:
            arrivals = pm.compute_arrivals(env)
            r = plt.figure(title=env_params['name'] + ' arrivals', xlabel="amplitude", ylabel="arrival time (s)", width=600, height=350)
            pm.plot_arrivals(arrivals, width=900)
            r = plt.gcf()
            r.title.align = "center"
            r.title.text_color = "black"
        except Exception as e:
            self.add_to_command_output(f"Error computing or plotting arrivals: {e}")
            r = figure(title="Error plotting arrivals", width=600, height=350)

        try:
            rays = pm.compute_rays(env)
            s = plt.figure(title=env_params['name'] + ' rays', xlabel="depth (m)", ylabel="range (m)", width=600, height=350)
            pm.plot_rays(rays, env=env, width=600)
            s = plt.gcf()
            s.title.align = "center"
            s.title.text_color = "black"
        except Exception as e:
            self.add_to_command_output(f"Error computing or plotting rays: {e}")
            s = figure(title="Error plotting rays", width=600, height=350)

        try:
            t = plt.figure(title=env_params['name'] + ' SSP', xlabel="soundspeed (m/s)", ylabel="depth (m)",  width=600, height=350)
            plt.hold(True)
            pm.plot_ssp(env)
            t = plt.gcf()
            t.title.align = "center"
            t.title.text_color = "black"
        except Exception as e:
            self.add_to_command_output(f"Error plotting SSP: {e}")
            t = figure(title="Error plotting SSP", width=600, height=350)

        self.add_to_command_output("Simulation run with updated values.")

        return p, q, r, s, t

bellhop = BellhopSimulation()

# Update function for the Bokeh widgets
def update(attr, old, new):
    for key, widget in bellhop.widgets.items():
        value = widget.value
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
        else:
            bellhop.params[key] = float(value)

    p, q, r, s, t = bellhop.run_simulation()
    bellhop.add_to_command_output("Simulation updated.")

    layout.children[1].children[0] = p
    layout.children[1].children[1] = q
    layout.children[1].children[2] = r
    layout.children[2].children[0] = t
    layout.children[2].children[1] = s

bellhop.create_widgets()

# Connect the update function to the widget events
for widget in bellhop.widgets.values():
    widget.on_change('value', update)

def switch_theme(attr, old, new):
    curdoc().theme = new

theme_select = Select(title='Theme', options=list(built_in_themes), value='light_minimal')
theme_select.on_change('value', switch_theme)    

reset_button = Button(label="Reset to Default", button_type="success")
def reset_params():
    for key, widget in bellhop.widgets.items():
        widget.value = str(bellhop.params[key])
    bellhop.add_to_command_output("Parameters reset to default.")
reset_button.on_click(reset_params)

# Create the initial plots
p, q, r, s, t = bellhop.run_simulation()

# Ensure all plots are valid Bokeh figure objects
if p is None: p = figure(title="Error plotting environment", width=600, height=350)
if q is None: q = figure(title="Error plotting eigen rays", width=600, height=350)
if r is None: r = figure(title="Error plotting arrivals", width=600, height=350)
if s is None: s = figure(title="Error plotting rays", width=600, height=350)
if t is None: t = figure(title="Error plotting SSP", width=600, height=350)

# Create the layout
control_widgets = [widget for widget in bellhop.widgets.values()]
controls = column(*control_widgets, width=250)
layout = row(controls, column(p, q, r), column(t, s), column(bellhop.command_output, theme_select, reset_button))

# Add the layout to the current document
curdoc().add_root(layout)
curdoc().title = "Bellhop Simulation"
