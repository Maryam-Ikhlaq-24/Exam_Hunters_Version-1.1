# player.py - Player class for managing stats and state
class Player:
    def __init__(self, name="Student"):
        self.name = name
        # Initialize player stats
        self.stats = {
            "mental_health": 70,
            "energy": 80,
            "social_connections": 60,
            "academic_readiness": 40
        }
        self.status_effects = []
        self.history = []  # Track player actions and events
        self.lowest_stats = {  # Track lowest values for Phoenix ending
            "mental_health": 70,
            "energy": 80,
            "social_connections": 60,
            "academic_readiness": 40
        }

    def update_stat(self, stat_name, value):
        """Update a player stat, ensuring it stays within 0-100 range"""
        if stat_name in self.stats:
            # Track lowest stat values for Phoenix ending
            if value < 0:
                self.lowest_stats[stat_name] = min(self.lowest_stats[stat_name], self.stats[stat_name] + value)

            # Update the stat with bounds checking
            self.stats[stat_name] = max(0, min(100, self.stats[stat_name] + value))
            return True
        return False

    def apply_status_effect(self, effect):
        """Apply a status effect to the player"""
        self.status_effects.append(effect)

    def remove_status_effect(self, effect_name):
        """Remove a status effect from the player"""
        self.status_effects = [e for e in self.status_effects if e["name"] != effect_name]

    def log_action(self, action, results):
        """Log an action and its results to player history"""
        self.history.append({
            "action": action,
            "results": results
        })

    def get_stat(self, stat_name):
        """Get the current value of a stat"""
        return self.stats.get(stat_name, 0)

    def get_all_stats(self):
        """Get all player stats"""
        return self.stats

    def check_ending(self):
        """Determine which ending the player has achieved based on stats"""
        stats = self.stats

        # Pearl: The Balanced Achiever
        if all(stat >= 60 for stat in stats.values()):
            return "Pearl"

        # Eagle: The High Flyer
        if stats["academic_readiness"] >= 85:
            return "Eagle"

        # Wolf: The Social Leader
        if stats["social_connections"] >= 85:
            return "Wolf"

        # Turtle: The Steady Survivor
        if stats["mental_health"] >= 75 and stats["energy"] >= 75:
            return "Turtle"

        # Phoenix: The Comeback Story
        # Check if any stat dropped below 30 but is now above 70
        for stat_name, current_value in stats.items():
            if self.lowest_stats[stat_name] <= 30 and current_value >= 70:
                return "Phoenix"

        # Also check for recovery flag in history
        if any("recovery" in action.get("results", {}) for action in self.history):
            return "Phoenix"

        # Default ending if no conditions are met
        return "Survivor"