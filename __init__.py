import re
from aqt import gui_hooks
from aqt.browser import SearchContext
from anki import version
from aqt.utils import showInfo, qconnect

search_regex = re.compile(r'\word(?:_)?count\s?\((.+?)\)\s*(<=|>=|=|==|<|>|!=|)\s*(\d+)\b')

def createSearchString(field: str, operator: str, n: int) -> str:
    
    if operator == "=" or operator == "==":
        return '"{}:re:^(?:(&nbsp;|\\W|\\b)\\w+(&nbsp;|\\W|\\b)){{{}}}$"'.format(field, n)
    elif operator == ">":
        return '"{}:re:(?:(&nbsp;|\\W|\\b)\\w+(&nbsp;|\\W|\\b)){{{},}}"'.format(field, n + 1)
    elif operator == ">=":
        return '"{}:re:(?:(&nbsp;|\\W|\\b)\\w+(&nbsp;|\\W|\\b)){{{},}}"'.format(field, n)
    elif operator == "<":
        return '-"{}:re:(?:(&nbsp;|\\W|\\b)\\w+(&nbsp;|\\W|\\b)){{{},}}"'.format(field, n)
    elif operator == "<=":
        return '-"{}:re:(?:(&nbsp;|\\W|\\b)\\w+(&nbsp;|\\W|\\b)){{{},}}"'.format(field, n + 1)
    elif operator == "!=":
        return '-"{}:re:^(?:(&nbsp;|\\W|\\b)\\w+(&nbsp;|\\W|\\b)){{{}}}$"'.format(field, n)

    return ""

def len_browser_will_search(context: SearchContext) -> None:
    check = context.ids if version >= "2.1.45" else context.card_ids
    if check is not None:
        return

    for entry in search_regex.finditer(context.search):
        original = entry.group(0)
        field = entry.group(1)
        operator = entry.group(2)
        number = int(entry.group(3))
        change_string = createSearchString(field, operator, number)  

        context.search = context.search.replace(original, change_string)

gui_hooks.browser_will_search.append(len_browser_will_search)