class NonTerminal:
    def __init__(self):
        self.nullable = None
        self.first = []
        self.follow = []
        
    def add_first(self, first):
        self.first.append(first)
        
    def add_follow(self, follow):
        self.follow.append(follow)

def get_value(dictionary, key):
    values = list(dictionary.values())
    keys = list(dictionary.keys())
    return keys[values.index(key)]
    
def set_nullable(g, n, t, key):
    if n[key].nullable is not None:
        return n[key].nullable 
    
    for p in g[key]:
        if p is None:
            return True
        
        if type(p) is int:
            return False
        
        if type(p) is list:
            for p2 in p:
                if type(p2) is int:
                    return False
                    
                elif p2 != key:
                    n[key].nullable = set_nullable(g, n, t, p2)
        
        elif type(p) is int:
            return False
        
        elif p != key:
            n[key].nullable = set_nullable(g, n, t, p)
        
def nullable(g, n, t):
    for p in g:
        n[p].nullable = set_nullable(g, n, t, p)
                

def get_first(g, n, t, key):
    if key is None:
        return []
    
    first = []
    
    for p in g[key]:
        if isinstance(p, str):
            if(not n[p].nullable):
                return first
            
            first += get_first(g, n, t, p)
                
        else:
            first.append(get_value(t, p))
            return first
        
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
    "Stm" : [[t["ID"], t["="], "Expr"], ["Expr"]],
    "Expr" : [["Expr", t["OP"], "Term"], ["Term"]],
    "Term" : [[t["ID"]], [t["NUM"]]]
}

n = {}

for p in g:
    n[p] = NonTerminal()
    
nullable(g, n, t)
#first(g, n, t)
print_table(n)
