# game.py - Main game class for Exam Hunters
from player import Player
from commands import CommandProcessor
import random

class Game:
    def __init__(self):
        self.player = Player()
        self.commands = CommandProcessor(self)
        self.day = 1
        self.period = "Morning"  # "Morning" or "Day"
        self.actions_remaining = 3
        self.total_days = 3
        self.game_over = False
        self.events = self.get_default_events()

    def get_default_events(self):
        """Return default events for the game"""
        return {
            "day1": {
                "morning": [
                    {
                        "type": "introduction",
                        "text": "Welcome to your final exam week! You have 3 days until your exams begin."
                    }
                ],
                "day": [
                    {
                        "type": "challenge",
                        "text": "Your laptop crashes while working on an assignment!",
                        "options": [
                            "Take a deep breath and restart",
                            "Call tech-savvy friend",
                            "Panic and try random solutions"
                        ]
                    }
                ]
            },
            "day2": {
                "morning": [
                    {
                        "type": "news",
                        "text": "You receive an email: History exam has been moved up a day!"
                    }
                ],
                "day": [
                    {
                        "type": "social",
                        "text": "Your friend is having a crisis and needs support.",
                        "options": [
                            "Be there for them (Social ++, Academic --)",
                            "Offer brief support (Social +, Academic -)",
                            "Focus on studying (Academic +, Social --)"
                        ]
                    }
                ]
            },
            "day3": {
                "morning": [
                    {
                        "type": "final",
                        "text": "This is your last day to prepare for exams!"
                    }
                ],
                "day": [
                    {
                        "type": "reflection",
                        "text": "As the day ends, you reflect on your preparation for tomorrow's exams."
                    }
                ]
            }
        }

    def start(self):
        """Start the game"""
        welcome_text = """
===================================
EXAM HUNTERS: SURVIVE THE SEMESTER
===================================

"Even under pressure, every decision can bring you closer to the person you're meant to be."

Welcome to your final exam week! You have 3 days until your exams begin.
Your choices will determine not just your grades, but who you become.
"""
        print(welcome_text)

        # Show initial stats
        print(self.commands.process("status"))

        # Show current time
        print(self.commands.process("time"))

        # Show help
        print("\nType 'help' for a list of commands.\n")

        # Process day 1 morning event
        self.process_event("day1", "morning")

        # Main game loop
        self.game_loop()

    def game_loop(self):
        """Main game loop"""
        while not self.game_over:
            # Get player command
            command = input("> ").strip()

            # Process command
            result = self.commands.process(command)
            print(result)

            # Check if game should end
            if self.day > self.total_days:
                self.end_game()
                break

            # Check if we need to transition to next period or day
            if self.actions_remaining <= 0:
                if self.period == "Morning":
                    self.period = "Day"
                    self.actions_remaining = 3
                    print(f"\n--- DAY {self.day} DAY ---\n")
                    self.process_event(f"day{self.day}", "day")
                else:
                    # Auto-sleep at end of day
                    print("\nYou've used all your actions for the day. Time to sleep.")
                    print(self.commands.process("sleep"))

    def use_time(self, actions=1):
        """Use up player actions"""
        self.actions_remaining -= actions

    def end_day(self):
        """End the current day and start a new one"""
        self.day += 1
        self.period = "Morning"
        self.actions_remaining = 3

        if self.day <= self.total_days:
            print(f"\n--- DAY {self.day} MORNING ---\n")
            self.process_event(f"day{self.day}", "morning")

    def get_time_string(self):
        """Get a string representation of the current time"""
        return f"Day {self.day}, {self.period} ({self.actions_remaining} actions remaining)"

    def process_event(self, day_key, period_key):
        """Process an event for the current day and period"""
        try:
            events = self.events.get(day_key, {}).get(period_key, [])
            if events:
                for event in events:
                    print(f"\n{event['text']}\n")

                    if event.get("options"):
                        print("Options:")
                        for i, option in enumerate(event["options"], 1):
                            print(f"{i}. {option}")

                        # In a full implementation, we would handle player choice here
                        choice = input("\nEnter your choice (or press Enter to continue): ")
                        if choice.isdigit() and 1 <= int(choice) <= len(event["options"]):
                            option_index = int(choice) - 1
                            print(f"\nYou chose: {event['options'][option_index]}")

                            # Apply some basic effects based on choice
                            option_text = event["options"][option_index].lower()

                            if "academic ++" in option_text:
                                self.player.update_stat("academic_readiness", 10)
                                print("Academic Readiness +10")
                            elif "academic +" in option_text:
                                self.player.update_stat("academic_readiness", 5)
                                print("Academic Readiness +5")
                            elif "academic --" in option_text:
                                self.player.update_stat("academic_readiness", -10)
                                print("Academic Readiness -10")
                            elif "academic -" in option_text:
                                self.player.update_stat("academic_readiness", -5)
                                print("Academic Readiness -5")

                            if "social ++" in option_text:
                                self.player.update_stat("social_connections", 10)
                                print("Social Connections +10")
                            elif "social +" in option_text:
                                self.player.update_stat("social_connections", 5)
                                print("Social Connections +5")
                            elif "social --" in option_text:
                                self.player.update_stat("social_connections", -10)
                                print("Social Connections -10")
                            elif "social -" in option_text:
                                self.player.update_stat("social_connections", -5)
                                print("Social Connections -5")

        except Exception as e:
            print(f"Error processing event: {e}")

    def end_game(self):
        """End the game and show the player's ending"""
        self.game_over = True

        ending = self.player.check_ending()

        print("\n===================================")
        print("EXAM WEEK COMPLETE")
        print("===================================\n")

        print(f"Your journey has led you to the {ending} ending!\n")

        # Display ending text based on which ending was achieved
        endings = {
            "Pearl": """Like a pearl formed through pressure but maintaining its luster, you've emerged from exam week with a balanced approach to life. Your grades are solid, your relationships intact, and your wellbeing preserved. You've learned that success isn't just about academic achievement—it's about thriving as a whole person.""",

            "Eagle": """Like an eagle soaring above the clouds, you've reached academic heights that few can match. Your laser focus on studies has paid off with exceptional exam results. While your social connections and mental health took a backseat, you've proven your ability to achieve excellence through dedication and sacrifice.""",

            "Wolf": """Like a wolf who draws strength from the pack, you've prioritized your connections with others. Your exam results may not top the charts, but you've built a network of support that will last far beyond this semester. Your friends recognize you as someone who values people over perfection.""",

            "Turtle": """Like a turtle who knows when to retreat into its shell, you recognized the importance of self-preservation. You paced yourself, protected your wellbeing, and made it through exams without burning out. Your balanced approach may not have maximized every opportunity, but you've learned sustainable success strategies that will serve you for life.""",

            "Phoenix": """Like a phoenix rising from the ashes, you faced moments of near-collapse but found the strength to rebuild. Your journey through exam week wasn't smooth, but your resilience in the face of challenges revealed an inner strength you didn't know you had. This experience has transformed you.""",

            "Survivor": """You made it through exam week. It wasn't pretty, and it wasn't perfect, but you survived. Sometimes that's enough."""
        }

        print(endings.get(ending, "You completed your exams."))
        print("\nFinal Stats:")
        print(self.commands.process("status"))

        print("\nThank you for playing Exam Hunters: Survive the Semester!")