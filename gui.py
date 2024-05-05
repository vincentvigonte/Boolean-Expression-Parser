import tkinter as tk
from tkinter import messagebox
from logic import get_tokens, Parser, Simplifier

def display_tokens_vertically(tokens):
    for token in tokens:
        print(token[0], "\t", token[1])

def process_expression():
    expression_text = expression_entry.get()
    tokens = get_tokens(expression_text)
    token_text.delete('1.0', tk.END)
    for token in tokens:
        token_text.insert(tk.END, f"{token[0]}: {token[1]}\n")
    
    parser = Parser(expression_text)
    parsed_expression = parser.parse()
    parsed_text.delete('1.0', tk.END)
    parsed_text.insert(tk.END, str(parsed_expression))

    simplifier = Simplifier(parsed_expression)
    simplified_expression = simplifier.simplify()
    simplified_text.delete('1.0', tk.END)
    simplified_text.insert(tk.END, str(simplified_expression))

root = tk.Tk()
root.title("Boolean Expression Minimizer")

expression_label = tk.Label(root, text="Enter Boolean Expression:")
expression_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

expression_entry = tk.Entry(root, width=50)
expression_entry.grid(row=0, column=1, padx=5, pady=5)

process_button = tk.Button(root, text="Simplify", command=process_expression)
process_button.grid(row=0, column=2, padx=5, pady=5)

token_label = tk.Label(root, text="Tokens:")
token_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

token_text = tk.Text(root, width=30, height=10)
token_text.grid(row=1, column=1, padx=5, pady=5, sticky="w", columnspan=2)

parsed_label = tk.Label(root, text="Parsed Expression:")
parsed_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

parsed_text = tk.Text(root, width=30, height=2)
parsed_text.grid(row=2, column=1, padx=5, pady=5, sticky="w", columnspan=2)

simplified_label = tk.Label(root, text="Simplified Expression:")
simplified_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

simplified_text = tk.Text(root, width=30, height=2)
simplified_text.grid(row=3, column=1, padx=5, pady=5, sticky="w", columnspan=2)

root.mainloop()
