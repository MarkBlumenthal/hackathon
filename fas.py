#This is a text based style, Python game designed to help educate people on how to deal with anti-semitisim.
#it uses the API tkinter to help manage the GUI toolkit in python. It also incoporates the use of Postgresql,
#by sending all game data to a psql database which can retrieve player scores etc.
#All questions and answers are stored in a json file which allows easy manipulation and adding and removing,
#scenarios and responses.

#Before running the code, make sure you have: tkinter, json and psycopg2 installed in your vscode.


#********************************************************************************************************************************#

import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import psycopg2
import json
from tkinter import Toplevel, ttk  # ttk is needed for the Treeview widget




#**************************************************************************************************************************************#


#create the object of FightAntiSemitisimGame
class FightAntiSemitisimGame:

    def educate_person(self):
        outcome = self.current_actions['educate person'] #retrieves the outcome when a player selects"educate person"
        self.output_text.insert(tk.END, outcome + "\n") #inserts the outcome into the widget and makes sure the response is printed on an new line.
        self.points += 10  # Add points for educating
        self.update_points_display()  # Update the points display
        self.update_player_points(self.points, self.player_name) #updates the points in Postgresql
        self.get_question() #calls the game to move on to the next question

    def ignore_person(self):
        outcome = self.current_actions['ignore person']
        self.output_text.insert(tk.END, outcome + "\n")
        self.points += 5  # Add points for ignoring
        self.update_points_display()  # Update the points display
        self.update_player_points(self.points, self.player_name)
        self.get_question()

    def respond_with_violence(self):
        outcome = self.current_actions['respond with violence']
        self.output_text.insert(tk.END, outcome + "\n")
        self.points += 0  # No points for violence
        self.update_points_display()  # Update the points display
        self.update_player_points(self.points, self.player_name)
        self.get_question()  

    def update_points_display(self):
        # Method to update the points display. 
        self.output_text.insert(tk.END, f"Current Points: {self.points}\n")

    def show_final_score(self):
    # This method shows the player's total score in a pop-up message box.
     messagebox.showinfo("Total Score", f"Your total score is: {self.points}")
      # Automatically show the leaderboard after displaying the final score
     self.show_leaderboard()  # or self.show_leaderboard()


    def fetch_top_players(self):
     self.cur.execute("SELECT player_name, points FROM player_data ORDER BY points DESC LIMIT 10")
     top_players = self.cur.fetchall()  # Fetches the top 10 players
     return top_players
    
    def show_leaderboard(self):
      top_players = self.fetch_top_players()
      # Create a new Toplevel window
      leaderboard_window = Toplevel(self.window)
      leaderboard_window.title("Leaderboard")
    
    # Create a Treeview widget
      leaderboard_tree = ttk.Treeview(leaderboard_window, columns=('Rank', 'Name', 'Points'), show='headings', height=10)
      leaderboard_tree.pack(side='top', fill='x')
    
    # Define the columns
      leaderboard_tree.heading('Rank', text='Rank')
      leaderboard_tree.heading('Name', text='Name')
      leaderboard_tree.heading('Points', text='Points')
    
    # Adjust the columns' width to the content
      leaderboard_tree.column('Rank', width=50, anchor='center')
      leaderboard_tree.column('Name', width=150, anchor='center')
      leaderboard_tree.column('Points', width=100, anchor='center')
    
    # Insert the player data into the Treeview
      for index, player in enumerate(top_players, start=1):
       leaderboard_tree.insert("", 'end', values=(index, player[0], player[1]))




    



#************************************************************************************************************************************#



    def __init__(self, window):

        self.points = 0 

        self.window = window
        self.window.title("Welcome to Fight Anti-Semitisim")
        self.window.configure(background='lightblue')  # Sets the background color of the window

        self.conn = psycopg2.connect(dbname="Hackathon-1", user="postgres", password="arsenal_1", host="localhost") #info required to connect to the psql database
        self.cur = self.conn.cursor()

        self.start_time = None
        self.end_time = None
        self.question_index = 0  # Initialize question index to start from the beggining

        self.welcome_label = tk.Label(window, text="Welcome To Fight Anti-Semitisim", bg='lightblue')
        self.welcome_label.pack()
        self.question_label = tk.Label(window, text="Lets Change people's views in this world", bg='lightblue') #inserts the labels into the opening screen
        self.question_label.pack()

        self.yes_button = tk.Button(window, text="Yes", command=self.start_game) #creates a new button in the widget
        self.yes_button.pack(side=tk.LEFT, padx=10)
        self.no_button = tk.Button(window, text="No", command=self.close_game)
        self.no_button.pack(side=tk.RIGHT, padx=10)

        self.demon_slayer_image = Image.open("images/fightantisemitisim.png").resize((300, 150)) #sets the homescreen picture in the widget
        self.demon_slayer_photo = ImageTk.PhotoImage(self.demon_slayer_image)
        self.demon_slayer_label = tk.Label(window, image=self.demon_slayer_photo)
        self.demon_slayer_label.pack()

        self.game_frame = tk.Frame(window) #main window widget
        self.game_frame.pack(pady=20)

        self.output_text = tk.Text(self.game_frame, width=140, height=20) #text window widget
        self.output_text.pack()

        self.actions = [
            ("educate person", self.educate_person), #[]=list ()=tuple within a list, note that the methods are not being called here. 
            ("ignore person", self.ignore_person),   # this is a stored reference to the method in the json file
            ("respond with violence", self.respond_with_violence)
        ]

        for text, command in self.actions: #selects the action when a button is pushed
            button = tk.Button(self.game_frame, text=text, command=command, bg='lightblue') #creates the buttons for actions
            button.pack(side=tk.LEFT, padx=5, pady=5) #where the buttons are displayed



#**********************************************************************************************************************#



    def close_game(self):
     if messagebox.askokcancel("Quit", "Do you really want to quit?"): #asks the user if they want to quit. returns true if they say ok
        self.end_time = datetime.now()
        duration = self.end_time - self.start_time #subtracts start time from end time
        self.output_text.insert(tk.END, f"Game Duration: {duration}\n")
        if hasattr(self, 'player_name'):  #This is a safety check to ensure that the game has a player name set before trying to update the database.
            self.update_player_points(self.points, self.player_name)  # Update points in psql database
        self.window.destroy()
        self.close_connection()


    def start_game(self):
        self.points = 0
        self.start_time = datetime.now()
        messagebox.showinfo("Game Started", "Let the educating begin!")
        self.welcome_label.pack_forget()
        self.question_label.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.demon_slayer_label.pack_forget()
        self.create_character_selection()



#*************************************************************************************************************************************#



    def create_character_selection(self):
        character_label = tk.Label(self.window, text="Select Your Character:", bg='lightblue')
        character_label.pack()

        characters = [("images/dwight.jpeg", "Character 1"), ("images/EricCartman.png", "Character 2"), ("images/Yoda.png", "Character 3")]

        character_frame = tk.Frame(self.window, bg='lightblue')
        character_frame.pack()

        for image_path, character_name in characters:
            character_image = Image.open(image_path).resize((100, 100))
            character_photo = ImageTk.PhotoImage(character_image)
            character_button = tk.Button(character_frame, image=character_photo, command=lambda name=character_name: self.select_character(name))
            character_button.photo = character_photo
            character_button.pack(side=tk.LEFT, padx=10)

    def select_character(self, character):
     self.points = 0  # Reset points to zero when a new character is selected
     player_name = self.ask_for_name()
     if player_name:
        self.player_name = player_name  # Store player name as an instance variable
        self.insert_player_data(player_name, character, self.points)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f"Player Name: {player_name}\nSelected character: {character}\n")
        self.get_question()  # Start the game with the first question



#********************************************************************************************************************************************************************************************************#

    #inserts all player data into the psql database
    def insert_player_data(self, player_name, character_name, points):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #formats date and time into a string
        sql = "INSERT INTO player_data (player_name, character_name, play_time, points) VALUES (%s, %s, %s, %s)" #inserts data into psql. %s are placeholders used to seperate sql code from data values
        self.cur.execute(sql, (player_name, character_name, timestamp, points))
        self.conn.commit()

    def ask_for_name(self):
        return simpledialog.askstring("Player's Name", "Enter your name:")



#***********************************************************************************************************************************************************************************************************#



    def get_question(self):
       
       with open('questions.json', 'r') as file: #opens the json file
        data = json.load(file) #moves the file from json into a python dictionary
        questions = data["questions"] #accesess the value associated with the key "questions"
        
        if self.question_index >= len(questions): #This line checks if the current question has reached or exceeded the total number of questions available. "len" calculates total number of questions
            self.show_final_score()
            # If all questions have been asked, show a game over message and reset
            messagebox.showinfo("Game Over", "You've responded to all scenarios! Would you like to play again? If you do then select a new character!")
            self.question_index = 0
            return
        
        self.current_actions = questions[self.question_index]["actions"] #retireves action associated with current questions
        selected_question = questions[self.question_index]["text"] # extracts text of current question
        self.display_question(selected_question)
        self.question_index += 1 #this increments the system to prepare the next question
        

    def display_question(self, question):
        self.output_text.insert(tk.END, question + "\n\nYour answer: ")



#*****************************************************************************************************************************************************************************************************************#



    def update_player_points(self, points, player_name):
     sql = "UPDATE player_data SET points = %s WHERE player_name = %s"
     print("Updating points for player:", player_name)
     print("Old points:", points)
     print("Data type of points:", type(points))
     self.cur.execute(sql, (int(points), player_name))
     self.conn.commit()
    

    def close_connection(self):
        self.cur.close()
        self.conn.close()



#*********************************************************************************************************************************************#



def main():
    window = tk.Tk()
    FightAntiSemitisimGame(window)
    window.mainloop()

if __name__ == "__main__":
    main()   














   
