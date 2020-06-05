import typing as tp

import numpy as np

class PyplotBuilder:
    def __init__(self) -> None:
        return
        

    def build(self, elem, pycode: str, canvas=None):
        _globals = globals()
        _globals["np"] = np

        self.vars = {}

        exec(pycode, _globals, self.vars)

        self.fig = plt.figure() if canvas is None else canvas

        return self._build(elem)


    def _build(self, elem):
        name, children, args = elem

        fn_name = f"_build_{name}"

        if not hasattr(self, fn_name):
            raise Exception(fn_name)

        return getattr(self, fn_name)(children, args)


    def _build_Root(self, children, args):
        self.ax = self.fig.gca()

        for child in children:
            self._build(child)

        if "title" in args.keys():
            self.fig.suptitle(args["title"])

        return self.fig


    def _build_Line(self, children, args):
        x = self.vars[args["x"].name]
        y = self.vars[args["y"].name]

        linewidth = args["width"] if "width" in args.keys() else None

        self.ax.plot(x, y, linewidth=linewidth)
