import tkinter as tk
from tkinter import messagebox, ttk
import math
import ast
import operator as op


# EXPRESSION EVALUATOR

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "abs": abs,
    "factorial": math.factorial,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

def safe_eval(expr):
    node = ast.parse(expr, mode="eval")
    return _eval_node(node.body)

def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise TypeError("Unsupported constant")

    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_type = type(node.op)
        if operator_type in OPERATORS:
            return OPERATORS[operator_type](left, right)
        raise TypeError("Unsupported operator")

    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_type = type(node.op)
        if operator_type in OPERATORS:
            return OPERATORS[operator_type](operand)
        raise TypeError("Unsupported unary operator")

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise TypeError("Invalid function call")

        func_name = node.func.id
        if func_name not in FUNCTIONS:
            raise TypeError(f"Unsupported function: {func_name}")

        args = [_eval_node(arg) for arg in node.args]

        if func_name == "factorial":
            if len(args) != 1:
                raise ValueError("factorial() takes exactly one argument")
            value = args[0]
            if not float(value).is_integer() or value < 0:
                raise ValueError("factorial() only works for non-negative integers")
            return FUNCTIONS[func_name](int(value))

        return FUNCTIONS[func_name](*args)

    elif isinstance(node, ast.Name):
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise TypeError(f"Unknown name: {node.id}")

    else:
        raise TypeError("Unsupported expression")

def convert_factorials(expr):
    i = 0
    while i < len(expr):
        if expr[i] == "!":
            if i == 0:
                raise ValueError("Nothing before !")

            j = i - 1

            if expr[j] == ")":
                depth = 1
                j -= 1
                while j >= 0:
                    if expr[j] == ")":
                        depth += 1
                    elif expr[j] == "(":
                        depth -= 1
                        if depth == 0:
                            break
                    j -= 1
                if j < 0:
                    raise ValueError("Mismatched parentheses")
                inner = expr[j:i]
                expr = expr[:j] + f"factorial{inner}" + expr[i+1:]
                i = j + len(f"factorial{inner}") - 1
            else:
                while j >= 0 and (expr[j].isdigit() or expr[j] == "."):
                    j -= 1
                j += 1
                inner = expr[j:i]
                if not inner:
                    raise ValueError("Invalid factorial usage")
                expr = expr[:j] + f"factorial({inner})" + expr[i+1:]
                i = j + len(f"factorial({inner})") - 1
        i += 1
    return expr


# UNIT CONVERSIONS from 2020 Calculator

conversion_data = {
    "Length": {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.344,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
    },
    "Mass": {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.45359237,
        "Ounce": 0.028349523125,
    },
    "Volume": {
        "Liter": 1.0,
        "Milliliter": 0.001,
        "Cubic Meter": 1000.0,
        "Gallon (US)": 3.785411784,
        "Quart (US)": 0.946352946,
        "Pint (US)": 0.473176473,
        "Cup (US)": 0.2365882365,
        "Fluid Ounce (US)": 0.0295735295625,
    }
}

def convert_units(category, value, from_unit, to_unit):
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)

    base_value = value * conversion_data[category][from_unit]
    result = base_value / conversion_data[category][to_unit]
    return result

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    # Convert to Celsius first
    if from_unit == "Celsius":
        c = value
    elif from_unit == "Fahrenheit":
        c = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        c = value - 273.15
    else:
        raise ValueError("Invalid temperature unit")

    # Convert from Celsius to target
    if to_unit == "Celsius":
        return c
    elif to_unit == "Fahrenheit":
        return (c * 9 / 5) + 32
    elif to_unit == "Kelvin":
        return c + 273.15
    else:
        raise ValueError("Invalid temperature unit")


# GUI


history_items = []

def insert_text(text):
    entry.insert(tk.END, text)

def clear_all():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current[:-1])

def format_result(value):
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)

def add_to_history(text):
    history_items.append(text)
    history_listbox.insert(tk.END, text)

def clear_history():
    history_items.clear()
    history_listbox.delete(0, tk.END)

def use_history_item(event):
    selection = history_listbox.curselection()
    if selection:
        item = history_listbox.get(selection[0])
        if " = " in item:
            result = item.split(" = ", 1)[1]
            entry.delete(0, tk.END)
            entry.insert(0, result)

def calculate():
    expr = entry.get().strip()
    if not expr:
        return

    try:
        processed_expr = convert_factorials(expr)
        result = safe_eval(processed_expr)
        formatted = format_result(result)

        entry.delete(0, tk.END)
        entry.insert(0, formatted)

        add_to_history(f"{expr} = {formatted}")

    except Exception as exc:
        messagebox.showerror("Error", f"Invalid expression:\n{exc}")

def run_conversion():
    try:
        category = category_var.get()
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()
        value = float(conversion_entry.get())

        result = convert_units(category, value, from_unit, to_unit)
        formatted = format_result(result)

        conversion_result_var.set(formatted)
        add_to_history(f"{value} {from_unit} -> {to_unit} = {formatted}")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for conversion.")
    except Exception as exc:
        messagebox.showerror("Error", str(exc))

def update_unit_options(*args):
    category = category_var.get()
    if category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
    else:
        units = list(conversion_data[category].keys())

    from_unit_menu["values"] = units
    to_unit_menu["values"] = units

    if units:
        from_unit_var.set(units[0])
        to_unit_var.set(units[1] if len(units) > 1 else units[0])

def on_button_click(value):
    if value == "C":
        clear_all()
    elif value == "←":
        backspace()
    elif value == "=":
        calculate()
    elif value == "EXP":
        insert_text("e")
    elif value == "!":
        insert_text("!")
    else:
        insert_text(value)


# WINDOW


root = tk.Tk()
root.title("Scientific Calculator with Conversions")
root.geometry("1050x680")
root.configure(bg="#202124")


# CALCULATOR GUI

left_frame = tk.Frame(root, bg="#202124")
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

entry = tk.Entry(
    left_frame,
    font=("Arial", 22),
    bd=8,
    relief="ridge",
    justify="right",
    bg="white"
)
entry.grid(row=0, column=0, columnspan=6, padx=10, pady=10, ipadx=8, ipady=15, sticky="nsew")

buttons = [
    ["C", "←", "(", ")", "//", "%"],
    ["7", "8", "9", "/", "**", "sqrt("],
    ["4", "5", "6", "*", "pi", "e"],
    ["1", "2", "3", "-", "sin(", "cos("],
    ["0", ".", "EXP", "+", "tan(", "log("],
    ["asin(", "acos(", "atan(", "ln(", "abs(", "!"],
    ["exp(", "=", "", "", "", ""]
]

for r, row_vals in enumerate(buttons, start=1):
    for c, text in enumerate(row_vals):
        if text == "":
            continue

        btn = tk.Button(
            left_frame,
            text=text,
            font=("Arial", 16),
            width=7,
            height=2,
            command=lambda t=text: on_button_click(t),
            bg="#303134",
            fg="white",
            activebackground="#5f6368",
            activeforeground="white"
        )

        if text == "=":
            btn.grid(row=r, column=c, columnspan=5, padx=5, pady=5, sticky="nsew")
        else:
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

for i in range(6):
    left_frame.grid_columnconfigure(i, weight=1)
for i in range(len(buttons) + 1):
    left_frame.grid_rowconfigure(i, weight=1)


# HISTORY GUI

right_frame = tk.Frame(root, bg="#202124", width=320)
right_frame.pack(side="right", fill="y", padx=10, pady=10)

# History section
history_label = tk.Label(
    right_frame,
    text="Calculation History",
    font=("Arial", 16, "bold"),
    bg="#202124",
    fg="white"
)
history_label.pack(pady=(0, 8))

history_listbox = tk.Listbox(
    right_frame,
    font=("Consolas", 11),
    width=40,
    height=18,
    bg="white"
)
history_listbox.pack(fill="both", padx=5)
history_listbox.bind("<Double-Button-1>", use_history_item)

history_button_frame = tk.Frame(right_frame, bg="#202124")
history_button_frame.pack(fill="x", pady=6)

clear_history_button = tk.Button(
    history_button_frame,
    text="Clear History",
    font=("Arial", 11),
    command=clear_history,
    bg="#8b0000",
    fg="white"
)
clear_history_button.pack(fill="x", padx=5)

# Conversion section
conversion_label = tk.Label(
    right_frame,
    text="Unit Conversion",
    font=("Arial", 16, "bold"),
    bg="#202124",
    fg="white"
)
conversion_label.pack(pady=(18, 8))

category_var = tk.StringVar(value="Length")
from_unit_var = tk.StringVar()
to_unit_var = tk.StringVar()
conversion_result_var = tk.StringVar(value="")

category_var.trace_add("write", update_unit_options)

tk.Label(right_frame, text="Category", bg="#202124", fg="white", font=("Arial", 11)).pack(anchor="w", padx=5)
category_menu = ttk.Combobox(
    right_frame,
    textvariable=category_var,
    values=["Length", "Mass", "Temperature", "Volume"],
    state="readonly"
)
category_menu.pack(fill="x", padx=5, pady=3)

tk.Label(right_frame, text="Value", bg="#202124", fg="white", font=("Arial", 11)).pack(anchor="w", padx=5)
conversion_entry = tk.Entry(right_frame, font=("Arial", 12))
conversion_entry.pack(fill="x", padx=5, pady=3)

tk.Label(right_frame, text="From", bg="#202124", fg="white", font=("Arial", 11)).pack(anchor="w", padx=5)
from_unit_menu = ttk.Combobox(right_frame, textvariable=from_unit_var, state="readonly")
from_unit_menu.pack(fill="x", padx=5, pady=3)

tk.Label(right_frame, text="To", bg="#202124", fg="white", font=("Arial", 11)).pack(anchor="w", padx=5)
to_unit_menu = ttk.Combobox(right_frame, textvariable=to_unit_var, state="readonly")
to_unit_menu.pack(fill="x", padx=5, pady=3)

convert_button = tk.Button(
    right_frame,
    text="Convert",
    font=("Arial", 12, "bold"),
    command=run_conversion,
    bg="#1f6aa5",
    fg="white"
)
convert_button.pack(fill="x", padx=5, pady=8)

tk.Label(right_frame, text="Result", bg="#202124", fg="white", font=("Arial", 11)).pack(anchor="w", padx=5)
conversion_result_entry = tk.Entry(
    right_frame,
    textvariable=conversion_result_var,
    font=("Arial", 12),
    state="readonly",
    readonlybackground="white"
)
conversion_result_entry.pack(fill="x", padx=5, pady=3)

update_unit_options()

root.bind("<Return>", lambda event: calculate())
root.mainloop()