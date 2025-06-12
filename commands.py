# commands.py - Command processor for handling player actions
import random

class CommandProcessor:
    def __init__(self, game):
        self.game = game
        self.commands = {
            "study": self.study,
            "rest": self.rest,
            "eat": self.eat,
            "call": self.call,
            "meet": self.meet,
            "exercise": self.exercise,
            "sleep": self.sleep,
            "status": self.status,
            "time": self.check_time,
            "help": self.help,
            "quit": self.quit
        }

    def process(self, command_text):
        """Process a command string from the player"""
        parts = command_text.strip().lower().split()
        if not parts:
            return "Please enter a command. Type 'help' for options."

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if command in self.commands:
            return self.commands[command](args)
        else:
            return f"Unknown command: '{command}'. Type 'help' for available commands."

    def study(self, args):
        """Study command: increases academic readiness at cost of energy and mental health"""
        if not args:
            return "Please specify a subject to study. Example: 'study math'"

        # Join all arguments to handle multi-word subjects
        subject = " ".join(args)
        player = self.game.player

        # Apply the effects
        results = {
            "academic_readiness": 15,
            "mental_health": -10,
            "energy": -10
        }

        # Check for special effect (20% chance of breakthrough)
        if random.random() < 0.2:
            results["academic_readiness"] += 5
            special_effect = "Breakthrough! You had a moment of clarity that boosted your understanding."
        else:
            special_effect = None

        # Apply all stat changes
        for stat, value in results.items():
            player.update_stat(stat, value)

        # Use up time
        self.game.use_time(1)

        # Log the action
        player.log_action("study", {
            "subject": subject,
            "results": results,
            "special_effect": special_effect
        })

        response = f"You spend time studying {subject}. "
        response += f"Academic Readiness +{results['academic_readiness']}, "
        response += f"Mental Health {results['mental_health']}, "
        response += f"Energy {results['energy']}."

        if special_effect:
            response += f"\n{special_effect}"

        return response

    def rest(self, args):
        """Rest command: increases energy and mental health"""
        player = self.game.player

        # Apply the effects
        results = {
            "energy": 15,
            "mental_health": 5
        }

        # Check for special effect (10% chance of rejuvenation)
        if random.random() < 0.1:
            special_effect = "Rejuvenation! You feel completely refreshed."
            # Add recovery flag for Phoenix ending
            results["recovery"] = True
        else:
            special_effect = None

        # Apply all stat changes
        for stat, value in results.items():
            if stat != "recovery":  # Skip non-stat keys
                player.update_stat(stat, value)

        # Use up time
        self.game.use_time(1)

        # Log the action
        player.log_action("rest", {
            "results": results,
            "special_effect": special_effect
        })

        response = "You take some time to rest and recharge. "
        response += f"Energy +{results['energy']}, "
        response += f"Mental Health +{results['mental_health']}."

        if special_effect:
            response += f"\n{special_effect}"

        return response

    def eat(self, args):
        """Eat command: increases energy and mental health"""
        player = self.game.player

        results = {
            "energy": 10,
            "mental_health": 5
        }

        for stat, value in results.items():
            player.update_stat(stat, value)

        self.game.use_time(1)
        player.log_action("eat", {"results": results})

        return f"You take time to eat a meal. Energy +{results['energy']}, Mental Health +{results['mental_health']}."

    def call(self, args):
        """Call a friend: increases social connections and mental health, decreases energy"""
        if not args:
            return "Please specify who to call. Example: 'call alex'"

        # Properly capitalize friend name
        friend = args[0].capitalize()
        player = self.game.player

        results = {
            "social_connections": 15,
            "mental_health": 5,
            "energy": -5
        }

        # Check for special effect (friend offers help)
        if random.random() < 0.3:
            results["academic_readiness"] = 5
            special_effect = f"{friend} shares some helpful study tips!"
        else:
            special_effect = None

        for stat, value in results.items():
            player.update_stat(stat, value)

        self.game.use_time(1)
        player.log_action("call", {
            "friend": friend,
            "results": results,
            "special_effect": special_effect
        })

        response = f"You call {friend} and chat for a while. "
        response += f"Social Connections +{results['social_connections']}, "
        response += f"Mental Health +{results['mental_health']}, "
        response += f"Energy {results['energy']}."

        if special_effect:
            response += f"\n{special_effect}"
            if "academic_readiness" in results:
                response += f" Academic Readiness +{results['academic_readiness']}."

        return response

    def meet(self, args):
        """Meet a friend: significantly increases social connections and mental health, decreases energy"""
        if not args:
            return "Please specify who to meet. Example: 'meet alex'"

        # Properly capitalize friend name
        friend = args[0].capitalize()
        player = self.game.player

        results = {
            "social_connections": 20,
            "mental_health": 10,
            "energy": -10
        }

        for stat, value in results.items():
            player.update_stat(stat, value)

        self.game.use_time(2)
        player.log_action("meet", {
            "friend": friend,
            "results": results
        })

        return f"You meet up with {friend}. Social Connections +{results['social_connections']}, Mental Health +{results['mental_health']}, Energy {results['energy']}."

    def exercise(self, args):
        """Exercise: increases energy and mental health, slightly decreases academic readiness"""
        player = self.game.player

        results = {
            "energy": 10,
            "mental_health": 5,
            "academic_readiness": -5
        }

        for stat, value in results.items():
            player.update_stat(stat, value)

        self.game.use_time(1)
        player.log_action("exercise", {"results": results})

        return f"You take time to exercise. Energy +{results['energy']}, Mental Health +{results['mental_health']}, Academic Readiness {results['academic_readiness']}."

    def sleep(self, args):
        """Sleep: ends the current day period, significantly increases energy and mental health"""
        player = self.game.player

        results = {
            "energy": 30,
            "mental_health": 15
        }

        for stat, value in results.items():
            player.update_stat(stat, value)

        self.game.end_day()
        player.log_action("sleep", {"results": results})

        return "You get some sleep. Energy +30, Mental Health +15.\n\nA new day begins."

    def status(self, args):
        """Check player stats"""
        stats = self.game.player.get_all_stats()

        response = "CURRENT STATS:\n"
        for stat, value in stats.items():
            stat_name = stat.replace("_", " ").title()
            response += f"- {stat_name}: {value}/100\n"

        return response

    def check_time(self, args):
        """Check current game time"""
        return self.game.get_time_string()

    def help(self, args):
        """Display available commands"""
        response = "Available commands:\n"
        response += "- study [subject]  (Uses 1 action, +15 Academic, -10 Mental, -10 Energy)\n"
        response += "- rest            (Uses 1 action, +15 Energy, +5 Mental)\n"
        response += "- eat             (Uses 1 action, +10 Energy, +5 Mental)\n"
        response += "- call [friend]   (Uses 1 action, +15 Social, +5 Mental, -5 Energy)\n"
        response += "- meet [friend]   (Uses 2 actions, +20 Social, +10 Mental, -10 Energy)\n"
        response += "- exercise        (Uses 1 action, +10 Energy, +5 Mental, -5 Academic)\n"
        response += "- sleep           (Ends current day period, +30 Energy, +15 Mental)\n"
        response += "- status          (Check your current stats)\n"
        response += "- time            (Check current time)\n"
        response += "- quit            (Exit the game)\n"

        return response

    def quit(self, args):
        """Exit the game"""
        self.game.game_over = True
        return "Thanks for playing Exam Hunters: Survive the Semester!"