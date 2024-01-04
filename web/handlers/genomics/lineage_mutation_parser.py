from pyparsing import *

# Grammar
lineageTerm = Combine(Word(alphanums) + OneOrMore("." + Word(alphanums))).setName("lineage") | quotedString.setParseAction( removeQuotes )
mutationTerm = Combine(Word(alphanums) + ":" + Word(alphanums)).setName("mutation") | quotedString.setParseAction( removeQuotes )

# When a match is encountered return object of corresponding class
class Lineage(object):
    def __init__(self, result):
        self.value = result[0]

    def generate(self):
        return "pangolin_lineage:{}".format(self.value)

class Mutation(object):
    def __init__(self, result):
        self.value = result[0]

    def generate(self):
        return "mutation:{}".format(self.value)

lineageTerm.addParseAction(Lineage)
mutationTerm.addParseAction(Mutation)

searchTerm = OneOrMore(MatchFirst([mutationTerm, lineageTerm]))

# Arbitrary operator precedence for now
op_and = CaselessLiteral("and")
op_or = CaselessLiteral("or")
op_not = CaselessLiteral("not")

searchExpr = operatorPrecedence( searchTerm,
    [
        (op_and, 2, opAssoc.LEFT),
        (op_or, 2, opAssoc.LEFT),
    ])

# Generate ES query_string. Needs validation.
def build_es_query_string(parsed_cond):
    query_string = ""
    for i in parsed_cond:
        if isinstance(i, ParseResults):
            query_string += "( {} )".format(build_es_query_string(i))
        elif isinstance(i, str) and i in ["and", "or"]:
            query_string += " {} ".format(i)
        elif type(i).__name__ in ["Lineage", "Mutation"]:
            query_string += "{}".format(i.generate())
    return query_string

# Testing
tests = """\
(BA.1 and S:L452R) or B.1.617.2
(BA.1 and S:L452R and S:P681R) or B.1.617.2 or (S:D614G and S:P681R)
BA.1 and (S:L452R or S:P681R)
S:L452R and BA.1\
""".split("\n")

for t in tests:
    print("\nQuery parameter: \n\"{}\"".format(t))
    parsed_cond = searchExpr.parseString(t)
    print("\nCorresponding ES query:\n\"{}\"\n".format(build_es_query_string(parsed_cond[0])))
    print("----")

