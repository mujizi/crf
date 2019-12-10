# -*- coding: UTF-8 -*-


class LengthNotEqualException(Exception):
    """
    corresponded data length is not equal.
    e.g. token count and pos tag count are not equal.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ModelNotExistedException(Exception):
    """
    model file doesn't exist
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FeatureNotImplemented(Exception):
    """
    Feature is not implemented.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParameterError(Exception):
    """
    parameter havs error.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
