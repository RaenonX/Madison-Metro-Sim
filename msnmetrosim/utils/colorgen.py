"""Generate a color and return it."""

__all__ = ("get_color",)

# Based on https://www.oberlo.com/blog/color-combinations-cheat-sheet
COLOR_PALETTE = [
    "#E1A730", "#2879C0", "#AB3910", "#2B5615", "#F8CF2C", "#DB55D4", "#9B948A",
    "#FF0BAC", "#490034", "#F6B405", "#FDBCFD", "#284E60", "#F99B45", "#63AAC0",
    "#D95980", "#425F06", "#0352A0", "#EF3340", "#A16AE8", "#B19FF9", "#0E3506",
    "#FEA303"
]  # pylint: disable=invalid-name
_COUNTER: int = -1  # pylint: disable=invalid-name


def get_color():
    """
    Get a color from palette in HEX. The color picking process is sequential.

    Currently not used in any place, but may be used in the future.
    """
    global _COUNTER  # pylint: disable=global-statement

    _COUNTER += 1
    _COUNTER %= len(COLOR_PALETTE)

    return COLOR_PALETTE[_COUNTER]
