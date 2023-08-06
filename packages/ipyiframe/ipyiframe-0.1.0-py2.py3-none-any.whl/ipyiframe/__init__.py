
from .__meta__ import __version__

from .widget_iframe import Iframe


def _jupyter_nbextension_paths():
    return [{
        # fixed syntax
        'section': 'notebook',
        # path relative to module directory - here: ipyiframe
        'src': 'static',
        # directory in the `nbextension/` namespace
        'dest': 'ipyiframe',
        # path in the `nbextension/` namespace
        'require': 'ipyiframe/extension'
    }]
