
cpp_text ::= [<comment_text>:i <class_source_text>:j] => write_text(i,j)
comment_text ::= [ <anything>*:i ] => write_comment(i)
class_source_text ::= [ <comment_text>:i <class_declaration_text>:j] => '%s\n%s' % (i,j)
class_declaration_text ::= [ :i <class_block_text>:j :k] => write_class(i,j,k)
class_block_text ::= [ <attributes_text>:a <methods_text>:m ] => '%s\n\n%s' % (a,m)
attributes_text ::= [ <attribute_text>*:a_s ] => '\n'.join([a for a in a_s if a])
attribute_text ::= [<comment_text>:i <attribute_declaration_text>:j] => write_attribute( i,j )
attribute_declaration_text ::= [ <attribute_allocation_text>:i <attribute_initialization_text>:j] => write_attribute_declaration(i,j)
attribute_allocation_text ::= [ <qualifiers_text>:k :i :b :j ] => write_attribute_allocation(i,j,k,b)
qualifiers_text ::= [ <anything>*:i ] => ' '.join(i)
attribute_initialization_text ::= [ <equals>?:i (<initial_text>|<dynamic_text>)?:j ] => j and str(' = %s' % j) or ''
initial_text ::= [ <anything>:i ] => i 
dynamic_text ::= [ <cast_text>?:i <simple_dynamic_text>:j ] => write_dynamic(i,j)
cast_text ::= <anything>:i
simple_dynamic_text ::= ( <new_text> | <call_text> | <dotted_text>):i => i
new_construction_text ::= [ "new":n <dotted_text>:i <csl_text>:j ] => 'new %s(%s)' % (i,j)
new_array_text ::= [ "new":n <dotted_text>:i [ <anything>:j ?(j.isdigit()) ] ] => 'new %s[%s]' % (i,j)
new_text ::= <new_construction_text> | <new_array_text>
call_text ::= [ <dotted_text>:i <csl_text>:j ] => '%s(%s)' % (i,j)
dotted_text ::= [ <dot_text>+:i ?(i[0] != "new")  ] => write_dotted(i)
dot_text	::= <identified_text>
identified_text ::= <identified_call_text> | <identifier_text>
identified_call_text ::= [<identifier_text>:i <csl_text>:j] => str('%s(%s)' % (i, j)) 
identifier_text	::= <anything>
literal_text ::= <anything>
csl_text ::= [ <dynamic_text>*:i ] => ', '.join(i)
methods_text ::= [ <method_text>*:m ] => '\n'.join(m)
method_text ::= [ <comment_text>:i (<method_stub_text>|<method_source_text>):j ] => write_method(i,j)
method_stub_text ::= [ <method_declaration_text>:i :j ?(j == [';']) ] => write_method_stub(i)
method_source_text ::= [ <method_declaration_text>:i <indented_block_text '\n\t'>:j] => write_method_source(i,j)
method_declaration_text ::= [ <return_declaration_text>:j <identifier_text>:k <formal_text>:l :m ] => write_method_declaration(j,k,l,m)
return_declaration_text ::= [ <return_qualifiers_text>:i <return_type_text>:j ] => write_return_declararation(i,j)
return_qualifiers_text ::= [ <anything>*:qs ] => qs
return_type_text ::= <anything>
formal_text ::= [ <formal_arg_text>*:i ] => '( %s )' % ','.join(i)
formal_arg_text ::= [ <type_text>:i <anything>:j <identifier_text>:k ] => write_formal_arg(i,j,k)
type_text ::= <anything>:i => change_type(i)
indented_block_text :p ::= [ "block":i [<sub_block p>*:j]] => '{%s%s%s}' % (p,p.join(j),p[:-1]) 
sub_block :p ::= <indented_block_text p+'\t'> | <anything>

tokens ::= [<token>*]
leaf ::= <anything>
token ::= <tokens> | <leaf>

cpp_file ::= <long_comment>:i <class_source>:j => glom_cpp_file([i, j])


short_comment_line ::= <any_blanks> <short_comment>:i <eol> =>i
short_comment_lines ::= (<blank_line>|<short_comment_line>)+:i => [ s[0] for s in i if s ]
short_comment ::= <any_blanks> '/' '/' <not_eol>*:i => [ ''.join(i) ]
long_comment	::= <comment_start> <comment_lines>:i <comment_end> => i
class_source ::= <long_comment>:i <class_declaration>:j => [ i, j ]
inherit ::= <some_blanks> (<implements>|<extends>) <some_blanks> <comma_separated_list 'type'>:i => ', '.join(i)
inheritance ::= <inherit>*:i <any_blanks> => ', '.join(i)
class_declaration ::= <qualifiers> (<class>|<interface>) <some_blanks> <identifier>:i <inheritance>:k <eol> <class_block>:j => [ i, j, k and k or '' ]
class_block ::= <blank_lines> <open_brace> <eol> <class_lines>:i <blank_lines> <close_brace> => i
class_lines ::= <attributes>:i <methods>:j => [i,j]
attribute_declaration ::= <attribute_allocation>:i <attribute_initialisation>?:j <any_blanks> <semi_colon> => [ i, j and j or [] ]
attribute_allocation ::= <some_blanks> <qualifiers>:k <type>:i <bricks>*:l <some_blanks> <identifier>:j => [ k, i, ''.join(l), j ]
attribute_initialisation ::= <some_blanks> <equals>:i (<some_blanks> <dynamic_value>|<initial_block>):j => [i, j] 

attribute_source ::= (<short_comment_lines>|<long_comment>)?:i <attribute_declaration>:j <short_comment>?:k => glom_attribute_source(i,j,k)
empty_attribute ::= <blank_line> | <long_comment> => None
attribute ::= <empty_attribute> | <attribute_source>
attributes ::= <attribute>*:ls => [ l for l in ls if l ]

class ::= 'c' 'l' 'a' 's' 's' => "class"
const ::= 'c' 'o' 'n' 's' 't' => "const"
final ::= 'f' 'i' 'n' 'a' 'l' => "final"
import ::= 'i' 'm' 'p' 'o' 'r' 't' => "import"
package	::= 'p' 'a' 'c' 'k' 'a' 'g' 'e' => "package"
private ::= 'p' 'r' 'i' 'v' 'a' 't' 'e' => "private"
static ::= 's' 't' 'a' 't' 'i' 'c' => "static"
public ::= 'p' 'u' 'b' 'l' 'i' 'c' => "public"
protected ::= 'p' 'r' 'o' 't' 'e' 'c' 't' 'e' 'd'  => "protected"
throws ::= 't' 'h' 'r' 'o' 'w' 's' => "throws"
block ::= 'b' 'l' 'o' 'c' 'k' => "block"
extends ::= 'e' 'x' 't' 'e' 'n' 'd' 's' => "extends"
implements ::= 'i' 'm' 'p' 'l' 'e' 'm' 'e' 'n' 't' 's' => "implements"
interface ::= 'i' 'n' 't' 'e' 'r' 'f' 'a' 'c' 'e' => "interface"
new ::= 'n' 'e' 'w' => "new"
abstract ::= 'a' 'b' 's' 't' 'r' 'a' 'c' 't' => "abstract"
 
comment_start	::= <any_blanks> <forward_slash> <asterisk> <asterisk>* <eol>?
comment_first_line ::= <any_blanks> ~('*') <comment_char>+:i <eol> => ''.join(i)
comment_lines  ::= <comment_line>+:i => [ j for j in i if j ]
comment_end	::= <start_comment_line> <forward_slash> <eol>
comment_line	::= ( <comment_first_line> | <comment_source_line> | <comment_empty_line> )
comment_source_line	::= <start_comment_line> <some_blanks> <comment_char>+:i <eol> => ''.join(i)
comment_empty_line	::= <start_comment_line> <eol> => None
start_comment_line ::= <spaces> <asterisk>?

import_statement ::= <import> <some_blanks> (<static> <some_blanks>)? <wild_name>
import_line ::= <import_statement>:i <semi_colon> <eol> => i

qualifier ::= <const> | <private> | <static> | <public> | <final> | <protected> | <abstract>
a_qualifier ::= <qualifier>:i <some_blanks> => i 
qualifiers ::= <a_qualifier>*


cast ::= <open_bracket> <type>:i <close_bracket> <any_blanks> => i
simple_dynamic_value ::= <add_expression> | <new_call> | <method_call> | <static_value>
dynamic_value ::= <cast>?:i <simple_dynamic_value>:j => [ i and i or '', j ]

static_value::= <literal> | <dotted_name>

add_expression ::= <static_value>:i (<any_blanks> '+' <any_blanks> <static_value>):j => j and ['%s + %s' % (i[0],j[0])] or i
expression ::= <add_expression> | <dynamic_value>

literal ::= (<string>|<number>):i => [ i ]

actual_arguments ::= <comma_separated_list 'dynamic_value'>
call_signature ::= <open_bracket> <actual_arguments>:i <any_blanks> <close_bracket> => i and i or []
values ::= ( <value> <comma> )*:vs <value>:v => [vs,v]
empty_block ::= <any_blanks> <open_brace> <any_blanks> <close_brace> => [] 
statement ::= (<single_statement> | <blocked_statement>)
single_statement ::= <any_blanks> <not_statement_ender>*:i ';' <eol> => ''.join(i)
not_statement_ender ::= <anything>:i ?(i not in ';{}') => i
blocked_statement ::= <any_white> ( <try_block> | <if_block> )
condition ::= <open_bracket> <any_white> <dynamic_value>:i <any_blanks> <conditional_operator>:j <any_blanks> <dynamic_value>:k <any_white> <close_bracket> => [i,j,k]
conditional_operator ::= '>'
start_block ::= <any_blanks> ( <eol> <some_blanks> )? <open_brace> <any_blanks> <eol>
end_block ::= <any_blanks> <close_brace> <any_white> => '\n'
indent ::= <any_blanks>
formal_argument ::= <qualifiers>:l <type>:i <bricks>*:k <some_blanks> <identifier>:j => [i,''.join(k),j]
bricks ::= <any_blanks> <open_brick> <close_brick> => '[]'
declaration_signature ::= <open_bracket> <any_blanks> <comma_separated_list 'formal_argument'>:i <any_blanks> <close_bracket> => i
type_blank ::= <type>:i <bricks>*:j <some_blanks> => '%s%s' % (i,''.join(j))
return_declaration ::= <qualifiers>:i <type_blank>?:j => j and [i, j] or [i, '']
throws_declaration ::= <some_blanks> <throws> <some_blanks> <comma_separated_list 'type'>:i => i


method_declaration ::= <indent>:i <return_declaration>:j <identifier>:k <any_blanks> <declaration_signature>:l <throws_declaration>?:m <any_blanks> => [ j, k, l, m and m or [] ] 
method_stub ::= <method_declaration>:i <semi_colon> <eol> => [ i, [';'] ]
method_source ::= <method_declaration>:i <eol> <indented_block>:j => [i , j]
method ::= (<long_comment> | <blank_lines>):i (<method_stub>|<method_source>):j => i and [ i, j ] or [[],j]
methods ::= <method>*:ms => [ m for m in ms if m ]


fargs ::= <comma_separated_list 'static_value'>:i => 'fargs: %s' % i
nums ::= <comma_separated_list 'letter'>
comma_separated_nothing :p ::= <any_blanks> => []
comma_separated_one :p ::= <apply p>:i => [i]
comma_separated_many :p ::= <apply p>:i (',' <any_blanks> <apply p>)+:j => [i] + j
comma_separated_list :p ::= <comma_separated_many p> | <comma_separated_one p> | <comma_separated_nothing p>

type ::= <identifier>:i => use_type(i)

wild_name	::= <dot_name>*:i (<identifier> | <asterisk>):j => i + [ j ]
array_dimension ::= <open_brick> <number>:i <close_brick> => i
array_dimensions ::= <array_dimension>*
new_call ::= <new> <some_blanks> <dot_name>*:i <identifier>:j (<call_signature>|<array_dimensions>):k => [ 'new', i + [j], k ]
method_call ::= <new>?:n <dot_name>*:i <identifier>:j <call_signature>:k => [ i + [j], k ]
dotted_name ::= <dot_name>*:i <identifier>:j => i + [ j ]
dot_name	::= <identified_value>:i <dot> => i
identified_value ::= <identifier>:i <call_signature>?:j => j is not None and [ i, j ] or i
identifier	::= <letter>:i <id_char>*:j => ''.join([i]+j)

other_thing ::= <numbered_word>*:i <word>:j => i + [j]
numbered_word	::= <word>:i <number>:j => i + j
word	::= <letter>+:i => as_string(i)
hex_prefix ::= '0' 'x' => '0x'
hex_number ::= <hex_prefix>:h <hex_digit>+:i => h + ''.join(i)
hex_digit ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F'
digits	::= <digit>+:i => ''.join(i)
integer ::= ('+'|'-')?:i <digits>:j => i and str('%s%s' % (i,j)) or j
float ::= <integer>:i <dot> <digits>:j => '%s.%s' % (i,j)
number ::= <hex_number> | <float> | <integer>


comment_char ::= <letter> | <digit> | <punctuation> | <geek_char> | <brackets> | <space>
brackets ::= <open_bracket> | <close_bracket> | <open_brace> | <close_brace> | <open_brick> | <close_brick>
geek_char ::= <double_quote> | <single_quote> | <underscore> | <forward_slash> | <at> | <greater> | <less> | '=' | '&' | '*' | '+' | '-' | '@' | '#' | '$'
punctuation	::= <comma> | <dot> | <semi_colon> | <colon> | <question> | <exclamation> | <dash>

id_char ::= <letter> | <digit> | '_' | '<' | '>'


line ::= <not_eol>*:i <eol> => ''.join(i).rstrip()
not_eol ::= <anything>:i ?(i not in '\n\r') => i

unblocker ::= <anything>:i ?(i not in '{}') =>i
block_line ::= <any_blanks> <unblocker>:i <line>:j => '%s%s' % (i,''.join(j))
block_starter ::= <any_blanks> <open_brace> <eol>
block_ender ::= <any_blanks> <close_brace> <semi_colon>?:i <eol> => i and ';' or ''
black_line ::= <indented_block> | <block_line>
indented_block ::= <blank_lines> <block_starter> <black_line>*:i <block_ender>:j => [ 'block', j and i + [ j ] or i ]
initial_block ::= <blank_lines> <block_starter> <black_line>*:i <any_blanks> <close_brace>  => [ '{ %s }' % ''.join(i) ]

empty_line ::= <eol> => None
blank_lines ::= <blank_line>* => []
some_blank_lines ::= <blank_line>+ => []
blank_line ::= <any_blanks> <eol> => None
any_blanks ::= <blank>*:i => ''.join(i)
some_blanks ::= <blank>+
blank ::= <space> | <tab>
any_white ::= <white>*
some_white ::= <white>+
white ::= <space> | <tab> | <eol>

asterisk ::= '*'
at ::= '@'
back_slash ::= '\\'
colon ::= ':'
comma ::= ','
close_brace ::= '}'
close_bracket ::= ')'
close_brick ::= ']'
dash ::= '-'
dot ::= '.'
eol ::= '\n'
equals ::= '='
exclamation ::= '!'
forward_slash ::= '/'
open_brace ::= '{'
open_bracket ::= '('
question ::= '?'
semi_colon ::= ';'
single_quote ::= '\''
space ::= ' '
tab ::= '\t'
underscore ::= '_'
open_brick ::= '['
double_quote ::= '"'
greater ::= '>'
less ::= '<'
string ::= (('"' | '\''):q (~<exactly q> <anything>)*:xs <exactly q> => '"%s"' % ''.join(xs))
