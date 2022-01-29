from re import T
import pyparsing as pp
from .select_stmt import select_stmt

stmt = pp.Forward()
stmt <<= select_stmt + pp.ZeroOrMore(stmt)

if __name__ == '__main__':
    test = (
        "select * from table1 where x > 5 and y < -1 group by x having z > 5 order by x, y desc;"
        "select x from table1 where x > 5 and y < -1;"
    )

    print(test)
    res = stmt.parse_string(test)

    print(res)
