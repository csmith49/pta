### POSITIONS

class Position(tuple):
    __slots__ = ()
    # there's no good reason to be changing positions, so they subclass tuples
    def __new__(cls, *args):
        # case 1: ls = [1, 2]; Position(ls)
        if len(args) == 1 and not isinstance(args[0], int):
            return tuple.__new__(cls, args[0])
        # case 2: Position(); Position(1); Position(1, 2)
        else:
            return tuple.__new__(cls, args)
    # the thing we check the most often --- is the pos empty?
    def is_root(self):
        return self == ()
    # for more clear accessing, etc.
    def head(self):
        return self[0]
    def rest(self):
        return self[1:]
    # pretty printing and whatnot
    def __str__(self):
        return "<{body}>".format(body=", ".join(map(str, self)))
    def __repr__(self):
        return str(self)
    # and a helper function for manipulation during traversal
    def extend(self, index):
        return Position([i] + list(self))
    def __radd__(self, other):
        return self.extend(other)
    # no need to explicity define an order --- super's is lexicographic, which
    # corresponds to left-right preorder traversal


### SUBSTITUTIONS

class SubstitutionError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Substitution(dict):
    __slots__ = ()
    def __init__(self, *args):
        dict.__init__(self, *args)
    # let's make things look nice
    def __str__(self):
        item_strings = ["{s} -> {t}".format(s=k, t=str(v)) for k, v in self.items()]
        return "[{items}]".format(items=", ".join(item_strings))
    def __repr__(self):
        return str(self)
    # simple wrapper for "updating"
    def __add__(self, other):
        # first, note that because we actually want this to be commutative we
        # throw an error if there's key-based non-determinism
        if set(self.keys()).isdisjoint(other.keys()):
            output = {}
            output.update(self)
            output.update(other)
            return output
        else:
            raise SubstitutionError("Can't add: non-disjoint key sets")


### TERMS

class Term(object):
    __slots__ = ('value', 'children')
    # let's try and keep it versatile
    def __init__(self, *args):
        if len(args) == 1:
            # case 1: made from an sexp
            if isinstance(args[0], (list, tuple)):
                # this takes advantage of case 3
                self.__init__(*args[0])
            # case 2: leaf
            else:
                self.value, self.children = args[0], []
        # case 3: node [?]
        else:
            self.value, self.children = args[0], []
            for arg in args[1:]:
                # the children may not be terms, so let's check
                if isinstance(arg, Term):
                    self.children.append(arg)
                else:
                    self.children.append(Term(arg))
    # a slew of helper functions
    def is_leaf(self):
        return self.children == []
    def arity(self):
        return len(self.children)
    # useful recursion and iteration techniques
    def cata(self, valuation):
        # valuation is a valuation function that tells us what to do on each value
        children = map(lambda t: t.cata(valuation), self.children)
        return valuation(self)(*list(children))
    # find all positions that match a predicate
    def filter(self, pred):
        if self.arity == 0:
            if pred(self): return [Position()]
            else: return []
        else:
            output = []
            if pred(self): output.append(Position())
            for index, child in enumerate(self.children):
                for pos in child.filter(pred):
                    output.append(index + pos)
            return output
    # this should rarely be used --- contexts are cleaner
    def _replace(self, pos, term):
        if pos.is_root(): return term
        else:
            output = [self.value]
            for index, child in enumerate(self.children):
                if index == pos.head():
                    output.append(child._replace(pos.rest(), term))
                else:
                    output.append(child)
            return Term(*output)
    # make use of positions for stuff like accessing
    def at_position(self, pos):
        current = self
        while not pos.is_root():
            current = current.children[pos.head()]
            pos = pos.rest()
        return current
    # which we wrap to make access match the latex Syntax
    def __or__(self, pos):
        return self.at_position(pos)
    # and we must be able to apply substitutions
    def substitute(self, sub):
        def valuation(term):
            if term.is_leaf():
                try: term = d[term.value]
                except KeyError: pass
                return lambda: term
            else:
                return lambda *kids: Term(*([term.value] + kids))
        return self.cata(valuation)
    # which we also wrap
    def __matmul__(self, sub):
        return self.substitute(sub)
    # while we typically avoid recursion, printing is slow anyways
    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        else:
            str_children = map(str, self.children)
            return "{f}({args})".format(f=str(self.value), args=", ".join(str_children))
    def __repr__(self):
        return str(self)


### CONTEXTS

class Context(object):
    def __init__(self, term, pos):
        self.term = term._replace(pos, Term("?"))
        self.pos = pos
    def __getitem__(self, term):
        return self.term._replace(self.pos, term)
    def __str__(self):
        return str(self.term)
    def __repr__(self):
        return str(self)

### LETS BREAK RECURSION

def context(self, pred):
    pos = min(self.filter(pred))
    return Context(self, pos)

Term.context = context
