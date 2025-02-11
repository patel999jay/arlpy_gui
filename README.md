# arlpy_gui
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

### Overview
This tool provides a quick way to visualize the underwater acoustic environment based on user inputs using [arlpy](https://github.com/org-arl/arlpy).

The default values are initialized from the `create_env2d()` function of [arlpy](https://github.com/org-arl/arlpy):

```python
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
```

## Installation and Usage
To run this **Bokeh** application, use the following command:
  ```bash
  bokeh serve --show main.py --websocket-max-message-size 104857600
  ```
## Parameter Configuration
### Supported List Inputs
Currently, the following parameters accept **list inputs**:
- `soundspeed`
- `depth`

Use the format below when specifying lists:

```python
# Example list inputs

# Depth profile: [range, depth]
depth = [
    [0, 30],  # At range 0m, depth is 30m
    [300, 20],  # At range 300m, depth is 20m
    [1000, 25]  # At range 1000m, depth is 25m
]

# Sound speed profile: [depth, sound speed]
soundspeed = [
    [0, 1540],   # At depth 0m, sound speed is 1540 m/s
    [10, 1530],  # At depth 10m, sound speed is 1530 m/s
    [20, 1532],  # At depth 20m, sound speed is 1532 m/s
    [25, 1533],  # At depth 25m, sound speed is 1533 m/s
    [30, 1535]   # At depth 30m, sound speed is 1535 m/s
]
```

### Example Command for Running with Lists
If testing with list inputs, ensure they are formatted correctly:
```bash
# Example: Run simulation with custom depth and sound speed profiles
bokeh serve --show main.py --websocket-max-message-size 104857600
```

### Screenshot:
![arlpy_gui](https://github.com/patel999jay/arlpy_gui/assets/5512610/38875016-fcac-48ac-9a61-70b23f0fb26e)

Useful links
------------
1. [arlpy home](https://github.com/org-arl/arlpy)
2. [arlpy documentation](http://arlpy.readthedocs.io)
---
This project is licensed under the **MIT License**.
