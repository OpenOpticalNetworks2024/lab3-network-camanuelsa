import json
import matplotlib.pyplot as plt
import math
from core.parameters import cf

class Signal_information(object):
    def __init__(self, signal_power, path):
        self._signal_power = signal_power
        self._noise_power = 1e-12
        self._latency = 0.0
        self._path = path

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
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
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
            line_label = self.label + nxt
            if line_label in self._successive:
                self._successive[line_label].propagate(sgn)


class Line(object):
    def __init__(self, label, length):
        self._label = label
        self._length = length
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

    def latency_generation(self):
        return self._length / cf

    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self._length

    def propagate(self, sgn):
        sgn.update_latency(self.latency_generation())
        sgn.update_noise_power(self.noise_generation(sgn.signal_power))
        if sgn.path:
            nxt = sgn.path[0]
            if nxt in self._successive:
                self._successive[nxt].propagate(sgn)

class Network(object):
    def __init__(self, json_file):
        self._nodes = {}
        self._lines = {}

        file = open(json_file, 'r')
        data = json.load(file)
        file.close()

        for label, node_data in data.items():
            node = Node(label, tuple(node_data['position']), node_data['connected_nodes'])
            self._nodes[label] = node

        for node_label, node in self._nodes.items():
            for connected_node_label in node.connected_nodes:
                if connected_node_label in self._nodes:
                    connected_node = self._nodes[connected_node_label]
                    distance = math.sqrt((node.position[0] - connected_node.position[0]) ** 2 + (node.position[1] - connected_node.position[1]) ** 2)
                    line_label = node_label + connected_node_label
                    self._lines[line_label] = Line(line_label, distance)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        fig, ax = plt.subplots()
        for line in self._lines.values():
            node_labels = line.label
            x_values = [self._nodes[node_labels[0]].position[0], self._nodes[node_labels[1]].position[0]]
            y_values = [self._nodes[node_labels[0]].position[1], self._nodes[node_labels[1]].position[1]]
            ax.plot(x_values, y_values, 'go-')

        for node in self._nodes.values():
            ax.text(node.position[0], node.position[1], node.label, fontsize=24)

        plt.xlabel('X position')
        plt.ylabel('Y position')
        plt.title('Network')
        plt.grid(True)
        plt.savefig('network.png')
        plt.show()

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2, path=None):
        if path is None:
            path = []
        path = path + [label1]
        if label1 == label2:
            return [path]
        if label1 not in self._nodes:
            return []
        paths = []
        for node_label in self._nodes[label1].connected_nodes:
            if node_label not in path:
                new_paths = self.find_paths(node_label, label2, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        for node_label, node in self._nodes.items():
            for connected_node_label in node.connected_nodes:
                if connected_node_label in self._nodes:
                    line_label = node_label + connected_node_label
                    node.successive[line_label] = self._lines[line_label]
                    self._lines[line_label].successive[connected_node_label] = self._nodes[connected_node_label]

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        start_node_label = signal_information.path[0]
        self._nodes[start_node_label].propagate(signal_information)
        return signal_information