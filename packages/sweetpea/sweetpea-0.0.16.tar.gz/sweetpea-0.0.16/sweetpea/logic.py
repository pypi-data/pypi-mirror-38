from collections import namedtuple
from functools import reduce
from itertools import product
from typing import Any, List, Tuple, Union, cast

And = namedtuple('And', 'input_list')
Or  = namedtuple('Or' , 'input_list')
Iff = namedtuple('Iff', 'p q')
Not = namedtuple('Not', 'c')

Formula = Union[And, Or, Not, int]
FormulaWithIff = Union[And, Or, Iff, Not, int]
FormulaAndFresh = Tuple[Formula, int]


"""
Converts to CNF using the pattern described on https://en.wikipedia.org/wiki/Conjunctive_normal_form#Converting_from_first-order_logic
The conversion is naive, which means it is subject to an exponential explosion
in the length of the formula. The upside is that it does not introduce any new
variables, which constrains the overall size of the solution space. (#SAT)
"""
def to_cnf_naive(f: FormulaWithIff, next_variable: int) -> Tuple[And, int]:
    formula = __eliminate_iff(f)
    formula = __apply_demorgan(formula)
    formula = __distribute_ors_naive(formula)
    if not isinstance(formula, And):
        formula = And([formula])
    return (formula, next_variable)


"""
Converts to CNF using the pattern described on https://en.wikipedia.org/wiki/Conjunctive_normal_form#Converting_from_first-order_logic
However, distributing ORs over ANDs is done via switching variables, to keep the
converted formula small, as described here: https://www.cs.jhu.edu/~jason/tutorials/convert-to-CNF.html
"""
def to_cnf_switching(f: FormulaWithIff, next_variable: int) -> Tuple[And, int]:
    # https://en.wikipedia.org/wiki/Conjunctive_normal_form#Converting_from_first-order_logic
    formula = __eliminate_iff(f)
    formula = __apply_demorgan(formula)
    (formula, fresh) = __distribute_ors_switching(formula, next_variable)
    if not isinstance(formula, And):
        formula = And([formula])
    return (formula, fresh)


"""
Converts to CNF using the Tseitin transformation. This will introduce addtional
variables, which will increase #SAT, but provides a linear bound on the length
increase of the new formula.
https://en.wikipedia.org/wiki/Tseytin_transformation
"""
def to_cnf_tseitin(f: FormulaWithIff, next_variable: int) -> Tuple[And, int]:
    raise Exception("to_cnf_tseitin is not yet implemented")


def cnf_to_json(formula: List[And]) -> List[List[int]]:
    or_list = []
    for a in formula:
        for o in a.input_list:
            if isinstance(o, Or):
                l = cast(List[int], [])
                for n in o.input_list:
                    if isinstance(n, int):
                        l.append(n)
                    elif isinstance(n, Not):
                        l.append(-n.c)
                    else:
                        raise ValueError("Value was not Not tuple or int")
                or_list.append(l)
            else:
                raise ValueError("Value was not Or tuple")
    return or_list


def __eliminate_iff(f: FormulaWithIff) -> Formula:
    if isinstance(f, And):
        return And(list(map(__eliminate_iff, f.input_list)))
    elif isinstance(f, Or):
        return Or(list(map(__eliminate_iff, f.input_list)))
    elif isinstance(f, Iff):
        new_formula = And([
            Or([f.p, Not(f.q)]),
            Or([Not(f.p), f.q])
        ])
        return __eliminate_iff(new_formula)
    elif isinstance(f, Not):
        return Not(__eliminate_iff(f.c))
    elif isinstance(f, int):
        return f


def __apply_demorgan(f: Formula) -> Formula:
    if isinstance(f, And):
        return __build_and(list(map(__apply_demorgan, f.input_list)))
    elif isinstance(f, Or):
        return __build_or(list(map(__apply_demorgan, f.input_list)))
    elif isinstance(f, Not):
        clause = cast(Formula, f.c)
        if isinstance(clause, And):
            return __apply_demorgan(__build_or(list(map(lambda c: Not(c), clause.input_list))))
        elif isinstance(clause, Or):
            return __apply_demorgan(__build_and(list(map(lambda c: Not(c), clause.input_list))))
        elif isinstance(clause, Not):
            return __apply_demorgan(clause.c)
        elif isinstance(clause, int):
            return f
    elif isinstance(f, int):
        return f


def __distribute_ors_naive(f: Formula) -> Formula:
    if isinstance(f, And):
        return __build_and(list(map(__distribute_ors_naive, f.input_list)))
    elif isinstance(f, Or):
        clauses = list(map(__distribute_ors_naive, f.input_list))
        crossable_clauses = list(map(__get_list_for_crossing, clauses))
        crossed_clauses = list(product(*crossable_clauses))
        or_list = list(map(__build_or, crossed_clauses))
        return __build_and(cast(List[Formula], or_list))
    elif isinstance(f, Not) or isinstance(f, int):
        return f


def __distribute_ors_switching(f: Formula, fresh: int) -> FormulaAndFresh:
    if isinstance(f, And):
        (clauses, new_fresh) = reduce(__apply_distribute_ors,
                                      f.input_list,
                                      (cast(List[Formula], []), fresh))
        return (__build_and(clauses), new_fresh)
    elif isinstance(f, Or):
        (clauses, new_fresh) = reduce(__apply_distribute_ors,
                                      f.input_list,
                                      (cast(List[Formula], []), fresh))
        clauses.sort(key=__order_clauses)
        if len(clauses) > 1:
            if __should_not_combine(clauses):
                return (f, fresh)
            elif __should_combine_naively(clauses):
                return __distribute_ors_switching(__naive_combination(clauses), new_fresh)
            else:
                (new_formula, new_fresh) = __switching_combination(clauses, new_fresh)
                return __distribute_ors_switching(new_formula, new_fresh)
        else:
            return (clauses[0], new_fresh)
    elif isinstance(f, Not):
        assert isinstance(f.c, int)
        return (f, fresh)
    elif isinstance(f, int):
        return (f, fresh)


def __flatten_clause_list(clauses: List[Formula], cls: Any) -> List[Formula]:
    flattened_list = cast(List[Formula], [])
    for c in clauses:
        if isinstance(c, cls):
            flattened_list.extend(c.input_list)
        else:
            flattened_list.append(c)
    flattened_list.sort(key=__order_clauses)
    return flattened_list


def __build_or(l: List[Formula]) -> Or:
    return Or(__flatten_clause_list(l, Or))


def __build_and(l: List[Formula]) -> And:
    return And(__flatten_clause_list(l, And))


def __apply_distribute_ors(acc: Tuple[List[Formula], int], elem: Formula) -> Tuple[List[Formula], int]:
    fs = acc[0]
    fresh = acc[1]
    (f, new_fresh) = __distribute_ors_switching(elem, fresh)
    fs.append(f)
    return (fs, new_fresh)


def __should_not_combine(clauses: List[Formula]) -> bool:
    return not any(isinstance(c, And) for c in clauses)


def __should_combine_naively(clauses: List[Formula]) -> bool:
    return \
        isinstance(clauses[0], int) or \
        isinstance(clauses[0], Not) or \
        isinstance(clauses[1], int) or \
        isinstance(clauses[1], Not)


def __naive_combination(clauses: List[Formula]) -> Formula:
    lhs = __get_list_for_crossing(clauses[0])
    rhs = __get_list_for_crossing(clauses[1])
    crossing = [list(tup) for tup in list(product(lhs, rhs))]
    combination = cast(Formula, And(list(map(lambda l: Or(__flatten_clause_list(l, Or)), crossing))))
    if len(clauses) > 2:
        return __build_or([combination] + clauses[2:])
    else:
        return combination


def __get_list_for_crossing(clause: Formula) -> List[Formula]:
    if isinstance(clause, int) or isinstance(clause, Not):
        return [clause]
    elif isinstance(clause, And) or isinstance(clause, Or):
        return clause.input_list


def __switching_combination(clauses: List[Formula], fresh: int) -> FormulaAndFresh:
    lhs = Or([Not(fresh), clauses[0]])
    rhs = Or([fresh, clauses[1]])
    combination = cast(Formula, And([lhs, rhs]))
    new_fresh = fresh + 1
    if len(clauses) > 2:
        return (__build_or([combination] + clauses[2:]), new_fresh)
    else:
        return (combination, new_fresh)


def __order_clauses(c: Formula) -> int:
    if isinstance(c, And) or isinstance(c, Or):
        return 0
    elif isinstance(c, Not):
        return c.c
    else:
        return c