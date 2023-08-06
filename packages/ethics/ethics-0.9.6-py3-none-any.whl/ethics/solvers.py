from ethics.language import Not, And, Or, Causes, Gt, Eq, U, Impl, Formula

class Branch:
    def __init__(self, formulas):
        self.formulas = []
        self.unexpanded = []
        self.formulas += formulas
        self.unexpanded += [f for f in formulas if not self.isLiteral(f)]
        self.interventions = {}

    def isLiteral(self, f):
        if isinstance(f, str):
            return True
        if isinstance(f, Not) and isinstance(f.f1, str):
            return True
        return False
    
    def setUnexpanded(self, formulas):
        self.unexpanded = []
        self.unexpanded += formulas
    
    def setInterventions(self, formulas):
        self.interventions = dict(formulas)
    
    def addFormula(self, formula):
        if formula not in self.formulas:
            self.formulas += [formula]
            if not self.isLiteral(formula):
                self.unexpanded += [formula]
    
    def isSaturated(self):
        return len(self.unexpanded) == 0
        
    def isClosed(self):
        for f in self.formulas:
            if Formula.getNegation(f) in self.formulas:
                self.unexpanded = [] # Saturate it 
                return True
        for k in self.interventions:
            for v in self.interventions[k]:
                if Not(v) in self.interventions[k]:
                    self.unexpanded = [] # Saturate it 
                    return True
        return False
        
    def printModel(self):
        s = ""
        for f in self.formulas:
            if isinstance(f, str):
                s += f+" "
            if isinstance(f, Eq):
                s += str(f)+" "
            if isinstance(f, Gt):
                s += str(f)+" "
        return s
    
class Tableau:
    def __init__(self, formulas):
        self.branches = []
        
    def addBranch(self, branch):
        self.branches += [branch]
        
    def unsaturatedBranchExists(self):
        for b in self.branches:
            if not b.isSaturated():
                return True
        return False
        
    def openBranchExists(self):
        for b in self.branches:
            if not b.isClosed():
                return True, b
        return False, None

class SatSolver:

    def satisfiable(self, formulas):
        t = Tableau(formulas)
        t.addBranch(Branch(formulas))
        while t.unsaturatedBranchExists():
            b = None
            for i in t.branches:
                if not i.isClosed() and not i.isSaturated():
                    b = i
                    break
            if b != None:
                while not b.isClosed() and not b.isSaturated():
                    f = b.unexpanded[0]
                    if isinstance(f, Not) and isinstance(f.f1, Not):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1.f1)
                    elif isinstance(f, str):
                        b.unexpanded.remove(f)
                    elif isinstance(f, And):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1)
                        b.addFormula(f.f2)
                    elif isinstance(f, Not) and isinstance(f.f1, Or):
                        b.unexpanded.remove(f)
                        b.addFormula(Not(f.f1))
                        b.addFormula(Not(f.f2))
                    elif isinstance(f, Or):
                        b.unexpanded.remove(f)
                        b2 = Branch(b.formulas)
                        b2.setUnexpanded(b.unexpanded)
                        b2.setInterventions(b.interventions)
                        b2.addFormula(Not(f.f1))
                        b2.addFormula(f.f2)
                        t.branches += [b2]
                        b.addFormula(f.f1)
                    elif isinstance(f, Not) and isinstance(f.f1, And):
                        b.unexpanded.remove(f)
                        b2 = Branch(b.formulas)
                        b2.setUnexpanded(b.unexpanded)
                        b2.setInterventions(b.interventions)
                        b2.addFormula(f.f1.f1)
                        b2.addFormula(Not(f.f1.f2))
                        t.branches += [b2]
                        b.addFormula(Not(f.f1.f1))
                    elif isinstance(f, Impl):
                        b.unexpanded.remove(f)
                        b.addFormula(Or(Not(f.f1), f.f2))
                    elif isinstance(f, Not) and isinstance(f.f1, Impl):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1.f1)
                        b.addFormula(Not(f.f1.f2))
                    elif isinstance(f, Causes):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1)
                        b.addFormula(f.f2)
                        if f.f1 not in b.interventions:
                            b.interventions[f.f1] = []
                        b.interventions[f.f1] += [Formula.getNegation(f.f1), Formula.getNegation(f.f2)]
                    elif isinstance(f, Not) and isinstance(f.f1, Causes):
                        b.unexpanded.remove(f)
                        b.addFormula(Or(Not(f.f1), Not(f.f2)))
                        b2 = Branch(b.formulas)
                        b2.setUnexpanded(b.unexpanded)
                        b2.setInterventions(b.interventions)
                        if f.f1.f1 not in b2.interventions:
                            b2.interventions[f.f1.f1] = []
                        b2.interventions[f.f1.f1] += [Formula.getNegation(f.f1.f1), f.f1.f2]
                    elif isinstance(f, Eq): # Assumes Eq(0, U(c)) or Eq(U(c), 0)
                        b.unexpanded.remove(f)
                        if f.f1 == 0:
                            term = f.f2
                        else:
                            term = f.f1
                        b.addFormula(Not(Gt(0, term)))
                        b.addFormula(Not(Gt(term, 0)))
                    elif isinstance(f, Not) and isinstance(f.f1, Eq):
                        b.unexpanded.remove(f)
                        if f.f1.f1 == 0:
                            term = f.f1.f2
                        else:
                            term = f.f1.f1
                        b.addFormula(Or(Gt(0, term), Gt(term, 0)))
                    elif isinstance(f, Gt): # Assumes Gt(0, U(c)) or Gt(U(c), 0)
                        b.unexpanded.remove(f)
                        if f.f1 == 0:
                            term = f.f2
                            b.addFormula(And(Not(Eq(0, term)), Not(Gt(term, 0))))
                        else:
                            term = f.f1
                            b.addFormula(And(Not(Eq(0, term)), Not(Gt(0, term))))
                    elif isinstance(f, Not) and isinstance(f.f1, Gt):
                        b.unexpanded.remove(f)
                        if f.f1.f1 == 0:
                            term = f.f1.f2
                            b.addFormula(Or(Gt(term, 0), Eq(0, term)))
                        else:
                            term = f.f1.f1
                            b.addFormula(Or(Gt(0, term), Eq(0, term)))
  
        return t.openBranchExists()
        
        
if __name__ == '__main__':
    f = [Causes("a1", "c1"), Not(Gt(0, U("c1"))), Not(Gt(U("c1"), 0))]
    s = SatSolver()
    b, br = s.satisfiable(f)
    print(b, None if br is None else br.printModel(), None if br is None else br.interventions)
