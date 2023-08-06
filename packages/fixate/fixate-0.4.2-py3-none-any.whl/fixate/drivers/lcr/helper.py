from abc import ABCMeta, abstractmethod

from fixate.core.discover import discover_sub_classes, open_visa_instrument


def open(restrictions=None):
    """Open is the public api for the dmm driver for discovering and opening a connection
    to a valid Digital Multimeter.
    At the moment opens the first dmm connected
    :param restrictions:
    A dictionary containing the technical specifications of the required equipment
    :return:
    A instantiated class connected to a valid dmm
    """
    return open_visa_instrument("LCR", restrictions)


def discover():
    """Discovers the dmm classes implemented
    :return:
    """
    return set(discover_sub_classes(LCR))


def validate_specifications(_class, specifications):
    """Validates the implemented dmm class against the specifications provided
    :return:
    True if all specifications are met
    False if one or more specifications are not met by the class
    """
    raise NotImplementedError()

class TestResult:
    Rs = None
    Cs = None
    Rp = None
    Cp = None
    Ls = None
    Lp = None
    Z = None
    TH = None
    F = None
    D = None
    Q = None

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

class LCR(metaclass=ABCMeta):
    REGEX_ID = "LCR"
    frequency = None
    range = None

    def __init__(self, instrument):
        self.instrument = instrument
        self.samples = 1

    @abstractmethod
    def measure(self, func=None, multiple_results=False, **mode_params):
        pass

    @abstractmethod
    def reset(self):
        pass