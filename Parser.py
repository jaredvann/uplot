import typing as tp

import lark


class Var():
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Var({self.name})"


class Parser:
    def __init__(self, spec) -> None:
        self.spec = spec

        self.scope = []
        self.cur_scope = None

        self.add_to_scope("Root")


    def add_to_scope(self, c: str):
        self.scope.append(c)
        self.cur_scope = self.spec[c]


    def pop_scope(self):
        self.scope.pop()
        self.cur_scope = self.spec[self.scope[-1]]


    def parse(self, ast: tp.Union[lark.Tree, lark.Token]) -> None:
        return self._parse(ast)


    def _parse(self, ast: tp.Union[lark.Tree, lark.Token]) -> None:
        fn_name = f"_parse_{ast.data}"

        if not hasattr(self, fn_name):
            raise NotImplementedError(fn_name)

        return getattr(self, fn_name)(ast)


    def _parse_arg_pair(self, ast: lark.Tree) -> None:
        arg_name = ast.children[0].value
        
        if arg_name not in self.cur_scope["fields"].keys():
            raise Exception(arg_name)

        # TODO: type checking

        arg_value = self._parse(ast.children[1])

        return (arg_name, arg_value)


    def _parse_arg_val(self, ast: lark.Tree) -> None:
        val = ast.children[0]

        if isinstance(val, lark.Tree):
            return self._parse(val)
        elif val.type == "STR":
            return Var(val.value)
        elif val.type == "NUMBER":
            return float(val.value)
        else:
            raise NotImplementedError()


    def _parse_elem(self, ast: lark.Tree) -> None:
        return self._parse(ast.children[0])


    def _parse_object(self, ast: lark.Tree) -> None:
        name, *args = ast.children

        if name.value not in self.cur_scope["allowed_children"]:
            raise Exception
        
        self.add_to_scope(name)

        arg_names = [arg.children[0].children[0].value for arg in args if arg.children[0].data == "arg_pair"]

        for req_field_name in self.cur_scope["required_fields"]:
            if req_field_name not in arg_names:
                 raise Exception

        children = [self._parse(child) for child in args if child.children[0].data == "object"]
        args = dict(self._parse(child) for child in args if child.children[0].data == "arg_pair")

        self.pop_scope()

        return (name.value, {}, args)


    def _parse_start(self, ast: lark.Tree) -> None:
        children = [self._parse(child) for child in ast.children if child.children[0].data == "object"]
        args = dict(self._parse(child) for child in ast.children if child.children[0].data == "arg_pair")

        return ("Root", children, args)


    def _parse_string(self, ast: lark.Tree) -> None:
        return ast.children[0].value[1:-1]

