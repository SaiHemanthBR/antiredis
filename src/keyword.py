import pyparsing as pp

keywords = {
    k: pp.CaselessKeyword(k)
    for k in """\
    SELECT DISTINCT FROM WHERE GROUP HAVING ORDER BY ASC DESC LIMIT
    """.split()
}

any_keyword = pp.MatchFirst(keywords.values())

vars().update(keywords)
