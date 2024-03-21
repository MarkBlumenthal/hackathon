import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import psycopg2
import random



class FightAntiSemitisimGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Welcome to Fight Anti-Semitisim")

        self.conn = psycopg2.connect(dbname="Hackathon-1", user="postgres", password="arsenal_1", host="localhost")
        self.cur = self.conn.cursor()

        self.start_time = None
        self.end_time = None

        self.welcome_label = tk.Label(window, text="Welcome To Fight Anti-Semitisim!")
        self.welcome_label.pack()
        self.question_label = tk.Label(window, text="Lets Change people's views in this world?")
        self.question_label.pack()

        self.yes_button = tk.Button(window, text="Yes", command=self.start_game)
        self.yes_button.pack(side=tk.LEFT, padx=10)
        self.no_button = tk.Button(window, text="No", command=self.close_game)
        self.no_button.pack(side=tk.RIGHT, padx=10)

        self.demon_slayer_image = Image.open("images/fightantisemitisim.png").resize((300, 150))
        self.demon_slayer_photo = ImageTk.PhotoImage(self.demon_slayer_image)
        self.demon_slayer_label = tk.Label(window, image=self.demon_slayer_photo)
        self.demon_slayer_label.pack()

        self.game_frame = tk.Frame(window)
        self.game_frame.pack(pady=20)

        self.output_text = tk.Text(self.game_frame, width=60, height=20)
        self.output_text.pack()

        self.actions = [("educate person", self.educate_person), ("ignore person", self.ignore_person), ("respond with violence", self.respond_with_violence)]

        for text, command in self.actions:
            button = tk.Button(self.game_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def close_game(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.end_time = datetime.now()
            duration = self.end_time - self.start_time
            self.output_text.insert(tk.END, f"Game Duration: {duration}\n")
            self.window.destroy()
            self.close_connection()

    def educate_person(self):
        self.output_text.insert(tk.END, "You educate the person.\n")

    def ignore_person(self):
        self.output_text.insert(tk.END, "You ignore the person and walk away!\n")

    def respond_with_violence(self):
        self.output_text.insert(tk.END, "You punch the person in the face\n")

    def start_game(self):
        self.start_time = datetime.now()
        messagebox.showinfo("Game Started", "Let the educating begin!")
        self.welcome_label.pack_forget()
        self.question_label.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.demon_slayer_label.pack_forget()
        self.create_character_selection()

    def create_character_selection(self):
        character_label = tk.Label(self.window, text="Select Your Character:")
        character_label.pack()

        characters = [("images/Rabbi.jpeg", "Character 1"), ("images/soldier.jpeg", "Character 2"), ("images/Israeli girl.png", "Character 3")]

        character_frame = tk.Frame(self.window)
        character_frame.pack()

        for image_path, character_name in characters:
            # Load character image
            character_image = Image.open(image_path).resize((100, 100))
            character_photo = ImageTk.PhotoImage(character_image)
            # Pass character_name to the command using a lambda function to avoid late binding issues
            character_button = tk.Button(character_frame, image=character_photo, command=lambda name=character_name: self.select_character(name))
            character_button.photo = character_photo  # Keep a reference to avoid garbage collection
            character_button.pack(side=tk.LEFT, padx=10)

    def select_character(self, character):
        player_name = self.ask_for_name()
        if player_name:  # Check if the player provided a name
            self.insert_player_data(player_name, character)
            self.output_text.delete('1.0', tk.END)  # Clear the text box
            self.output_text.insert(tk.END, f"Player Name: {player_name}\nSelected character: {character}\n")
            self.get_question()  # Proceed to get and display a question

    def insert_player_data(self, player_name, character_name):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO player_data (player_name, character_name, play_time) VALUES (%s, %s, %s)"
        self.cur.execute(sql, (player_name, character_name, timestamp))
        self.conn.commit()

    def ask_for_name(self):
        return simpledialog.askstring("Player's Name", "Enter your name:")

    def get_question(self):
        questions = [
            "What year was the State of Israel established?",
            "Name one Jewish holiday and its significance.",
            "Who was Theodor Herzl?"
        ]
        selected_question = random.choice(questions)
        self.display_question(selected_question)

    def display_question(self, question):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, question + "\n\nYour answer: ")

    def close_connection(self):
        self.cur.close()
        self.conn.close()

def main():
    window = tk.Tk()
    FightAntiSemitisimGame(window)
    window.mainloop()

if __name__ == "__main__":
    main()









