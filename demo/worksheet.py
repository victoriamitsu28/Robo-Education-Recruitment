"""Complete these two formulas, then compare with the reference detector."""


def centroid_and_error(moments, width):
    if moments['m00'] <= 0:
        return None
    # Exercise: replace both expressions. Keep None for an invalid detection.
    cx = ...
    error = ...
    return cx, error
