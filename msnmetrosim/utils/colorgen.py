"""Randomly generate a color and return it."""

__all__ = ("get_color",)

# Based on https://www.oberlo.com/blog/color-combinations-cheat-sheet
_palette = [
    "#E1A730", "#2879C0", "#AB3910", "#2B5615", "#F8CF2C", "#DB55D4", "#9B948A",
    "#FF0BAC", "#490034", "#F6B405", "#FDBCFD", "#284E60", "#F99B45", "#63AAC0",
    "#D95980", "#425F06", "#0352A0", "#EF3340", "#A16AE8", "#B19FF9", "#0E3506",
    "#FEA303"
]  # pylint: disable=invalid-name
_counter: int = -1  # pylint: disable=invalid-name


def get_color():
    """
    Get a color from palette in HEX. The color picking process is sequential.

    Currently not used in any place, but may be used in the future.
    """
    global _palette, _counter  # pylint: disable=global-statement

    _counter += 1
    _counter %= len(_palette)

    return _palette[_counter]
