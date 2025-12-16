#!/usr/bin/env python3


def prompt(prompt_str, cast):
    s = input(prompt_str + ': ')
    try:
        value = cast(s)
    except ValueError:
        s = None
    if not s:
        print(f'Please enter a {str(cast)} value')
        return prompt(prompt_str, cast)
    return value


def get_room_dimensions():
    lx = prompt('Room size X', float)
    ly = prompt('Room size Y', float)
    lz = prompt('Room size Z', float)
    return [lx, ly, lz]


def get_base_size():
    return prompt('Base size', float)


def get_max_ref():
    return prompt('Max refinement level', int)


def surface_area(dims):
    x, y, z = dims
    return 2 * (x * y) + 2 * (x * z) + 2 * (y * z)


def room_volume(dims):
    x, y, z = dims
    return x * y * z


n_cells_between_refinements = 3

dims = get_room_dimensions()
base_size = get_base_size()
max_ref = get_max_ref()
min_size = base_size/2**max_ref

volume = room_volume(dims)
area = surface_area(dims)

n_base_cells = round(volume / base_size**3)
n_boundary_faces = round(area / min_size**2)

print()
print(f'Room volume    = {room_volume(dims)} m3')
print(f'Surface area   = {surface_area(dims)} m2')
print(f'Base cells     = {n_base_cells}')
print(f'Boundary faces = {n_boundary_faces}')

n_ref_cells = 0
for level in range(max_ref, 0, -1):
    size = base_size / 2**level
    print(f'Level {level} size   = {size}')
    level_cells = n_cells_between_refinements * (area / size**2)
    n_ref_cells += round(level_cells)

print(f'Total cells    = {n_base_cells + n_ref_cells}')


