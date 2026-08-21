import tkinter as tk
from tkinter import ttk, messagebox
import math
import statistics
from datetime import date, timedelta


class ProCalc:

    def __init__(self, root):

        self.root = root
        self.root.title("ProCalc - Advanced Professional Calculator")
        self.root.geometry("900x600")
        self.root.minsize(820, 540)

        self.LIGHT = "#F2F4F7"
        self.DARK = "#273142"

        self.history = []

        self.memory = 0.0

        self.angle_mode = "DEG"

        self.current_mode = "Standard"

        self.standard_expression = tk.StringVar()

        self.scientific_expression = tk.StringVar()

        self.root.configure(bg=self.LIGHT)

        self.setup_styles()

        self.create_header()

        self.create_main_area()

        self.root.bind("<Key>", self.keyboard_input)

   
    def setup_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background=self.LIGHT,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=self.LIGHT,
            foreground=self.DARK,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.DARK)
            ],
            foreground=[
                ("selected", self.LIGHT)
            ]
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.LIGHT,
            background=self.LIGHT,
            foreground=self.DARK
        )

    def make_button(
        self,
        parent,
        text,
        command,
        accent=False,
        font=("Segoe UI", 11, "bold"),
        padx=12,
        pady=8
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,

            bg=self.DARK if accent else self.LIGHT,

            fg=self.LIGHT if accent else self.DARK,

            activebackground=self.DARK if accent else self.LIGHT,

            activeforeground=self.LIGHT if accent else self.DARK,

            font=font,

            relief="solid",

            bd=1,

            padx=padx,

            pady=pady,

            cursor="hand2"
        )

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.LIGHT
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        tk.Label(
            header,
            text="PROCALC",
            font=("Segoe UI", 18, "bold"),
            bg=self.LIGHT,
            fg=self.DARK
        ).pack(side="left")

        tk.Label(
            header,
            text="  Advanced Professional Calculator",
            font=("Segoe UI", 9),
            bg=self.LIGHT,
            fg=self.DARK
        ).pack(
            side="left",
            pady=(10, 0)
        )

        self.make_button(
            header,
            "History",
            self.show_history,
            accent=True
        ).pack(
            side="right",
            padx=5
        )

        self.make_button(
            header,
            "Settings",
            self.show_settings,
            accent=True
        ).pack(
            side="right",
            padx=5
        )


    def create_main_area(self):

        main = tk.Frame(
            self.root,
            bg=self.LIGHT
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # SIDEBAR

        self.sidebar = tk.Frame(
            main,
            bg=self.LIGHT,
            width=150,
            highlightbackground=self.DARK,
            highlightthickness=1
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )

        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="CALCULATOR MODES",
            font=("Segoe UI", 10, "bold"),
            bg=self.LIGHT,
            fg=self.DARK
        ).pack(
            pady=(22, 15)
        )

        modes = [

            ("Standard", self.standard_mode),

            ("Scientific", self.scientific_mode),

            ("Finance", self.finance_mode),

            ("Converter", self.converter_mode),

            ("Programmer", self.programmer_mode),

            ("Statistics", self.statistics_mode),

            ("Date & Time", self.date_time_mode)

        ]

        for text, command in modes:

            self.mode_button(
                text,
                command
            )

        # CONTENT

        self.content = tk.Frame(
            main,
            bg=self.LIGHT
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.standard_mode()

    def mode_button(
        self,
        text,
        command
    ):

        self.make_button(
            self.sidebar,
            text,
            command,
            accent=False,
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=8
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()

    def create_label(
        self,
        parent,
        text
    ):

        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=self.LIGHT,
            fg=self.DARK
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 3)
        )

    def create_entry(
        self,
        parent,
        width=30
    ):

        entry = tk.Entry(
            parent,
            width=width,
            font=("Segoe UI", 12),

            bg=self.LIGHT,

            fg=self.DARK,

            insertbackground=self.DARK,

            relief="solid",

            bd=1
        )

        entry.pack(
            fill="x",
            padx=12,
            pady=5,
            ipady=8
        )

        return entry

    def result_label(
        self,
        parent,
        text="Result: "
    ):

        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 15, "bold"),
            bg=self.LIGHT,
            fg=self.DARK,
            justify="left"
        )

        label.pack(
            pady=15
        )

        return label


    def format_result(
        self,
        value
    ):

        if isinstance(value, float):

            if not math.isfinite(value):

                raise ValueError(
                    "Invalid result"
                )

            if value.is_integer():

                return str(
                    int(value)
                )

            return f"{value:.10g}"

        return str(value)

    def add_history(
        self,
        expression,
        result
    ):

        self.history.insert(
            0,
            f"{expression} = {result}"
        )

    def standard_mode(self):

        self.current_mode = "Standard"

        self.clear_content()

        # DISPLAY

        display_frame = tk.Frame(
            self.content,
            bg=self.LIGHT,
            highlightbackground=self.DARK,
            highlightthickness=1
        )

        display_frame.pack(
            fill="x",
            pady=(0, 8)
        )

        self.standard_expression.set("")

        tk.Entry(
            display_frame,

            textvariable=self.standard_expression,

            font=("Segoe UI", 25, "bold"),

            justify="right",

            bg=self.LIGHT,

            fg=self.DARK,

            insertbackground=self.DARK,

            relief="flat"
        ).pack(
            fill="x",
            padx=20,
            pady=18,
            ipady=10
        )

        memory_frame = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        memory_frame.pack(
            fill="x",
            pady=3
        )

        memory_buttons = [

            ("MC", self.memory_clear),

            ("MR", self.memory_recall),

            ("M+", self.memory_add),

            ("M-", self.memory_subtract),

            ("MS", self.memory_store)

        ]

        for text, command in memory_buttons:

            self.make_button(
                memory_frame,
                text,
                command,
                accent=True,
                font=("Segoe UI", 9, "bold"),
                padx=10,
                pady=4
            ).pack(
                side="left",
                padx=3
            )

        self.memory_status = tk.Label(
            memory_frame,
            text=self.memory_text(),
            bg=self.LIGHT,
            fg=self.DARK,
            font=("Segoe UI", 9, "bold")
        )

        self.memory_status.pack(
            side="right",
            padx=10
        )
        button_frame = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        button_frame.pack(
            fill="both",
            expand=True
        )

        buttons = [

            ["C", "⌫", "(", ")"],

            ["7", "8", "9", "÷"],

            ["4", "5", "6", "×"],

            ["1", "2", "3", "−"],

            ["00", "0", ".", "+"],

            ["%", "±", "=", "H"]

        ]

        for r in range(6):

            button_frame.rowconfigure(
                r,
                weight=1
            )

        for c in range(4):

            button_frame.columnconfigure(
                c,
                weight=1
            )

        for r, row in enumerate(buttons):

            for c, value in enumerate(row):

                accent = value in {
                    "=",
                    "H",
                    "÷",
                    "×",
                    "−",
                    "+",
                    "%",
                    "±",
                    "C"
                }

                self.make_button(
                    button_frame,
                    value,
                    lambda v=value:
                    self.standard_click(v),
                    accent=accent,
                    font=("Segoe UI", 12, "bold")
                ).grid(
                    row=r,
                    column=c,
                    sticky="nsew",
                    padx=4,
                    pady=4
                )

    def standard_click(
        self,
        value
    ):

        current = self.standard_expression.get()

        if value == "C":

            self.standard_expression.set("")

        elif value == "⌫":

            self.standard_expression.set(
                current[:-1]
            )

        elif value == "H":

            self.show_history()

        elif value == "±":

            try:

                if current:

                    result = self.safe_eval(
                        current
                    )

                    self.standard_expression.set(
                        self.format_result(
                            -result
                        )
                    )

            except:

                pass

        elif value == "=":

            try:

                result = self.safe_eval(
                    current
                )

                formatted = self.format_result(
                    result
                )

                self.add_history(
                    current,
                    formatted
                )

                self.standard_expression.set(
                    formatted
                )

            except:

                messagebox.showerror(
                    "Calculation Error",
                    "Please enter a valid expression."
                )

        else:

            self.standard_expression.set(
                current + value
            )

    def safe_eval(
        self,
        expression
    ):

        expression = expression.replace(
            "×",
            "*"
        )

        expression = expression.replace(
            "÷",
            "/"
        )

        expression = expression.replace(
            "−",
            "-"
        )

        if not expression.strip():

            raise ValueError(
                "Empty expression"
            )

        return eval(
            expression,
            {
                "__builtins__": {}
            },
            {
                "pi": math.pi,
                "e": math.e
            }
        )
    def get_standard_number(self):

        try:

            return float(
                self.safe_eval(
                    self.standard_expression.get()
                )
            )

        except:

            return None

    def memory_text(self):

        return (
            f"M = {self.format_result(self.memory)}"
        )

    def update_memory_status(self):

        if hasattr(
            self,
            "memory_status"
        ):

            if self.memory_status.winfo_exists():

                self.memory_status.config(
                    text=self.memory_text()
                )

    def memory_clear(self):

        self.memory = 0.0

        self.update_memory_status()

    def memory_recall(self):

        self.standard_expression.set(
            self.format_result(
                self.memory
            )
        )

    def memory_add(self):

        value = self.get_standard_number()

        if value is None:

            messagebox.showerror(
                "Memory Error",
                "Enter a valid number or expression."
            )

            return

        self.memory += value

        self.update_memory_status()

    def memory_subtract(self):

        value = self.get_standard_number()

        if value is None:

            messagebox.showerror(
                "Memory Error",
                "Enter a valid number or expression."
            )

            return

        self.memory -= value

        self.update_memory_status()

    def memory_store(self):

        value = self.get_standard_number()

        if value is None:

            messagebox.showerror(
                "Memory Error",
                "Enter a valid number or expression."
            )

            return

        self.memory = value

        self.update_memory_status()

    def scientific_mode(self):

        self.current_mode = "Scientific"

        self.clear_content()

        self.scientific_expression.set("")

        display_frame = tk.Frame(
            self.content,
            bg=self.LIGHT,
            highlightbackground=self.DARK,
            highlightthickness=1
        )

        display_frame.pack(
            fill="x",
            pady=(0, 8)
        )

        tk.Entry(
            display_frame,
            textvariable=self.scientific_expression,
            font=("Segoe UI", 18, "bold"),
            justify="right",
            bg=self.LIGHT,
            fg=self.DARK,
            insertbackground=self.DARK,
            relief="flat"
        ).pack(
            fill="x",
            padx=20,
            pady=18,
            ipady=8
        )

        # DEG / RAD

        top = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        top.pack(
            fill="x",
            pady=4
        )

        self.make_button(
            top,
            "DEG",
            lambda:
            self.set_angle("DEG"),
            accent=True
        ).pack(
            side="left",
            padx=3
        )

        self.make_button(
            top,
            "RAD",
            lambda:
            self.set_angle("RAD"),
            accent=False
        ).pack(
            side="left",
            padx=3
        )

        self.angle_label = tk.Label(
            top,
            text=f"Angle Mode: {self.angle_mode}",
            bg=self.LIGHT,
            fg=self.DARK,
            font=("Segoe UI", 10, "bold")
        )

        self.angle_label.pack(
            side="left",
            padx=15
        )

        # FUNCTIONS

        functions = [

            "sin",
            "cos",
            "tan",
            "asin",

            "acos",
            "atan",
            "log",
            "ln",

            "√",
            "∛",
            "x²",
            "x³",

            "xʸ",
            "π",
            "e",
            "!",

            "10ˣ",
            "1/x",
            "abs",
            "floor",

            "ceil",
            "exp",
            "%",
            "⌫"

        ]

        function_frame = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        function_frame.pack(
            fill="both",
            expand=True
        )

        for r in range(6):

            function_frame.rowconfigure(
                r,
                weight=1
            )

        for c in range(4):

            function_frame.columnconfigure(
                c,
                weight=1
            )

        for i, func in enumerate(functions):

            self.make_button(
                function_frame,
                func,
                lambda x=func:
                self.scientific_function(x),
                accent=True,
                font=("Segoe UI", 11, "bold")
            ).grid(
                row=i // 4,
                column=i % 4,
                sticky="nsew",
                padx=3,
                pady=3
            )

        # NUMERIC BUTTONS

        bottom = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        bottom.pack(
            fill="x",
            pady=5
        )

        values = [

            "7",
            "8",
            "9",

            "4",
            "5",
            "6",

            "1",
            "2",
            "3",

            "0",
            ".",

            "(",
            ")",

            "=",

            "C"

        ]

        for value in values:

            self.make_button(
                bottom,
                value,
                lambda x=value:
                self.scientific_input(x),

                accent=value in {
                    "=",
                    "C"
                },

                font=("Segoe UI", 12, "bold"),

                padx=10
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=2
            )

    def set_angle(
        self,
        mode
    ):

        self.angle_mode = mode

        if hasattr(
            self,
            "angle_label"
        ):

            self.angle_label.config(
                text=f"Angle Mode: {mode}"
            )

    def scientific_function(
        self,
        func
    ):

        current = self.scientific_expression.get()

        try:

            if func == "π":

                self.scientific_expression.set(
                    current + "pi"
                )

                return

            if func == "e":

                self.scientific_expression.set(
                    current + "e"
                )

                return

            if func == "xʸ":

                self.scientific_expression.set(
                    current + "**"
                )

                return

            if func == "%":

                if not current:

                    raise ValueError

                value = self.safe_eval(
                    current
                )

                self.scientific_expression.set(
                    self.format_result(
                        value / 100
                    )
                )

                return

            if func == "⌫":

                self.scientific_expression.set(
                    current[:-1]
                )

                return

            value = float(
                self.safe_eval(
                    current
                )
            )

            if func in {
                "sin",
                "cos",
                "tan"
            }:

                x = (
                    math.radians(value)
                    if self.angle_mode == "DEG"
                    else value
                )

                result = getattr(
                    math,
                    func
                )(x)

            elif func in {
                "asin",
                "acos",
                "atan"
            }:

                result = getattr(
                    math,
                    func
                )(value)

                if self.angle_mode == "DEG":

                    result = math.degrees(
                        result
                    )

            elif func == "log":

                result = math.log10(
                    value
                )

            elif func == "ln":

                result = math.log(
                    value
                )

            elif func == "√":

                result = math.sqrt(
                    value
                )

            elif func == "∛":

                result = math.copysign(
                    abs(value) ** (1 / 3),
                    value
                )

            elif func == "x²":

                result = value ** 2

            elif func == "x³":

                result = value ** 3

            elif func == "!":

                if (
                    value < 0
                    or int(value) != value
                ):

                    raise ValueError

                result = math.factorial(
                    int(value)
                )

            elif func == "10ˣ":

                result = 10 ** value

            elif func == "1/x":

                result = 1 / value

            elif func == "abs":

                result = abs(value)

            elif func == "floor":

                result = math.floor(
                    value
                )

            elif func == "ceil":

                result = math.ceil(
                    value
                )

            elif func == "exp":

                result = math.exp(
                    value
                )

            else:

                return

            result = self.format_result(
                result
            )

            self.add_history(
                f"{func}({value})",
                result
            )

            self.scientific_expression.set(
                result
            )

        except:

            messagebox.showerror(
                "Scientific Error",
                "Invalid scientific calculation."
            )
    def scientific_input(
        self,
        value
    ):

        current = (
            self.scientific_expression.get()
        )

        if value == "C":

            self.scientific_expression.set("")

        elif value == "=":

            try:

                result = self.format_result(
                    self.safe_eval(
                        current
                    )
                )

                self.add_history(
                    current,
                    result
                )

                self.scientific_expression.set(
                    result
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Invalid expression."
                )

        else:

            self.scientific_expression.set(
                current + value
            )

    def finance_mode(self):

        self.current_mode = "Finance"

        self.clear_content()

        notebook = ttk.Notebook(
            self.content
        )

        notebook.pack(
            fill="both",
            expand=True
        )

        self.finance_simple_interest(
            notebook
        )

        self.finance_compound_interest(
            notebook
        )

        self.finance_emi(
            notebook
        )

        self.finance_gst(
            notebook
        )

        self.finance_discount(
            notebook
        )

        self.finance_profit_loss(
            notebook
        )

        self.finance_fd(
            notebook
        )

    def finance_tab(
        self,
        notebook,
        title
    ):

        frame = tk.Frame(
            notebook,
            bg=self.LIGHT
        )

        notebook.add(
            frame,
            text=title
        )

        return frame

    def labeled_entry(
        self,
        parent,
        label
    ):

        self.create_label(
            parent,
            label
        )

        return self.create_entry(
            parent
        )

    def finance_simple_interest(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "Simple Interest"
        )

        p = self.labeled_entry(
            frame,
            "Principal Amount"
        )

        r = self.labeled_entry(
            frame,
            "Rate (%)"
        )

        t = self.labeled_entry(
            frame,
            "Time (Years)"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate",
            lambda:
            self.calc_si(
                p,
                r,
                t,
                result
            ),
            accent=True
        ).pack()

    def calc_si(
        self,
        p,
        r,
        t,
        result
    ):

        try:

            P = float(p.get())

            R = float(r.get())

            T = float(t.get())

            interest = (
                P * R * T / 100
            )

            amount = P + interest

            text = (
                f"Interest: ₹{interest:.2f}\n"
                f"Total Amount: ₹{amount:.2f}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "Simple Interest",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

    def finance_compound_interest(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "Compound Interest"
        )

        p = self.labeled_entry(
            frame,
            "Principal Amount"
        )

        r = self.labeled_entry(
            frame,
            "Rate (%)"
        )

        t = self.labeled_entry(
            frame,
            "Time (Years)"
        )

        n = self.labeled_entry(
            frame,
            "Compounds Per Year"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate",
            lambda:
            self.calc_ci(
                p,
                r,
                t,
                n,
                result
            ),
            accent=True
        ).pack()

    def calc_ci(
        self,
        p,
        r,
        t,
        n,
        result
    ):

        try:

            P = float(p.get())

            R = float(r.get()) / 100

            T = float(t.get())

            N = float(n.get())

            if N <= 0:

                raise ValueError

            amount = (
                P *
                (1 + R / N) **
                (N * T)
            )

            interest = amount - P

            text = (
                f"Interest: ₹{interest:.2f}\n"
                f"Amount: ₹{amount:.2f}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "Compound Interest",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )


    def finance_emi(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "EMI"
        )

        p = self.labeled_entry(
            frame,
            "Loan Amount"
        )

        r = self.labeled_entry(
            frame,
            "Annual Interest Rate (%)"
        )

        t = self.labeled_entry(
            frame,
            "Tenure (Years)"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate EMI",
            lambda:
            self.calc_emi(
                p,
                r,
                t,
                result
            ),
            accent=True
        ).pack()

    def calc_emi(
        self,
        p,
        r,
        t,
        result
    ):

        try:

            P = float(p.get())

            annual_rate = float(
                r.get()
            )

            years = float(
                t.get()
            )

            months = years * 12

            if P <= 0 or months <= 0:

                raise ValueError

            monthly_rate = (
                annual_rate / 12 / 100
            )

            if monthly_rate == 0:

                emi = P / months

            else:

                emi = (
                    P *
                    monthly_rate *
                    (1 + monthly_rate) ** months
                ) / (
                    (1 + monthly_rate) ** months - 1
                )

            total = emi * months

            interest = total - P

            text = (
                f"Monthly EMI: ₹{emi:.2f}\n"
                f"Total Payment: ₹{total:.2f}\n"
                f"Total Interest: ₹{interest:.2f}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "EMI",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

    # ==================================================
    # GST
    # ==================================================

    def finance_gst(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "GST"
        )

        amount = self.labeled_entry(
            frame,
            "Amount"
        )

        gst = self.labeled_entry(
            frame,
            "GST (%)"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate GST",
            lambda:
            self.calc_gst(
                amount,
                gst,
                result
            ),
            accent=True
        ).pack()

    def calc_gst(
        self,
        amount,
        gst,
        result
    ):

        try:

            amount = float(
                amount.get()
            )

            rate = float(
                gst.get()
            )

            tax = (
                amount * rate / 100
            )

            total = amount + tax

            text = (
                f"GST: ₹{tax:.2f}\n"
                f"Final Amount: ₹{total:.2f}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "GST",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

    # ==================================================
    # DISCOUNT
    # ==================================================

    def finance_discount(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "Discount"
        )

        price = self.labeled_entry(
            frame,
            "Original Price"
        )

        discount = self.labeled_entry(
            frame,
            "Discount (%)"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate Discount",
            lambda:
            self.calc_discount(
                price,
                discount,
                result
            ),
            accent=True
        ).pack()

    def calc_discount(
        self,
        price,
        discount,
        result
    ):

        try:

            price = float(
                price.get()
            )

            discount = float(
                discount.get()
            )

            saving = (
                price *
                discount /
                100
            )

            final_price = (
                price -
                saving
            )

            text = (
                f"Saving: ₹{saving:.2f}\n"
                f"Final Price: ₹{final_price:.2f}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "Discount",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

    # ==================================================
    # PROFIT / LOSS
    # ==================================================

    def finance_profit_loss(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "Profit / Loss"
        )

        cp = self.labeled_entry(
            frame,
            "Cost Price"
        )

        sp = self.labeled_entry(
            frame,
            "Selling Price"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate",
            lambda:
            self.calc_profit_loss(
                cp,
                sp,
                result
            ),
            accent=True
        ).pack()

    def calc_profit_loss(
        self,
        cp,
        sp,
        result
    ):

        try:

            cost = float(
                cp.get()
            )

            selling = float(
                sp.get()
            )

            if cost <= 0:

                raise ValueError

            difference = (
                selling -
                cost
            )

            if difference > 0:

                percentage = (
                    difference /
                    cost *
                    100
                )

                text = (
                    f"PROFIT: ₹{difference:.2f}\n"
                    f"Profit %: {percentage:.2f}%"
                )

            elif difference < 0:

                loss = abs(
                    difference
                )

                percentage = (
                    loss /
                    cost *
                    100
                )

                text = (
                    f"LOSS: ₹{loss:.2f}\n"
                    f"Loss %: {percentage:.2f}%"
                )

            else:

                text = (
                    "NO PROFIT / NO LOSS"
                )

            result.config(
                text=text
            )

            self.add_history(
                "Profit/Loss",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

    # ==================================================
    # FD
    # ==================================================

    def finance_fd(
        self,
        notebook
    ):

        frame = self.finance_tab(
            notebook,
            "FD"
        )

        p = self.labeled_entry(
            frame,
            "Principal"
        )

        r = self.labeled_entry(
            frame,
            "Annual Rate (%)"
        )

        t = self.labeled_entry(
            frame,
            "Time (Years)"
        )

        result = self.result_label(
            frame
        )

        self.make_button(
            frame,
            "Calculate FD",
            lambda:
            self.calc_fd(
                p,
                r,
                t,
                result
            ),
            accent=True
        ).pack()

    def calc_fd(
        self,
        p,
        r,
        t,
        result
    ):

        try:

            P = float(
                p.get()
            )

            R = float(
                r.get()
            ) / 100

            T = float(
                t.get()
            )

            amount = (
                P *
                (1 + R) ** T
            )

            interest = (
                amount - P
            )

            text = (
                f"Interest: ₹{interest:.2f}\n"
                f"Maturity Amount: ₹{amount:.2f}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "FD",
                text.replace(
                    "\n",
                    " | "
                )
            )

        except:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

    # ==================================================
    # CONVERTER
    # ==================================================

    def converter_mode(self):

        self.current_mode = "Converter"

        self.clear_content()

        frame = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        self.create_label(
            frame,
            "Conversion Category"
        )

        category = ttk.Combobox(
            frame,
            values=[
                "Length",
                "Weight",
                "Temperature",
                "Area",
                "Volume",
                "Speed",
                "Time",
                "Data"
            ],
            state="readonly",
            font=("Segoe UI", 12)
        )

        category.pack(
            fill="x",
            padx=12,
            pady=5
        )

        category.set(
            "Length"
        )

        self.create_label(
            frame,
            "From"
        )

        from_unit = ttk.Combobox(
            frame,
            state="readonly",
            font=("Segoe UI", 12)
        )

        from_unit.pack(
            fill="x",
            padx=12,
            pady=5
        )

        self.create_label(
            frame,
            "To"
        )

        to_unit = ttk.Combobox(
            frame,
            state="readonly",
            font=("Segoe UI", 12)
        )

        to_unit.pack(
            fill="x",
            padx=12,
            pady=5
        )

        self.create_label(
            frame,
            "Value"
        )

        value = self.create_entry(
            frame
        )

        result = self.result_label(
            frame
        )

        units = {

            "Length": [
                "mm",
                "cm",
                "m",
                "km",
                "inch",
                "ft"
            ],

            "Weight": [
                "mg",
                "g",
                "kg",
                "lb"
            ],

            "Temperature": [
                "C",
                "F",
                "K"
            ],

            "Area": [
                "sqm",
                "sqft",
                "acre"
            ],

            "Volume": [
                "ml",
                "liter",
                "cubic_meter"
            ],

            "Speed": [
                "m/s",
                "km/h",
                "mph"
            ],

            "Time": [
                "seconds",
                "minutes",
                "hours",
                "days"
            ],

            "Data": [
                "B",
                "KB",
                "MB",
                "GB",
                "TB"
            ]

        }

        def update_units(event=None):

            selected = category.get()

            from_unit["values"] = units[
                selected
            ]

            to_unit["values"] = units[
                selected
            ]

            from_unit.set(
                units[selected][0]
            )

            to_unit.set(
                units[selected][1]
            )

        category.bind(
            "<<ComboboxSelected>>",
            update_units
        )

        update_units()

        self.make_button(
            frame,
            "Convert",
            lambda:
            self.convert_units(
                category.get(),
                from_unit.get(),
                to_unit.get(),
                value.get(),
                result
            ),
            accent=True
        ).pack(
            pady=15
        )

    def convert_units(
        self,
        category,
        from_unit,
        to_unit,
        value,
        result
    ):

        try:

            value = float(
                value
            )

            if category == "Temperature":

                if from_unit == "C":

                    celsius = value

                elif from_unit == "F":

                    celsius = (
                        value - 32
                    ) * 5 / 9

                else:

                    celsius = (
                        value - 273.15
                    )

                if to_unit == "C":

                    answer = celsius

                elif to_unit == "F":

                    answer = (
                        celsius *
                        9 / 5 +
                        32
                    )

                else:

                    answer = (
                        celsius +
                        273.15
                    )

            else:

                factors = {

                    "Length": {
                        "mm": 0.001,
                        "cm": 0.01,
                        "m": 1,
                        "km": 1000,
                        "inch": 0.0254,
                        "ft": 0.3048
                    },

                    "Weight": {
                        "mg": 0.000001,
                        "g": 0.001,
                        "kg": 1,
                        "lb": 0.453592
                    },

                    "Area": {
                        "sqm": 1,
                        "sqft": 0.092903,
                        "acre": 4046.856
                    },

                    "Volume": {
                        "ml": 0.001,
                        "liter": 1,
                        "cubic_meter": 1000
                    },

                    "Speed": {
                        "m/s": 1,
                        "km/h": 0.2777777778,
                        "mph": 0.44704
                    },

                    "Time": {
                        "seconds": 1,
                        "minutes": 60,
                        "hours": 3600,
                        "days": 86400
                    },

                    "Data": {
                        "B": 1,
                        "KB": 1024,
                        "MB": 1024 ** 2,
                        "GB": 1024 ** 3,
                        "TB": 1024 ** 4
                    }

                }

                base = (
                    value *
                    factors[category][from_unit]
                )

                answer = (
                    base /
                    factors[category][to_unit]
                )

            text = (
                f"{value} {from_unit} = "
                f"{self.format_result(answer)} "
                f"{to_unit}"
            )

            result.config(
                text=text
            )

            self.add_history(
                "Conversion",
                text
            )

        except:

            messagebox.showerror(
                "Conversion Error",
                "Invalid conversion."
            )

    # ==================================================
    # PROGRAMMER MODE
    # ==================================================

    def programmer_mode(self):

        self.current_mode = "Programmer"

        self.clear_content()

        notebook = ttk.Notebook(
            self.content
        )

        notebook.pack(
            fill="both",
            expand=True
        )

        self.programmer_base_converter(
            notebook
        )

        self.programmer_bitwise(
            notebook
        )

    # ==================================================
    # BASE CONVERTER
    # ==================================================

    def programmer_base_converter(
        self,
        notebook
    ):

        frame = tk.Frame(
            notebook,
            bg=self.LIGHT
        )

        notebook.add(
            frame,
            text="Base Converter"
        )

        self.create_label(
            frame,
            "Decimal Number"
        )

        entry = self.create_entry(
            frame
        )

        result = self.result_label(
            frame,
            ""
        )

        def convert():

            try:

                n = int(
                    entry.get()
                )

                text = (
                    f"DEC : {n}\n"
                    f"BIN : {bin(n)}\n"
                    f"OCT : {oct(n)}\n"
                    f"HEX : {hex(n)}"
                )

                result.config(
                    text=text
                )

                self.add_history(
                    "Programmer",
                    text.replace(
                        "\n",
                        " | "
                    )
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Enter a valid integer."
                )

        self.make_button(
            frame,
            "Convert",
            convert,
            accent=True
        ).pack()

    # ==================================================
    # BITWISE
    # ==================================================

    def programmer_bitwise(
        self,
        notebook
    ):

        frame = tk.Frame(
            notebook,
            bg=self.LIGHT
        )

        notebook.add(
            frame,
            text="Bitwise"
        )

        self.create_label(
            frame,
            "Number A"
        )

        a = self.create_entry(
            frame
        )

        self.create_label(
            frame,
            "Number B"
        )

        b = self.create_entry(
            frame
        )

        self.create_label(
            frame,
            "Operation"
        )

        operation = ttk.Combobox(
            frame,
            values=[
                "AND",
                "OR",
                "XOR",
                "NAND",
                "NOR",
                "XNOR",
                "LEFT SHIFT",
                "RIGHT SHIFT"
            ],
            state="readonly",
            font=("Segoe UI", 12)
        )

        operation.pack(
            fill="x",
            padx=12,
            pady=5
        )

        operation.set(
            "AND"
        )

        result = self.result_label(
            frame
        )

        def calculate():

            try:

                x = int(
                    a.get()
                )

                y = int(
                    b.get()
                )

                op = operation.get()

                if op == "AND":

                    answer = x & y

                elif op == "OR":

                    answer = x | y

                elif op == "XOR":

                    answer = x ^ y

                elif op == "NAND":

                    answer = ~(x & y)

                elif op == "NOR":

                    answer = ~(x | y)

                elif op == "XNOR":

                    answer = ~(x ^ y)

                elif op == "LEFT SHIFT":

                    answer = x << y

                else:

                    answer = x >> y

                text = (
                    f"{op}: {answer}\n"
                    f"Binary: {bin(answer)}"
                )

                result.config(
                    text=text
                )

                self.add_history(
                    "Bitwise",
                    text.replace(
                        "\n",
                        " | "
                    )
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Invalid numbers or operation."
                )

        self.make_button(
            frame,
            "Calculate",
            calculate,
            accent=True
        ).pack()

    # ==================================================
    # STATISTICS
    # ==================================================

    def statistics_mode(self):

        self.current_mode = "Statistics"

        self.clear_content()

        frame = tk.Frame(
            self.content,
            bg=self.LIGHT
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        tk.Label(
            frame,
            text="Enter numbers separated by commas",
            font=("Segoe UI", 13, "bold"),
            bg=self.LIGHT,
            fg=self.DARK
        ).pack(
            pady=10
        )

        entry = self.create_entry(
            frame,
            60
        )

        result = tk.Label(
            frame,
            text="",
            justify="left",
            font=("Consolas", 13),
            bg=self.LIGHT,
            fg=self.DARK
        )

        result.pack(
            pady=20
        )

        def calculate():

            try:

                numbers = [

                    float(x.strip())

                    for x in
                    entry.get().split(",")

                    if x.strip()

                ]

                if not numbers:

                    raise ValueError

                count = len(
                    numbers
                )

                total = sum(
                    numbers
                )

                mean = statistics.mean(
                    numbers
                )

                median = statistics.median(
                    numbers
                )

                modes = statistics.multimode(
                    numbers
                )

                mode = (
                    ", ".join(
                        map(
                            str,
                            modes
                        )
                    )
                    if modes
                    else
                    "No mode"
                )

                variance = (

                    statistics.variance(
                        numbers
                    )

                    if count > 1

                    else 0

                )

                stdev = (

                    statistics.stdev(
                        numbers
                    )

                    if count > 1

                    else 0

                )

                text = (

                    f"Count              : {count}\n"

                    f"Sum                : {total:.4f}\n"

                    f"Mean               : {mean:.4f}\n"

                    f"Median             : {median:.4f}\n"

                    f"Mode               : {mode}\n"

                    f"Variance           : {variance:.4f}\n"

                    f"Std. Deviation     : {stdev:.4f}\n"

                    f"Minimum            : {min(numbers):.4f}\n"

                    f"Maximum            : {max(numbers):.4f}"

                )

                result.config(
                    text=text
                )

                self.add_history(
                    "Statistics",
                    text.replace(
                        "\n",
                        " | "
                    )
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Enter valid numbers separated by commas."
                )

        self.make_button(
            frame,
            "Calculate Statistics",
            calculate,
            accent=True
        ).pack()

    # ==================================================
    # DATE & TIME
    # ==================================================

    def date_time_mode(self):

        self.current_mode = "Date & Time"

        self.clear_content()

        notebook = ttk.Notebook(
            self.content
        )

        notebook.pack(
            fill="both",
            expand=True
        )

        self.age_calculator(
            notebook
        )

        self.date_difference(
            notebook
        )

        self.add_subtract_days(
            notebook
        )

    # ==================================================
    # AGE CALCULATOR
    # ==================================================

    def age_calculator(
        self,
        notebook
    ):

        frame = tk.Frame(
            notebook,
            bg=self.LIGHT
        )

        notebook.add(
            frame,
            text="Age Calculator"
        )

        self.create_label(
            frame,
            "Date of Birth (DD-MM-YYYY)"
        )

        dob = self.create_entry(
            frame
        )

        result = self.result_label(
            frame
        )

        def calculate():

            try:

                d, m, y = map(
                    int,
                    dob.get().split("-")
                )

                birth = date(
                    y,
                    m,
                    d
                )

                today = date.today()

                years = (
                    today.year -
                    birth.year
                )

                if (
                    today.month,
                    today.day
                ) < (
                    birth.month,
                    birth.day
                ):

                    years -= 1

                text = (
                    f"Age: {years} years"
                )

                result.config(
                    text=text
                )

                self.add_history(
                    "Age Calculator",
                    text
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Use DD-MM-YYYY format."
                )

        self.make_button(
            frame,
            "Calculate Age",
            calculate,
            accent=True
        ).pack()

    # ==================================================
    # DATE DIFFERENCE
    # ==================================================

    def date_difference(
        self,
        notebook
    ):

        frame = tk.Frame(
            notebook,
            bg=self.LIGHT
        )

        notebook.add(
            frame,
            text="Date Difference"
        )

        self.create_label(
            frame,
            "Start Date (DD-MM-YYYY)"
        )

        start = self.create_entry(
            frame
        )

        self.create_label(
            frame,
            "End Date (DD-MM-YYYY)"
        )

        end = self.create_entry(
            frame
        )

        result = self.result_label(
            frame
        )

        def calculate():

            try:

                d1, m1, y1 = map(
                    int,
                    start.get().split("-")
                )

                d2, m2, y2 = map(
                    int,
                    end.get().split("-")
                )

                date1 = date(
                    y1,
                    m1,
                    d1
                )

                date2 = date(
                    y2,
                    m2,
                    d2
                )

                days = abs(
                    (
                        date2 -
                        date1
                    ).days
                )

                text = (
                    f"Difference: {days} days"
                )

                result.config(
                    text=text
                )

                self.add_history(
                    "Date Difference",
                    text
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Invalid date."
                )

        self.make_button(
            frame,
            "Calculate",
            calculate,
            accent=True
        ).pack()

    # ==================================================
    # ADD / SUBTRACT DAYS
    # ==================================================

    def add_subtract_days(
        self,
        notebook
    ):

        frame = tk.Frame(
            notebook,
            bg=self.LIGHT
        )

        notebook.add(
            frame,
            text="Add / Subtract Days"
        )

        self.create_label(
            frame,
            "Date (DD-MM-YYYY)"
        )

        input_date = self.create_entry(
            frame
        )

        self.create_label(
            frame,
            "Days (+ to add / - to subtract)"
        )

        days = self.create_entry(
            frame
        )

        result = self.result_label(
            frame
        )

        def calculate():

            try:

                d, m, y = map(
                    int,
                    input_date.get().split("-")
                )

                original = date(
                    y,
                    m,
                    d
                )

                number = int(
                    days.get()
                )

                new_date = (
                    original +
                    timedelta(
                        days=number
                    )
                )

                text = (
                    "New Date: " +
                    new_date.strftime(
                        "%d-%m-%Y"
                    )
                )

                result.config(
                    text=text
                )

                self.add_history(
                    "Date Calculation",
                    text
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Invalid input."
                )

        self.make_button(
            frame,
            "Calculate",
            calculate,
            accent=True
        ).pack()

    # ==================================================
    # HISTORY WINDOW
    # ==================================================

    def show_history(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "ProCalc - Calculation History"
        )

        window.geometry(
            "600x430"
        )

        window.configure(
            bg=self.LIGHT
        )

        tk.Label(
            window,
            text="Calculation History",
            font=("Segoe UI", 18, "bold"),
            bg=self.LIGHT,
            fg=self.DARK
        ).pack(
            pady=15
        )

        text_frame = tk.Frame(
            window,
            bg=self.LIGHT
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        scrollbar = tk.Scrollbar(
            text_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        history_box = tk.Text(
            text_frame,
            font=("Consolas", 11),
            bg=self.LIGHT,
            fg=self.DARK,
            insertbackground=self.DARK,
            relief="solid",
            bd=1,
            yscrollcommand=scrollbar.set
        )

        history_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar.config(
            command=history_box.yview
        )

        if self.history:

            for i, item in enumerate(
                self.history,
                1
            ):

                history_box.insert(
                    "end",
                    f"{i}. {item}\n\n"
                )

        else:

            history_box.insert(
                "end",
                "No calculations yet."
            )

        history_box.config(
            state="disabled"
        )

        bottom = tk.Frame(
            window,
            bg=self.LIGHT
        )

        bottom.pack(
            fill="x",
            padx=20,
            pady=10
        )

        def clear_history():

            self.history.clear()

            history_box.config(
                state="normal"
            )

            history_box.delete(
                "1.0",
                "end"
            )

            history_box.insert(
                "end",
                "No calculations yet."
            )

            history_box.config(
                state="disabled"
            )

        self.make_button(
            bottom,
            "Clear History",
            clear_history,
            accent=True
        ).pack(
            side="left"
        )

        self.make_button(
            bottom,
            "Close",
            window.destroy,
            accent=False
        ).pack(
            side="right"
        )

    # ==================================================
    # SETTINGS
    # ==================================================

    def show_settings(self):

        messagebox.showinfo(
            "ProCalc Settings",

            "PROCALC\n\n"

            "7 Calculator Modes\n"

            "Scientific Functions\n"

            "Finance Tools\n"

            "Unit Converter\n"

            "Programmer Tools\n"

            "Statistics\n"

            "Date & Time\n"

            "Memory System\n"

            "Calculation History\n"

            "Keyboard Support"
        )

    # ==================================================
    # KEYBOARD SUPPORT
    # ==================================================

    def keyboard_input(
        self,
        event
    ):

        if self.current_mode != "Standard":

            return

        if event.char in "0123456789.+-*/%()":

            char = {
                "*": "×",
                "/": "÷",
                "-": "−"
            }.get(
                event.char,
                event.char
            )

            self.standard_expression.set(
                self.standard_expression.get()
                + char
            )

        elif event.keysym == "Return":

            self.standard_click(
                "="
            )

        elif event.keysym == "BackSpace":

            self.standard_click(
                "⌫"
            )

        elif event.keysym == "Escape":

            self.standard_click(
                "C"
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = ProCalc(
        root
    )

    root.mainloop()