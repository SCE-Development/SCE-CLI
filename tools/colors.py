class Colors:
    """
    This is a class that helps with printing out colors to the terminal.
    """
    PINK = '\033[95m'
    PURPLE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    CLEAR = '\x1b[2J\x1b[H'

    def clear_screen(self):
        print(self.CLEAR, end="")

    def reset_color(self):
        print(self.ENDC, end="")

    def print_color(self, color_type, string, is_input=False):
        """
        This is a factory method that will print text of a certain color.
            Parameters:
            color_type (string): One of the enums above or user supplied to
                                 print a certain color.
            string (string):     The string that the user wants to print out.
            is_input (bool):     Decides whether we print the string with a newline
                                 or not. Helpful for when we want the user to
                                 input a value on the same line of what we are
                                 printing.
        """
        print(color_type, end="")
        if is_input:
            input(string)
        else:
            print(string)

        self.reset_color()

    def print_pink(self, string, is_input=False):
        self.print_color(self.PINK, string, is_input)

    def print_purple(self, string, is_input=False):
        self.print_color(self.PURPLE, string, is_input)

    def print_green(self, string, is_input=False):
        self.print_color(self.GREEN, string, is_input)

    def print_yellow(self, string, is_input=False):
        self.print_color(self.YELLOW, string, is_input)

    def print_red(self, string, is_input=False):
        self.print_color(self.RED, string, is_input)
