import tkinter as tk
from tkinter import messagebox
import configparser
import random


# ... [previous functions, including roll_d100, get_hit_location, critical_hit, etc.]
def roll_d10():
   """Roll a ten-sided die and return the result."""
   return random.randint(1, 10)


def roll_d100():
   """Roll a percentile die (d100) and return the result."""
   return random.randint(1, 100)


def get_hit_location(roll):
   """Determine the hit location based on the roll."""
   reversed_roll = int(str(roll).zfill(2)[::-1])  # Reverse the roll digits.
  
   if 1 <= reversed_roll <= 15:
       return "Head"
   elif 16 <= reversed_roll <= 35:
       return "Right Arm"
   elif 36 <= reversed_roll <= 55:
       return "Left Arm"
   elif 56 <= reversed_roll <= 80:
       return "Body"
   else:
       return "Legs"
  
def critical_hit(target, hit_location):
   """Determine the effect of a critical hit."""
   roll = roll_d10()
   print(f"Critical hit on {target.name}'s {hit_location}! Rolled {roll} for severity.")


   if 1 <= roll <= 3:
       print("Minor Injury. No additional effect.")
   elif 4 <= roll <= 6:
       print("Major Injury. An additional wound inflicted.")
       target.wounds -= 1
   elif 7 <= roll <= 9:
       print("Severe Injury. Two additional wounds inflicted.")
       target.wounds -= 2
   else:
       print("Fatal Injury. The target is taken out!")
       target.wounds -= target.wounds + 10  # Ensure the target's wounds go below 0 significantly


class Character:
   def __init__(self, name, weapon_skill, wounds, strength):
       self.name = name
       self.weapon_skill = weapon_skill
       self.wounds = wounds
       self.strength = strength


   def attack(self, target):
       """Attempt to attack a target character."""
       roll = roll_d100()
       hit_location = get_hit_location(roll)
       print(f"{self.name} aimed for the {hit_location} and rolled {roll} (target WS: {self.weapon_skill}).")
      
       if roll <= self.weapon_skill:
           damage = self.strength
           target.wounds -= damage
           print(f"{self.name} hit {target.name}'s {hit_location} for {damage} damage! {target.name} now has {target.wounds} wounds.")
          
           if target.wounds <= 0:
               critical_hit(target, hit_location)
       else:
           print(f"{self.name} missed!")


   def is_alive(self):
       """Check if the character is alive."""
       return self.wounds > 0


class CombatApp:
   def __init__(self, root):
       self.root = root
       self.root.title("WFRP Combat Simulator")
      
       # Load character data from config
       config = configparser.ConfigParser()
       config.read('config.ini')


       player_attributes = config['Player']
       enemy_attributes = config['Enemy']


       self.player = Character("Player", int(player_attributes['weapon_skill']), int(player_attributes['wounds']), int(player_attributes['strength']))
       self.enemy = Character("Enemy", int(enemy_attributes['weapon_skill']), int(enemy_attributes['wounds']), int(enemy_attributes['strength']))
      
       # Player Labels and Data
       self.player_label = tk.Label(root, text="Player")
       self.player_label.grid(row=0, column=0, padx=10, pady=10)


       self.player_wounds = tk.Label(root, text=f"Wounds: {self.player.wounds}")
       self.player_wounds.grid(row=1, column=0, padx=10, pady=10)


       # Enemy Labels and Data
       self.enemy_label = tk.Label(root, text="Enemy")
       self.enemy_label.grid(row=0, column=1, padx=10, pady=10)


       self.enemy_wounds = tk.Label(root, text=f"Wounds: {self.enemy.wounds}")
       self.enemy_wounds.grid(row=1, column=1, padx=10, pady=10)


       # Action Button
       self.attack_button = tk.Button(root, text="Attack!", command=self.attack)
       self.attack_button.grid(row=2, column=0, columnspan=2, pady=20)


       # Log Textbox
       self.log_text = tk.Text(root, wrap=tk.WORD, height=10, width=50)
       self.log_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


   def log(self, message):
       """Add a message to the log textbox."""
       self.log_text.insert(tk.END, message + "\n")
       self.log_text.see(tk.END)


   def update_wounds(self):
       """Update the displayed wounds for both characters."""
       self.player_wounds.config(text=f"Wounds: {self.player.wounds}")
       self.enemy_wounds.config(text=f"Wounds: {self.enemy.wounds}")


   def attack(self):
       """Simulate a round of combat."""
       # Player attacks enemy
       roll = roll_d100()
       hit_location = get_hit_location(roll)
       if roll <= self.player.weapon_skill:
           damage = self.player.strength
           self.enemy.wounds -= damage
           self.log(f"{roll}, player hits Enemy's {hit_location} for {damage} damage!")
          
           if self.enemy.wounds <= 0:
               critical_hit(self.enemy, hit_location)
               self.log(f"Enemy suffered a critical hit to the {hit_location}!")
          
           self.update_wounds()


           if not self.enemy.is_alive():
               self.end_combat("Player wins!")
               return


       else:
           self.log(f"{roll}, player misses!")


       # Enemy attacks player
       roll = roll_d100()
       hit_location = get_hit_location(roll)
       if roll <= self.enemy.weapon_skill:
           damage = self.enemy.strength
           self.player.wounds -= damage
           self.log(f"Enemy hits Player's {hit_location} for {damage} damage!")


           if self.player.wounds <= 0:
               critical_hit(self.player, hit_location)
               self.log(f"Player suffered a critical hit to the {hit_location}!")
          
           self.update_wounds()


           if not self.player.is_alive():
               self.end_combat("Enemy wins!")
               return


       else:
           self.log("Enemy misses!")


   def end_combat(self, message):
       """End the combat and display a message."""
       self.attack_button.config(state=tk.DISABLED)
       messagebox.showinfo("Combat Ended", message)


if __name__ == "__main__":
   root = tk.Tk()
   app = CombatApp(root)
   root.mainloop()




