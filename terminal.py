# terminal.py - Terminal interface for text display
class Terminal:
    def __init__(self):
        self.width = 80

    def clear(self):
        """Clear the terminal screen"""
        print("\n" * 50)

    def print_header(self, text):
        """Print a header with decoration"""
        print("=" * self.width)
        print(text.center(self.width))
        print("=" * self.width)

    def print_divider(self):
        """Print a divider line"""
        print("-" * self.width)

    def print_stats(self, stats):
        """Print player stats in a formatted way"""
        self.print_divider()
        print("STATS:".center(self.width))

        for stat, value in stats.items():
            stat_name = stat.replace("_", " ").title()
            bar_length = int(value / 2)  # Scale to fit in terminal
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"{stat_name:20} [{bar}] {value}/100")

        self.print_divider()

    def print_event(self, event_text):
        """Print an event with formatting"""
        self.print_divider()
        print("EVENT:".center(self.width))
        print(event_text)
        self.print_divider()

    def get_input(self, prompt="What would you like to do?"):
        """Get input from the user with a prompt"""
        return input(f"{prompt}\n> ")
