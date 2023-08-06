
import random
import ipywidgets as wg

from traitlets import observe, validate, Unicode, Int, Bytes, Float, TraitError

from .widget_util import Util
from .__meta__ import __version_js__

__semver_range_frontend__ = '~' + __version_js__


class Iframe(wg.DOMWidget):
    """
    File upload widget
    """
    _model_name = Unicode('IframeModel').tag(sync=True)
    _view_name = Unicode('IframeView').tag(sync=True)
    _model_module = Unicode('ipyiframe').tag(sync=True)
    _view_module = Unicode('ipyiframe').tag(sync=True)
    _view_module_version = Unicode(__semver_range_frontend__).tag(sync=True)
    _model_module_version = Unicode(__semver_range_frontend__).tag(sync=True)

    _id = Int(0).tag(sync=True)

    help = 'The URL of the page to embed'
    src = Unicode('', help=help).tag(sync=True)

    help = 'The content of the page that the embedded context is to contain'
    srcdoc = Bytes(help=help).tag(sync=True, to_json=Util.to_json)

    help = 'Indicates the width of the frame in CSS pixels'
    width = Int(0, help=help).tag(sync=True)

    help = 'Indicates the height of the frame in CSS pixels'
    height = Int(0, help=help).tag(sync=True)

    help = 'Iframe border CSS'
    border = Unicode('', help=help).tag(sync=True)

    help = 'Iframe margin CSS'
    margin = Unicode('', help=help).tag(sync=True)

    help = 'Iframe padding CSS'
    padding = Unicode('', help=help).tag(sync=True)

    help = 'Indicates if the iframe has a scroll bar: auto (only when needed), or yes, or no'
    scrolling = Unicode('', help=help).tag(sync=True)

    help = 'Indicates scaling factor tyically between 0.1 and 2.0'
    scale = Float(1.0, help=help).tag(sync=True)

    help = 'Indicates where the iframe is located, by default "top left" - only useful if scale is not 1.0'
    transform_origin = Unicode('', help=help).tag(sync=True)

    help = 'Compress level: from 1 to 9 - 0 for no compression'
    compress_level = Int(1, help=help).tag(sync=True)

    def __init__(self,
                 src='',
                 srcdoc='',
                 width=400,
                 height=150,
                 border='1 px solid gray',
                 margin='0 px',
                 padding='1 px',
                 scrolling='auto',
                 scale=1.0,
                 transform_origin='top left',
                 compress_level=9,
                 ):
        """
        Instantiate widget
        """

        self._id = random.randint(0, int(1e9))

        msg = 'Exactly one of src or srcdoc must be set'
        assert ((src != '') != (srcdoc != '')), msg

        self.src = src
        self.srcdoc = srcdoc.encode('utf-8')
        self.width = width
        self.height = height
        self.border = border
        self.margin = margin
        self.margin = margin
        self.padding = padding
        self.scrolling = scrolling
        self.scale = scale
        self.transform_origin = transform_origin
        self.compress_level = compress_level

        super().__init__()

    @validate('compress_level')
    def _valid_compress_level(self, proposal):
        if proposal['value'] not in range(1, 10):
            raise TraitError('compress_level must be an int from 1 to 9 included')
        return proposal['value']

    @validate('scrolling')
    def _valid_scrolling(self, proposal):
        if proposal['value'] not in ['auto', 'yes', 'no']:
            raise TraitError('scrolling must be ["auto", "yes", "no"]')
        return proposal['value']
