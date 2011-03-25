import ast
import sys

def free_vars(astnode):
    global_vars = set()

    def freevars(params=(), *nodes):
        visitor = LocalVisitor(params)
        for n in nodes:
            visitor.visit(n)
        return visitor.get_free_vars()

    def arguments_to_set(args):
        params = set(a.id for a in args.args)
        if args.vararg:
            params.add(args.vararg)
        if args.kwarg:
            params.add(args.kwarg)
        return params

    class LocalVisitor(ast.NodeVisitor):
        def __init__(self, local=set()):
            self.free_vars = set()
            self.local_vars = set(local)
            self.global_vars = set()

        def visit_Global(self, node):
            for n in node.names:
                global_vars.add(n)

        def visit_Name(self, node):
            self.free_vars.add(node.id)
            if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Param):
                self.local_vars.add(node.id)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            self.local_vars.add(node.name)
            params = arguments_to_set(node.args)
            self.free_vars |= freevars(params, *node.body)

        def visit_ClassDef(self, node):
            self.local_vars.add(node.name)
            self.free_vars |= freevars((), *node.body)

        def visit_Lambda(self, node):
            params = arguments_to_set(node.args)
            self.free_vars |= freevars(params, node.body)

        # list comprehensions are specifically *not* a scope:
        # >>> def foo():
        # ...     fs = [ x for x in range(10) ]
        # ...     return x
        # >>> foo()
        # 9

        def visit_GeneratorExp(self, node):
            self.free_vars |= freevars((), node.elt, *node.generators)

        def get_free_vars(self):
            return self.free_vars - (self.local_vars - self.global_vars)

    return freevars((), astnode) | global_vars

def main():
    print free_vars(ast.parse(open(sys.argv[1]).read())) - set(dir(__builtins__))

if __name__ == '__main__':
    main()
