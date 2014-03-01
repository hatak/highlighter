from highlighter._mapping import FONTS

def get_all_fonts():
    """
    Return a font of tuples in the form ``(name, allow_japanese)`` of all registered fonts.
    """
    for item in FONTS.itervalues():
        yield item[1:]
