#!/usr/bin/env python3
# ex_bezier_surface.py
from geomdl import BSpline
from geomdl import utilities
from geomdl import exchange

# Create a BSpline surface instance
surf = BSpline.Surface()

# Set evaluation delta
surf.delta = 0.01

# Set up the surface
surf.degree_u = 3
surf.degree_v = 2
control_points = [[0, 0, 0], [0, 1, 0], [0, 2, -3],
                  [1, 0, 6], [1, 1, 0], [1, 2, 0],
                  [2, 0, 0], [2, 1, 0], [2, 2, 3],
                  [3, 0, 0], [3, 1, -3], [3, 2, 0]]
surf.set_ctrlpts(control_points, 4, 3)
surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, 4)
surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, 3)

# Evaluate surface
surf.evaluate()

from geomdl.shapes import surface

# Generate cylindirical surface
surf2 = surface.cylinder(radius=5, height=12.5)

# Set evaluation delta
surf2.delta = 0.01

# Evaluate the surface
surf2.evaluate()

# Save surface as a .obj file
exchange.export_obj(surf2, "cylindirical_surf.obj")


# Save surface as a .obj file
exchange.export_obj(surf, "bezier_surf.obj")

