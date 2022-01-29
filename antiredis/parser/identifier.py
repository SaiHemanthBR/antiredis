import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from ..classes.identifier import Identifier, TableName, ColName, RowName, FuncName
from . import keyword as kw

quoted_identifier = pp.QuotedString('`')
identifier = (
    (~kw.any_keyword + pp.Word(pp.alphas, pp.alphanums + '_')
     ).set_parse_action(ppc.downcase_tokens)
    | quoted_identifier
).set_parse_action(Identifier.parse_action)
table_name = identifier().set_parse_action(TableName.parse_action)
col_name = identifier().set_parse_action(ColName.parse_action)
row_name = identifier().set_parse_action(RowName.parse_action)
func_name = identifier().set_parse_action(FuncName.parse_action)

if __name__ == "__main__":
    print(identifier.parse_string('xyz'))
    # print(identifier.parse_string('select'))
