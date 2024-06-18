from tkinter import PhotoImage
from tkinter import messagebox
import tkinter as tk
import pygame
import random
suits = ["hearts", "diamonds", "clubs", "spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
class WelcomeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to Solitaire")
        self.canvas = tk.Canvas(self, width=1600, height=800, bg="white")
        self.attributes('-fullscreen',True)
        self.bg_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/well.png")  
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)
        self.instructions = "                                         WELCOME TO THE GAME\n\nInstructions:\n1. Select three cards to remove from the pile whose sum is equal to 10 or 20 or 30.\n2.The Value of the Face Cards K,Q,J is 10 and A is 1.\n3. Ensure that the selected cards are within the same pile.\n5. The positions of the cards must be the first and last two or last three or first two and last one.\n4. Make sure to disappear 5 combinations within a deal of 70 cards to win.\nScoring Pattern:\n1.Each time you select a valid combination its sum will be your score.\n2.If you clear a pile you would score a bonus of 50"
        name_label = tk.Label(self, text="Enter Your Name:",fg='goldenrod2',bg='black', font = (("Times New Roman"),20))
        name_label.place(relx=0.7, rely=0.4, anchor=tk.CENTER)
        self.name_entry = tk.Entry(self,fg='goldenrod2',bg='black', font = (("Times New Roman"),20))
        self.name_entry.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
        play_button = tk.Button(self, text="Play Now", fg='goldenrod2',bg='black',command=self.show_instructions, font = (("Times New Roman"),24))
        play_button.place(relx=0.7, rely=0.6, anchor=tk.CENTER) 
    def show_instructions(self):
        self.instructions_window = tk.Toplevel(self) 
        self.instructions_window.title("Instructions")
        self.instructions_window.attributes('-fullscreen', True)
        canvas = tk.Canvas(self.instructions_window, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        canvas.pack()
        background_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/purps.png")
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        instructions_label = tk.Label(self.instructions_window, text=self.instructions, font = (("Times New Roman"),20), bg='black',fg='goldenrod',justify=tk.LEFT)
        instructions_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        continue_button = tk.Button(self.instructions_window, text="Continue", command=self.start_game,bg='black',fg='goldenrod', font = (("Times New Roman"),24))
        continue_button.place(relx=0.55, rely=0.95, anchor=tk.SE)
        canvas.background = background_image
        self.instructions_window.mainloop()
    def start_game(self):
        self.instructions_window.destroy()

        self.player_name = self.name_entry.get()
        if not self.player_name.strip():
            self.player_name = "Anonymous"
        self.destroy()
        deck = random.sample(cards_input, k=154)
        app = CardDeck(deck, self.player_name)
        app.mainloop()
class CardDeck(tk.Tk):
    def __init__(self, deck,player_name):
        super().__init__()
        self.title("10-20-30 SOLITAIRE")
        self.attributes('-fullscreen',True) 
        self.canvas = tk.Canvas(self, width=1600, height=800, bg="dark green")
        self.canvas.pack()
        self.bg_image = PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/green_bg.png") 
        self.bg_label = tk.Label(self.canvas, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  
        self.bg_label_instance = self.bg_label
        self.photoimg = tk.PhotoImage(file="C:/Users/harsh/OneDrive/Desktop/cards/heart.png")
        image_label = tk.Label(self, image=self.photoimg)
        image_label.place(relx=1, rely=1, anchor="se", x=-150, y=-80)
        self.photoimg1 = tk.PhotoImage(file="C:/Users/harsh/OneDrive/Desktop/cards/club.png")
        image_label1 = tk.Label(self, image=self.photoimg1)
        image_label1.place(relx=1, rely=1, anchor="se", x=-50, y=-290)
        self.photoimg2 = tk.PhotoImage(file="C:/Users/harsh/OneDrive/Desktop/cards/diamond.png")
        image_label2 = tk.Label(self, image=self.photoimg2)
        image_label2.place(relx=1, rely=1, anchor="se", x=-150, y=-480)
        self.photoimg3 = tk.PhotoImage(file="C:/Users/harsh/OneDrive/Desktop/cards/spade.png")
        image_label3 = tk.Label(self, image=self.photoimg3)
        image_label3.place(relx=1, rely=1, anchor="se", x=-50, y=-670)
        frame = tk.Frame(self,bg='black')
        frame.pack(fill=tk.BOTH, expand=True)    
        pygame.init()
        pygame.mixer.init()
        self.sound_combination = pygame.mixer.Sound(f"C:/Users/harsh/Downloads/chime_up.wav")
        self.sound_win = pygame.mixer.Sound(f"C:/Users/harsh/Downloads/cheering.wav")
        self.sound_click = pygame.mixer.Sound(f"C:/Users/harsh/Downloads/click_x.wav")
        self.sound_win = pygame.mixer.Sound(f"C:/Users/harsh/Downloads/cheering.wav")
        self.sound_loose = pygame.mixer.Sound(f"C:/Users/harsh/Downloads/negative_beeps-6008.mp3")
        self.sound_loost = pygame.mixer.Sound(f"C:/Users/harsh/Downloads/Sad Trombone.mp3")
        self.is_music_playing = False  # Flag to track music play state
        self.play_music()
        self.best_dealt_cards = []
        self.card_images = {} 
        self.cards_labels = {} 
        self.generate_cards()
        self.deck = deck
        self.piles = self.create_piles(deck)
        self.display_piles()
        self.selected_cards = []
        self.clicked_cards = []
        self.card_index = 0
        self.dealing_pile_index = 0
        self.exclude_pile_index = None
        button_frame = tk.Frame(self)
        button_frame.place(relx=0.5, rely=0.97, anchor=tk.CENTER) 
        self.deal_button = tk.Button(button_frame, text="Deal Cards", bd=0,command=self.deal_cards,fg='goldenrod2',bg='gray9', font = (("Times New Roman"),18))
        self.deal_button.pack(side=tk.LEFT, padx=0)
        self.restart_button = tk.Button(button_frame, text="Restart Game",bd=0, command=self.restart_game,fg='goldenrod2',bg='gray9', font = (("Times New Roman"),18))
        self.restart_button.pack(side=tk.LEFT, padx=0)
        self.exit_button = tk.Button(button_frame, text="Exit Game",bd=0, command=self.exit_game,fg='goldenrod2',bg='gray9', font = (("Times New Roman"),18))
        self.exit_button.pack(side=tk.LEFT, padx=0)
        self.card_count_label = tk.Button(button_frame, text="Cards Dealt: 0",bd=0,fg='goldenrod2',bg='gray9', font = (("Times New Roman"),18))
        self.card_count_label.pack(side=tk.LEFT, padx=0)
        self.current_score = 0
        self.score_label = tk.Button(button_frame, text="Current Score: 0",bd=0,fg='goldenrod2',bg='gray9',  font = (("Times New Roman"),18))
        self.score_label.pack(side=tk.LEFT, padx=0)
        self.best_score = self.load_best_score()
        self.score_label1 = tk.Button(button_frame, text=f"Best Score: {self.best_score}",fg='goldenrod2',bg='gray9', bd=0, font = (("Times New Roman"),18))
        self.score_label1.pack(side=tk.LEFT, padx=0)
        self.player_name = player_name
        self.moves = 0
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.dealt_piles = []
        self.last_dealt_pile = -1
        self.dealt_card_count = 0
        self.combinations_removed = 0    
    def play_music(self):
        if not self.is_music_playing:
            pygame.mixer.music.load(f"C:/Users/harsh/Downloads/background_music.mp3.mp3")  
            pygame.mixer.music.play(loops=-1)  
            self.is_music_playing = True
    def display_piles(self):
        for widget in self.canvas.winfo_children():
            if widget != self.bg_label_instance:
                widget.destroy()
        for pile_index in range(7):
            pile = self.piles[pile_index]
            if pile:
                for card_position in range(len(pile)):
                    card_value = pile[card_position]
                    suit_index = (card_value - 1) % 4
                    suit = suits[suit_index]
                    card_name = str(card_value)
                    if card_value == 1:
                        card_name = "a"
                    elif card_value == 10:
                        card_name = random.choice(["10", "k", "q", "j"])
                    card_image = self.card_images.get((card_name, suit))
                    card_button = tk.Button(self.canvas, image=card_image, bd=0, highlightthickness=0,
                                        command=lambda pile_index=pile_index, card_position=card_position: self.card_clicked(pile_index, card_position))
                    card_button.image = card_image
                    x_position = 20 + pile_index * 150
                    y_position = 40 + card_position * 30
                    card_button.place(x=x_position, y=y_position)
            else:
                back_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/bck.png")
                card_button = tk.Button(self.canvas, image=back_image, bd=0, highlightthickness=0)
                card_button.image = back_image
                x_position = 20 + pile_index * 150
                y_position = 40
                card_button.place(x=x_position, y=y_position)
        back_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/bck.png")
        for i in range(31):
            card_button = tk.Button(self.canvas, image=back_image, bd=0, highlightbackground="black", highlightthickness=1)
            card_button.image = back_image
            card_button.place(x=20 + i * 10, y=650)

    def create_piles(self, deck):
        piles = [deck[i:i + 3] for i in range(0, 21, 3)]
        for pile in piles:
            for card in pile:
                deck.remove(card)
        return piles
    def generate_cards(self):
        for suit in suits:
            for rank in ranks:
                card_name = f"C:/Users/harsh/OneDrive/Desktop/cards/{rank}_of_{suit}.png"
                my_image = tk.PhotoImage(file=card_name)
                self.card_images[(rank, suit)] = my_image
    def deal_remaining_cards(self):
        remaining_cards = self.deck[self.card_index:]
        for card in remaining_cards:
            self.piles[self.card_index % 7].append(card)
            self.card_index += 1
        self.display_piles()
    suit_index=0
    def deal_cards(self):
        if self.card_index < len(self.deck):
            for pile_index in range(7):
                pile = self.piles[pile_index]
                if pile:
                    self.sound_click.play()
                    card_to_deal = self.deck[self.card_index]
                    self.piles[pile_index].append(card_to_deal)
                    self.card_index += 1
                    self.display_piles()
            self.card_count_label.config(text="Cards Dealt: " + str(self.card_index))
            if self.card_index > 70:
                self.deal_button.config(state=tk.DISABLED)
                self.deal_remaining_cards()
                if self.combinations_removed < 5:
                    self.sound_loost.play()
                    result_text = "Sorry, {}! You have run out of moves. Try Again!\nYour Score: {}".format(self.player_name, self.current_score)
                    self.show_results(result_text)
                    self.restart_game()
            if self.card_index == len(self.deck):
                self.deal_button.config(state=tk.DISABLED)
    def card_clicked(self, pile_index, card_position):
        self.sound_click.play()
        if len(self.selected_cards) == 3:
            self.clear_selection()
        self.selected_cards.append((pile_index, card_position))
        self.moves += 1  
        if len(self.selected_cards) == 3:
            self.process_selection()
    def process_selection(self):
        pile_indexes = [card[0] for card in self.selected_cards]
        selected_positions = sorted([card[1] for card in self.selected_cards])
        valid_positions = [[0, 1, len(self.piles[pile_indexes[0]]) - 1],[0, len(self.piles[pile_indexes[0]]) - 2, len(self.piles[pile_indexes[0]]) - 1],[len(self.piles[pile_indexes[0]]) - 3, len(self.piles[pile_indexes[0]]) - 2, len(self.piles[pile_indexes[0]]) - 1],]
        if len(set(pile_indexes)) == 1:
            pile_index = pile_indexes[0]
            if selected_positions in valid_positions:
                self.check_and_move_selected_cards(pile_index)
            else:
                self.sound_loose.play()
                messagebox.showinfo("Invalid Selection", "Select valid cards.")
        else:
            self.sound_loose.play()
            messagebox.showinfo("Invalid Selection", "Select cards within the same pile.")
        self.clear_selection()
        self.display_piles()
        if self.combinations_removed >= 5:
            self.sound_win.play()
            result_text = "     Congratulations, {}! You have successfully removed five combinations!\nYour Score: {}".format(self.player_name, self.current_score)
            self.show_results(result_text)
            self.restart_game()
        elif self.card_index == len(self.deck):
            self.sound_loose.play()
            result_text = "    Sorry, {}! You have run out of moves. Try Again!\nYour Score: {}".format(self.player_name, self.current_score)
            self.show_results(result_text)
            self.restart_game()
    def check_and_move_selected_cards(self, pile_index):
        selected_values = [self.piles[pile_index][pos] for _, pos in self.selected_cards]
        sum_of_selected = sum(selected_values)

        if sum_of_selected in [10, 20, 30]:
            if sum_of_selected == 10:
                self.sound_combination.play()
                self.current_score += 10
                messagebox.showinfo("Combination!", "Good, you got a 10!")
            elif sum_of_selected == 20:
                self.sound_combination.play()
                self.current_score += 20
                messagebox.showinfo("Combination!", "Cool, it's 20! ")
            else:
                self.sound_combination.play()
                self.current_score += 30
                messagebox.showinfo("Combination!", "Bingo, it's 30! ")

            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.save_best_score()
                self.score_label1.config(text=f"Best Score: {self.best_score}")
            for _, pos in sorted(self.selected_cards, reverse=True):
                card_button = self.cards_labels.get((pile_index, pos))
                if card_button:
                    card_button.destroy()
            for _, pos in sorted(self.selected_cards, reverse=True):
                self.piles[pile_index].pop(pos)

            self.combinations_removed += 1
        else:
            self.sound_loose.play()
            messagebox.showinfo("Invalid Selection", "Select valid Sum cards.")

        if not self.piles[pile_index]:
            self.sound_combination.play()
            self.current_score += 50
            messagebox.showinfo("Empty Pile!", "A pile became empty! Your score +50")

        self.score_label.config(text="Current Score: " + str(self.current_score))
        self.display_piles()
        self.clear_selection()

        if self.combinations_removed >= 5:
            self.sound_win.play()
            result_text = f"Congratulations, {self.player_name}! You have successfully removed five combinations!\nYour Score: {self.current_score}"
            self.show_results(result_text)
            self.restart_game()
        elif self.card_index == len(self.deck):
            self.sound_loose.play()
            result_text = f"Sorry, {self.player_name}! You have run out of moves. Try Again!\nYour Score: {self.current_score}"
            self.show_results(result_text)
            self.restart_game()

    def load_best_score(self):
            with open(f"C:/Users/harsh/OneDrive/Desktop/best_score.txt", "r") as file:
                return int(file.read())
    def save_best_score(self):
        current_best_score = self.load_best_score()

        if self.best_score > current_best_score:
            with open(f"C:/Users/harsh/OneDrive/Desktop/best_score.txt", "w") as file:
                file.write(str(self.best_score))
    def clear_selection(self):
        self.selected_cards.clear()
        self.exclude_pile_index = None
    def show_results(self, result_text):
        pygame.mixer.music.stop()
        self.results_window = tk.Toplevel(self)
        self.results_window.title("Game Result")     
        self.results_window.attributes('-fullscreen',True)
        self.results_window.configure(bg="black")      
        if "Congratulations" in result_text:
            canvas = tk.Canvas(self.results_window, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
            canvas.pack()
            background_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/congbg.png")
            canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
            result_label = tk.Label(self.results_window, text=result_text, bg='DeepPink2',font=("Helvetica", 20))
            result_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
            # Add other widgets on top of the background image
            congratulations_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/congi.png")
            congratulations_label = tk.Label(self.results_window, image=congratulations_image)
            congratulations_label.image = congratulations_image
            congratulations_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            exit_button = tk.Button(self.results_window, text="Exit the Game", bg='plum1',command=self.exit_game, font=("Helvetica", 16))
            exit_button.place(relx=0.8, rely=0.9, anchor=tk.SE)
            self.results_window.mainloop()          
        elif "Sorry" in result_text:
            canvas = tk.Canvas(self.results_window, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
            canvas.pack()
            # Load and display the background image
            background_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/lossg.png")
            canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
            result_label = tk.Label(self.results_window, text=result_text, bg='plum1',font=("Helvetica", 20))
            result_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            lose_image = tk.PhotoImage(file=f"C:/Users/harsh/OneDrive/Desktop/cards/gmov.png")
            lose_label = tk.Label(self.results_window,bg='plum1', image=lose_image)
            lose_label.image = lose_image  # Important to keep a reference to the image
            lose_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
            los_image_path = f"C:/Users/harsh/OneDrive/Desktop/cards/sad.png"  # Replace with the path to your win image
            los_image = tk.PhotoImage(file=los_image_path)
            los_label = tk.Label(self.results_window, image=los_image)
            los_label.image = los_image  # Important to keep a reference to the image
            los_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
            exit_button = tk.Button(self.results_window, text="Exit the Game", bg='plum1',command=self.exit_game, font=("Helvetica", 16))
            exit_button.place(relx=0.8, rely=0.9, anchor=tk.SE) 
            self.results_window.mainloop()  
    def restart_game(self):
        self.current_score = 0
        self.card_index = 0
        self.combinations_removed = 0
        self.selected_cards = []
        self.deck = random.sample(cards_input, k=52)
        self.piles = self.create_piles(self.deck)
        self.display_piles()
        self.deal_button.config(state=tk.NORMAL)
        self.card_count_label.config(text="Cards Dealt: 0")
        self.score_label.config(text="Current Score: 0")
        self.mainloop()

    def exit_game(self):
        if self.winfo_exists():
        # Stop music
            pygame.mixer.music.stop()
            self.destroy()
if __name__ == "__main__":
    cards_input = [2, 6, 5, 10, 10, 4, 10, 10, 10, 4, 5, 10, 4, 5, 10, 9, 7, 6, 1, 7, 6, 9, 5, 3, 10, 10, 4, 10,9, 2, 1, 10, 1, 10, 10, 10, 3, 10, 9, 8, 10, 8, 7, 1, 2, 8, 6, 7, 3, 3, 8, 2, 4, 3, 2, 10, 8,10, 6, 8, 9, 5, 8, 10, 5, 3, 5, 4, 6, 9, 9, 1, 7, 6, 3, 5, 10, 10, 8, 10, 9, 10, 10, 7, 2, 6, 10,10, 4, 10, 1, 3, 10, 1, 1, 10, 2, 2, 10, 4, 10, 7, 7, 10, 10, 5, 4, 3, 5, 7, 10, 8, 2, 3, 9, 10, 8,4, 5, 1, 7, 6, 7, 2, 6, 9, 10, 2, 3, 10, 3, 4, 4, 9, 10, 1, 1, 10, 5, 10, 10, 1, 8, 10, 7, 8, 10, 6, 10, 10, 10, 9, 6, 2, 10, 10]
    deck = random.sample(cards_input, k=156)
    welcome_window = WelcomeWindow()
    welcome_window.mainloop()
