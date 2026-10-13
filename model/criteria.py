"""Search criteria (US7): type, text-contains, time comparison, and/or/not.

Textual syntax accepted by parse_criterion (tokens separated by spaces,
strings may be double-quoted; quoted text is always literal, so it may
contain ( ) ! && ||):

    type=task
    contains "meeting"            (searches every text field)
    time < "2026-11-01 09:00"     (checks every time field)
    ( type=task && contains "hw" ) || ! type=note
"""
from abc import ABC, abstractmethod
from .records import PIR, parse_time


class Criterion(ABC):
    @abstractmethod
    def matches(self, pir: PIR) -> bool: ...


class TypeCriterion(Criterion):
    def __init__(self, type_name: str):
        self.type_name = type_name.lower()

    def matches(self, pir):
        return pir.TYPE == self.type_name


class ContainsCriterion(Criterion):
    """True if any text field contains the string (case-insensitive)."""
    def __init__(self, needle: str):
        self.needle = needle.lower()

    def matches(self, pir):
        return any(self.needle in t.lower() for t in pir.text_fields())


class TimeCriterion(Criterion):
    """True if any time field satisfies the comparison. op in <, >, =."""
    def __init__(self, op: str, when):
        if op not in ("<", ">", "="):
            raise ValueError(f"Unknown time operator '{op}'")
        self.op = op
        self.when = parse_time(when) if isinstance(when, str) else when

    def matches(self, pir):
        for t in pir.time_fields():
            if (self.op == "<" and t < self.when) or \
               (self.op == ">" and t > self.when) or \
               (self.op == "=" and t == self.when):
                return True
        return False


class AndCriterion(Criterion):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def matches(self, pir):
        return self.left.matches(pir) and self.right.matches(pir)


class OrCriterion(Criterion):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def matches(self, pir):
        return self.left.matches(pir) or self.right.matches(pir)


class NotCriterion(Criterion):
    def __init__(self, inner):
        self.inner = inner

    def matches(self, pir):
        return not self.inner.matches(pir)


# ---------------- parser (recursive descent; ! > && > ||) ----------------
class _Op(str):
    """An operator token. Quoted text is never an operator; it stays a str."""


def _tokenize(text: str):
    tokens = []
    cur, literal, quote = "", False, None    # literal: token has a quoted part
    i = 0
    while i < len(text):
        ch = text[i]
        i += 1
        if quote:
            if ch == quote:
                quote = None
            elif ch == "\\" and quote == '"' and text[i:i + 1] in ('"', "\\"):
                cur += text[i]               # \" and \\ inside double quotes
                i += 1
            else:
                cur += ch                    # ( ) ! & | are plain text here
        elif ch in "\"'":
            quote, literal = ch, True
        elif ch.isspace() or ch in "()":
            if cur or literal:
                tokens.append(_word(cur, literal))
            cur, literal = "", False
            if ch in "()":                   # "(" may be glued to words
                tokens.append(_Op(ch))
        elif ch == "!" and not cur and not literal and text[i:i + 1] != "=":
            tokens.append(_Op("!"))          # allow "!type=note" without a space
        else:
            cur += ch
    if quote:
        raise ValueError("Bad criterion syntax: No closing quotation")
    if cur or literal:
        tokens.append(_word(cur, literal))
    return tokens


def _word(text, literal):
    return _Op(text) if not literal and text in ("&&", "||") else text


class _Parser:
    def __init__(self, tokens):
        self.t, self.i = tokens, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def at(self, op):
        tok = self.peek()
        return isinstance(tok, _Op) and tok == op

    def take(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of criterion")
        self.i += 1
        return tok

    def parse_or(self):
        node = self.parse_and()
        while self.at("||"):
            self.take()
            node = OrCriterion(node, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.at("&&"):
            self.take()
            node = AndCriterion(node, self.parse_not())
        return node

    def parse_not(self):
        if self.at("!"):
            self.take()
            return NotCriterion(self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        if self.at("("):
            self.take()
            node = self.parse_or()
            if not self.at(")"):
                raise ValueError("Expected ')'")
            self.take()
            return node
        tok = self.take()
        if tok.startswith("type="):
            return TypeCriterion(tok[5:])
        if tok == "type":
            if self.take() != "=":
                raise ValueError("Expected '=' after type")
            return TypeCriterion(self.take())
        if tok == "contains":
            return ContainsCriterion(self.take())
        if tok == "time":
            op = self.take()
            return TimeCriterion(op, self.take())
        raise ValueError(f"Unexpected token '{tok}'")


def parse_criterion(text: str) -> Criterion:
    tokens = _tokenize(text)
    if not tokens:
        raise ValueError("Empty criterion")
    parser = _Parser(tokens)
    node = parser.parse_or()
    if parser.peek() is not None:
        raise ValueError(f"Unexpected token '{parser.peek()}'")
    return node
