import customtkinter as ctk
import math
import numpy as np
import matplotlib.pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("420x650")
        self.root.resizable(False, False)

        self.expression = ""
        self.history = []
        self.memory = 0
        self.mode = "DEG"

        self.create_ui()
        self.root.bind("<Key>", self.key_input)

    # ---------------- UI ----------------
    def create_ui(self):
        self.display = ctk.CTkEntry(
            self.root, height=60, font=("Arial", 24), justify="right"
        )
        self.display.pack(fill="x", padx=10, pady=10)

        self.mode_btn = ctk.CTkButton(self.root, text="DEG", command=self.toggle_mode)
        self.mode_btn.pack(pady=5)

        frame = ctk.CTkFrame(self.root)
        frame.pack()

        buttons = [
            ["sin", "cos", "tan", "log"],
            ["ln", "√", "^", "!"],
            ["(", ")", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "C"],
            ["CE", "M+", "MR", "MC"],
            ["GRAPH", "HIST", "", ""]
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == "":
                    continue
                btn = ctk.CTkButton(
                    frame, text=text, width=80, height=50,
                    command=lambda t=text: self.on_click(t)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)

    # ---------------- BUTTON LOGIC ----------------
    def on_click(self, char):
        if char == "=":
            self.calculate()
        elif char == "C":
            self.expression = ""
        elif char == "CE":
            self.expression = self.expression[:-1]
        elif char == "M+":
            self.memory += self.safe_eval(self.expression)
        elif char == "MR":
            self.expression += str(self.memory)
        elif char == "MC":
            self.memory = 0
        elif char == "GRAPH":
            self.plot_graph()
        elif char == "HIST":
            self.show_history()
        elif char == "√":
            self.expression += "math.sqrt("
        elif char == "^":
            self.expression += "**"
        elif char == "!":
            self.expression += "math.factorial("
        elif char == "ln":
            self.expression += "math.log("
        elif char == "log":
            self.expression += "math.log10("
        elif char in ["sin", "cos", "tan"]:
            self.expression += f"{char}("
        else:
            self.expression += char

        self.update_display()

    # ---------------- DISPLAY ----------------
    def update_display(self):
        self.display.delete(0, "end")
        self.display.insert(0, self.expression)

    # ---------------- CALCULATION ----------------
    def calculate(self):
        try:
            result = self.safe_eval(self.expression)
            self.history.append(f"{self.expression} = {result}")
            self.expression = str(result)
        except:
            self.expression = "Error"
        self.update_display()

    # ---------------- SAFE EVAL ----------------
    def safe_eval(self, expr):
        def sin(x): return math.sin(math.radians(x)) if self.mode == "DEG" else math.sin(x)
        def cos(x): return math.cos(math.radians(x)) if self.mode == "DEG" else math.cos(x)
        def tan(x): return math.tan(math.radians(x)) if self.mode == "DEG" else math.tan(x)

        allowed = {
            "math": math,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "np": np
        }

        return eval(expr, {"__builtins__": None}, allowed)

    # ---------------- MODE ----------------
    def toggle_mode(self):
        self.mode = "RAD" if self.mode == "DEG" else "DEG"
        self.mode_btn.configure(text=self.mode)

    # ---------------- GRAPH ----------------
    def plot_graph(self):
        try:
            x = np.linspace(-10, 10, 100)
            expr = self.expression.replace("^", "**")
            y = eval(expr, {"x": x, "np": np, "math": math})
            plt.plot(x, y)
            plt.title(f"y = {self.expression}")
            plt.grid()
            plt.show()
        except:
            self.expression = "Graph Error"
            self.update_display()

    # ---------------- HISTORY ----------------
    def show_history(self):
        win = ctk.CTkToplevel(self.root)
        win.title("History")
        win.geometry("300x400")

        box = ctk.CTkTextbox(win)
        box.pack(fill="both", expand=True)

        for item in self.history:
            box.insert("end", item + "\n")

    # ---------------- KEYBOARD SUPPORT ----------------
    def key_input(self, event):
        key = event.keysym

        if key in "0123456789":
            self.expression += key
        elif key in ["plus", "minus", "asterisk", "slash"]:
            self.expression += {
                "plus": "+", "minus": "-", "asterisk": "*", "slash": "/"
            }[key]
        elif key == "Return":
            self.calculate()
            return
        elif key == "BackSpace":
            self.expression = self.expression[:-1]
        elif key == "Escape":
            self.expression = ""
        elif key == "period":
            self.expression += "."
        elif key == "parenleft":
            self.expression += "("
        elif key == "parenright":
            self.expression += ")"

        self.update_display()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = ctk.CTk()
    app = ScientificCalculator(root)
    root.mainloop()
    
    