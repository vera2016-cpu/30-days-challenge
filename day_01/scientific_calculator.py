import tkinter as tk
from tkinter import messagebox
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("500x550")  # FIXED: Better height
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = ""
        self.result_var = tk.StringVar(value="0")
        self.history = []
        self.is_scientific_mode = False
        self.deg_rad_mode = "DEG"
        
        # Colors
        self.set_theme("dark")
        
        # Create widgets
        self.create_widgets()
        
        # Bind keyboard events
        self.bind_keyboard()
    
    def set_theme(self, theme):
        if theme == "dark":
            self.bg_color = "#1e1e1e"
            self.display_bg = "#2d2d2d"
            self.btn_color = "#3c3f41"
            self.text_color = "#ffffff"
            self.operator_color = "#ff9500"
            self.scientific_color = "#007acc"
            self.special_color = "#a6a6a6"
            self.history_bg = "#252526"
        else:
            self.bg_color = "#f0f0f0"
            self.display_bg = "#ffffff"
            self.btn_color = "#e0e0e0"
            self.text_color = "#000000"
            self.operator_color = "#ff9500"
            self.scientific_color = "#007acc"
            self.special_color = "#a0a0a0"
            self.history_bg = "#f5f5f5"
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)  # Reduced padding
        
        # Mode toggle button
        mode_frame = tk.Frame(main_frame, bg=self.bg_color)
        mode_frame.pack(fill=tk.X, pady=(0, 5))  # Reduced padding
        
        self.mode_btn = tk.Button(
            mode_frame,
            text="Standard",
            font=("Arial", 9),  # Slightly smaller font
            bg=self.scientific_color,
            fg=self.text_color,
            command=self.toggle_mode
        )
        self.mode_btn.pack(side=tk.LEFT)
        
        # DEG/RAD toggle
        self.deg_rad_btn = tk.Button(
            mode_frame,
            text=self.deg_rad_mode,
            font=("Arial", 9),
            bg=self.scientific_color,
            fg=self.text_color,
            command=self.toggle_deg_rad
        )
        self.deg_rad_btn.pack(side=tk.RIGHT)
        
        # History display (reduced height)
        history_frame = tk.Frame(main_frame, bg=self.history_bg, height=70)  # Reduced from 100
        history_frame.pack(fill=tk.X, pady=(0, 5))  # Reduced padding
        history_frame.pack_propagate(False)
        
        tk.Label(
            history_frame,
            text="History",
            font=("Arial", 9, "bold"),  # Smaller font
            bg=self.history_bg,
            fg=self.text_color
        ).pack(anchor="w", padx=10, pady=(3, 0))  # Reduced padding
        
        self.history_text = tk.Text(
            history_frame,
            font=("Arial", 8),  # Smaller font
            bg=self.history_bg,
            fg=self.text_color,
            height=3,  # Reduced from 4
            relief=tk.FLAT,
            state="disabled"
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 3))  # Reduced padding
        
        # Main display (reduced height)
        display_frame = tk.Frame(main_frame, bg=self.display_bg, height=60)  # Reduced from 80
        display_frame.pack(fill=tk.X, pady=(0, 5))  # Reduced padding
        display_frame.pack_propagate(False)
        
        tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=("Arial", 28, "bold"),  # Slightly smaller font
            bg=self.display_bg,
            fg=self.text_color,
            anchor="e",
            padx=15  # Reduced padding
        ).pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_standard_buttons(buttons_frame)
    
    def create_standard_buttons(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        
        if self.is_scientific_mode:
            buttons = [
                ['C', '⌫', '%', '/', '√', 'x²', 'xʸ', '10ˣ'],
                ['7', '8', '9', '*', 'sin', 'cos', 'tan', 'log'],
                ['4', '5', '6', '-', 'asin', 'acos', 'atan', 'ln'],
                ['1', '2', '3', '+', 'π', 'e', '(', ')'],
                ['00', '0', '.', '=', '±', '!', 'mod', 'exp']
            ]
            font_size = 12  # Smaller font for scientific mode
        else:
            buttons = [
                ['C', '⌫', '%', '/', '√', 'x²'],
                ['7', '8', '9', '*', 'sin', 'cos'],
                ['4', '5', '6', '-', 'tan', 'log'],
                ['1', '2', '3', '+', 'ln', 'π'],
                ['00', '0', '.', '=', 'e', '(']
            ]
            font_size = 14  # Standard font
        
        for i, row in enumerate(buttons):
            parent.grid_rowconfigure(i, weight=1)
            for j, text in enumerate(row):
                parent.grid_columnconfigure(j, weight=1)
                
                if text in ['/', '*', '-', '+', '=', 'mod']:
                    bg_color = self.operator_color
                elif text in ['C', '⌫', '%']:
                    bg_color = self.special_color
                elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'xʸ', '10ˣ', 
                             'asin', 'acos', 'atan', 'π', 'e', '±', '!', 'exp', '(']:
                    bg_color = self.scientific_color
                else:
                    bg_color = self.btn_color
                
                tk.Button(
                    parent,
                    text=text,
                    font=("Arial", font_size, "bold"),
                    bg=bg_color,
                    fg=self.text_color,
                    borderwidth=0,
                    command=lambda t=text: self.on_button_click(t)
                ).grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
    
    def toggle_mode(self):
        self.is_scientific_mode = not self.is_scientific_mode
        self.mode_btn.config(text="Scientific" if self.is_scientific_mode else "Standard")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        self.create_standard_buttons(child)
                        break
    
    def toggle_deg_rad(self):
        self.deg_rad_mode = "RAD" if self.deg_rad_mode == "DEG" else "DEG"
        self.deg_rad_btn.config(text=self.deg_rad_mode)
    
    def on_button_click(self, text):
        if text == 'C':
            self.current_input = ""
            self.result_var.set("0")
        elif text == '⌫':
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self.result_var.set(self.current_input if self.current_input else "0")
        elif text == '=':
            self.calculate_result()
        elif text == '%':
            try:
                result = eval(self.current_input or "0") / 100
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid operation!")
        elif text == '√':
            try:
                result = math.sqrt(float(self.current_input or 0))
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid input!")
        elif text == 'x²':
            try:
                result = float(self.current_input or 0) ** 2
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid input!")
        elif text == 'xʸ':
            self.current_input += '**'
            self.result_var.set(self.current_input)
        elif text == '10ˣ':
            try:
                result = 10 ** float(self.current_input or 0)
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid input!")
        elif text in ['sin', 'cos', 'tan']:
            try:
                value = float(self.current_input or 0)
                if self.deg_rad_mode == "DEG":
                    value = math.radians(value)
                result = getattr(math, text)(value)
                self.current_input = str(round(result, 10))
                self.result_var.set(self.current_input)
            except:
                self.show_error(f"Invalid input for {text}!")
        elif text in ['asin', 'acos', 'atan']:
            try:
                value = float(self.current_input or 0)
                if text == 'asin':
                    result = math.asin(value)
                elif text == 'acos':
                    result = math.acos(value)
                else:
                    result = math.atan(value)
                if self.deg_rad_mode == "DEG":
                    result = math.degrees(result)
                self.current_input = str(round(result, 10))
                self.result_var.set(self.current_input)
            except:
                self.show_error(f"Invalid input for {text}!")
        elif text == 'log':
            try:
                value = float(self.current_input or 0)
                result = math.log10(value)
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid input!")
        elif text == 'ln':
            try:
                value = float(self.current_input or 0)
                result = math.log(value)
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid input!")
        elif text == 'π':
            self.current_input += str(math.pi)
            self.result_var.set(self.current_input)
        elif text == 'e':
            self.current_input += str(math.e)
            self.result_var.set(self.current_input)
        elif text == '±':
            if self.current_input and self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_var.set(self.current_input)
        elif text == '!':
            try:
                n = int(float(self.current_input or 0))
                result = math.factorial(n)
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            except:
                self.show_error("Invalid input!")
        elif text == 'mod':
            self.current_input += '%'
            self.result_var.set(self.current_input)
        elif text == 'exp':
            self.current_input += 'e'
            self.result_var.set(self.current_input)
        elif text in ['(', ')']:
            self.current_input += text
            self.result_var.set(self.current_input)
        else:
            self.current_input += text
            self.result_var.set(self.current_input)
    
    def calculate_result(self):
        if not self.current_input:
            return
        try:
            expression = self.current_input
            expression = expression.replace('π', str(math.pi))
            expression = expression.replace('e', str(math.e))
            result = eval(expression)
            self.history.append(f"{self.current_input} = {result}")
            self.update_history_display()
            self.result_var.set(str(result))
            self.current_input = str(result)
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero!")
            self.current_input = ""
            self.result_var.set("0")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
            self.current_input = ""
            self.result_var.set("0")
    
    def update_history_display(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        for entry in reversed(self.history[-8:]):  # Show only 8 entries
            self.history_text.insert(1.0, entry + "\n")
        self.history_text.config(state="disabled")
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
    
    def bind_keyboard(self):
        for i in range(10):
            self.root.bind(str(i), lambda e, num=str(i): self.on_key_press(num))
        operators = {
            '+': '+', '-': '-', '*': '*', '/': '/',
            '=': '=', 'enter': '=', 'return': '=',
            '%': '%', '(': '(', ')': ')', '^': '**',
            '.': '.', 'c': 'C', 'C': 'C'
        }
        for key, value in operators.items():
            self.root.bind(key, lambda e, val=value: self.on_key_press(val))
        self.root.bind('<BackSpace>', lambda e: self.on_button_click('⌫'))
        self.root.bind('<Escape>', lambda e: self.on_button_click('C'))
        self.root.bind('<Delete>', lambda e: self.on_button_click('C'))
        self.root.bind('<Control-h>', lambda e: self.clear_history())
    
    def on_key_press(self, key):
        if key == '=':
            self.calculate_result()
        else:
            self.on_button_click(key)
    
    def clear_history(self):
        self.history = []
        self.update_history_display()

def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()