# -*- coding: future_fstrings -*-

# Copyright 2018 Streamlit Inc. All rights reserved.

"""Allows us to create and absorb changes (aka Deltas) to elements."""

# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
from streamlit.compatibility import setup_2_3_shims
setup_2_3_shims(globals())

from functools import wraps
import io
import json
import math
import numpy as np
import pandas as pd
import random
import sys
import textwrap
import traceback

from streamlit import DeckGlChart
from streamlit import VegaLiteChart
from streamlit import data_frame_proto
from streamlit import generic_binary_proto
from streamlit import image_proto
from streamlit import protobuf
from streamlit.Chart import Chart
from streamlit.caseconverters import to_snake_case
from streamlit.chartconfig import CHART_TYPES
from streamlit.logger import get_logger

EXPORT_FLAG = '__export__'

# setup logging
from streamlit.logger import get_logger
LOGGER = get_logger()


MAX_DELTA_BYTES = 14 * 1024 * 1024 # 14MB


def _export(method):
    """Flag this DeltaGenerator method to be exported to the streamlit
    package.

    This should be the outermost decorator, i.e. before all others.
    """
    setattr(method, EXPORT_FLAG, True)
    return method

def _create_element(method):
    """Allows you to easily create a method which creates a new element delta.

    Converts a method of the with arguments (self, element, ...) into a method
    with arguments (self, ...). Thus, the intantiation of the element proto
    object and creation of the element are handled automaticallyself.

    Args
    ----
    method: A DeltaGenerator method with arguments (self, element, ...)

    Returns
    -------
    A new DeltaGenerator method with arguments (self, ...)
    """
    @wraps(method)
    def wrapped_method(self, *args, **kwargs):
        try:
            def create_element(element):
                method(self, element, *args, **kwargs)
            return self._new_element(create_element)
        except Exception as e:
            self.exception(e)
            import sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, file=sys.stderr)

    return wrapped_method

class DeltaGenerator(object):
    """
    Creates delta messages. If id is set to none, then an id is created for each
    message and a new Generator with that id is created."
    """

    def __init__(self, queue, id=None):
        """
        Constructor.

        queue - callback when delta is generated
        id    - id for deltas, or None to create a new generator each time
        """
        self._queue = queue
        if id == None:
            self._generate_new_ids = True
            self._next_id = 0
        else:
            self._generate_new_ids = False
            self._id = id

    @_export
    @_create_element
    def balloons(self, element):
        """Draws celebratory balloons!
        """
        element.balloons.type = protobuf.Balloons.DEFAULT
        element.balloons.execution_id = random.randrange(0xFFFFFFFF)

    @_export
    @_create_element
    def text(self, element, body):
        """Writes fixed width text.

        Args
        ----
        body : string
            The string to display.
        """
        element.text.body = str(body)
        element.text.format = protobuf.Text.PLAIN

    @_export
    @_create_element
    def markdown(self, element, body):
        """Displays the string, formatted as markdown.

        Args
        ----
        string : string
            The string to display as markdown.

        Returns
        -------
        A DeltaGenerator object which allows you to overwrite this element.
        """
        element.text.body = textwrap.dedent(body).strip()
        element.text.format = protobuf.Text.MARKDOWN

    @_export
    @_create_element
    def json(self, element, body):
        """Displays the object as a pretty JSON string.

        Args
        ----
        object : object
            The object to stringify. All referenced objects should have JSON counterpart.
            If object is a string, we assume it is already JSON formatted.
        """
        element.text.body = (body if isinstance(body, string_types) else json.dumps(body))
        element.text.format = protobuf.Text.JSON

    @_export
    @_create_element
    def title(self, element, string):
        """Displays the string as a title (h1) header.

        Args
        ----
        string : string
            The string to display.

        Returns
        -------
        A DeltaGenerator object which allows you to overwrite this element.
        """
        element.text.body = str(string)
        element.text.format = protobuf.Text.TITLE

    @_export
    @_create_element
    def header(self, element, string):
        """Displays the string as a h2 header.

        Args
        ----
        string : string
            The string to display.

        Returns
        -------
        A DeltaGenerator object which allows you to overwrite this element.
        """
        element.text.body = str(string)
        element.text.format = protobuf.Text.HEADER

    @_export
    @_create_element
    def subheader(self, element, string):
        """Displays the string as a h3 header.

        Args
        ----
        string : string
            The string to display.

        Returns
        -------
        A DeltaGenerator object which allows you to overwrite this element.
        """
        element.text.body = str(string)
        element.text.format = protobuf.Text.SUB_HEADER

    @_export
    @_create_element
    def error(self, element, body):
        """
        Creates an element with showing an error string.

        Args
        ----
        body: str
            The text to display. Can include newlines.
        """
        element.text.body = str(body)
        element.text.format = protobuf.Text.ERROR

    @_export
    @_create_element
    def warning(self, element, body):
        """
        Creates an element with showing an warning string.

        Args
        ----
        body: str
            The text to display. Can include newlines.
        """
        element.text.body = str(body)
        element.text.format = protobuf.Text.WARNING

    @_export
    @_create_element
    def info(self, element, body):
        """
        Creates an element with showing an info string.

        Args
        ----
        body: str
            The text to display. Can include newlines.
        """
        element.text.body = str(body)
        element.text.format = protobuf.Text.INFO

    @_export
    @_create_element
    def success(self, element, body):
        """
        Creates an element with showing an success string.

        Args
        ----
        body: str
            The text to display. Can include newlines.
        """
        element.text.body = str(body)
        element.text.format = protobuf.Text.SUCCESS

    @_export
    def link(self, *args, **kwargs):
        """
        Creates an element showing a link

        Args
        ----
        body: str
            The link.
        """
        raise RuntimeError('Link() is deprecated. Please use markdown() instead.')

    @_export
    @_create_element
    def help(self, element, obj):
        """Displays the doc string for this object, nicely formatted.

        Displays the doc string for this object. If the doc string is
        represented as ReStructuredText, then it will be converted to
        Markdown on the client before display.

        Args
        ----
        obj: Object
            The object to display.

        Returns
        -------
        A DeltaGenerator object which allows you to overwrite this element.

        Example
        -------
        To learn how the st.write function works, call::
            st.help(st.write)
        """
        if not hasattr(obj, '__name__'):
            raise RuntimeError(f'help() expects module or method, not type `{type(obj).__name__}`')
        element.doc_string.name = obj.__name__
        try:
            element.doc_string.module = obj.__module__
        except AttributeError:
            pass
        doc_string = obj.__doc__
        if not isinstance(doc_string, string_types):
            doc_string = f'No docs available.'
        element.doc_string.doc_string = textwrap.dedent(doc_string).strip()

    @_export
    @_create_element
    def exception(self, element, exception, exception_traceback=None):
        """
        Prints this exception to the Report.

        Args
        ----
        exception: Exception
            The exception to display.
        exception_traceback: Exception Traceback or None
            Set to non-None to force the display of this traceback. Otherwise,
            the traceback will be figure out implicitly.
        """
        element.exception.type = type(exception).__name__
        element.exception.message = str(exception)

        # Get and extract the traceback for the exception.
        if exception_traceback != None:
            extracted_traceback = traceback.extract_tb(exception_traceback)
        elif hasattr(exception, '__traceback__'):
            # This is the Python 3 way to get the traceback.
            extracted_traceback = traceback.extract_tb(exception.__traceback__)
        else:
            # Hack for Python 2 which will extract the traceback as long as this
            # method was called on the exception as it was caught, which is
            # likely what the user would do.
            _, live_exception, live_traceback = sys.exc_info()
            if exception == live_exception:
                extracted_traceback = traceback.extract_tb(live_traceback)
            else:
                extracted_traceback = None

        # Format the extracted traceback and add it to the protobuf element.
        if extracted_traceback == None:
            stack_trace = [
                'Cannot extract the stack trace for this exception. '\
                'Try calling exception() within the `catch` block.']
        else:
            stack_trace = traceback.format_list(extracted_traceback)
        element.exception.stack_trace.extend(stack_trace)

    @_export
    def dataframe(self, pandas_df):
        """
        Renders a dataframe to the client.

        pandas_df - The dataframe.
        """
        def set_data_frame(element):
            data_frame_proto.marshall_data_frame(pandas_df, element.data_frame)
        return self._new_element(set_data_frame)

    def _native_chart(self, chart):
        """Displays a chart.
        """
        def set_chart(element):
            chart.marshall(element.chart)
        return self._new_element(set_chart)

    @_export
    @_create_element
    def vega_lite_chart(self, element, data=None, spec=None, **kwargs):
        """Displays a chart using the Vega Lite library.

        Parameters
        ----------
        data : list or Numpy Array or DataFrame or None
            Data to be plotted.

        spec : dict
            The Vega Lite spec for the chart.

        **kwargs : any
            Same as spec, but as keywords. Keys are "unflattened" at the
            underscore characters. For example, foo_bar_baz=123 becomes
            foo={'bar': {'bar': 123}}.

        """
        VegaLiteChart.marshall(element.vega_lite_chart, data, spec, **kwargs)

    @_export
    @_create_element
    def pyplot(self, element, fig=None):
        """Displays a matplotlib.pyplot image.

        Args
        ----
        fig : Matplotlib Figure
            The figure to plot. When this argument isn't specified, which is
            the usual case, this function will render the global plot.
        """
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            plt.ioff()
        except ImportError:
            raise ImportError(f'pyplot() command requires matplotlib')

        # You can call .savefig() on a Figure object or directly on the pyplot
        # module, in which case you're doing it to the latest Figure.
        if not fig:
            fig = plt

        image = io.BytesIO()
        fig.savefig(image, format='png')
        image_proto.marshall_images(image, None, -2, element.imgs, False)

    # TODO: Make this accept files and strings/bytes as input.
    @_export
    @_create_element
    def image(self, element, image, caption=None, width=None,
            use_column_width=False, clamp=False):
        """Displays an image or images.

        Args
        ----
        image : image or array of images
            Monochrome image of shape (w,h) or (w,h,1)
            OR a color image of shape (w,h,3)
            OR an RGBA image of shape (w,h,4)
            OR a list of one of the above
        caption : string or list of strings
            String caption
        width : int or None
            Image width. 'None' means use the image width.
        use_column_width : bool
            If True, set the image width to the column width. This overrides
            the `width` parameter.
        clamp : bool
            Clamp the image to the given range.
        """
        if use_column_width:
            width = -2
        elif width == None:
            width = -1
        elif width <= 0:
            raise RuntimeError('Image width must be positive.')
        image_proto.marshall_images(image, caption, width, element.imgs, clamp)

    # TODO: remove `img()`, now replaced by `image()`
    @_export
    def img(self, *args, **kwargs):
        """DEPRECATED. Use st.image() instead."""
        raise RuntimeError('DEPRECATED. Please use image() instead.')

    @_export
    @_create_element
    def audio(self, element, data, format='audio/wav'):
        """Inserts an audio player.

        Args
        ----
        data : The audio bytes as a str, bytes, BytesIO, NumPy array, or a file
            opened with io.open(). Must include headers and any other bytes
            required in the actual file.
        format : The mime type for the audio file. Defaults to 'audio/wav'.
            See https://tools.ietf.org/html/rfc4281 for more info.
        """
        # TODO: Provide API to convert raw NumPy arrays to audio file (with
        # proper headers, etc)?
        generic_binary_proto.marshall(element.audio, data)
        element.audio.format=format

    @_export
    @_create_element
    def video(self, element, data, format='video/mp4'):
        """Inserts a video player.

        Args
        ----
        data : The video bytes as a str, bytes, BytesIO, NumPy array, or a file
            opened with io.open(). Must include headers and any other bytes
            required in the actual file.
        format : The mime type for the video file. Defaults to 'video/mp4'.
            See https://tools.ietf.org/html/rfc4281 for more info.
        """
        # TODO: Provide API to convert raw NumPy arrays to video file (with
        # proper headers, etc)?
        generic_binary_proto.marshall(element.video, data)
        element.video.format=format

    @_export
    @_create_element
    def progress(self, element, value):
        """Displays the string as a h3 header.

        Args
        ----
        value : int
            The percentage complete: 0 <= value <= 100

        Returns
        -------
        A DeltaGenerator object which allows you to overwrite this element.

        Examples
        --------
        Here is an example of a progress bar increasing over time:
            import time
            my_bar = st.progress(0)
            for percent_complete in range(100):
                my_bar.progress(percent_complete + 1)
        """
        element.progress.value = value

    @_export
    @_create_element
    def empty(self, element):
        """Adds an element that will not be rendered.
        """
        # NOTE: protobuf needs something to be set
        element.empty.unused = True

    @_export
    @_create_element
    def map(self, element, points):
        """Creates a map element.

        Args
        ----
        points : DataFrame
            The points to display. Must have 'lat' and 'lon' columns.
        """
        LAT_LON = ['lat', 'lon']
        assert set(points.columns) >= set(LAT_LON), \
            'Map points must contain "lat" and "lon" columns.'
        data_frame_proto.marshall_data_frame(points[LAT_LON],
            element.map.points)

    @_export
    @_create_element
    def deck_gl_chart(self, element, data=None, spec=None, **kwargs):
        """Draw a map chart using the DeckGL library.

        See https://deck.gl/#/documentation for more info.

        Parameters
        ----------
        data : list or Numpy Array or DataFrame or None
            Data to be plotted, if no layer specified.

        spec : dict
            Keys/values in this dict can be:
            - Anything accepted by DeckGl's top level element.
            - "layers": a list of dicts containing information to build a new
              DeckGl layer in the map. Each layer accepts the following keys:
                - "data" : DataFrame
                    The data for that layer.
                - "type" : string - a layer type accepted by DeckGl
                    The layer type, such as 'HexagonLayer', 'ScatterplotLayer',
                    etc.
                - "encoding" : dict - Accessors accepted by that layer type.
                  The keys should be the accessor name without the "get"
                  prefix. For example instead of "getColor" you should
                  useinstead of "getColor" you should use "color". If strings,
                  these get automatically transformed into getters for that
                  column.
                - And anything accepted by that layer type

        **kwargs : any
            Same as spec, but as keywords. Keys are "unflattened" at the
            underscore characters. For example, foo_bar_baz=123 becomes
            foo={'bar': {'bar': 123}}.

        Examples
        --------
            # If you pass in a dataframe and no spec, you get a scatter plot.
            st.deck_gl_chart(my_data_frame)

            # For anything else, pass in a spec and no top-level dataframe. For
            # instance:
            st.deck_gl_chart(
                viewport={
                    'latitude': 37.76,
                    'longitude': -122.4,
                    'zoom': 11,
                    'pitch': 50,
                },
                layers=[{
                    'type': 'HexagonLayer',
                    'data': my_dataframe,
                    'radius': 200,
                    'elevationScale': 4,
                    'elevationRange': [0, 1000],
                    'pickable': True,
                    'extruded': True,
                }, {
                    'type': 'ScatterplotLayer',
                    'data': my_other_dataframe,
                    'pickable': True,
                    'autoHighlight': True,
                    'radiusScale': 0.02,
                    'encoding': {
                        'radius': 'exits',
                    },
                }])

        """
        DeckGlChart.marshall(element.deck_gl_chart, data, spec, **kwargs)

    @_export
    @_create_element
    def table(self, element, df):
        """Creates a map element.

        Args
        ----
        df : DataFrame
            The table data.
        """
        data_frame_proto.marshall_data_frame(df, element.table)

    def add_rows(self, df):
        assert not self._generate_new_ids, \
            'Only existing elements can add_rows.'
        delta = protobuf.Delta()
        delta.id = self._id
        data_frame_proto.marshall_data_frame(df, delta.add_rows)
        self._queue(delta)
        return self

    def _new_element(self, set_element):
        """
        Creates a new element delta, sets its value with set_element,
        sends the new element to the delta queue, and finally
        returns a generator for that element ID.

        set_element - Function which sets the fields for a protobuf.Element
        """
        # Create a delta message.
        delta = protobuf.Delta()
        set_element(delta.new_element)

        # Figure out if we need to create a new ID for this element.
        if self._generate_new_ids:
            delta.id = self._next_id
            generator = DeltaGenerator(self._queue, delta.id)
            self._next_id += 1
        else:
            delta.id = self._id
            generator = self

        self._queue(delta)
        return generator


def createNewDelta():
    """Creates a new DeltaGenerator and sets up some basic info."""
    delta = protobuf.Delta()
    return delta


def register_native_chart_method(chart_type):
    """Adds a chart-building method to DeltaGenerator for a specific chart type.

    Args:
        chart_type -- A string with the snake-case name of the chart type to
        add.
    """
    @_export
    def chart_method(self, data, **kwargs):
        return self._native_chart(Chart(data, type=chart_type, **kwargs))

    setattr(DeltaGenerator, chart_type, chart_method)


# Add chart-building methods to DeltaGenerator
for chart_type in CHART_TYPES:
    register_native_chart_method(to_snake_case(chart_type))
