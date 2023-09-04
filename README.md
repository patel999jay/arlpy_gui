# arlpy_gui

This is just a tool that can quickly plot the underwater enviornment from user inputs using [arlpy](https://github.com/org-arl/arlpy).

It is initially assigned the default values from `create_env2d()` function from [arlpy](https://github.com/org-arl/arlpy).

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
currently only params - `soundspeed`,`depth` takes list as input.
```bash
# currently use this for testing, refer screenshot below for more details.
depth = [[0, 30],     [300, 20],   [2000, 25]]
soundspeed =  [[ 0, 1540], [10, 1530], [20, 1532], [25, 1533], [30, 1535] ]
```


- To run this python bokeh application, use below command :
  ```bash
  bokeh serve --show main.py
  ```

### Screenshot:
![arlpy_gui](https://github.com/patel999jay/arlpy_gui/assets/5512610/38875016-fcac-48ac-9a61-70b23f0fb26e)

Useful links
------------
1. [arlpy home](https://github.com/org-arl/arlpy)
2. [arlpy documentation](http://arlpy.readthedocs.io)
