class TextVisitor:
    def visit(self, el):
        method_name = "visit_" + el.tag
        if hasattr(self, method_name):
            return getattr(self, method_name)(el)
        else:
            return self.generic_visit(el)

    def generic_visit(self, el):
        raise NotImplementedError
