import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 10
        self.difficulty = "Medium"
        self.game_active = False
        
        # Colors
        self.bg_color = "#2c3e50"
        self.btn_color = "#3498db"
        self.text_color = "#ecf0f1"
        self.win_color = "#2ecc71"
        self.lose_color = "#e74c3c"
        self.hint_color = "#f39c12"
        
        self.root.configure(bg=self.bg_color)
        self.create_widgets()
        self.start_new_game()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🎯 Number Guessing Game",
            font=("Arial", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=20)
        
        # Difficulty frame
        diff_frame = tk.Frame(self.root, bg=self.bg_color)
        diff_frame.pack(pady=10)
        
        tk.Label(
            diff_frame,
            text="Select Difficulty:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.diff_var = tk.StringVar(value="Medium")
        diff_menu = tk.OptionMenu(
            diff_frame,
            self.diff_var,
            "Easy", "Medium", "Hard",
            command=self.change_difficulty
        )
        diff_menu.config(
            font=("Arial", 10),
            bg=self.btn_color,
            fg="white",
            width=10
        )
        diff_menu.pack(side=tk.LEFT, padx=10)
        
        # Game info display
        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=400,
            justify="center"
        )
        self.info_label.pack(pady=15)
        
        # Guess entry frame
        entry_frame = tk.Frame(self.root, bg=self.bg_color)
        entry_frame.pack(pady=15)
        
        tk.Label(
            entry_frame,
            text="Your Guess:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.guess_entry = tk.Entry(
            entry_frame,
            font=("Arial", 14, "bold"),
            width=15,
            justify="center"
        )
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.bind("<Return>", self.check_guess)
        
        # Guess button
        self.guess_btn = tk.Button(
            self.root,
            text="🚀 Make Guess",
            font=("Arial", 12, "bold"),
            bg=self.btn_color,
            fg="white",
            command=self.check_guess,
            width=15,
            height=1
        )
        self.guess_btn.pack(pady=10)
        
        # Result display
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            wraplength=400,
            justify="center",
            height=3
        )
        self.result_label.pack(pady=10)
        
        # Attempts counter
        self.counter_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.counter_label.pack(pady=5)
        
        # Progress bar frame
        self.progress_frame = tk.Frame(self.root, bg=self.bg_color)
        self.progress_frame.pack(pady=10)
        
        self.progress_canvas = tk.Canvas(
            self.progress_frame,
            width=300,
            height=20,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.progress_canvas.pack()
        
        # Control buttons frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # New game button
        new_game_btn = tk.Button(
            button_frame,
            text="🔄 New Game",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white",
            command=self.start_new_game,
            width=12
        )
        new_game_btn.grid(row=0, column=0, padx=5)
        
        # Hint button
        self.hint_btn = tk.Button(
            button_frame,
            text="💡 Hint",
            font=("Arial", 11),
            bg=self.hint_color,
            fg="white",
            command=self.give_hint,
            width=12,
            state=tk.DISABLED
        )
        self.hint_btn.grid(row=0, column=1, padx=5)
        
        # Quit button
        quit_btn = tk.Button(
            button_frame,
            text="❌ Quit",
            font=("Arial", 11),
            bg=self.lose_color,
            fg="white",
            command=self.root.quit,
            width=12
        )
        quit_btn.grid(row=0, column=2, padx=5)
    
    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.start_new_game()
    
    def start_new_game(self):
        # Set game parameters based on difficulty
        if self.difficulty == "Easy":
            self.secret_number = random.randint(1, 50)
            self.max_attempts = 15
            range_text = "1 to 50"
        elif self.difficulty == "Medium":
            self.secret_number = random.randint(1, 100)
            self.max_attempts = 10
            range_text = "1 to 100"
        else:  # Hard
            self.secret_number = random.randint(1, 200)
            self.max_attempts = 5
            range_text = "1 to 200"
        
        self.attempts = 0
        self.game_active = True
        
        # Update UI
        self.info_label.config(
            text=f"I'm thinking of a number between {range_text}.\nCan you guess it?",
            fg=self.text_color
        )
        self.result_label.config(text="")
        self.update_counter()
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_btn.config(state=tk.NORMAL, text="🚀 Make Guess")
        self.hint_btn.config(state=tk.DISABLED)
        self.update_progress_bar()
        self.guess_entry.focus()
    
    def update_counter(self):
        self.counter_label.config(
            text=f"Attempts: {self.attempts}/{self.max_attempts} | Difficulty: {self.difficulty}"
        )
    
    def update_progress_bar(self):
        self.progress_canvas.delete("all")
        
        # Calculate progress
        if self.max_attempts > 0:
            progress = (self.attempts / self.max_attempts) * 300
        else:
            progress = 0
        
        # Draw background
        self.progress_canvas.create_rectangle(
            0, 0, 300, 20,
            fill="#34495e",
            outline=""
        )
        
        # Draw progress (color changes based on attempts left)
        if self.attempts < self.max_attempts * 0.5:
            fill_color = self.win_color
        elif self.attempts < self.max_attempts * 0.8:
            fill_color = self.hint_color
        else:
            fill_color = self.lose_color
        
        self.progress_canvas.create_rectangle(
            0, 0, progress, 20,
            fill=fill_color,
            outline=""
        )
        
        # Draw border
        self.progress_canvas.create_rectangle(
            0, 0, 300, 20,
            outline=self.text_color,
            width=1
        )
    
    def check_guess(self, event=None):
        if not self.game_active:
            return
        
        guess_text = self.guess_entry.get()
        
        # Validate input
        if not guess_text.isdigit():
            self.result_label.config(
                text="❌ Please enter a valid number!",
                fg=self.lose_color
            )
            self.guess_entry.delete(0, tk.END)
            return
        
        guess = int(guess_text)
        
        # Validate range
        if self.difficulty == "Easy" and (guess < 1 or guess > 50):
            self.result_label.config(
                text="❌ Please enter a number between 1 and 50!",
                fg=self.lose_color
            )
            self.guess_entry.delete(0, tk.END)
            return
        elif self.difficulty == "Medium" and (guess < 1 or guess > 100):
            self.result_label.config(
                text="❌ Please enter a number between 1 and 100!",
                fg=self.lose_color
            )
            self.guess_entry.delete(0, tk.END)
            return
        elif self.difficulty == "Hard" and (guess < 1 or guess > 200):
            self.result_label.config(
                text="❌ Please enter a number between 1 and 200!",
                fg=self.lose_color
            )
            self.guess_entry.delete(0, tk.END)
            return
        
        self.attempts += 1
        self.hint_btn.config(state=tk.NORMAL)
        
        # Check guess
        if guess < self.secret_number:
            self.result_label.config(
                text=f"📉 Too low! Try a higher number.",
                fg=self.hint_color
            )
            self.guess_entry.delete(0, tk.END)
            
        elif guess > self.secret_number:
            self.result_label.config(
                text=f"📈 Too high! Try a lower number.",
                fg=self.hint_color
            )
            self.guess_entry.delete(0, tk.END)
            
        else:  # Correct guess
            self.result_label.config(
                text=f"🎉 CONGRATULATIONS!\nYou found the number in {self.attempts} attempts!",
                fg=self.win_color
            )
            self.game_active = False
            self.guess_entry.config(state=tk.DISABLED)
            self.guess_btn.config(state=tk.DISABLED)
            self.hint_btn.config(state=tk.DISABLED)
            messagebox.showinfo(
                "You Win!",
                f"Excellent! You guessed the number {self.secret_number} in {self.attempts} attempts!"
            )
            self.update_counter()
            self.update_progress_bar()
            return
        
        # Update UI
        self.update_counter()
        self.update_progress_bar()
        
        # Check if game over
        if self.attempts >= self.max_attempts:
            self.result_label.config(
                text=f"💀 GAME OVER!\nThe number was {self.secret_number}",
                fg=self.lose_color
            )
            self.game_active = False
            self.guess_entry.config(state=tk.DISABLED)
            self.guess_btn.config(state=tk.DISABLED)
            self.hint_btn.config(state=tk.DISABLED)
            messagebox.showinfo(
                "Game Over",
                f"You've used all {self.max_attempts} attempts.\nThe number was {self.secret_number}."
            )
    
    def give_hint(self):
        if not self.game_active or self.attempts == 0:
            messagebox.showinfo("Hint", "Make at least one guess to get a hint!")
            return
        
        hints = [
            f"The number is {'even' if self.secret_number % 2 == 0 else 'odd'}.",
            f"The number is between {max(1, self.secret_number - 15)} and {self.secret_number + 15}.",
            f"The sum of its digits is {sum(int(d) for d in str(self.secret_number))}.",
            f"It's {'greater' if self.secret_number > 50 else 'less'} than 50." if self.difficulty != "Easy" else 
            f"It's {'greater' if self.secret_number > 25 else 'less'} than 25.",
            f"The number divided by 5 gives remainder {self.secret_number % 5}."
        ]
        
        # Show different hints based on attempts
        hint_index = min(self.attempts - 1, len(hints) - 1)
        messagebox.showinfo("💡 Hint", hints[hint_index])

def main():
    root = tk.Tk()
    game = NumberGuessingGame(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()