import numbers


attribs = ['corners', 'shotson', 'cards']


class SingleParamState:
    """
    Describes the param state, i.e. set the mean and standard deviation for the
    attribute of interest of the match
    """
    def __init__(self, mean=None, stdev=None):
        self._mean = mean
        self._stdev = stdev

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, new_val):
        if (not isinstance(new_val, numbers.Real)) or (new_val < 0):
            raise Exception("Expected value entered is not a positive number")
        else:
            self._mean = new_val

    @property
    def stdev(self):
        return self._stdev

    @stdev.setter
    def stdev(self, new_val):
        if (not isinstance(new_val, numbers.Real)) or (new_val < 0):
            raise Exception("Standard deviation value entered is not a positive number")
        else:
            self._stdev = new_val


class ParamStates:
    """
    Creates an attribute for each quantity of interest with the attribute holding
    a SingleParamState.
    """
    def __init__(self, single_param_states: dict, version_one: bool = True):
        self.version_one = version_one
        for attrib in attribs:
            self.set_param_state(attrib, single_param_states.get(attrib, SingleParamState()))

    def set_param_state(self, attrib, single_param_state):
        setattr(self, attrib, single_param_state)
        if self.version_one:
            self.use_version_one_approx(attrib)

    def use_version_one_approx(self, attrib):
        single_param_state = getattr(self, attrib)
        single_param_state.stdev = single_param_state.mean/2
