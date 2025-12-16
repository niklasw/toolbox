#!/usr/bin/env python3
import h5py
from pathlib import Path
import argparse
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl


def find_array_interval(sequence: list, value: float):
    '''Returns the "left" element of the interval in which value resides and
    the interpolation weight needed to blend left and right sequence values.
    If value lies outside of sequence, corresponding end point is returned.
    No extrapolation is done (or call it "constant extrapolation")'''
    if value <= sequence[0]:
        return 0, 1
    elif value >= sequence[-1]:
        return len(sequence) - 1, 1
    else:
        i = 0
        for i, s in enumerate(sequence):
            if s > value:
                break
        i -= 1
        weight = 1 - (value - sequence[i]) / (sequence[i + 1] - sequence[i])
        return i, weight


def linear_interpolate(times, data: np.ndarray, instant):
    '''data can be an ndarray with time-series in first rank
    so that data[i] -> field at time index i'''
    i, w = find_array_interval(times, instant)
    if w == 1:
        return data[i]
    else:
        return data[i] * w + data[i + 1] * (1 - w)


class hdf5_ice_parser:

    def __init__(self, filename: str, zone: str = ''):
        self.h5file = h5py.File(filename, 'r')
        self.zone: str = zone
        self.translation = [0, 0, 0]
        if not self.zone:
            print(f'Selecting first zone from {self.list_zones()}')
        if not zone:
            self.zone = self.list_zones()[0]

    def close(self):
        self.h5file.close()

    def check(self):
        # are there zones?
        if len(self.list_zones()) > 0 \
           and self.zone in self.list_zones() \
           and len(self.list_fields()) > 3:
            return True
        else:
            print('Error hdf5_ice_parser.check')
            return False

    def list_zones(self):
        return [z for z in self.h5file.keys()]

    def list_fields(self):
        if self.zone in self.list_zones():
            return [f for f in self.h5file.get(self.zone).keys()]
        else:
            return []

    def get_field(self, field_name: str):
        zone = self.zone
        if field_name in self.list_fields():
            data = self.h5file.get(zone).get(field_name)
            if isinstance(data, h5py.Dataset):
                return np.array(data)
            elif isinstance(data, h5py.Group):
                return np.array(data.get('data')).transpose()  # NOTE!
        else:
            print('Wrong field name', field_name)
            sys.exit(1)

    def get_field_value(self, field_name: str, instant: float):
        times = self.get_times()
        if not times[0] <= instant <= times[-1]:
            print('Instant not in time range')
            sys.exit(1)
        field = self.get_field(field_name)
        return linear_interpolate(times, field, instant)

    def get_coords(self):
        t = self.translation
        return [self.get_field(x) + t[i] for i, x in enumerate('XYZ')]

    def get_times(self):
        return self.get_field('time')

    def plot(self, field: str, instant: float):
        mesh = np.meshgrid(*self.get_coords(), indexing='ij')
        plt.figure(figsize=(22, 22))
        ax = plt.axes(projection='3d')
        data = self.get_field_value(field, instant)
        c = ax.scatter3D(*mesh, c=data, cmap=mpl.colormaps['viridis'], s=90)
        ax.set_aspect('equal')
        plt.colorbar(c, location='bottom')
        plt.tight_layout()
        plt.show()
        return data.shape, mesh[0].shape

    def write_openfoam(self, field: str, instant: float, filename: str):
        foamHeader =                                     \
            'FoamFile\n'                                   \
            '{\n'                                          \
            '    format      ascii;\n'                     \
            '    class       dictionary;\n'                \
            '    location    "constant";\n'                \
            '    object      interpolationData;\n'        \
            '}\n\n'

        def yield_point(X, Y, Z):
            for i, x in enumerate(X):
                for j, y in enumerate(Y):
                    for k, z in enumerate(Z):
                        yield x, y, z

        print(f'Writing {filename}')
        with open(filename, 'w') as f:
            f.write(foamHeader)
            X, Y, Z = self.get_coords()
            data = self.get_field_value(field, instant)
            n_data = len(data.flatten())
            f.write(f'points\n{n_data}\n(\n')
            for p in yield_point(X, Y, Z):
                f.write(f'({p[0]} {p[1]} {p[2]})\n')
            f.write(');\n')

            f.write(f'data\n{n_data}\n(\n')
            for i in range(n_data):
                f.write(f'{data.flatten()[i]}\n')
            f.write(');\n')

    def write_csv(self, field: str, instant: float, filename: str):
        print(f'Writing {filename}')
        with open(filename, 'w') as f:
            X, Y, Z = self.get_coords()
            data = self.get_field_value(field, instant)
            f.write(f'#X, Y, Z, {field}\n')
            for i, x in enumerate(X):
                for j, y in enumerate(Y):
                    for k, z in enumerate(Z):
                        f.write(f'{x}, {y}, {z}, {data[i,j,k]}\n')


def get_args():
    prog = Path(__file__).name
    descString = '''
    FIXME: Write description.
    '''

    parser = argparse.ArgumentParser(description=descString)

    parser.usage = f'''
    {prog} <options> <command>

    FIXME: Write usage

    '''

    parser.add_argument('-f', '--file',
                        dest='h5file',
                        type=Path,
                        default=None,
                        help='Input hdf5 file')
    parser.add_argument('-p',
                        '--plot',
                        action='store_true',
                        dest='plot',
                        default=False,
                        help='Plot field')
    parser.add_argument('-F', '--field',
                        dest='field',
                        type=str,
                        default=None,
                        help='Field to op on')
    parser.add_argument('-t', '--time',
                        dest='time',
                        type=float,
                        default=0,
                        help='Choose instant')
    parser.add_argument('-T', '--translate',
                        type=str,
                        dest='translate',
                        default='(0 0 0)',
                        help='Translate coodinates like "(1 0 0)"')

    def read_vector(vstr: str):
        vstr = vstr.strip('([])')
        try:
            return [float(a) for a in vstr.split()]
        except ValueError:
            print('Wrong vector specification')
            sys.exit(1)

    options = parser.parse_args()

    options.translate = read_vector(options.translate)

    if not options.h5file.is_file():
        print(f'No such file {options.h5file}')
        sys.exit(1)

    return options


def test():
    opts = get_args()
    parser = hdf5_ice_parser(opts.h5file)
    parser.translation = opts.translate
    parser.check()
    times = parser.get_times()
    if times[0] <= opts.time <= times[-1]:
        t = opts.time
    else:
        print(f'Time selection {opts.time} is out of range'
              f'{(times[0], times[-1])}. Choosing middle.')
        t = sum(times) / len(times)
    if opts.plot:
        parser.plot(opts.field, t)
    parser.write_csv(opts.field, t, f'{opts.field}.csv')
    parser.write_openfoam(opts.field, t, f'{opts.field}Data')


if __name__ == '__main__':
    test()
