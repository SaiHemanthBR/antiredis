import pyparsing as pp

keywords = {
    k: pp.CaselessKeyword(k)
    for k in """\
    SELECT DISTINCT FROM WHERE GROUP HAVING ORDER BY ASC DESC LIMIT OFFSET
    TRUE FALSE NULL CURRENT_DATE CURRENT_TIME CURRENT_TIMESTAMP
    NOT AND OR XOR BETWEEN
    """.split()
}

any_keyword = pp.MatchFirst(keywords.values())

vars().update(keywords)
