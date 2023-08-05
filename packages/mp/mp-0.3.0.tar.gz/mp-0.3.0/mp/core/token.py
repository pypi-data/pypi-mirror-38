from mp.core.error import SyntaxError
from mp.core.expression import Expression as Exp


class Token:

    TYPE_BINARY = 0
    TYPE_OPERATOR = 1
    TYPE_NUMBER = 2
    TYPE_VARIABLE = 3
    TYPE_TUPLE = 4
    TYPE_SIZEOF = 5

    def __init__(self, name: str, data_type: int, *args):
        self.name = name
        self.data_type = data_type
        self.args = args

    @classmethod
    def from_binary(cls, raw):
        pass

    @classmethod
    def from_operator(cls, operator, *args):
        operator = str(operator)
        return Token(operator, cls.TYPE_OPERATOR, *args)

    @classmethod
    def from_save(cls, dir_from, *files):
        return Token(Exp.SAVE[0], cls.TYPE_OPERATOR, dir_from, *files)

    @classmethod
    def from_delete(cls, dir_from, *files):
        return Token(Exp.DELETE[0], cls.TYPE_OPERATOR, dir_from, *files)

    @classmethod
    def from_number(cls, num_type, value):
        return Token(num_type, cls.TYPE_NUMBER, value)

    @classmethod
    def from_var(cls, name):
        return Token(name, cls.TYPE_VARIABLE)

    @classmethod
    def from_tuple(cls, *data):
        return Token(Exp.TUPLE, cls.TYPE_TUPLE, *data)

    @classmethod
    def from_range(cls, range_type, *data):
        return Token(range_type, cls.TYPE_OPERATOR, *data)

    def update_graph(self, graph):
        self.update_graph_recursive(graph)
        return graph

    def update_graph_recursive(self, graph):
        if self.data_type == self.TYPE_OPERATOR:
            operands = self._get_operands(self.args, graph)
            # (save, delete) files
            if self.name in Exp.SAVE + Exp.DELETE:
                operate = graph.save if self.name in Exp.SAVE else graph.delete
                if len(operands) == 1:
                    operate(None, operands[0])
                else:
                    root = operands[0]
                    for f in operands[1:]:
                        operate(root, f)
                return None
            # slice
            elif self.name in Exp.IDX:
                start = operands[0]
                stop = operands[1] if len(operands) >= 2 else None
                step = operands[2] if len(operands) == 3 else None
                start = start if bool(start) else None
                stop = stop if bool(stop) else None
                return graph.slice(start, stop, step)
            # view
            elif self.name in Exp.SHELL_AA:
                return graph.view(*operands)
            # call method or indices
            elif self.name in Exp.SHELL_RR:
                # call method
                sub = operands[0]
                if sub.is_method_delegate:
                    # if user-defined method delegate
                    if sub.is_method_defined and sub.toward is None:
                        var = sub
                        if len(operands) == 1:
                            raise SyntaxError(var.name)
                        args, toward = operands[1:-1], operands[-1]
                        var.args = args
                        var.toward = toward
                    # if user-defined method
                    # or just to call
                    else:
                        var = graph.point_method(graph.new_name(), sub)
                        var.args = operands[1:]
                        var.is_data = True
                        var.is_method_delegate = False
                    return var
                # indices
                return graph.indices(*operands)
            # if repeat call
            elif self.name in Exp.MUL:
                # repeat call
                sub = operands[0]
                if sub.is_method_delegate:
                    var = graph.point_method(graph.new_name(), sub)
                    repeat = operands[1]
                    # double multiply
                    if var.repeat is not None:
                        repeat = graph.operate(self.name, var.repeat, repeat)
                    var.repeat = repeat
                    return var
                # normal multiply
                else:
                    return graph.operate(self.name, *operands)
            # just operators
            else:
                return graph.operate(self.name, *operands)
        # constant
        elif self.data_type == self.TYPE_NUMBER:
            return graph.alloc(self.name, self.args[0])
        # variable or method (builtins)
        elif self.data_type == self.TYPE_VARIABLE:
            return graph.find(self.name)
        # tuple
        elif self.data_type == self.TYPE_TUPLE:
            operands = self._get_operands(self.args, graph)
            return graph.tuple(*operands)

    @classmethod
    def _get_operands(cls, args, graph):
        operands = list()
        for arg in args:
            if arg is None:
                operands.append(None)
                continue
            operand = arg.update_graph_recursive(graph)
            operands.append(operand)
        return operands

    def __repr__(self):
        return self.name + '{ ' + ', '.join([repr(data) for data in self.args]) + ' }'
