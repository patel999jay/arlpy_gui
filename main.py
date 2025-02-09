# MIT License

# Copyright (c) 2025 Jay Patel

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# bokeh serve --show main.py --websocket-max-message-size 104857600 

import warnings

# Suppress specific Bokeh deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*asterisk\\(\\) method.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*circle\\(\\) method.*")

from bokeh.layouts import column, row
from bokeh.models import TextInput, PreText, TextAreaInput, Select, Button, Div
from bokeh.plotting import curdoc, figure
from bokeh.themes import built_in_themes  

import arlpy.uwapm as pm
import arlpy.plot as plt
import json
import numpy as np
import ast

class BellhopSimulation:
    """Class to handle Bellhop underwater acoustic simulations."""
    def __init__(self):
        """
        Initializes the BellhopSimulation class with default parameters.
        """
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
        """
        Appends new text to the command output area.
        
        Args:
            text (str): The text to be appended to the output log.
        """
        if text != self.last_command_output:
            self.command_output.text += "\n" + text
            self.last_command_output = text

    def create_widgets(self):
        """
        Creates Bokeh input widgets for each simulation parameter.
        """
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
        """
        Runs the Bellhop acoustic simulation using the provided parameters.
        
        Returns:
            Tuple of Bokeh figures representing different simulation results.
        """
        env_params = {}
        for key, val in self.params.items():
            if val == 'None' or val is None:
                env_params[key] = None
            elif key in ['depth', 'soundspeed']:
                try:
                    if isinstance(val, str):  # Convert only if it's a string
                        try:
                            env_params[key] = json.loads(val)
                        except json.JSONDecodeError:
                            self.add_to_command_output(f"Invalid JSON format for {key}.")
                            return None, None, None, None, None, None
                    else:
                        env_params[key] = val  # If already a list, use it directly
                except json.JSONDecodeError:
                    self.add_to_command_output(f"Invalid JSON format for {key}.")
                    return None, None, None, None, None, None
            elif key not in ['name', 'depth_interp', 'soundspeed_interp', 'surface_interp', 'tx_directionality', 'type']:
                try:
                    env_params[key] = float(val)
                except ValueError:
                    self.add_to_command_output(f"Invalid value for {key}, expected a number.")
                    return None, None, None, None, None, None
            else:
                env_params[key] = val


        # Debugging: Print the environment parameters
        print("Environment parameters:", env_params)

        # Run simulation and generate plot using your Bellhop code
        try:
            env = pm.create_env2d(**env_params)
        except Exception as e:
            self.add_to_command_output(f"Error creating environment: {e}")
            return None, None, None, None, None, None

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

        try:
            # Place receivers in a grid to visualize the acoustic pressure field
            env['rx_range'] = np.linspace(0, 1000, 1001)
            env['rx_depth'] = np.linspace(0, 30, 301)
            tloss = pm.compute_transmission_loss(env, mode='incoherent')
            u = plt.figure(title=env_params['name'] + ' transmission loss', xlabel="range (m)", ylabel="depth (m)", width=600, height=350)
            pm.plot_transmission_loss(tloss, env=env, clim=[-60, -30], width=350)
            u = plt.gcf()
            u.title.align = "center"
            u.title.text_color = "black"
        except Exception as e:
            self.add_to_command_output(f"Error computing or plotting transmission loss: {e}")
            u = figure(title="Error plotting transmission loss", width=600, height=350)

        self.add_to_command_output("Simulation run with updated values.")

        return p, q, r, s, t, u

bellhop = BellhopSimulation()

def parse_numpy_expression(expression):
    """
    Safely parse NumPy expressions from user input.
    """
    try:
        # Remove surrounding quotes if present
        if isinstance(expression, str):
            expression = expression.strip('"').strip("'")
        
        # Parse using ast.literal_eval for basic safety
        parsed_value = eval(expression, {"np": np, "array": np.array, "linspace": np.linspace, "sin": np.sin, "pi": np.pi})

        if isinstance(parsed_value, np.ndarray):
            return parsed_value  # Return the actual NumPy array
        else:
            print(f"Error: Expected a NumPy array, got {type(parsed_value)}")
            return None
    except Exception as e:
        print(f"Error parsing numpy expression: {e}")
        return None

def reset_params():
    for key, widget in bellhop.widgets.items():
        widget.value = str(bellhop.params[key])
    bellhop.add_to_command_output("Parameters reset to default.")
        
def switch_theme(attr, old, new):
    """
    Switches the Bokeh theme.
    
    Args:
        attr (str): The attribute being modified.
        old: The previous theme.
        new: The new theme.
    """
    curdoc().theme = new
    
# Update function for the Bokeh widgets
def update(attr, old, new):
    """
    Updates simulation parameters and reruns the simulation when a widget value changes.
    
    Args:
        attr (str): The attribute name being modified.
        old: The previous value of the attribute.
        new: The new value of the attribute.
    """
    for key, widget in bellhop.widgets.items():
        value = widget.value
        if value == 'None':
            bellhop.params[key] = None  
        elif key in ['soundspeed', 'depth']:
            try:
                parsed_value = json.loads(value)
                if isinstance(parsed_value, list):
                    bellhop.params[key] = parsed_value
                else:
                    bellhop.add_to_command_output(f"Invalid format for {key}, expected a list.")
                    print(f"Invalid format for {key}, expected a list.")
            except json.JSONDecodeError:
                bellhop.add_to_command_output(f"Invalid JSON entered for {key}.")
                print(f"Invalid JSON entered for {key}.")
            continue
        elif key == 'surface':
            try:
                # Parse the numpy expression safely
                surface_data = parse_numpy_expression(value)
                if surface_data is not None and isinstance(surface_data, np.ndarray):
                    bellhop.params[key] = surface_data
                else:
                    print("Invalid surface input. Using default value.")
                    bellhop.params[key] = None
            except Exception as e:
                print(f"Error processing surface input: {e}")
                bellhop.params[key] = None   
        elif key in ['name', 'depth_interp', 'soundspeed_interp', 'surface_interp', 'tx_directionality', 'type']:
            bellhop.params[key] = value
        else:
            if key == 'surface':
                parsed_value = parse_numpy_expression(value)
                if parsed_value is not None:
                    bellhop.params[key] = parsed_value
                else:
                    print(f"Invalid input for {key}. Using default value.")
                    bellhop.params[key] = None
            elif isinstance(value, str) and value.startswith("["):
                try:
                    bellhop.params[key] = json.loads(value)  # Handle lists correctly
                except json.JSONDecodeError:
                    print(f"Invalid JSON format for {key}. Expected list.")
                    bellhop.params[key] = None
            elif isinstance(value, np.ndarray):
                bellhop.params[key] = value  # Keep NumPy arrays
            else:
                try:
                    bellhop.params[key] = float(value)  # Convert only scalars
                except ValueError:
                    print(f"Invalid format for {key}, expected a float.")



    p, q, r, s, t, u = bellhop.run_simulation()
    bellhop.add_to_command_output("Simulation updated.")

    layout.children[1].children[0] = p
    layout.children[1].children[1] = q
    layout.children[1].children[2] = r
    layout.children[2].children[0] = t
    layout.children[2].children[1] = s
    layout.children[2].children[2] = u

bellhop.create_widgets()

# Connect the update function to the widget events
for widget in bellhop.widgets.values():
    widget.on_change('value', update)

theme_select = Select(title='Theme', options=list(built_in_themes), value='light_minimal')
theme_select.on_change('value', switch_theme)    

reset_button = Button(label="Reset to Default", button_type="success")


reset_button.on_click(reset_params)

# Additional Widgets
export_button = Button(label="Export Results", button_type="primary")
def export_results():
    # Implement export functionality
    bellhop.add_to_command_output("Results exported.")
export_button.on_click(export_results)

presets_select = Select(title='Presets', options=['Preset 1', 'Preset 2', 'Preset 3'], value='Preset 1')
def load_preset(attr, old, new):
    preset_values = {
        'Preset 1': {'bottom_absorption': 0.1, 'bottom_density': 1600, 'bottom_soundspeed': 1600},
        'Preset 2': {'bottom_absorption': 0.2, 'bottom_density': 1700, 'bottom_soundspeed': 1650},
        'Preset 3': {'bottom_absorption': 0.3, 'bottom_density': 1800, 'bottom_soundspeed': 1700}
    }
    for key, value in preset_values[new].items():
        bellhop.widgets[key].value = str(value)
    bellhop.add_to_command_output(f"Preset {new} loaded.")
presets_select.on_change('value', load_preset)

# Create the initial plots
p, q, r, s, t, u = bellhop.run_simulation()

# Ensure all plots are valid Bokeh figure objects
if p is None: p = figure(title="Error plotting environment", width=600, height=350)
if q is None: q = figure(title="Error plotting eigen rays", width=600, height=350)
if r is None: r = figure(title="Error plotting arrivals", width=600, height=350)
if s is None: s = figure(title="Error plotting rays", width=600, height=350)
if t is None: t = figure(title="Error plotting SSP", width=600, height=350)
if u is None: u = figure(title="Error plotting transmission loss", width=600, height=350)

# Create the layout
control_widgets = [widget for widget in bellhop.widgets.values()]
controls = column(*control_widgets, width=250)
extra_controls = column(presets_select, export_button, theme_select, reset_button)
layout = row(controls, column(p, q, r), column(t, s, u), column(bellhop.command_output), column(extra_controls))

# Add the layout to the current document

curdoc().add_root(layout)
curdoc().title = "Bellhop Simulation"


# In depth: [[0, 30],[300, 20], [1000, 25]]
# In soundspeed : [ [ 0, 1540], [10, 1530],  [20, 1532], [25, 1533],  [30, 1535] ]
