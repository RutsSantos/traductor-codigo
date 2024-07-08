import sys
from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from JavaParserListener import JavaParserListener
import tkinter as tk
from tkinter import scrolledtext
from antlr4.tree.Tree import TerminalNodeImpl

"""
Rut Santos, 2-17-1270.

Traductor de código Java a javascript en Python, usando la libreria Antlr4 que tiene el
parser y lexer del lenguaje java. Con tkinter realizo la interfaz gráfica.

"""
class JavaToJsListener(JavaParserListener):
    def __init__(self):
        self.js_code = ""

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        class_name = ctx.identifier().getText()
        self.js_code += f"class {class_name} {{\n"

    def exitClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        self.js_code += "}\n"

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_name = ctx.identifier().getText()
        self.js_code += f"  {method_name}() {{\n"

    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        self.js_code += "  }\n"

    def enterStatement(self, ctx: JavaParser.StatementContext):
        if ctx.getChild(0).getText() == "System.out.println":
            expr = ctx.expression(0).getText()
            self.js_code += f"    console.log({expr});\n"

def print_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, TerminalNodeImpl):
        print(f"{indent}{node.getText()}")
    else:
        print(f"{indent}{node.__class__.__name__}")
        for child in node.children:
            print_tree(child, level + 1)

def translate_java_to_js(java_code):
    input_stream = InputStream(java_code)
    lexer = JavaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.compilationUnit()
    
    print_tree(tree)
    
    js_listener = JavaToJsListener()
    walker = ParseTreeWalker()
    walker.walk(js_listener, tree)
    
    return js_listener.js_code

def translate_code():
    java_code = java_text.get("1.0", tk.END)
    js_code = translate_java_to_js(java_code)
    js_text.delete("1.0", tk.END)
    js_text.insert(tk.END, js_code)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Traductor de Java a JavaScript")

frame = tk.Frame(root)
frame.pack(pady=20)

java_label = tk.Label(frame, text="Código Java")
java_label.pack()

java_text = scrolledtext.ScrolledText(frame, height=15, width=70)
java_text.pack()

translate_button = tk.Button(frame, text="Traducir", command=translate_code)
translate_button.pack(pady=10)

js_label = tk.Label(frame, text="Código JavaScript")
js_label.pack()

js_text = scrolledtext.ScrolledText(frame, height=15, width=70)
js_text.pack()

root.mainloop()
