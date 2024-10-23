import json

class Signal_information(object):
    def __init__(self, signal_power, path):
        self._signal_power = float(signal_power)
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = list(map(str, path))

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self, inc):
        self._signal_power += inc

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, val):
        self._noise_power = val

    def update_noise_power(self, inc):
        self._noise_power += inc

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, val):
        self._latency = val

    def update_latency(self, inc):
        self._latency += inc

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

    def update_path(self):
        if self._path:
            self._path.pop(0)


class Node(object):
    def __init__(self, label, position, connected_nodes):
        self._label = str(label)
        self._position = tuple(position)
        self._connected_nodes = list(map(str, connected_nodes))
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, dic):
        self._successive = dic

    def propagate(self, sgn):
        sgn.update_path()
        if sgn.path:
            nxt = sgn.path[0]
            if nxt in self._successive:
                self._successive[nxt].propagate(sgn)


class Line(object):
    def __init__(self, label, length):
        self._label = str(label)
        self._length = float(length)
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, dic):
        self._successive = dic

    def latency_generation(self, cf):
        return self._length / cf

    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self._length

    def propagate(self, sgn, cf):
        sgn.update_latency(self.latency_generation(cf))
        sgn.update_noise_power(self.noise_generation(sgn.signal_power))
        if sgn.path:
            nxt = sgn.path[0]
            if nxt in self._successive:
                self._successive[nxt].propagate(sgn, cf)

class Network(object):
    def __init__(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def lines(self):
        pass

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass