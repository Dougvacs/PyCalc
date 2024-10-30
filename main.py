from typing import List
from enum import Enum
from textual.app import App, ComposeResult
from textual.widgets import Footer, Button, Static
from textual.containers import Vertical

class State(Enum):
    First = 0,
    Second = 1,
    Result = 2

class Operation(Enum):
    Unset = 0,
    Add = 1,
    Subtract = 2,
    Multiply = 3,
    Divide = 4

class DisplayArea(Static):
    lines: List[str] = []
    current_operation: Operation = Operation.Unset
    result: float = 0.0
    state: State = State.First
    def on_mount(self):
        for s in ["" for _ in range(4)]: self.lines.append(s)
    def new_line(self):
        self.lines.append("")
        self.lines.pop(0)
    def add_to_line(self, new_str: str):
        self.lines[-1] += new_str
        self.refresh_display()
    def refresh_display(self):
        screen_str = ""
        for (i, l) in enumerate(self.lines):
            screen_str += str(l)
            if i < len(self.lines):
                screen_str += "\n"
        self.update(screen_str)
    def clear_display(self):
        self.lines = []
        for s in ["" for _ in range(4)]: self.lines.append(s)
        self.refresh_display()
    def reset_calculator(self):
        self.result = 0.0
        self.state = State.First
        self.clear_display()
    def print_result(self):
        self.new_line()
        self.add_to_line(str(self.result))
        self.refresh_display()
    def next(self):
        match self.state:
            case State.First:
                self.state = State.Second
                self.result = int(self.lines[-1])
                self.new_line()
                match self.current_operation:
                    case Operation.Add: self.add_to_line("+")
                    case Operation.Subtract: self.add_to_line("-")
                    case Operation.Multiply: self.add_to_line("x")
                    case Operation.Divide: self.add_to_line("/")
                self.new_line()
            case State.Second:
                self.state = State.Result
                match self.current_operation:
                    case Operation.Add: self.result += int(self.lines[-1])
                    case Operation.Subtract: self.result -= int(self.lines[-1])
                    case Operation.Multiply: self.result *= int(self.lines[-1])
                    case Operation.Divide: self.result /= int(self.lines[-1])
                self.print_result()
            case State.Result:
                self.state = State.First
                self.clear_display()

class ButtonArea(Static):
    def compose(self) -> ComposeResult:
        yield Button("1", classes="calc_button blue", id="num1")
        yield Button("2", classes="calc_button blue", id="num2")
        yield Button("3", classes="calc_button blue", id="num3")
        yield Button("CLR", classes="calc_button orange", id="btn_clr")
        yield Button("4", classes="calc_button blue", id="num4")
        yield Button("5", classes="calc_button blue", id="num5")
        yield Button("6", classes="calc_button blue", id="num6")
        yield Button("+", classes="calc_button orange", id="btn_plus")
        yield Button("7", classes="calc_button blue", id="num7")
        yield Button("8", classes="calc_button blue", id="num8")
        yield Button("9", classes="calc_button blue", id="num9")
        yield Button("-", classes="calc_button orange", id="btn_minus")
        yield Button("0", classes="calc_button blue", id="num0")
        yield Button("x", classes="calc_button orange", id="btn_times")
        yield Button("/", classes="calc_button orange", id="btn_division")
        yield Button("=", classes="calc_button red", id="btn_equals")

class CalculatorApp(App):
    CSS_PATH = "pycalc.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode")
    ]
    display_area: DisplayArea
    def compose(self) -> ComposeResult:
        self.display_area = DisplayArea()
        yield Footer()
        yield Vertical(
            self.display_area,
            ButtonArea()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is not None:
            button_id = str(event.button.id)
            if "num" in button_id:
                number = int(button_id.replace("num", ""))
                self.display_area.add_to_line(str(number))
            if "btn" in button_id:
                match button_id:
                    case "btn_equals": pass
                    case "btn_plus":
                        self.display_area.current_operation = Operation.Add
                    case "btn_minus":
                        self.display_area.current_operation = Operation.Subtract
                    case "btn_times":
                        self.display_area.current_operation = Operation.Multiply
                    case "btn_division":
                        self.display_area.current_operation = Operation.Divide
                self.display_area.next()

def main():
    app = CalculatorApp()
    app.run()

if __name__ == "__main__":
    main()