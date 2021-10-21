import sqlite3
import re
from pymystem3 import Mystem

m = Mystem()

con = sqlite3.connect('тексты (3).bd', check_same_thread=False)
cur = con.cursor()


def parse_search(expression):
    elems = expression.lower().split(' ')
    final_search_line = ''
    for elem in elems:
        if '+' in elem:
            double = ''
            new_elems = elem.split('+')
            if new_elems[0].startswith('"') and new_elems[0].endswith('"'):
                new_form = new_elems[0].strip('"')
                double += ' ?' + new_form + '/[а-я]+/'
            else:
                new_lex = (m.analyze(new_elems[0]))[0]['analysis'][0]['lex']
                double += ' ?[а-я]+/' + new_lex + '/'
            double += new_elems[1].upper()
            final_search_line += double + ' ?'
        elif elem.startswith('"') and elem.endswith('"'):
            form = elem.strip('"')
            form = str(form + '/[а-я]+/[A-Z]+ ?')
            final_search_line += form
        elif re.fullmatch(r'[A-Za-z]+', elem):
            pos = ' ?[а-я]+/[а-я]+/' + elem.upper() + ' ?'
            final_search_line += pos
        else:
            analyzed_elem = m.analyze(elem)
            elem_lex = ' ?[а-я]+/' + analyzed_elem[0]['analysis'][0]['lex'] + '/[A-Z]+ ?'
            final_search_line += elem_lex
    return final_search_line


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


def search(search_expression):
    regex = parse_search(search_expression)
    con.create_function("REGEXP", 2, regexp)
    query = """
    SELECT Texts.text_id, Texts.author, Texts.title, Texts.text, Parsed.text
    FROM Texts
    JOIN Parsed on Texts.text_id=Parsed.text_id
    WHERE Parsed.text REGEXP ?
    """
    cur.execute(query, [regex],)
    result = cur.fetchall()
    res_string = ''
    for res in result:
        text_id, author, title, text, parsed = res
        res_string += 'ID: ' + str(
            text_id) + '. Автор: ' + author + '. Произведение: ' + title + '\n' + text + '\n' + parsed + '\n\n'
    if len(res_string) == 0:
        res_string = 'Результатов нет('
    return res_string




