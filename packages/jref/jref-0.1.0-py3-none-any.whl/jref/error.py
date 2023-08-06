class Error(Exception):
    def __str__(self):
        return self.MESSAGE.format(*self.args)
