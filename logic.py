from sympy import symbols, simplify_logic

class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                value = ""
                while self.current_char is not None and self.current_char.isalpha():
                    value += self.current_char
                    self.advance()
                return Token("VARIABLE", value)

            if self.current_char == '(':
                self.advance()
                return Token("LEFT_PAREN", "(")

            if self.current_char == ')':
                self.advance()
                return Token("RIGHT_PAREN", ")")

            if self.current_char == '&':
                self.advance()
                return Token("AND_OPERATOR", "&")

            if self.current_char == '|':
                self.advance()
                return Token("OR_OPERATOR", "|")

            if self.current_char == '~':
                self.advance()
                return Token("NOT_OPERATOR", "~")
            
            if self.current_char == '^':
                self.advance()
                return Token("XOR_OPERATOR", "^")

            raise SyntaxError("Invalid character: {}".format(self.current_char))

        return Token("EOF")

class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        return self.expression()

    def expression(self):
        result = self.term()

        while self.current_token.token_type == "OR_OPERATOR":
            self.eat("OR_OPERATOR")
            result |= self.term() 
        return result

    def term(self):
        result = self.factor()

        while self.current_token.token_type == "AND_OPERATOR":
            self.eat("AND_OPERATOR")
            result &= self.factor()

        return result

    def factor(self):
        token = self.current_token
        if token.token_type == "LEFT_PAREN":
            self.eat("LEFT_PAREN")
            result = self.expression()
            self.eat("RIGHT_PAREN")
            return result
        elif token.token_type == "NOT_OPERATOR":
            self.eat("NOT_OPERATOR")
            return ~self.factor()  
        elif token.token_type == "VARIABLE":
            var = symbols(token.value)
            self.eat("VARIABLE")
            return var

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError("Unexpected token: {}".format(self.current_token))

class Simplifier:
    def __init__(self, expression):
        self.expression = expression

    def simplify(self):
        return simplify_logic(self.expression)

def get_tokens(text):
    lexer = Lexer(text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.token_type == "EOF":
            break
        tokens.append((token.token_type, token.value))
    return tokens
