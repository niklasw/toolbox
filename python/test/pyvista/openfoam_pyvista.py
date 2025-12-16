#!/usr/bin/env python3

import sys
import pyvista as pv
from pyvista import examples

SLICE_ACTOR = {'actor': None, 'visible': False}
MESH_ACTOR = {'actor': None, 'visible': True}

def create_scene(plotter):
    plotter.add_floor(face='-z',
                      i_resolution=10, j_resolution=10,
                      color='lightgray',
                      line_width=1,
                      opacity=0.5,
                      show_edges=True,
                      lighting=False,
                      edge_color='black',
                      reset_camera=True,
                      pad=0.5,
                      offset=0.1,
                      pickable=False)


def press_key_event(plotter, key):
    """
    Callback function to handle key press events for camera positioning.

    'x': XY Plane view (Z-axis is up)
    'y': YZ Plane view (X-axis is up)
    'z': XZ Plane view (Y-axis is up)
    """
    print(f"Key pressed: {key}")

    # PyVista camera positions:
    # 'xy': View from positive Z-axis.
    # 'yz': View from positive X-axis.
    # 'xz': View from positive Y-axis.

    if key == 'z':
        plotter.camera_position = 'xy'
    elif key == 'x':
        plotter.camera_position = 'yz'
    elif key == 'y':
        plotter.camera_position = 'xz'

    elif key == 'c':
        # Toggle the slice visibility
        slice_visibility = SLICE_ACTOR['visible']
        if SLICE_ACTOR['actor'] is not None:
            slice_visibility = SLICE_ACTOR['visible']
            SLICE_ACTOR['actor'].SetVisibility(not slice_visibility)
            SLICE_ACTOR['visible'] = not slice_visibility
            print(f"Slice visibility set to: {SLICE_ACTOR['visible']}")
        if MESH_ACTOR['actor'] is not None:
            slice_visibility = MESH_ACTOR['visible']
            MESH_ACTOR['actor'].SetVisibility(not slice_visibility)
            MESH_ACTOR['visible'] = not slice_visibility
            print(f"Mesh visibility set to: {MESH_ACTOR['visible']}")

    plotter.render()

def read_openfoam_case(case_path):
    """Read an OpenFOAM case file and return a PyVista dataset."""
    reader = pv.POpenFOAMReader(case_path)
    reader.case_type = 'decomposed'
    reader.set_active_time_value(1220)
    dataset = reader.read()
    return dataset['internalMesh'], dataset['boundary']


def extract_internal_mesh(dataset):
    """Extract the internal mesh from the OpenFOAM dataset."""
    internal_mesh = dataset.extract_cells(dataset.cell_arrays['internalMesh'] == 1)
    return internal_mesh


def add_temperature_slice(plotter, dataset, scalar_name='T'):
    """
    Adds a slice through the center of the dataset colored by temperature.
    Returns the slice actor for later manipulation (e.g., toggling visibility).
    """
    if scalar_name not in dataset.point_data \
                   and scalar_name not in dataset.cell_data:
        print(f"Error: Scalar '{scalar_name}' not found in the dataset. Cannot add slice.")
        return None

    slice_mesh = dataset.slice(normal=[1, 0, 0])

    actor = plotter.add_mesh(slice_mesh,
                             scalars=scalar_name,
                             cmap='viridis',
                             show_edges=False,
                             name='Temperature_Slice')

    actor.SetVisibility(False)

    # Update the global tracking variable
    SLICE_ACTOR['actor'] = actor
    SLICE_ACTOR['visible'] = False

    return actor


def add_mesh_actor(plotter, dataset, scalar_name='T'):
    """Adds the main mesh actor to the plotter."""
    actor = plotter.add_mesh(dataset,
                             scalars=scalar_name,
                             cmap='viridis',
                             opacity=1,
                             show_edges=True,
                             name='Main_Mesh')

    # Update the global tracking variable
    MESH_ACTOR['actor'] = actor
    MESH_ACTOR['visible'] = True

    return actor


def visualize_openfoam_case(dataset):
    """Visualize the OpenFOAM dataset using PyVista."""
    plotter = pv.Plotter()

    # --- Register the key press event handler ---
    # The key_press_event is registered to call press_key_event
    # with the plotter and the key character.
    plotter.add_key_event('x', lambda: press_key_event(plotter, 'x'))
    plotter.add_key_event('y', lambda: press_key_event(plotter, 'y'))
    plotter.add_key_event('z', lambda: press_key_event(plotter, 'z'))
    plotter.add_key_event('c', lambda: press_key_event(plotter, 'c'))
    # You can also add a help key like 'h'
    plotter.add_key_event('h', lambda: print("\nControls:\nx - XY View\ny - YZ View\nz - XZ View\n"))

    if 'T' in dataset.point_data or 'T' in dataset.cell_data:
        scalar_name = 'T'
        title = 'Temperature'
        add_mesh_actor(plotter, dataset, scalar_name=scalar_name)
        add_temperature_slice(plotter, dataset, scalar_name=scalar_name)
    else:
        scalar_name = None
        title = 'Dataset'
        print("Warning: 'T' scalar not found. Visualizing geometry only.")
        plotter.add_mesh(dataset, show_edges=True) # Just show the mesh outline

    create_scene(plotter)
    plotter.show()

if __name__ == "__main__":
    # Example OpenFOAM case file path (replace with your own case file)
    case_file_path = sys.argv[1] if len(sys.argv) > 1 else \
        '/home/niklas/F/ice-cases/cfd-dev/attefall2/cfd/v13/setup.foam'
    
    # Read the OpenFOAM case
    internalBlock, boundaryBlock = read_openfoam_case(case_file_path)

    # Visualize the dataset
    visualize_openfoam_case(internalBlock)
