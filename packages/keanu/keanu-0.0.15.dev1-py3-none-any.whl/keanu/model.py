from .net import BayesNet
from .vertex.base import Vertex

class Model:
    def __init__(self, vertices={}):
        self.__dict__["_vertices"] = {}
        self.__dict__["_vertices"].update(vertices)

    def to_bayes_net(self):
        return BayesNet((filter(lambda vertex: isinstance(vertex, Vertex), self._vertices.values())))

    def __setattr__(self, k, v):
        if k in self.__dict__:
            super(Model, self).__setattr__(k, v)
        else:
            self._vertices[k] = v

    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        return self._vertices[k]

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass
