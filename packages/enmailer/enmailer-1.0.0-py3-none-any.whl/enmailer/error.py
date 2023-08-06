class DataTypeError(Exception):
    def __init__(self, value, dtype):
        self.value = value
        self.dtype = dtype

    def __str__(self):
        return "`{}` should be in <{}> type.".format(self.value, self.dtype)


class InvalidEmailAddressError(Exception):
    def __init__(self, value, dtype):
        self.value = value
        self.dtype = dtype

    def __str__(self):
        return "`{}` (for `{}`) is not a valid email address." \
            .format(self.value, self.dtype)
