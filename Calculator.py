import math
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDIconButton, MDFloatingActionButton
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty

KV = '''
BoxLayout:
    orientation: 'vertical'
    output_text: "Answer"
    
    MDTextField:
        id: input_field
        hint_text: "Enter expression"
        helper_text: "You can use +, -, *, /"
        helper_text_mode: "on_focus"
        input_filter: "float"
        multiline: False
        padding: "10dp"
        size_hint: (1, 0.2)
    
    MDLabel:
        text: app.output_text
        halign: 'center'
        size_hint: (1, 0.1)
    
    GridLayout:
        cols: 5
        spacing: "10dp"
        padding: "10dp"
        size_hint: (1, 0.7)
        
        MDRectangleFlatButton:
            text: "7"
            on_press: app.append_to_input("7")
            
        MDRectangleFlatButton:
            text: "8"
            on_press: app.append_to_input("8")
        
        MDRectangleFlatButton:
            text: "9"
            on_press: app.append_to_input("9")
            
        MDRectangleFlatButton:
            text: "sqrt("
            on_press: app.append_to_input("sqrt(")
        
        MDRectangleFlatButton:
            text: "log("
            on_press: app.append_to_input("log(")
        
        
        MDRectangleFlatButton:
            text: "4"
            on_press: app.append_to_input("4")
        
        MDRectangleFlatButton:
            text: "5"
            on_press: app.append_to_input("5")
        
        MDRectangleFlatButton:
            text: "6"
            on_press: app.append_to_input("6")
        
        MDRectangleFlatButton:
            text: "*"
            on_press: app.append_to_input("*")

        MDRectangleFlatButton:
            text: "/"
            on_press: app.append_to_input("/")
        
        MDRectangleFlatButton:
            text: "1"
            on_press: app.append_to_input("1")
        
        MDRectangleFlatButton:
            text: "2"
            on_press: app.append_to_input("2")
        
        MDRectangleFlatButton:
            text: "3"
            on_press: app.append_to_input("3")
        
        MDRectangleFlatButton:
            text: "-"
            on_press: app.append_to_input("-")

        MDRectangleFlatButton:
            text: "sin("
            on_press: app.append_to_input("sin(")

        MDRectangleFlatButton:
            text: "cos("
            on_press: app.append_to_input("cos(")
        
        MDRectangleFlatButton:
            text: "0"
            on_press: app.append_to_input("0")
        
        MDRectangleFlatButton:
            text: "."
            on_press: app.append_to_input(".")
        
        MDRectangleFlatButton:
            text: "C"
            on_press: app.clear_input()
        
        MDRectangleFlatButton:
            text: "+"
            on_press: app.append_to_input("+")
        
        MDRectangleFlatButton:
            text: "="
            on_press: app.calculate()

        MDRectangleFlatButton:
            text: "^"
            on_press: app.append_to_input("^")

        MDRectangleFlatButton:
            text: "tan("
            on_press: app.append_to_input("tan(")

        MDRectangleFlatButton:
            text: "("
            on_press: app.append_to_input("(")

        MDRectangleFlatButton:
            text: ")"
            on_press: app.append_to_input(")")
            
'''

class CalculatorApp(MDApp):
    output_text = StringProperty()

    def build(self):
        return Builder.load_string(KV)
    
    def append_to_input(self, text):
        current_text = self.root.ids.input_field.text
        self.root.ids.input_field.text = current_text + text
    
    def clear_input(self):
        self.root.ids.input_field.text = ''
        self.output_text = ''

    def calculate(self):
        expression = self.root.ids.input_field.text.strip()
        
        if not expression:
            self.output_text = "Error: Enter an expression"
            return
        try:
            result = self.evaluate_expression(expression)
            self.output_text = str(result)
        except ZeroDivisionError:
            self.output_text = "Error: Division by zero"
            # Replace '^' with '**' for exponentiation
            expression = expression.replace("^", "**")

            # Evaluate square root, logarithm, and trigonometric functions
            expression = expression.replace("sqrt(", "math.sqrt(")
            expression = expression.replace("log(", "math.log10(")
            expression = expression.replace("sin(", "math.sin(math.radians(")
            expression = expression.replace("cos(", "math.cos(math.radians(")
            expression = expression.replace("tan(", "math.tan(math.radians(")

            # Calculate the expression and display the result through self.output_text
            result = eval(expression)

            btn = MDFlatButton(text='Continue', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Answer", text=str(result), size_hint=(0.7, 0.2), buttons=[btn])
            self.dialog.open()

     main
        except Exception as e:
            self.output_text = "Error: " + str(e)

    def evaluate_expression(self, expression):
        operators = {'+': (lambda x, y: x + y), '-': (lambda x, y: x - y),
                     '*': (lambda x, y: x * y), '/': (lambda x, y: x / y)}
        tokens = expression.split()
        stack = []

        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i - 1] in operators):
                # Handle negative numbers
                continue

            if token.isnumeric() or (token[0] == '-' and token[1:].isnumeric()):
                stack.append(float(token))
            elif token in operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                operand2 = stack.pop()
                operand1 = stack.pop()
                operation = operators[token]
                result = operation(operand1, operand2)
                stack.append(result)
            else:
                raise ValueError("Invalid token: {}".format(token))

        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]

    def close_dialogue(self, obj):
        self.root.ids.input_field.text = ''
        self.output_text = ''
        self.dialog.dismiss()

if __name__ == '__main__':
    CalculatorApp().run()
