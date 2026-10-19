class RegressionError(Exception):
    """Error raised when linear regression fails."""

class OutsideBoundsError(Exception):
    """Error raised when a value is outside its own bounds."""

class SmoothingError(Exception):
    """Error raised when signal smoothing fails."""

class PropertyError(Exception):
    pass

class MissingModelError(Exception):
    """Error raised when a model could not be found."""