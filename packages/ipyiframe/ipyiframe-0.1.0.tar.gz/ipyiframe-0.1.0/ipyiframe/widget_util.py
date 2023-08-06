
import zlib


class Util:
    """
    """

    @staticmethod
    def to_json(obj, widget):
        """
        """
        level = widget.compress_level
        compressed = zlib.compress(obj, level=level)

        return compressed
