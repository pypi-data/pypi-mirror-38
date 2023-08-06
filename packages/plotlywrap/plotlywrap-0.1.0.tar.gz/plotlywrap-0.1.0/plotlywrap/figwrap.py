"""Module to hold the FigWrap class, which provides some convenience wrapper
functionality around the Plotly Figure object."""

import pathlib
import copy
import shutil
import os
import subprocess
import threading

from plotly import graph_objs as go
from plotly.offline import plot
from plotly import io as pio
from IPython.core.display import display
from IPython.display import IFrame
from ipywidgets import Button, Layout, Checkbox, Box, HBox, VBox, Output

from plotlywrap.figgrid import Grid

_AXIS_PROPS_KEYS = [
    'subplot_idx',
    'axis',
    'title',
    'titlefont',
    'title_thickness',
    'label_thickness',
]


def pdf2svg(pdf_path, dest_dir=None):
    """Use pdf2svg.exe to convert a PDF to a SVG, in which fonts are replaced
    with shapes."""

    pdf_path = pathlib.Path(pdf_path)
    pdf_dir = pdf_path.parent
    pdf_name = pdf_path.name

    svg_path = pdf_path.with_suffix('.svg')
    svg_name = svg_path.name

    _ = subprocess.run(
        ['pdf2svg.exe', pdf_name, svg_name],
        shell=True,
        cwd=str(pdf_dir),
        stdout=subprocess.PIPE
    )

    if dest_dir is not None:
        shutil.copy(str(svg_path), str(dest_dir))


def pdf2png(pdf_path, density=300, quality=90, dest_dir=None):
    """Use ImageMagic to convert a PDF to a PNG."""

    pdf_path = pathlib.Path(pdf_path)
    pdf_dir = pdf_path.parent
    pdf_name = pdf_path.name

    png_path = pdf_path.with_suffix('.png')
    png_name = png_path.name

    com = 'magick convert -density {} -quality {} {} {}'.format(
        density, quality, pdf_name, png_name)

    _ = subprocess.run(
        com,
        shell=True,
        cwd=str(pdf_dir),
        stdout=subprocess.PIPE
    )

    if dest_dir is not None:
        shutil.copy(str(png_path), str(dest_dir))


def confirm(prompt=None, resp=False):
    """
    Prompts for yes or no response from the user, returning True for yes and
    False for no.

    Parameters
    ----------
    prompt : str
        The prompt to show the user. Default is 'Confirm'
    resp : bool
        The default response if the user types `Enter`.

    Returns
    -------
    bool

    """

    pos = ['y', 'Y']
    neg = ['n', 'N']

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '{} [{}]|{}: '.format(prompt, 'y', 'n')
    else:
        prompt = '{} [{}]|{}: '.format(prompt, 'n', 'y')

    while True:

        ans = input(prompt)

        if not ans:
            return resp

        if ans not in (pos + neg):
            print('Please enter y or n.')
            continue

        if ans in pos:
            return True
        elif ans in neg:
            return False


def remove_folder_contents(folder):

    for the_file in os.listdir(folder):

        file_path = os.path.join(folder, the_file)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:
            print(e)


def get_available_filename(filename):
    """Check if a filename already exists and if it does modify until an
    available filename is found."""

    count = 0
    while filename.is_file():
        count += 1
        new_name = filename.stem + '_{}'.format(count) + filename.suffix
        filename = filename.with_name(new_name)

    #print('get_available_filename: filename: {}'.format(filename))

    return filename


def get_axis_str_short(letter, idx):
    return '{}{}'.format(letter, str(idx + 1))


def get_axis_str_long(letter, idx):
    return '{}axis{}'.format(letter, str(idx + 1))


class ExportConfig(object):
    """Class to store configuration options for exporting static images."""

    def __init__(self, tex_compile_dir=None, tex_template_path=None,
                 tex_macros_path=None, export_dir=None):

        if tex_compile_dir is not None:
            tex_compile_dir = pathlib.Path(tex_compile_dir)

        if tex_template_path is not None:
            tex_template_path = pathlib.Path(tex_template_path)

        if tex_macros_path is not None:
            tex_macros_path = pathlib.Path(tex_macros_path)

        if export_dir is not None:
            export_dir = pathlib.Path(export_dir)
        else:
            export_dir = pathlib.Path('').cwd()

        self.tex_compile_dir = tex_compile_dir
        self.tex_template_path = tex_template_path
        self.tex_macros_path = tex_macros_path
        self.export_dir = export_dir


class FigWrap(object):
    """Class to represent a Plotly Figure with additional helper methods."""

    margin_standard_def = 5
    margin_interactivity = 35
    margin_plotly_controls = 25
    margin_title = 30

    _filename_def = 'my_figure'
    _fig_margins_def = ('standard', 'plotly_controls', 'title')
    _fig_widget_margins_def = _fig_margins_def + ('interactivity',)
    _fig_export_margins_def = ('standard',)
    _leg_shape_color = 'lightblue'

    def __init__(self, data=None, layout=None, axes=None, title=None, legend=None,
                 export_config=None):

        if layout is None:
            layout = {}
        if axes is None:
            axes = []
        if data is None:
            data = []

        self.layout = self._separate_layout_props(layout)
        self.export_config = export_config or ExportConfig()
        self.grid = Grid(layout, axes)
        self.axes = self.grid.axes
        self.title = title

        self.axes_dicts = {}
        self.axes_idx = {}
        self.annotations = {'axis_titles': []}

        self._add_axes()
        self._add_axis_titles()

        self.data = []
        for i in data:
            self._add_data(i)

        self.legend = self._validate_legend(legend)
        self.all_margins = self._get_all_margins(layout.get('margin', {}))

    def _separate_layout_props(self, layout):
        """Extract out layout properties that are Plotly layout properties."""

        exclude_keys = [
            'num_rows',
            'num_cols',
            'width',
            'height',
            'width_includes',
            'height_includes',
            'x',
            'y',
            'margin',
        ]

        layout = {
            key: val for key, val in layout.items()
            if key not in exclude_keys
        }

        return layout

    def _validate_legend(self, legend_props):
        """Validate the specified legend properties and set defaults, if
        necessary.

        Notes
        -----
        Default orientation is vertical if the legend is placed within the
        plotting area. If the legend is placed externally to the plotting area,
        the default orientation is vertical if placed on the left or right
        side, and horizontal if placed on the bottom or top sides.

        Returns
        -------
        dict
        Legend options dict, with defaults set.

        """

        # By default set the legend to be external
        is_ext = legend_props.get('external', True)
        try:
            subplot_idx = self.grid.normalise_suplot_idx(
                legend_props.get('subplot_idx'))
        except ValueError as val_err:
            raise ValueError(
                '`subplot_idx` in `legend` is invalid: {}'.format(val_err))

        # Defaults, regardless of internal/external placement:
        leg_def = {
            'item_height': 30,
            'item_width': 100,
            'external': is_ext,
            'subplot_idx': None,
        }

        ori_def = 'v'

        if is_ext:

            if legend_props.get('side') in ['bottom', 'top']:
                ori_def = 'h'

            leg_def.update({
                'side': 'right',
                'orientation': ori_def,
                'align_x': None,
                'align_y': None,
            })

        else:

            # If aligning relative to a subplot, by default, align to the left
            # if there's data, otherwise align in the center.
            align_x = 'left'
            if subplot_idx not in self.subplots_with_data:
                align_x = 'center'

            leg_def.update({
                'side': None,
                'orientation': ori_def,
                'align_x':  align_x,
                'align_y': 'top',
            })

        leg = {**leg_def, **legend_props}
        leg['subplot_idx'] = subplot_idx

        # Set default offset
        leg_offset_def = {k: 0 for k in ['t', 'r', 'b', 'l']}
        leg_offset = {**leg_offset_def, **legend_props.get('offset', {})}
        leg.update({'offset': leg_offset})

        sides_hor = ['left', 'right']
        sides_ver = ['bottom', 'top']
        sides_all = sides_hor + sides_ver

        # More validation:
        if is_ext:
            if leg['subplot_idx'] is not None:
                msg = ('`subplot_idx` must be `None` (or not specified) when '
                       '`external` is True, but "{}" was '
                       'specified'.format(leg['subplot_idx']))
                raise ValueError(msg)

            if leg['side'] not in sides_all:
                msg = ('`sides` must be one of {}, but "{}" was '
                       'specified'.format(sides_all, leg['side']))
                raise ValueError(msg)

            if leg['side'] in sides_hor:

                if leg['align_x'] is not None:
                    msg = ('`align_x` must be `None` (or not specified) when '
                           '`side` is in {}, but "{}" was '
                           'specified.'.format(sides_hor, leg['align_x']))
                    raise ValueError(msg)

                if leg['align_y'] is None:
                    leg['align_y'] = 'top'

            if leg['side'] in sides_ver:

                if leg['align_y'] is not None:
                    msg = ('`align_y` must be `None` (or not specified) when '
                           '`side` is in {}, but "{}" was '
                           'specified.'.format(sides_ver, leg['align_y']))
                    raise ValueError(msg)

                if leg['align_x'] is None:
                    leg['align_x'] = 'center'

        else:
            if leg['side'] is not None:
                msg = ('`side` must be `None` (or not specified) when '
                       '`external` is False (or not specified), but "{}" was '
                       'specified'.format(leg['side']))
                raise ValueError(msg)

        # Set legend nominal width and height and validate `orientation`:
        num_items = self._num_legend_items

        width = leg['item_width']
        height = leg['item_height']

        if leg['orientation'] == 'v':
            height *= num_items
        elif leg['orientation'] == 'h':
            width *= num_items
        else:
            msg = ('Legend `orientation` must be one of "h" (horizontal), "v" '
                   '(vertical).')
            raise ValueError(msg)

        leg.update({
            'width': width,
            'height': height,
            'num_items': num_items
        })

        return leg

    def _extract_plotly_legend_props(self):
        """Extract properties in `self.legend` that are Plotly legend 
        properties."""

        exclude_keys = [
            'align_x',
            'align_y',
            'subplot_idx',
            'width',
            'height',
            'external',
            'item_width',
            'item_height',
            'offset',
            'side',
            'num_items',
        ]

        # Pass through plotly legend properties from legend options:
        plotly_leg = {
            k: v for k, v in self.legend.items()
            if k not in exclude_keys
        }

        return plotly_leg

    def _get_plotly_legend(self, margin_contributions):
        """Get the Plotly legend dict."""

        leg = self.legend
        plotly_leg = self._extract_plotly_legend_props()

        # Get offset in domain coordinates:
        leg_offset = copy.deepcopy(leg['offset'])

        if leg['external'] and 'standard' in margin_contributions:
            # If external, add additional offset to account for standard margin:
            leg_side_let = leg['side'][0]
            leg_offset[leg_side_let] -= self.all_margins['standard'][leg_side_let]

        leg_offset_x = leg_offset['l'] - leg_offset['r']
        leg_offset_y = leg_offset['b'] - leg_offset['t']
        leg_offset_frac = [
            leg_offset_x / self.grid.domain_width,
            leg_offset_y / self.grid.domain_height
        ]

        aligns = [leg['align_x'], leg['align_y']]
        letters = ['x', 'y']
        anchors = ['xanchor', 'yanchor']
        align_vals = [['left', 'right', 'center'], ['bottom', 'top', 'middle']]

        if leg['external']:

            plot_domains_external = [[0, 1], [0, 1, 0.5], ]
            leg_side_vals = [['left', 'right'], ['bottom', 'top']]
            side_align_letters = [['x', 'y'], ['y', 'x']]
            side_align_anchors = [['{}anchor'.format(i) for i in j]
                                  for j in side_align_letters]

            leg_side_idx = [leg['side'] in i
                            for i in leg_side_vals].index(True)
            anchor_idx = -(leg_side_idx + 1)

            side_letter = side_align_letters[leg_side_idx][0]
            align_letter = side_align_letters[leg_side_idx][1]
            side_anchor = side_align_anchors[leg_side_idx][0]
            align_anchor = side_align_anchors[leg_side_idx][1]

            align = leg['align_{}'.format(align_letter)]

            side_letter_val = (
                plot_domains_external[0][leg_side_vals[leg_side_idx].index(leg['side'])] +
                leg_offset_frac[leg_side_idx]
            )
            side_anchor_val = leg_side_vals[leg_side_idx][-(
                leg_side_vals[leg_side_idx].index(leg['side']) + 1)]

            align_letter_val = (
                plot_domains_external[1][align_vals[anchor_idx].index(align)] +
                leg_offset_frac[anchor_idx]
            )

            plotly_leg.update({
                align_anchor: align,
                side_anchor: side_anchor_val,
                side_letter: side_letter_val,
                align_letter: align_letter_val
            })

        else:

            if leg['subplot_idx'] is not None:

                # Legend is inside plotting area, and alignment is relative to
                # a given subplot
                ridx, cidx = self.grid.get_row_col_idx(leg['subplot_idx'])

                if leg['subplot_idx'] in self.subplots_with_data:
                    domain_key = 'plot_area'
                else:
                    domain_key = 'subplot'

                plot_domain_x = self.grid.domains_x[cidx][domain_key]
                plot_domain_y = self.grid.domains_y[ridx][domain_key]

                plot_domains = [[i[0], i[1], (i[0] + i[1]) / 2]
                                for i in [plot_domain_x, plot_domain_y]]

            else:
                # Legend is inside plotting area, and alignment is relative to
                # edges of plotting area
                plot_domains = [[0, 1, 0.5]] * 2

            for i in [0, 1]:
                if aligns[i] in align_vals[i]:
                    plotly_leg.update({
                        letters[i]: (
                            plot_domains[i][align_vals[i].index(aligns[i])] +
                            leg_offset_frac[i]
                        ),
                        anchors[i]: aligns[i]
                    })

        return plotly_leg

    def _get_all_margins(self, margins):

        sides = ['t', 'r', 'b', 'l']
        margins_def = {k: FigWrap.margin_standard_def for k in sides}
        interactivity = {k: FigWrap.margin_interactivity for k in sides}
        interactivity['t'] = FigWrap.margin_interactivity / 3

        leg_margin = {k: 0 for k in sides}
        if self.legend['external']:
            leg_side = self.legend['side'][0]
            if leg_side in ['l', 'r']:
                leg_margin[leg_side] = self.legend['width']
            elif leg_side in ['b', 't']:
                leg_margin[leg_side] = self.legend['height']

        all_margins = {
            'standard': {**margins_def, **margins},
            'interactivity': interactivity,
            'plotly_controls': {'t': FigWrap.margin_plotly_controls},
            'title': {'t': FigWrap.margin_title if self.title is not None else 0},
            'legend': leg_margin,
        }

        return all_margins

    def _extract_axis_props(self, axis):
        exclude_keys = _AXIS_PROPS_KEYS
        out = {k: v for k, v in axis.items() if k not in exclude_keys}
        return out

    def _check_show_ticks(self, axis_letter, axis):
        """Check whether to show tick labels for a given axis letter and
        row/col index"""
        return True if axis['label_thickness'] > 0 else False

    def _add_axes(self):
        """Construct and save axis dicts."""

        ax_props_idx = [(i['subplot_idx'], i['axis'])
                        for i in self.axes]

        for row_idx in range(self.grid.num_rows):

            for col_idx in range(self.grid.num_cols):

                subplot_idx = self.grid.get_grid_idx(row_idx, col_idx)

                #print('subplot_idx: {}'.format(subplot_idx))

                props_x_idx = ax_props_idx.index((subplot_idx, 'x'))
                props_x_all = self.axes[props_x_idx]
                props_x = self._extract_axis_props(props_x_all)

                props_y_idx = ax_props_idx.index((subplot_idx, 'y'))
                props_y_all = self.axes[props_y_idx]
                props_y = self._extract_axis_props(props_y_all)

                # print('props_y: {}'.format(props_y))

                xax_name = get_axis_str_long('x', subplot_idx)
                xax_name_short = get_axis_str_short('x', subplot_idx)
                yax_name = get_axis_str_long('y', subplot_idx)
                yax_name_short = get_axis_str_short('y', subplot_idx)

                xax_dict = {
                    'anchor': yax_name_short,
                    'domain': self.grid.domains_x[col_idx]['plot_area'],
                    'showticklabels': self._check_show_ticks('x', props_x_all),
                    #'mirror': 'ticks',
                    #'showline': True,
                    'zeroline': False,
                    **props_x,
                }
                yax_dict = {
                    'anchor': xax_name_short,
                    'domain': self.grid.domains_y[row_idx]['plot_area'],
                    'showticklabels': self._check_show_ticks('y', props_y_all),
                    #'mirror': 'ticks',
                    #'showline': True,
                    'zeroline': False,
                    **props_y,
                }
                self.axes_dicts.update({
                    xax_name: xax_dict,
                    yax_name: yax_dict,
                })
                self.axes_idx.update({
                    subplot_idx: {
                        'x': [subplot_idx],
                        'y': [subplot_idx],
                    }
                })

    def _get_axis_bounding_box(self, subplot_idx, axis_letter, component):
        """Get bounding box in domain coordinates of axis title or label.

        Parameters
        ----------
        component : str ("title" or "label")
        """

        allowed_comps = ['title', 'label']
        if component not in allowed_comps:
            msg = ('`component` must be one of {}, not '
                   '"{}"'.format(allowed_comps, component))
            raise ValueError(msg)

        row_idx, col_idx = self.grid.get_row_col_idx(subplot_idx)
        axis_comp_str = 'axis_{}'.format(component)

        if axis_letter == 'x':
            bounds_x_key = 'plot_area'
            bounds_y_key = axis_comp_str
        elif axis_letter == 'y':
            bounds_x_key = axis_comp_str
            bounds_y_key = 'plot_area'
        else:
            raise ValueError('`axis_letter` must be "x" or "y".')

        bounds_x = self.grid.domains_x[col_idx][bounds_x_key]
        bounds_y = self.grid.domains_y[row_idx][bounds_y_key]

        return bounds_x, bounds_y

    def _add_axis_titles(self):

        title_annots = []
        title_shapes = []

        for ax in self.axes:

            if ax['title_thickness'] <= 0:
                continue

            ax_bounds = self._get_axis_bounding_box(
                ax['subplot_idx'], ax['axis'], 'title')

            title_shapes.append({
                'type': 'rect',
                'xref': 'paper',
                'yref': 'paper',
                'x0': ax_bounds[0][0],
                'x1': ax_bounds[0][1],
                'y0': ax_bounds[1][0],
                'y1': ax_bounds[1][1],
                'line': {
                    'width': 1,
                }
            })

            if ax['axis'] == 'x':

                width_frac = (ax_bounds[0][1] - ax_bounds[0][0])
                anot = {
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'align': 'center',
                    'x': (ax_bounds[0][1] + ax_bounds[0][0]) / 2,
                    'y': ax_bounds[1][1],
                    'width': width_frac * self.grid.domain_width,
                }

            elif ax['axis'] == 'y':

                width_frac = (ax_bounds[1][1] - ax_bounds[1][0])
                anot = {
                    'xanchor': 'right',
                    'yanchor': 'middle',
                    'textangle': 270,
                    'x': ax_bounds[0][1],
                    'y': (ax_bounds[1][1] + ax_bounds[1][0]) / 2,
                    'width': width_frac * self.grid.domain_height,
                }

            anot.update({
                'xref': 'paper',
                'yref': 'paper',
                'height': ax['title_thickness'],
                'text': ax['title'],
                'font': ax['titlefont'],
                'showarrow': False,
                'borderpad': 0,
                'borderwidth': 0,
            })

            self.annotations['axis_titles'].append(anot)

    def _add_data(self, data, xaxis_idx=0, yaxis_idx=0):
        """Add a trace to a given subplot. Primarily, the task here is to resolve the
        correct axis dicts in `layout`.

        Parameters
        ----------
        subplot_idx : int
            Index of subplot, zero-indexed from top-left to bottom-right.
            Specify either `subplot_idx` or `row_idx` and `col_idx`.
        xaxis_idx : int
            Index of xaxis, default is zero.
        yaxis_idx : int
            Index of yaxis, default is zero.

        """

        subplot_idx = self.grid.normalise_suplot_idx(data['subplot_idx'])
        xax_name = get_axis_str_short(
            'x', self.axes_idx[subplot_idx]['x'][xaxis_idx])
        yax_name = get_axis_str_short(
            'y', self.axes_idx[subplot_idx]['y'][yaxis_idx])

        data.update({
            'xaxis': xax_name,
            'yaxis': yax_name,
            'subplot_idx': subplot_idx,
        })
        self.data.append(data)

    @property
    def subplots_with_data(self):
        out = [i['subplot_idx'] for i in self.data]
        return list(set(out))

    def _get_plotly_layout_margin(self, contributions):
        """Compute, figure (Plotly layout) width, height and margins."""

        lay_margin = {
            'autoexpand': False,
            'pad': 0,
            't': 0,
            'r': 0,
            'b': 0,
            'l': 0,
        }

        for i in contributions:

            for side in ['t', 'r', 'b', 'l']:

                lay_margin[side] += self.all_margins[i].get(side, 0)

        tot_width = self.grid.domain_width + lay_margin['l'] + lay_margin['r']
        tot_height = self.grid.domain_height + \
            lay_margin['b'] + lay_margin['t']

        out = {
            'margin': lay_margin,
            'width': tot_width,
            'height': tot_height,
        }

        return out

    def _get_axis_title_annotations(self, show_layout=False):

        out = []
        for title in self.annotations['axis_titles']:
            if show_layout:
                title = {**title, 'bgcolor': '#acc4ce'}
            out.append(title)
        return out

    def _get_axis_label_shapes(self):

        out = []
        data_subplot_idx = self.subplots_with_data

        for ax in self.axes:

            if ax['label_thickness'] <= 0:
                continue

            if ax['subplot_idx'] not in data_subplot_idx:
                continue

            ax_bounds = self._get_axis_bounding_box(
                ax['subplot_idx'], ax['axis'], 'label')

            shp = {
                'type': 'rect',
                'xref': 'paper',
                'yref': 'paper',
                'x0': ax_bounds[0][0],
                'x1': ax_bounds[0][1],
                'y0': ax_bounds[1][0],
                'y1': ax_bounds[1][1],
                'fillcolor': '#9eb9b3',
                'layer': 'below',
                'line': {
                    'width': 0,
                }
            }
            out.append(shp)

        return out

    def _get_spacing_mid_shapes(self):

        out = []
        ln_width = 0.1

        for idx, dom_x in enumerate(self.grid.domains_x):

            if idx == 0:
                continue

            shp = {
                'type': 'line',
                'xref': 'paper',
                'yref': 'paper',
                'x0': dom_x['subplot+spacing'][0],
                'x1': dom_x['subplot+spacing'][0],
                'y0': 0,
                'y1': 1,
                'layer': 'below',
                'line': {
                    'width': ln_width,
                }
            }

            out.append(shp)

        for idx, dom_y in enumerate(self.grid.domains_y[::-1]):

            if idx == 0:
                continue

            shp = {
                'type': 'line',
                'xref': 'paper',
                'yref': 'paper',
                'x0': 0,
                'x1': 1,
                'y0': dom_y['subplot+spacing'][0],
                'y1': dom_y['subplot+spacing'][0],
                'layer': 'below',
                'line': {
                    'width': ln_width,
                }
            }

            out.append(shp)

        return out

    def _get_spacing_block_shapes(self):

        out = []
        fillcolor = '#ffd5d5'

        com_shp = {
            'type': 'rect',
            'xref': 'paper',
            'yref': 'paper',
            'layer': 'below',
            'fillcolor': fillcolor,
            'line': {
                'width': 0,
            },
        }

        for idx in range(self.grid.num_cols):

            if idx == 0:
                continue

            dom_prev = self.grid.domains_x[idx - 1]
            dom_curr = self.grid.domains_x[idx]

            shp = {
                **com_shp,
                'x0': dom_prev['spacing_1'][0],
                'x1': dom_curr['spacing_0'][1],
                'y0': 0,
                'y1': 1,
            }

            out.append(shp)

        for idx in range(self.grid.num_rows):

            if idx == 0:
                continue

            dom_prev = self.grid.domains_y[::-1][idx - 1]
            dom_curr = self.grid.domains_y[::-1][idx]

            shp = {
                **com_shp,
                'x0': 0,
                'x1': 1,
                'y0': dom_prev['spacing_1'][0],
                'y1': dom_curr['spacing_0'][1],
            }

            out.append(shp)

        return out

    def _get_domain_shape(self):

        out = []
        shp = {
            'type': 'rect',
            'xref': 'paper',
            'yref': 'paper',
            'x0': 0,
            'x1': 1,
            'y0': 0,
            'y1': 1,
            'layer': 'below',
            'fillcolor': 'white',
            'line': {
                'width': 0,
            },
        }
        out.append(shp)
        return out

    def _get_subplot_shapes(self):

        out = []
        for sp_idx in self.grid.all_subplot_idx:

            r_idx, c_idx = self.grid.get_row_col_idx(sp_idx)

            x0 = self.grid.domains_x[c_idx]['subplot'][0]
            x1 = self.grid.domains_x[c_idx]['subplot'][1]
            y0 = self.grid.domains_y[::-1][r_idx]['subplot'][0]
            y1 = self.grid.domains_y[::-1][r_idx]['subplot'][1]

            shp = {
                'type': 'rect',
                'xref': 'paper',
                'yref': 'paper',
                'x0': x0,
                'x1': x1,
                'y0': y0,
                'y1': y1,
                'line': {
                    'width': 0.7,
                    'color': 'red',
                }
            }
            out.append(shp)

        return out

    def _get_margin_shapes(self, margin_contributions):

        out = []

        all_marg = [
            'standard',
            'legend',
            'interactivity',
            'title',
            'plotly_controls',
        ]
        all_marg_cols = [
            '#ffccaa',
            '#5599ff',
            '#d3e3b6',
            '#b0d3bf',
            '#589d62',
        ]
        marg_sum = {'t': 0, 'r': 0, 'b': 0, 'l': 0}

        for i_idx, i in enumerate(all_marg):

            if i in margin_contributions:

                for j in ['t', 'r', 'b', 'l']:
                    marg_sum[j] += self.all_margins[i].get(j, 0)

                x0, x1 = 0, 1
                y0, y1 = 0, 1

                x0 -= marg_sum['l'] / self.grid.domain_width
                x1 += marg_sum['r'] / self.grid.domain_width
                y0 -= marg_sum['b'] / self.grid.domain_height
                y1 += marg_sum['t'] / self.grid.domain_height

                shp = {
                    'type': 'rect',
                    'xref': 'paper',
                    'yref': 'paper',
                    'x0': x0,
                    'x1': x1,
                    'y0': y0,
                    'y1': y1,
                    'fillcolor': all_marg_cols[i_idx],
                    'line': {
                        'width': 0,
                    },
                    'layer': 'below',
                }
                out.append(shp)

        out[:] = out[::-1]

        return out

    def _get_legend_shape(self, legend, show_layout=False):

        out = []
        if not show_layout:
            return out

        xanchor = legend['xanchor']
        yanchor = legend['yanchor']
        width = self.legend['width']
        height = self.legend['height']

        if xanchor == 'left':
            out_x0 = legend['x']
        elif xanchor == 'right':
            out_x0 = legend['x'] - (width / self.grid.domain_width)
        elif xanchor == 'center':
            out_x0 = legend['x'] - \
                (width / (2 * self.grid.domain_width))
        out_x1 = out_x0 + (width / self.grid.domain_width)

        if yanchor == 'bottom':
            out_y0 = legend['y']
        elif yanchor == 'top':
            out_y0 = legend['y'] - (height / self.grid.domain_height)
        elif yanchor == 'middle':
            out_y0 = legend['y'] - \
                (height / (2 * self.grid.domain_height))
        out_y1 = out_y0 + (height / self.grid.domain_height)

        leg_outline = {
            'type': 'rect',
            'xref': 'paper',
            'yref': 'paper',
            'x0': out_x0,
            'x1': out_x1,
            'y0': out_y0,
            'y1': out_y1,
            'line': {
                'width': 0,
            },
            'fillcolor': FigWrap._leg_shape_color,
        }
        out.append(leg_outline)

        return out

    def _get_title_annotation(self, margin_contributions):

        marg_contr_sub = [i for i in margin_contributions
                          if i in ['standard', 'interactivity', 'legend']]

        top_offset = sum([v['t'] for k, v in self.all_margins.items()
                          if k in marg_contr_sub])
        annot = {
            'text': self.title,
            'font': {
                'size': 17,
            },
            'showarrow': False,
            'xref': 'paper',
            'yref': 'paper',
            'xanchor': 'center',
            'yanchor': 'bottom',
            'x': 0.5,
            'y': 1 + (top_offset / self.grid.domain_height),
        }
        return [annot]

    def get_layout_shapes(self, margin_contributions):
        """Generate shapes to highlight the different regions of the layout."""

        # Order is important:
        shapes = (
            self._get_margin_shapes(margin_contributions) +
            self._get_domain_shape() +
            self._get_axis_label_shapes() +
            self._get_spacing_block_shapes() +
            self._get_spacing_mid_shapes() +
            self._get_subplot_shapes()
        )

        return shapes

    def get_plotly_layout(self, margin_contributions, show_layout, show_legend):
        """Construct the Plotly layout dict."""

        layout = {
            'showlegend': show_legend,
            **self.axes_dicts,
            **self._get_plotly_layout_margin(margin_contributions)
        }

        # Add legend:
        shapes_legend = []
        if show_legend:
            legend_props = self._get_plotly_legend(margin_contributions)
            shapes_legend = self._get_legend_shape(legend_props, show_layout)
            layout.update({
                'legend': legend_props
            })

        shapes = []
        if show_layout:
            shapes.extend(self.get_layout_shapes(margin_contributions))
            shapes.extend(shapes_legend)

        # Add figure title:
        title_annot = []
        if 'title' in margin_contributions:
            title_annot = self._get_title_annotation(margin_contributions)

        annot_ax_titles = self._get_axis_title_annotations(show_layout)

        layout.update({
            'annotations': annot_ax_titles + title_annot,
            'shapes': shapes,
        })

        # Add any Plotly layout properties:
        layout.update(self.layout)

        return layout

    def get_plotly_data(self, exclude_keys=None, set_keys=None):
        """Construct the Plotly data list."""

        if set_keys is None:
            set_keys = {}

        if exclude_keys is None:
            exclude_keys = []

        exclude_keys += ['subplot_idx']

        data = []
        for i in self.data:
            dat_i = {k: v for k, v in i.items() if k not in exclude_keys}
            dat_i.update(set_keys)
            data.append(dat_i)

        return data

    @property
    def filename(self):
        return self.title or FigWrap._filename_def

    @property
    def _num_legend_items(self):
        """Get the number of legend items based on the Plotly `showlegend`
        trace property."""
        return sum([int(dat.get('showlegend', True)) for dat in self.data])

    def get_figure(self, margins=None, show_layout=False, show_legend=True,
                   widget=False):

        if margins is None:
            if widget:
                margins = list(FigWrap._fig_widget_margins_def)
            else:
                margins = list(FigWrap._fig_margins_def)

        if show_legend and 'legend' not in margins:
            margins.append('legend')

        layout = self.get_plotly_layout(margins, show_layout, show_legend)
        data = self.get_plotly_data()

        fig_class = go.FigureWidget if widget else go.Figure
        fig = fig_class(data, layout)

        return fig

    def get_figure_widget(self, margins=None, show_layout=False, show_legend=True):
        return self.get_figure(margins=margins, show_layout=show_layout,
                               show_legend=show_legend, widget=True)

    def get_legend_plotly_layout(self, show_layout=False):
        """Construct the Plotly layout dict for just the legend."""

        com_ax = {
            'domain': [0, 1],
            'showline': False,
            'zeroline': False,
            'showgrid': False,
            'showticklabels': False,
        }

        layout = {
            'showlegend': True,
            'width': self.legend['width'],
            'height': self.legend['height'],
            'margin': {
                't': 0,
                'r': 0,
                'b': 0,
                'l': 0,
            },
            'xaxis': com_ax,
            'yaxis': com_ax,
            'legend': {
                **self._extract_plotly_legend_props(),
                'x': 0.5,
                'y': 0.5,
                'xanchor': 'center',
                'yanchor': 'middle',
            },
            'hovermode': False,
        }

        if show_layout:
            layout.update({
                'shapes': [
                    {
                        'type': 'rect',
                        'xref': 'paper',
                        'yref': 'paper',
                        'x0': 0,
                        'x1': 1,
                        'y0': 0,
                        'y1': 1,
                        'line': {
                            'width': 0,
                        },
                        'fillcolor': FigWrap._leg_shape_color,
                    }
                ]
            })

        layout.update(self.layout)

        return layout

    def get_legend_figure(self, show_layout=False, widget=False):
        """Get a figure consisting of the legend only. A subplot of dimensions
        equal to the nominal legend dimensions is necessary."""

        layout = self.get_legend_plotly_layout(show_layout)
        data = self.get_plotly_data(exclude_keys=['x', 'y', 'xaxis', 'yaxis'],
                                    set_keys={'x': [0], 'y': [0]})

        fig_class = go.FigureWidget if widget else go.Figure
        fig = fig_class(data, layout)
        return fig

    def get_legend_figure_widget(self, show_layout=False):
        """Get a figure widget consisting of the legend only. A subplot of
        dimensions equal to the nominal legend dimensions is necessary."""
        fig = self.get_legend_figure(show_layout=show_layout, widget=True)
        return fig

    def write_image_legend(self, export_dir=None, formats='svg', show_layout=False,
                           overwrite=False, filename_label='', parse_latex=True):

        filename_label = filename_label + '_legend'
        fig = self.get_legend_figure(show_layout)
        path = self._write_image(fig, export_dir, formats,
                                 overwrite, filename_label, parse_latex)
        return path

    def write_image(self, export_dir=None, formats='svg', show_layout=False,
                    show_legend=True, margins=None, overwrite=False,
                    filename_label='', parse_latex=True):

        if margins is None:
            margins = list(FigWrap._fig_export_margins_def)

        fig = self.get_figure(margins, show_layout, show_legend)
        path = self._write_image(fig, export_dir, formats,
                                 overwrite, filename_label, parse_latex)
        return path

    def _write_image(self, fig, export_dir, formats, overwrite, filename_label,
                     parse_latex):
        """Wrapper around `plotly.io.write_image`"""

        if parse_latex:
            pio.orca.config.mathjax = None
        else:
            pio.orca.config.mathjax = ''

        if export_dir is None:
            export_dir = self.export_config.export_dir
        export_dir = pathlib.Path(export_dir)

        fn_with_label = self.filename
        if filename_label is not '':
            fn_with_label += '_' + filename_label

        if isinstance(formats, str):
            formats = [formats]

        paths = []
        for fmt in formats:

            file_path = export_dir.joinpath(
                fn_with_label).with_suffix('.' + fmt)
            if not overwrite:
                file_path = get_available_filename(file_path)
            paths.append(file_path)

            args = {
                'fig': fig,
                'file': str(file_path),
                'format': fmt,
                'width': fig.layout.width,
                'height': fig.layout.height,
            }
            #print('pio.orca.config.mathjax: {}'.format(pio.orca.config.mathjax))
            pio.write_image(**args)

        return paths

    def compile_tex(self, export_dir=None, formats=None, show_layout=False,
                    show_legend=True, overwrite=False, copy_raw_svg=False,
                    macros_path=None, compile_dir=None, template_path=None,
                    make_svg_changes=False):

        self._compile_tex(export_dir, formats, show_layout, show_legend,
                          overwrite, copy_raw_svg, macros_path, compile_dir,
                          template_path, make_svg_changes, is_legend=False)

    def compile_tex_legend(self, export_dir=None, formats=None, show_layout=False,
                           overwrite=False, copy_raw_svg=False,
                           macros_path=None, compile_dir=None, template_path=None,
                           make_svg_changes=False):

        self._compile_tex(export_dir, formats, show_layout, False,
                          overwrite, copy_raw_svg, macros_path, compile_dir,
                          template_path, make_svg_changes, is_legend=True)

    def _compile_tex(self, export_dir, formats, show_layout, show_legend,
                     overwrite, copy_raw_svg, macros_path, compile_dir,
                     template_path, make_svg_changes, is_legend):
        """Compile the Figure with LaTeX, optionally using a file containing
        LaTeX macros. A LaTeX distribution must be installed."""

        allowed_fmts = ['pdf', 'svg', 'png']
        fmts_msg = (
            'If specified, `formats` must be a list containing at least one '
            'of the following: {}, not "{}"'.format(allowed_fmts, formats)
        )

        if formats is None:
            formats = ['pdf']
        elif isinstance(formats, list):
            if not formats and not copy_raw_svg:
                raise ValueError(fmts_msg)
            for i in formats:
                if i not in allowed_fmts:
                    raise ValueError(fmts_msg)
        else:
            raise ValueError(fmts_msg)

        if macros_path is None:
            macros_path = self.export_config.tex_macros_path

        # Use of macros file is optional:
        use_macros = False
        if macros_path is not None:
            use_macros = True
            macros_path = pathlib.Path(macros_path)

        # Compile path must be specified at class or instance level:
        if compile_dir is None:
            compile_dir = self.export_config.tex_compile_dir
        if compile_dir is None:
            msg = ('Specify either `FigWrap.tex_compile_dir` or specify the '
                   '`compile_dir` argument to the `compile_tex` function. '
                   'This is the directory path in which the LaTeX file is '
                   'compiled. WARNING: the contents of this directory are '
                   'removed before compilation!')
            raise ValueError(msg)
        compile_dir = pathlib.Path(compile_dir)

        # LaTeX template path must be specified at class or instance level:
        if template_path is None:
            template_path = self.export_config.tex_template_path
        if template_path is None:
            msg = ('Specify either `FigWrap.tex_compile_dir` or specify the '
                   '`template_path` argument to the `compile_tex` function. '
                   'This is the template LaTeX file.')
            raise ValueError(msg)
        template_path = pathlib.Path(template_path)

        # Clean compile directory
        remove_folder_contents(str(compile_dir))

        # Write a "raw" SVG (containing LaTeX commands) using `plotly.io`:
        if export_dir is None:
            export_dir = self.export_config.export_dir
        export_dir = pathlib.Path(export_dir)

        if is_legend:
            path_raw_svg = self.write_image_legend(
                export_dir=compile_dir,
                formats='svg',
                filename_label='raw',
                show_layout=show_layout,
                parse_latex=False,
            )[0]
            base_filename = self.filename + '_legend'
        else:
            path_raw_svg = self.write_image(
                export_dir=compile_dir,
                formats='svg',
                filename_label='raw',
                show_layout=show_layout,
                show_legend=show_legend,
                parse_latex=False,
            )[0]
            base_filename = self.filename

        # If necessary, user can modify the raw SVG file here:
        if make_svg_changes:
            changes_msg = ('Make any changes to the raw SVG '
                           'file at: {}'.format(str(path_raw_svg)))
            if not confirm(changes_msg):
                return

        with template_path.open() as handle:
            tex_tmp = handle.read()

        command_input = ''
        if use_macros:
            shutil.copy(macros_path, compile_dir)
            command_input = r'\input{{{}}}'.format(macros_path.stem)

        name_raw_svg = path_raw_svg.name
        tex_tmp = tex_tmp.replace('<REPLACE_WITH_INPUT>', command_input)
        tex_tmp = tex_tmp.replace('<REPLACE_WITH_SVG_NAME>', str(name_raw_svg))

        name_tex = base_filename + '.tex'
        path_tex = compile_dir.joinpath(name_tex)

        with path_tex.open(mode='w') as handle:
            handle.write(tex_tmp)

        # Compile to PDF
        _ = subprocess.run(
            ["latexmk", "-pdf", "-shell-escape"],
            shell=True,
            cwd=str(compile_dir),
            stdout=subprocess.PIPE,
        )

        name_pdf = base_filename + '.pdf'
        path_src_pdf = compile_dir.joinpath(name_pdf)
        path_dst_pdf = export_dir.joinpath(name_pdf)

        if copy_raw_svg:
            # Copy the raw svg (produced by Plotly) to export directory:
            path_dst_raw_svg = export_dir.joinpath(name_raw_svg)
            shutil.copy(str(path_raw_svg), str(path_dst_raw_svg))

        if 'pdf' in formats:
            # Copy compiled PDF to export directory:
            shutil.copy(str(path_src_pdf), str(path_dst_pdf))

        if 'svg' in formats:
            pdf2svg(path_src_pdf, dest_dir=export_dir)

        if 'png' in formats:
            pdf2png(path_src_pdf, dest_dir=export_dir)

    def show_legend(self, sub_dir='html_plots_test', show_layout=False,
                    compile_button=True, write_button=False):

        fig = self.get_legend_figure(show_layout=show_layout)
        config = {'showLink': False, 'displayModeBar': False}
        self._show(fig, sub_dir, show_layout, False, config,
                   True, compile_button, write_button)

    def show(self, sub_dir='html_plots_test', show_layout=False, show_legend=True,
             compile_button=True, write_button=False):

        fig = self.get_figure(show_layout=show_layout, show_legend=show_legend)
        config = {'showLink': False}
        self._show(fig, sub_dir, show_layout, show_legend,
                   config, False, compile_button, write_button)

    def _show(self, fig, sub_dir, show_layout, show_legend, config, is_legend,
              compile_button, write_button):
        """Save the figure as an HTML file in a sub-directory and show this
        file as an Iframe in the Jupyter notebook."""

        cwd = pathlib.Path('').cwd()
        save_dir = cwd.joinpath(sub_dir)
        save_dir.mkdir(exist_ok=True)

        base_filename = self.filename
        if is_legend:
            base_filename += '_legend'

        save_path_abs = save_dir.joinpath(base_filename + '.html')
        save_path_rel = save_path_abs.relative_to(cwd)

        plot(fig, filename=str(save_path_abs), auto_open=False,
             include_plotlyjs='directory', config=config)

        display(IFrame(str(save_path_rel.as_posix()),
                       '100%', fig.layout.height + 30)
                )

        if compile_button:
            self._display_compile_widget(show_layout, show_legend, is_legend)
        if write_button:
            self._display_write_image_widget(
                show_layout, show_legend, is_legend)

    def _display_compile_widget(self, show_layout, show_legend, is_legend):

        compile_widget_out = Output()

        def _compile_from_button(button):

            descript = button.description
            color = button.style.button_color

            button.disabled = True
            button.description = 'Compiling with LaTeX...'
            button.style.button_color = 'gray'

            kwargs = {
                'formats': [i.description.lower()
                            for i in format_checks if i.value],
                'show_layout': layout_check.value,
                'copy_raw_svg': svg_raw_check.value,
                'make_svg_changes': modify_check.value
            }

            with compile_widget_out:

                if is_legend:
                    self.compile_tex_legend(**kwargs)
                else:
                    kwargs.update({'show_legend': legend_check.value})
                    self.compile_tex(**kwargs)

            button.disabled = False
            button.description = descript
            button.style.button_color = color

        def _on_click(button):
            thread = threading.Thread(
                target=_compile_from_button, args=(button,))
            thread.start()

        compile_button = Button(
            description='Compile LaTeX',
            disabled=False,
            tooltip='Compile with LaTeX',
        )

        check_layout = Layout(width='80px', padding='0px 0px 0px 10px')
        check_layout2 = Layout(width='110px', padding='0px 0px 0px 10px')
        pdf_check = Checkbox(description='PDF', indent=False, value=True)
        png_check = Checkbox(description='PNG', indent=False)
        svg_check = Checkbox(description='SVG', indent=False)
        svg_raw_check = Checkbox(description='Raw SVG', indent=False)
        format_checks = [pdf_check, png_check, svg_check]
        layout_check = Checkbox(description='Show layout',
                                indent=False, value=show_layout)
        legend_check = Checkbox(description='Legend',
                                indent=False, value=show_legend)
        modify_check = Checkbox(description='Modify',
                                indent=False)
        style_buttons = [
            Box(children=[legend_check], layout=check_layout2),
            Box(children=[layout_check], layout=check_layout2),
            Box(children=[modify_check], layout=check_layout2),
        ]
        if is_legend:
            style_buttons = style_buttons[1:]

        compile_widget = VBox(
            children=[
                HBox(
                    children=[
                        compile_button,
                        HBox(
                            children=[
                                Box(children=[pdf_check], layout=check_layout),
                                Box(children=[png_check], layout=check_layout),
                                Box(children=[svg_check], layout=check_layout),
                                Box(children=[svg_raw_check],
                                    layout=check_layout2),
                            ],
                            layout=Layout(
                                border='1px solid gray',
                                margin='0 0 0 10px',
                                padding='0 0 0 10px',
                            )
                        ),
                        HBox(
                            children=style_buttons,
                            layout=Layout(
                                border='1px solid gray',
                                margin='0 0 0 10px',
                                padding='0 0 0 10px',
                            )
                        ),
                    ]
                ),
                compile_widget_out
            ]
        )

        display(compile_widget)
        compile_button.on_click(_on_click)

    def _display_write_image_widget(self, show_layout, show_legend, is_legend):

        write_widget_out = Output()

        def _write_from_button(button):
            descript = button.description
            color = button.style.button_color

            button.disabled = True
            button.description = 'Writing'
            button.style.button_color = 'gray'

            kwargs = {
                'formats': [i.description.lower()
                            for i in format_checks if i.value],
                'show_layout': layout_check.value,
            }

            with write_widget_out:
                if is_legend:
                    self.write_image_legend(**kwargs)
                else:
                    kwargs.update({'show_legend': legend_check.value})
                    self.write_image(**kwargs)

            button.disabled = False
            button.description = descript
            button.style.button_color = color

        def _on_click(button):
            thread = threading.Thread(
                target=_write_from_button, args=(button,))
            thread.start()

        write_button = Button(
            description='Write image',
            disabled=False,
            tooltip='Write image',
        )

        check_layout = Layout(width='80px', padding='0px 0px 0px 10px')
        check_layout2 = Layout(width='110px', padding='0px 0px 0px 10px')
        pdf_check = Checkbox(description='PDF', indent=False, value=True)
        png_check = Checkbox(description='PNG', indent=False)
        svg_check = Checkbox(description='SVG', indent=False)
        format_checks = [pdf_check, png_check, svg_check]
        layout_check = Checkbox(description='Show layout',
                                indent=False, value=show_layout)
        legend_check = Checkbox(description='Legend',
                                indent=False, value=show_legend)

        style_buttons = [
            Box(children=[legend_check], layout=check_layout2),
            Box(children=[layout_check], layout=check_layout2),
        ]
        if is_legend:
            style_buttons = style_buttons[1:]

        write_widget = VBox(
            children=[
                HBox(
                    children=[
                        write_button,
                        HBox(
                            children=[
                                Box(children=[pdf_check], layout=check_layout),
                                Box(children=[png_check], layout=check_layout),
                                Box(children=[svg_check], layout=check_layout),
                            ],
                            layout=Layout(
                                border='1px solid gray',
                                margin='0 0 0 10px',
                                padding='0 0 0 10px',
                            )
                        ),
                        HBox(
                            children=style_buttons,
                            layout=Layout(
                                border='1px solid gray',
                                margin='0 0 0 10px',
                                padding='0 0 0 10px',
                            )
                        ),
                    ]
                ),
                write_widget_out
            ]
        )

        display(write_widget)
        write_button.on_click(_on_click)
