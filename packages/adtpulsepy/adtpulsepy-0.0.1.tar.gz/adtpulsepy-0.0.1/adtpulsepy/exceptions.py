"""The exceptions used by ADTPulsePy."""

class ADTPulseException(Exception):
    """Class to throw general abode exception."""

    def __init__(self, error, details=None):
        """Initialize ADTPulseException."""
        # Call the base class constructor with the parameters it needs
        super(ADTPulseException, self).__init__(error[1])

        self.errcode = error[0]
        self.message = error[1]
        self.details = details


class ADTPulseAuthException(ADTPulseException):
    """Class to throw authentication exception."""

    pass
