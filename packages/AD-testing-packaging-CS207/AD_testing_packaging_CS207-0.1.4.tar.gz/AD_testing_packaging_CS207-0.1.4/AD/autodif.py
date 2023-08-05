import AD.interpreter as ast

class AD():
    """
    User friendly interface for the AST interpreter.
    Usage
    =============
    import autodif
    def main():
        f1 = "x*y*z"
        vd = "x:2,y:3,z:4"
        F1 = autodif.AD(f1)
        print(F1.diff_all(vd))
        print(F1.diff("x"))
        F1.new_formula("a+b")
        vd = "a:10, b : 1"
        F1.set_point(vd)
        print(F1.val())
        print(F1.diff_all())
    """

    def __init__(self, frmla):
        self.formula = frmla
        self.lexer = ast.Lexer(frmla)
        self.parser = ast.Parser(self.lexer)
        self.interpreter = ast.Interpreter(self.parser)
        self.vd = None

    def set_point(self, vd):
        if vd is not None:
            self.vd = vd
        if self.vd is None:
            raise NameError("Must set point to evaluate")
    
    def diff(self, dv, vd=None):
        self.set_point(vd)
        return self.interpreter.differentiate(self.vd, dv)
    
    def diff_all(self, vd=None):
        self.set_point(vd)
        return self.interpreter.diff_all(self.vd)
    
    def val(self, vd=None):
        self.set_point(vd)
        return self.interpreter.interpret(self.vd)
    
    def new_formula(self, frmla):
        self.formula = frmla
        self.lexer = ast.Lexer(frmla)
        self.parser = ast.Parser(self.lexer)
        self.interpreter = ast.Interpreter(self.parser)
        self.vd = None
