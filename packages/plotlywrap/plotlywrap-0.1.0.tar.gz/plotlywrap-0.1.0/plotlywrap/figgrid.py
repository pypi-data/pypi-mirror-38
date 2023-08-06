"""Module for generating grids for use in Plotly subplot figures."""

import copy

import numpy as np


class BaseGrid(object):
    """Class to represent a grid of rows and columns."""

    def __init__(self, num_rows, num_cols):

        self.num_rows = num_rows
        self.num_cols = num_cols

    def get_row_col_idx(self, grid_idx):
        """Get the row and column index of a position in the grid,
        indexed from top-left to bottom-right."""

        col_idx = grid_idx % self.num_cols
        row_idx = int(grid_idx / self.num_cols)
        return (row_idx, col_idx)

    def get_grid_idx(self, row_idx=None, col_idx=None):
        """Get position(s) of a given row and/or column, zero-indexed from 
        top-left to bottom right of a grid.

        Parameters
        ----------
        row_idx : int or list of int, optional
            If not specified, `col_idx` must be a list.
        col_idx : int or list of int, optional
            If not specified, `row_idx` must be a list.

        Returns
        -------
        grid_idx : int of list of int

        """

        if (row_idx is None and col_idx is None):
            msg = ('Specify at least one of `row_idx` and `col_idx`.')
            raise ValueError(msg)

        if row_idx is None:
            row_idx = np.arange(self.num_rows)
        elif col_idx is None:
            col_idx = np.arange(self.num_cols)
        else:
            row_idx, col_idx = np.array([row_idx]), np.array([col_idx])

        grid_idx = ((row_idx * self.num_cols) + col_idx)

        if len(grid_idx) == 1:
            grid_idx = grid_idx[0]
        else:
            grid_idx = grid_idx.tolist()

        return grid_idx


class LengthSpec(object):
    """Class to store and validate the parameters for the partitioning of
    the plotting width or height."""

    def __init__(self, direction, grid_spec, ax_thickness):

        spec = {
            'spacing': grid_spec[direction].get('spacing'),
            'fractions': grid_spec[direction].get('fractions'),
            'axis_label_thickness': [i['label'] for i in ax_thickness],
            'axis_title_thickness': [i['title'] for i in ax_thickness],
        }

        self.direction = direction

        # Replace direction dependent keys with direction-agnostic keys:
        spec.update({
            key: grid_spec.get(val)
            for key, val in self.len_keys.items()
            if key in ['num', 'length', 'length_includes']
        })
        spec.update({
            key: grid_spec[direction].get(val)
            for key, val in self.len_keys.items()
            if key in ['sub_lengths', 'sub_lengths_include']
        })

        self.num = spec['num']
        spec = self._validate_spec(spec)

        self.num = spec['num']
        self.spacing = spec['spacing']
        self.fractions = spec['fractions']
        self.length = spec['length']
        self.length_includes = spec['length_includes']
        self.sub_lengths = spec['sub_lengths']
        self.sub_lengths_include = spec['sub_lengths_include']
        self.axis_label_thickness = spec['axis_label_thickness']
        self.axis_title_thickness = spec['axis_title_thickness']

        self.domain_length = None  # Set in get_subplot_domain()

    def _validate_spec(self, spec):
        """Validate the x or y specification and set defaults."""

        # `sub_lengths_include` is always allowed:
        if spec['sub_lengths_include'] is None:
            spec['sub_lengths_include'] = Grid.sub_lengths_include_def

        spec['spacing'] = self._validate_spacing(spec['spacing'])

        allowed_inc = ['', 'axes', 'axes+spacing']
        if spec['sub_lengths_include'] not in allowed_inc:
            msg = ('`{}` must be one of: {}, not "{}"'.format(
                self.len_keys['sub_lengths_include'], allowed_inc,
                spec['sub_lengths_include']))
            raise ValueError(msg)

        if spec['sub_lengths'] is not None:

            if spec['length'] is not None:
                msg = ('Specify either `{}` (and, optionally, `{}[fractions]`)'
                       ' or `{}[{}]`, but not both.'.format(
                           self.len_keys['length'], self.direction,
                           self.direction, self.len_keys['sub_lengths']))
                raise ValueError(msg)

            if spec['fractions'] is not None:
                msg = ('Specify either `{}[fractions]` or `{}[{}]`, but not '
                       'both.'.format(self.direction, self.direction,
                                      self.len_keys['sub_lengths']))
                raise ValueError(msg)

            sub_lens_msg = (
                '`{}[{}]` must be a number, or list of length equal '
                'to `{}` (i.e. {}), not "{}".'.format(
                    self.direction, self.len_keys['sub_lengths'],
                    self.len_keys['num'], self.num, spec['sub_lengths']
                )
            )

            if isinstance(spec['sub_lengths'], list):
                if len(spec['sub_lengths']) != self.num:
                    raise ValueError(sub_lens_msg)

            elif isinstance(spec['sub_lengths'], (int, float)):
                spec['sub_lengths'] = [spec['sub_lengths']] * self.num

            else:
                raise ValueError(sub_lens_msg)

        else:
            if spec['length_includes'] is None:
                spec['length_includes'] = Grid.lengths_include_def

            spec['fractions'] = self._validate_fractions(spec['fractions'])

            if spec['length'] is None:
                # set default total length as num * default subplot length
                if self.direction == 'x':
                    spec['length'] = self.num * Grid.width_def
                elif self.direction == 'y':
                    spec['length'] = self.num * Grid.height_def

        return spec

    def _validate_fractions(self, fractions):
        """Validate and set defaults for the x or y `fractions`."""

        if fractions is None:
            fractions = [1 / self.num for _ in range(self.num)]

        if isinstance(fractions, list):
            if len(fractions) != self.num:
                msg = ('`{}[fractions]` must have length equal to `{}` (i.e. '
                       '{})'.format(self.direction, self.len_keys['num'], self.num))
                raise ValueError(msg)
        else:
            msg = ('If specified, `{}[fractions]` must be a list of length '
                   'equal to `{}`'.format(self.direction, self.num))
            raise ValueError(msg)

        if np.sum(fractions) != 1:
            msg = '`fractions` must sum to 1'
            raise ValueError(msg)

        for i in fractions:
            if i > 1 or i <= 0:
                msg = '`fractions` elements must be between 0 and 1.'
                raise ValueError(msg)

        return fractions

    def _validate_spacing(self, spacing):
        """Validate and set defaults for the x or y `spacing`."""

        if spacing is None:
            spacing = Grid.spacing_def

        spacing_msg = (
            'If specified, `{}[spacing]` must be either a number, or a list of'
            ' length equal to `{}` - 1 (i.e. {})'.format(
                self.direction, self.len_keys['num'], self.num - 1)
        )

        if isinstance(spacing, list):
            if len(spacing) != (self.num - 1):
                raise ValueError(spacing_msg)

        elif isinstance(spacing, (int, float)):
            spacing = [spacing] * (self.num - 1)

        else:
            raise ValueError(spacing_msg)

        return spacing

    @property
    def len_keys(self):
        """Get the direction-dependent keys of the LengthSpec."""
        if self.direction == 'x':
            out = {
                'num': 'num_cols',
                'length': 'width',
                'length_includes': 'width_includes',
                'sub_lengths': 'sub_widths',
                'sub_lengths_include': 'sub_widths_include'
            }
        elif self.direction == 'y':
            out = {
                'num': 'num_rows',
                'length': 'height',
                'length_includes': 'height_includes',
                'sub_lengths': 'sub_heights',
                'sub_lengths_include': 'sub_heights_include'
            }
        else:
            raise ValueError('`direction` must be "x" or "y".')

        return out

    def get_subplot_domain(self):
        """Find the domains of the plot areas and axis label and titles."""

        fractions = self.fractions
        spacing = self.spacing
        num = self.num
        axis_label_thickness = self.axis_label_thickness
        axis_title_thickness = self.axis_title_thickness
        sub_len = self.sub_lengths
        sub_len_inc = self.sub_lengths_include
        len_inc = self.length_includes

        if self.direction == 'y':
            reverse = True
        else:
            reverse = False

        if reverse:
            axis_label_thickness = axis_label_thickness[::-1]
            axis_title_thickness = axis_title_thickness[::-1]

        # Add a final spacing of zero so we have one spacing entry for each subplot:
        spacing = [0] + spacing + [0]

        ax_sum_tot = sum(axis_label_thickness + axis_title_thickness)
        ax_sum = [i + j
                  for i, j in zip(axis_label_thickness, axis_title_thickness)]

        spacing_tot = []
        for i_idx in range(len(spacing) - 1):
            spacing_tot.append(
                (0.5 * spacing[i_idx]) + (0.5 * spacing[i_idx + 1])
            )

        if self.length is not None:

            if reverse:
                fractions = fractions[::-1]

            domain_len = self.length
            if 'spacing' not in len_inc:
                domain_len += sum(spacing)
            if 'axes' not in len_inc:
                domain_len += ax_sum_tot

            subplot_len_tot_sum = domain_len
            if 'spacing' not in sub_len_inc:
                subplot_len_tot_sum -= sum(spacing)
            if 'axes' not in sub_len_inc:
                subplot_len_tot_sum -= ax_sum_tot

            subplot_len_tot = [i * subplot_len_tot_sum for i in fractions]

            subplot_len = subplot_len_tot
            if 'axes' in sub_len_inc:
                subplot_len = [i - j for i, j in zip(subplot_len, ax_sum)]
            if 'spacing' in sub_len_inc:
                subplot_len = [i - j for i, j in zip(subplot_len, spacing_tot)]

            subplot_axes_len = [i + j for i, j in zip(subplot_len, ax_sum)]
            subplot_axes_spacing_len = [i + j for i,
                                        j in zip(subplot_axes_len, spacing_tot)]

        else:

            subplot_len = sub_len
            if 'axes' in sub_len_inc:
                subplot_len = [i - j for i, j in zip(subplot_len, ax_sum)]
            if 'spacing' in sub_len_inc:
                subplot_len = [i - j for i, j in zip(subplot_len, spacing_tot)]

            subplot_axes_len = [i + j for i, j in zip(subplot_len, ax_sum)]
            subplot_axes_spacing_len = [i + j for i,
                                        j in zip(subplot_axes_len, spacing_tot)]

            domain_len = sum(subplot_axes_spacing_len)

        too_small = 10
        for i in subplot_len:
            if i < too_small:
                msg = ('Plotting area for subplot is too small (less than {} '
                       'px). Reconsider the plotting dimensions.'.format(too_small))
                raise ValueError(msg)

        self.domain_length = domain_len

        # Key lengths as proportions of domain length
        subplot_len_dom = [i / domain_len for i in subplot_len]
        subplot_axes_len_dom = [i / domain_len for i in subplot_axes_len]
        subplot_axes_spacing_len_dom = [i / domain_len
                                        for i in subplot_axes_spacing_len]

        spacing_dom = [i / domain_len for i in spacing]
        ax_lab_dom = [i / domain_len for i in axis_label_thickness]
        ax_tit_dom = [i / domain_len for i in axis_title_thickness]

        domains = []
        for i_idx in range(num):

            if i_idx == 0:
                subplot_start_i = 0
            else:
                subplot_start_i = domains[-1]['subplot+spacing'][1]

            spacing_0_i = [
                subplot_start_i,
                subplot_start_i + (spacing_dom[i_idx] / 2)
            ]
            ax_tit_i = [
                spacing_0_i[1],
                spacing_0_i[1] + ax_tit_dom[i_idx]
            ]
            ax_lab_i = [
                ax_tit_i[1],
                ax_tit_i[1] + ax_lab_dom[i_idx]
            ]
            plot_i = [
                ax_lab_i[1],
                ax_lab_i[1] + subplot_len_dom[i_idx]
            ]
            spacing_1_i = [
                plot_i[1],
                plot_i[1] + (spacing_dom[i_idx + 1] / 2)
            ]
            subplot_i = [spacing_0_i[1], spacing_1_i[0]]
            subplot_spacing_i = [subplot_start_i, spacing_1_i[1]]

            dom_i = {
                'spacing_0': spacing_0_i,
                'spacing_1': spacing_1_i,
                'axis_label': ax_lab_i,
                'axis_title': ax_tit_i,
                'plot_area': plot_i,
                'subplot': subplot_i,
                'subplot+spacing': subplot_spacing_i,
            }
            domains.append(dom_i)

        if reverse:
            domains[:] = domains[::-1]

        return domains


class Grid(object):
    """Class to represent the partitioning of the plotting area domain into
    subplots and the spacing between them."""

    width_def = 250
    height_def = 250
    num_rows_def = 1
    num_cols_def = 1

    yax_lab_thick_def = 25
    xax_lab_thick_def = 20
    ax_tit_thick_def = 20
    spacing_def = 30

    sub_lengths_include_def = ''
    lengths_include_def = 'axes+spacing'

    def __init__(self, grid_spec, axes):

        grid_spec = self._set_default_grid_spec(grid_spec)
        base_grid = BaseGrid(grid_spec['num_rows'], grid_spec['num_cols'])
        self.base_grid = base_grid

        self.num_rows = base_grid.num_rows
        self.num_cols = base_grid.num_cols
        self.get_row_col_idx = base_grid.get_row_col_idx
        self.get_grid_idx = base_grid.get_grid_idx

        self.axes = self._validate_axes(axes)
        ax_thick = self._get_axis_thicknesses(self.axes)

        self.x = LengthSpec('x', grid_spec, ax_thick['x'])
        self.y = LengthSpec('y', grid_spec, ax_thick['y'])
        self.width = self.x.length
        self.height = self.y.length

        self.domains_x = self.x.get_subplot_domain()
        self.domains_y = self.y.get_subplot_domain()
        self.domain_width = self.x.domain_length
        self.domain_height = self.y.domain_length

    def _set_default_grid_spec(self, grid_spec):
        """Set defaults in the grid spec dict."""

        allowed_len_inc = [
            '',
            'axes',
            'axes+spacing',
        ]

        gs_def = {
            'num_rows': Grid.num_rows_def,
            'num_cols': Grid.num_cols_def,
            'x': {},
            'y': {},
        }

        grid_spec = {**gs_def, **grid_spec}

        len_str = ['width', 'height']
        len_inc_str = ['{}_includes'.format(i) for i in len_str]

        for i, j in zip(len_str, len_inc_str):

            length = grid_spec.setdefault(i)
            length_inc = grid_spec.get(j)

            if length_inc is not None:

                if length is None:
                    msg = ('If `{}` is not specified (or set to `None`), '
                           '`{}` must not be specified, or must be set to '
                           '`None`.'.format(i, j))
                    raise ValueError(msg)

                if length_inc not in allowed_len_inc:
                    msg = ('`{}` specified as "{}", but must be one '
                           'of: {}'.format(i, length_inc, allowed_len_inc))
                    raise ValueError(msg)

        return grid_spec

    @property
    def all_subplot_idx(self):
        return range(self.num_cols * self.num_rows)

    def _validate_axis_dict(self, axis):

        allowed_letters = ['x', 'y']

        subplot_idx = self.normalise_suplot_idx(axis['subplot_idx'])
        if subplot_idx not in self.all_subplot_idx:
            msg = ('`subplot_idx` "{}" is not understood/in '
                   'range.'.format(subplot_idx))
            raise ValueError(msg)
        else:
            axis['subplot_idx'] = subplot_idx

        if axis['axis'] not in allowed_letters:
            msg = ('`axis` must be one of {}, '
                   'not "{}"'.format(allowed_letters, axis['axis']))
            raise ValueError(msg)

    def _validate_axes(self, axes):
        """Generate an axis dict for each x and y axis in each subplot, where
        not already specified, and add sensible defaults."""

        axes_valid = []

        for ax in axes:
            self._validate_axis_dict(ax)

        for sp_idx in self.all_subplot_idx:

            for letter in ['x', 'y']:

                if letter == 'x':
                    lab_thick = Grid.xax_lab_thick_def
                else:
                    lab_thick = Grid.yax_lab_thick_def

                axis = {
                    'subplot_idx': sp_idx,
                    'axis': letter,
                    'title_thickness': 0,
                    'titlefont': ax.get('titlefont'),
                    'label_thickness': lab_thick
                }

                # Check whether this axis is specified already:
                for ax in axes:

                    if (ax['subplot_idx'] == sp_idx) and (ax['axis'] == letter):

                        axis.update(**ax)

                        if ((ax.get('title') is not None) and
                                (ax.get('title_thickness') is None)):
                            axis.update({
                                'title_thickness': Grid.ax_tit_thick_def
                            })

                axes_valid.append(axis)

        return axes_valid

    def _get_axis_thicknesses(self, axes):
        """Get axis thicknesses (title + labels), where the largest thickness
        for a given row/col is used.

        Notes
        -----
        x-axes titles/labels effect the distribution of thicknesses in the
        y-direction and vice versa.

        """

        x_thick = [{'title': -1, 'label': -1} for _ in range(self.num_cols)]
        y_thick = [{'title': -1, 'label': -1} for _ in range(self.num_rows)]

        for ax in axes:

            row_idx, col_idx = self.get_row_col_idx(ax['subplot_idx'])

            if ax['axis'] == 'x':
                idx = row_idx
                ax_thick = y_thick

            elif ax['axis'] == 'y':
                idx = col_idx
                ax_thick = x_thick

            if ax_thick[idx]['title'] < ax['title_thickness']:
                ax_thick[idx]['title'] = ax['title_thickness']

            if ax_thick[idx]['label'] < ax['label_thickness']:
                ax_thick[idx]['label'] = ax['label_thickness']

        out = {
            'x': x_thick,
            'y': y_thick,
        }
        return out

    def normalise_suplot_idx(self, subplot_idx=None):

        if isinstance(subplot_idx, tuple):
            _subplot_idx = self.get_grid_idx(*subplot_idx)
        else:
            _subplot_idx = subplot_idx

        if _subplot_idx not in self.all_subplot_idx:
            msg = (
                '`subplot_idx` must be an integer between 0 and {}, or a '
                'two-tuple, representing the row (0 to {}) and column (0 to '
                '{}) indices, but "{}" was specified.'.format(
                    len(self.all_subplot_idx) - 1, self.num_rows - 1,
                    self.num_cols - 1, subplot_idx
                )
            )
            raise ValueError(msg)
        else:
            subplot_idx = _subplot_idx
        return subplot_idx
