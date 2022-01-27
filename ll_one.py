class NonTerminal:
    def __init__(self):
        self.nullable = None
        self.first = []
        self.follow = []
        
    def add_first(self, first):
        if type(first) is not list:
            first = [first]
        
        for el in first:
            if el not in self.first:
                self.first.append(el)
        
    def add_follow(self, follow):
        if type(follow) is not list:
            follow = [follow]
        
        for el in follow:
            if el not in self.follow:
                self.follow.append(el)

def get_value(dictionary, key):
    values = list(dictionary.values())
    keys = list(dictionary.keys())
    return keys[values.index(key)]
    
def set_nullable(g, n, t, key):
    if n[key].nullable is not None:
        return n[key].nullable 
        
    productions = []
        
    if type(g[key][0]) is list:
        productions = g[key]
    else:
        productions.append(g[key])
    
    for production in productions:
        for element in production:
            #One nullable element
            if element is None and len(production) == 1:
                return True
            
            #Non terminal in production
            if type(element) is int:
                return False
            
            if element != key:
                n[element].nullable = set_nullable(g, n, t, element)
                
                if not n[element].nullable:
                    return False
    
    return True
        
def nullable(g, n, t):
    for p in g:
        n[p].nullable = set_nullable(g, n, t, p)
                

def get_first(g, n, t, key):
    if len(n[key].first) > 0:
        return n[key].first
        
    productions = []
        
    if type(g[key][0]) is list:
        productions = g[key]
    else:
        productions.append(g[key])
    
    for production in productions:
        for element in production:
            if type(element) is int:
                n[key].add_first(get_value(t, element))
                break
                    
            if not n[element].nullable and element != key:
                n[key].add_first(get_first(g, n, t, element))
                break
            
    return n[key].first
        
        
def first(g, n, t):
    for p in g:
        n[p].add_first(get_first(g, n, t, p))


def print_table(n):
    for key in n:
        print(f"Non Terminal: {key}")
        print(f"Nullable: {n[key].nullable}")
        
        print("First:", end=" ")
        for p in n[key].first:
            print(p, end=" ")
        
        print("\nFollow:", end=" ")
        for p in n[key].follow:
            print(p, end=" ")
        
        print("\n")

t = {
    "ID" : 1,
    "OP" : 2,
    "NUM" : 3,
    "=" : 4
}

g = {
    "Start" : ["Stm"],
    "Stm" : [
        [t["ID"], t["="], "Expr"], 
        ["Expr"]
    ],
    "Expr" : [
        ["Expr", t["OP"], "Term"], 
        ["Term"]
    ],
    "Term" : [
        [t["ID"]], 
        [t["NUM"]]
    ]
}

n = {}

for p in g:
    n[p] = NonTerminal()
    
nullable(g, n, t)
first(g, n, t)
print_table(n)
