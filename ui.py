from tkinter import *
from PIL import ImageTk, Image
import webbrowser
import random
import json
# Import your other files
from config import *
from auth import User
from poker_logic import Deck, StatsCalc, GetTypeOfHand
from player import Player

class Menu:
    def __init__(self, loggedin):
        while not loggedin:
            self.Users = User()
            self.username, loggedin, self.chips, self.tips_enabled, self.colour_scheme = self.Users.get_facts()


        self.menu_screen()
    
    def menu_screen(self):
        self.menu_window = Tk()
        self.menu_window.geometry("300x500")
        self.menu_window.title("My Poker Game Menu")
        self.menu_window.configure(bg = self.colour_scheme)


        #Creation of my buttons
        Label(text=f'User: {self.username}\nChips: {self.chips}', bg = self.colour_scheme, width = 300, height = "5",font = ("Calibri",16)).pack()
        Button(text = "Play a Game", height = "5", width = "15", command = self.run_game).pack()
        Button(text = "See Leaderboard", height = "5", width = "15", command = self.leaderboard).pack()
        Button(text="Settings", height = "5", width = "15", command = self.settings).pack()
        Button(text = "Quit Game", height = "5", width = "15", command = self.quit_game).pack()


        self.menu_window.mainloop()


    def run_game(self):
        game = Game(self.chips, self.tips_enabled, self.colour_scheme, self.username)
        


    def leaderboard(self):
        #creation of my leaderboard window
        leaderboard_screen = Toplevel(self.menu_window)
        leaderboard_screen.geometry("500x375")
        leaderboard_screen.title("Leaderboard")


        frame = Frame(leaderboard_screen, width = 600, height = 400)
        frame.pack()
        frame.place(anchor='center',relx=0.5,rely=0.5)
        
        #adding image of the podium onto the frame
        img = ImageTk.PhotoImage(Image.open(f'{ROUTETOIMAGES}winners_podium_{self.colour_scheme}.png'))
        label = Label(frame, image = img)
        label.pack()


        #adding a button
        button = Button(leaderboard_screen, text = "Back to Menu", width = 10, height = 2, command = leaderboard_screen.destroy)
        button.place(x=210, y=330)


        #filters the top 3 uers with the most chips and stores it as an array
        sorted_leaderboard = self.filter_leaderboard()


        #placing the names and chips of the users onto the podium
        first_user = Label(leaderboard_screen, bg = self.colour_scheme, text = f'{sorted_leaderboard[0][0]}\n{sorted_leaderboard[0][2]}', font=("Calibri", 25, 'italic'))
        first_user.place(x= 200, y= 40)


        second_username = Label(leaderboard_screen, bg = self.colour_scheme, text =  f'{sorted_leaderboard[1][0]}\n{sorted_leaderboard[1][2]}', font=("Calibri", 25, 'italic'))
        second_username.place(x= 60, y= 70)


        third_user = Label(leaderboard_screen, bg = self.colour_scheme, text =  f'{sorted_leaderboard[2][0]}\n{sorted_leaderboard[2][2]}', font=("Calibri", 25, 'italic'))
        third_user.place(x= 370, y= 80)


        leaderboard_screen.mainloop()


    def filter_leaderboard(self):
        with open (USERDATABASE,'r') as f:
            accounts = json.load(f)
        chips_accounts = []
        for i in accounts:
            chips_accounts.append(i[2])
        self.sort_leaderboard(chips_accounts)
        sorted_chip_counts = chips_accounts[::-1]


        # add null entries to array if less than 3 users are stored
        if len(sorted_chip_counts) < 3:
            sorted_chip_counts.extend([0,0,0])


        top = []
        for i in range(3):
            chips = sorted_chip_counts[i]


            # add null entry
            if chips == 0:
                top.append(["","","","",""])


            else:
                for j in accounts:
                    if chips == j[2] and len(top) <3:
                        top.append(j)
        return top


    def sort_leaderboard(self, array):
        if len(array) >1:
            middle = len(array) //2
            left_half = array[:middle]
            right_half = array[middle:]


            #recursively splits the array until each item is fully separated from one another
            self.sort_leaderboard(left_half)
            self.sort_leaderboard(right_half)


            #iterators for traversing the halves
            i = 0
            j = 0


            #iterator for the main list
            k = 0


            while i < len(left_half) and j < len(right_half):
                if left_half[i] <= right_half[j]:
                    #the value from the left half has been used
                    array[k] = left_half[i]
                    #move the iterator forward
                    i += 1
                else:
                    #the value from the right half has been used
                    array[k] = right_half[j]
                    j += 1
                #move to the next slot
                k += 1


            #for all the remaining values
            while i < len(left_half):
                array[k] = left_half[i]
                i += 1
                k += 1


            while j < len(right_half):
                array[k]=right_half[j]
                j += 1
                k += 1


    def settings(self):
        #creates the settings window
        self.settings_screen = Tk()
        self.settings_screen.geometry("300x500")
        self.settings_screen.title("Settings")
        self.settings_screen.configure(bg= self.colour_scheme)


        Label(self.settings_screen, text = "Settings", bg = self.colour_scheme, width = 300, height = "5",font = ("Calibri",16)).pack()


        Button(self.settings_screen, text = "View Rules", height = "5", width = "15", command = self.game_rules).pack()
        if self.tips_enabled == "True":
            self.button1 = Button(self.settings_screen, fg = 'green', text = "Toggle Tips", height = "5", width = "15", command = self.toggle_tips)
        else:
            self.button1 = Button(self.settings_screen, fg = 'red', text = "Toggle Tips", height = "5", width = "15", command = self.toggle_tips)
        self.button1.pack()


        Button(self.settings_screen, text = "Change Colour", height = "5", width = "15", command = self.change_colour).pack()


        Button(self.settings_screen, text = "Back to Menu", height = "5",  width = "15", command = self.settings_screen.destroy).pack()


        self.settings_screen.mainloop()


    def toggle_tips(self):
        if self.tips_enabled == "True":
            self.tips_enabled = "False"
            self.button1.configure(fg = 'red')
        else:
            self.tips_enabled = "True"
            self.button1.configure(fg = "green")


    def change_colour(self):
        self.settings_screen.destroy()


        self.changecolour_screen = Tk()
        self.changecolour_screen.geometry("300x500")
        self.changecolour_screen.title("Change Colour Menu")
        self.changecolour_screen.configure(bg=self.colour_scheme)


        Label(self.changecolour_screen, text = "Select Colour",bg = self.colour_scheme, width = 300, height = "5",font = ("Calibri",16)).pack()


        Button(self.changecolour_screen, text = "Green", height = "5", width = "15", command = self.SetGreen).pack()
        Button(self.changecolour_screen, text = "Light Blue", height = "5", width = "15", command = self.SetBlue).pack()
        Button(self.changecolour_screen, text = "Orange", height = "5", width = "15", command = self.SetOrange).pack()
        Button(self.changecolour_screen, text = "Pink", height = "5", width = "15", command = self.SetPink).pack()


        self.changecolour_screen.mainloop()


    def SetGreen(self):
        self.colour_scheme = 'green'
        self.changecolour_screen.destroy()
        self.menu_window.destroy()
        self.menu_screen()


    def SetBlue(self):
        self.colour_scheme = '#9898F5'
        self.changecolour_screen.destroy()
        self.menu_window.destroy()
        self.menu_screen()


    def SetOrange(self):
        self.colour_scheme = '#ff9100'
        self.changecolour_screen.destroy()
        self.menu_window.destroy()
        self.menu_screen()


    def SetPink(self):
        self.colour_scheme = '#dd00ff'
        self.changecolour_screen.destroy()
        self.menu_window.destroy()
        self.menu_screen()


    def game_rules(self):
        webbrowser.open_new(RULESWEBPAGELINK)


    def quit_game(self):
        self.Users.update_player_info(self.chips, self.tips_enabled, self.colour_scheme)
        quit()


class Game(StatsCalc):
    def __init__(self, chips, tips, colour, name):
        #creating my different player objects
        self.player1 = Player(name)
        self.player2 = Player("Bot1")
        self.player3 = Player("Bot2")
        self.player4 = Player("Bot3")
        self.current_players = [self.player1, self.player2, self.player3, self.player4]
        self.chips, self.tips_enabled, self.colour_scheme = chips, tips, colour
        self.pot_size = 0
        self.deck = Deck()


        self.set_up_game()


        # check that each player has the required amount of chips to play
        self.check_chips_of_players()


        self.update_player_hand()
        self.create_game_window()


    def set_up_game(self):
        # stages 2,4,6,8 are betting rounds, 1 is the preflop stage, 3 is dealing flop stage, 5 is dealing turn stage, 7 is dealing river stage, 9 is determine winner stage
        self.game_round = 1


        self.player1.chips = self.chips


        # will give the bots chips depending on the chip count of the user. 
        for player in (self.player2, self.player3, self.player4):
            player.chips = self.player1.chips + random.randint(-int((self.player1.chips * 0.4)),int((self.player1.chips * 0.4)))


        for player in self.current_players:
            self.deck.deal_hole_cards(player)


    def create_game_window(self): 
        self.poker_screen = Toplevel()
        self.poker_screen.geometry("1500x800")
        self.poker_screen.title("Poker Game")
        self.poker_screen.configure(bg = self.colour_scheme)
        canvas = Canvas(self.poker_screen, width = 1500, height = 800, bg = self.colour_scheme, highlightthickness = 0)
        canvas.pack()
        if self.colour_scheme == 'green':
            self.secondary_colour = "dark green"
        elif self.colour_scheme == '#9898F5':
            self.secondary_colour = "#905ef5"
        elif self.colour_scheme == '#ff9100':
            self.secondary_colour = "orange"
        else:
            self.secondary_colour = "#8f0085"


        canvas.create_oval(200, 150, 1300, 700, outline = self.secondary_colour, fill = self.secondary_colour)


        self.create_game_events_window()


        self.update_game_window()


    def update_game_window(self):
        user = Label(self.poker_screen, text = f'{self.player1.name}\n{self.player1.chips}', bg = self.colour_scheme, font = ("Calibri",25))
        user.place(x= 730,y= 725)
        bot1 = Label(self.poker_screen, text = f'{self.player2.name}\n{self.player2.chips}', bg = self.colour_scheme, font = ("Calibri",25))
        bot1.place(x= 75,y= 400)
        bot2 = Label(self.poker_screen, text = f'{self.player3.name}\n{self.player3.chips}', bg = self.colour_scheme, font = ("Calibri",25))
        bot2.place(x= 730,y= 50)
        bot3 = Label(self.poker_screen, text = f'{self.player4.name}\n{self.player4.chips}', bg = self.colour_scheme, font = ("Calibri",25))
        bot3.place(x= 1350,y= 400)
        pot = Label(self.poker_screen, text = f'The current pot size is: {self.pot_size}', bg = self.secondary_colour, font = ("Calibri",25))
        pot.place(x=625, y = 550)


        # code to allow user to bet first
        if self.player1.fold == False and self.player1.turn == True and self.player1.stake == 0 and self.player1.stake_gap == 0 and not self.player1.check:
            self.bet_button = Button(self.poker_screen, text = "Bet chips", height = "2", width = "8", font = ("Calibri",16),command = self.bet)
            self.bet_button.place(x= 1000,y= 650)


            self.check_button = Button(self.poker_screen, text = "Check", height = "2", width = "8", font = ("Calibri",16),command = self.check)
            self.check_button.place(x= 900,y= 650)


            self.fold_button = Button(self.poker_screen, text = "fold", height = "2", width = "8", font = ("Calibri",16),command = self.fold)
            self.fold_button.place(x= 1100,y= 650)


        # check to see if user needs to put in additional chips
        if self.player1.fold == False and self.player1.turn == True and self.player1.stake_gap != 0:
            # reset check attribute to false as user cannot check now
            self.player1.check = False


            self.required_chips = Label(self.poker_screen, bg = self.secondary_colour, text = f'You must bet {self.player1.stake_gap} chips to continue')
            self.required_chips.place(x=900, y= 625)


            self.bet_button = Button(self.poker_screen, text = "Call chips", height = "2", width = "8", font = ("Calibri",16),command = self.call_bet)
            self.bet_button.place(x= 900,y= 650)


            self.fold_button = Button(self.poker_screen, text = "fold", height = "2", width = "8", font = ("Calibri",16),command = self.dont_call_bet)
            self.fold_button.place(x= 1000,y= 650)


        # if user does not need to put in additional chips, incriment game round to deal next round of cards
        if self.player1.fold == False and self.player1.turn == True and self.player1.stake_gap == 0 and (self.player1.check or self.player1.all_in or self.player1.stake != 0):
            self.game_round += 1
            self.game_flow()


        # if user has folded, progress onwards with the game
        if self.player1.fold == True and self.game_round < 9 and self.game_round not in [1,3,5,7]:
            self.game_round +=1
            self.game_flow()


        # displays a message if the player has folded
        if self.player1 not in self.current_players:
            user_fold = Label(self.poker_screen, text = 'This player has folded', bg=self.secondary_colour)
            user_fold.place(x= 690, y=700)
        if self.player2 not in self.current_players:
            bot1_fold = Label(self.poker_screen, text = 'This player has folded', bg=self.secondary_colour)
            bot1_fold.place(x= 50, y=375)
        if self.player3 not in self.current_players:
            bot2_fold = Label(self.poker_screen, text = 'This player has folded', bg=self.secondary_colour)
            bot2_fold.place(x= 690, y=120)
        if self.player4 not in self.current_players:
            bot3_fold = Label(self.poker_screen, text = 'This player has folded', bg=self.secondary_colour)
            bot3_fold.place(x= 1300, y=375)


        # display the required tips on the screen:
        if self.tips_enabled == 'True':
            user_stats = StatsCalc(self.player1.cards)
            strength = round(float(user_stats.get_stats()) * 100)
            user_percentage = Label(self.poker_screen, bg = self.colour_scheme, text = f'Your current hand beats {strength}% of hands.', font = ("Calibri",25))
            user_percentage.place(x=100, y = 700)


            tips_canvas = Canvas(self.poker_screen, width = 500, height = 172)
            tips_canvas.place(x=0,y=0)
            tips_canvas.configure(bg = self.colour_scheme, highlightbackground= self.colour_scheme)
            tips_img = (Image.open(f'{ROUTETOIMAGES}hands_{self.colour_scheme}.png'))
            tips_img = ImageTk.PhotoImage(tips_img)
            tips_canvas.create_image(0,0, anchor = NW, image = tips_img)


        # display the necessary cards
        if self.game_round == 1:
            # display user hole cards
            canvas1 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas1.place(x=675,y=615)
            img1 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[0]}.png'))
            resized_img1 = img1.resize((75,110))
            new_img1 = ImageTk.PhotoImage(resized_img1)
            canvas1.create_image(0,0, anchor=NW, image=new_img1)


            canvas2 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas2.place(x=755,y=615)
            img2 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[1]}.png'))
            resized_image2 = img2.resize((75,110))
            new_image2 = ImageTk.PhotoImage(resized_image2)
            canvas2.create_image(0,0, anchor=NW, image=new_image2)


            # display bot1 hole cards
            canvas3 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas3.place(x=45,y=290)
            img3 =(Image.open(f'{ROUTETOIMAGES}cards/back_of_card.png'))
            resized_image3 = img3.resize((75,110))
            new_image3 = ImageTk.PhotoImage(resized_image3)
            canvas3.create_image(0,0, anchor=NW, image=new_image3)


            canvas4 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas4.place(x=125,y=290)
            img4 =(Image.open(f'{ROUTETOIMAGES}cards/back_of_card.png'))
            resized_image4 = img4.resize((75,110))
            new_image4 = ImageTk.PhotoImage(resized_image4)
            canvas4.create_image(0,0, anchor=NW, image=new_image4)


            # display bot2 hole cards
            canvas5 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas5.place(x=675,y=130)
            img5 =(Image.open(f'{ROUTETOIMAGES}cards/back_of_card.png'))
            resized_image5 = img5.resize((75,110))
            new_image5 = ImageTk.PhotoImage(resized_image5)
            canvas5.create_image(0,0, anchor=NW, image=new_image5)


            canvas6 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas6.place(x=755,y=130)
            img6 =(Image.open(f'{ROUTETOIMAGES}cards/back_of_card.png'))
            resized_image6 = img6.resize((75,110))
            new_image6 = ImageTk.PhotoImage(resized_image6)
            canvas6.create_image(0,0, anchor=NW, image=new_image6)


            # display bot3 hole cards
            canvas7 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas7.place(x=1305,y=290)
            img7 =(Image.open(f'{ROUTETOIMAGES}cards/back_of_card.png'))
            resized_image7 = img7.resize((75,110))
            new_image7 = ImageTk.PhotoImage(resized_image7)
            canvas7.create_image(0,0, anchor=NW, image=new_image7)


            canvas8 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas8.place(x=1385,y=290)
            img8 =(Image.open(f'{ROUTETOIMAGES}cards/back_of_card.png'))
            resized_image8 = img8.resize((75,110))
            new_image8 = ImageTk.PhotoImage(resized_image8)
            canvas8.create_image(0,0, anchor=NW, image=new_image8)


        elif self.game_round == 3:
            # show the 3 community cards on the screen
            canvas9 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas9.place(x=550,y=350)
            img9 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[2]}.png'))
            resized_image9 = img9.resize((75,110))
            new_image9 = ImageTk.PhotoImage(resized_image9)
            canvas9.create_image(0,0, anchor=NW, image=new_image9)


            canvas10 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas10.place(x=630,y=350)
            img10 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[3]}.png'))
            resized_image10 = img10.resize((75,110))
            new_image10 = ImageTk.PhotoImage(resized_image10)
            canvas10.create_image(0,0, anchor=NW, image=new_image10)


            canvas11 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas11.place(x=710,y=350)
            img11 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[4]}.png'))
            resized_image11 = img11.resize((75,110))
            new_image11 = ImageTk.PhotoImage(resized_image11)
            canvas11.create_image(0,0, anchor=NW, image=new_image11)


            if self.player1.fold or self.player1.all_in:
                self.game_round += 1 
                self.game_flow()


        elif self.game_round == 5:
            # show the turn card on the screen
            canvas12 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas12.place(x=790,y=350)
            img12 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[5]}.png'))
            resized_image12 = img12.resize((75,110))
            new_image12 = ImageTk.PhotoImage(resized_image12)
            canvas12.create_image(0,0, anchor=NW, image=new_image12)


            if self.player1.fold or self.player1.all_in:
                self.game_round += 1 
                self.game_flow()


        elif self.game_round == 7:
            # show the river card on the screen
            canvas13 = Canvas(self.poker_screen, width = 70, height = 100)
            canvas13.place(x=870,y=350)
            img13 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player1.cards[6]}.png'))
            resized_image13 = img13.resize((75,110))
            new_image13 = ImageTk.PhotoImage(resized_image13)
            canvas13.create_image(0,0, anchor=NW, image=new_image13)


            if self.player1.fold or self.player1.all_in:
                self.game_round += 1 
                self.game_flow()


        elif self.game_round >= 9:
            if len(self.current_players) == 1:
                winner_label = Label(self.poker_screen, text = f'The winner of this round is {self.current_players[0].name}!\nEveryone else has folded!', bg = self.secondary_colour, font = ("Calibri",25))
                winner_label.place(x=550,y=250)


                self.current_players[0].chips += self.pot_size
                winner = self.current_players[0]
                if self.player2 == winner:
                    canvas3 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas3.place(x=45,y=290)
                    img3 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player2.cards[0]}.png'))
                    resized_image3 = img3.resize((75,110))
                    new_image3 = ImageTk.PhotoImage(resized_image3)
                    canvas3.create_image(0,0, anchor=NW, image=new_image3)


                    canvas4 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas4.place(x=125,y=290)
                    img4 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player2.cards[1]}.png'))
                    resized_image4 = img4.resize((75,110))
                    new_image4 = ImageTk.PhotoImage(resized_image4)
                    canvas4.create_image(0,0, anchor=NW, image=new_image4)


                elif self.player3 == winner:
                    canvas5 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas5.place(x=675,y=130)
                    img5 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player3.cards[0]}.png'))
                    resized_image5 = img5.resize((75,110))
                    new_image5 = ImageTk.PhotoImage(resized_image5)
                    canvas5.create_image(0,0, anchor=NW, image=new_image5)


                    canvas6 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas6.place(x=755,y=130)
                    img6 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player3.cards[1]}.png'))
                    resized_image6 = img6.resize((75,110))
                    new_image6 = ImageTk.PhotoImage(resized_image6)
                    canvas6.create_image(0,0, anchor=NW, image=new_image6)


                elif self.player4 == winner:
                    canvas7 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas7.place(x=1305,y=290)
                    img7 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player4.cards[0]}.png'))
                    resized_image7 = img7.resize((75,110))
                    new_image7 = ImageTk.PhotoImage(resized_image7)
                    canvas7.create_image(0,0, anchor=NW, image=new_image7)


                    canvas8 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas8.place(x=1385,y=290)
                    img8 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player4.cards[1]}.png'))
                    resized_image8 = img8.resize((75,110))
                    new_image8 = ImageTk.PhotoImage(resized_image8)
                    canvas8.create_image(0,0, anchor=NW, image=new_image8)


            else:
                rank_names = ["high card","pair","two pair","three of a kind","straight","flush","full house","four of a kind","straight flush"]
                player_scores = []
                for player in self.current_players:
                    player_scores.append(self.get_hand_rank(player.cards))


                winners = []
                winning_score = max(player_scores)
                for i in range(len(player_scores)):
                    if player_scores[i] == winning_score:
                        winners.append(self.current_players[i])


                winning_hand = rank_names[int(winning_score)]


                if len(winners) == 1:
                    winner_label = Label(self.poker_screen, text = f'The winner of this round is {winners[0].name}!\nThey have won the pot with the hand {winning_hand}', bg = self.secondary_colour, font = ("Calibri",25))
                    winner_label.place(x=550,y=250)


                    winners[0].chips += self.pot_size


                elif len(winners) == 2:
                    winner_label = Label(self.poker_screen, text = f'The winners of this round are {winners[0].name} and {winners[1].name}!\nThey have won the pot with the hand {winning_hand}', bg = self.secondary_colour, font = ("Calibri",25))
                    winner_label.place(x=550,y=250)


                    winners[0].chips += self.pot_size // 2
                    winners[1].chips += self.pot_size // 2


                elif len(winners) == 3:
                    winner_label = Label(self.poker_screen, text = f'The winners of this round are {winners[0].name} and {winners[1].name} and {winners[2].name}!\nThey have won the pot with the hand {winning_hand}', bg = self.secondary_colour, font = ("Calibri",25))
                    winner_label.place(x=550,y=250)


                    winners[0].chips += self.pot_size // 3
                    winners[1].chips += self.pot_size // 3
                    winners[2].chips += self.pot_size // 3


                else:
                    winner_label = Label(self.poker_screen, text = f'Everyone has the same strength hand of {winning_hand}\nThe pot will be split equally', bg = self.secondary_colour, font = ("Calibri",25))
                    winner_label.place(x=550,y=250)


                    winners[0].chips += self.pot_size // 4
                    winners[1].chips += self.pot_size // 4
                    winners[2].chips += self.pot_size // 4 
                    winners[3].chips += self.pot_size // 4 


                # show the winner's cards or all cards
                if self.tips_enabled == 'True':
                    # show player2 cards
                    canvas3 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas3.place(x=45,y=290)
                    img3 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player2.cards[0]}.png'))
                    resized_image3 = img3.resize((75,110))
                    new_image3 = ImageTk.PhotoImage(resized_image3)
                    canvas3.create_image(0,0, anchor=NW, image=new_image3)


                    canvas4 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas4.place(x=125,y=290)
                    img4 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player2.cards[1]}.png'))
                    resized_image4 = img4.resize((75,110))
                    new_image4 = ImageTk.PhotoImage(resized_image4)
                    canvas4.create_image(0,0, anchor=NW, image=new_image4)


                    # show player3 cards
                    canvas5 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas5.place(x=675,y=130)
                    img5 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player3.cards[0]}.png'))
                    resized_image5 = img5.resize((75,110))
                    new_image5 = ImageTk.PhotoImage(resized_image5)
                    canvas5.create_image(0,0, anchor=NW, image=new_image5)


                    canvas6 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas6.place(x=755,y=130)
                    img6 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player3.cards[1]}.png'))
                    resized_image6 = img6.resize((75,110))
                    new_image6 = ImageTk.PhotoImage(resized_image6)
                    canvas6.create_image(0,0, anchor=NW, image=new_image6)


                    # show player4 cards
                    canvas7 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas7.place(x=1305,y=290)
                    img7 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player4.cards[0]}.png'))
                    resized_image7 = img7.resize((75,110))
                    new_image7 = ImageTk.PhotoImage(resized_image7)
                    canvas7.create_image(0,0, anchor=NW, image=new_image7)


                    canvas8 = Canvas(self.poker_screen, width = 70, height = 100)
                    canvas8.place(x=1385,y=290)
                    img8 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player4.cards[1]}.png'))
                    resized_image8 = img8.resize((75,110))
                    new_image8 = ImageTk.PhotoImage(resized_image8)
                    canvas8.create_image(0,0, anchor=NW, image=new_image8)


                else:
                    if self.player2 in winners:
                        canvas3 = Canvas(self.poker_screen, width = 70, height = 100)
                        canvas3.place(x=45,y=290)
                        img3 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player2.cards[0]}.png'))
                        resized_image3 = img3.resize((75,110))
                        new_image3 = ImageTk.PhotoImage(resized_image3)
                        canvas3.create_image(0,0, anchor=NW, image=new_image3)


                        canvas4 = Canvas(self.poker_screen, width = 70, height = 100)
                        canvas4.place(x=125,y=290)
                        img4 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player2.cards[1]}.png'))
                        resized_image4 = img4.resize((75,110))
                        new_image4 = ImageTk.PhotoImage(resized_image4)
                        canvas4.create_image(0,0, anchor=NW, image=new_image4)


                    if self.player3 in winners:
                        canvas5 = Canvas(self.poker_screen, width = 70, height = 100)
                        canvas5.place(x=675,y=130)
                        img5 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player3.cards[0]}.png'))
                        resized_image5 = img5.resize((75,110))
                        new_image5 = ImageTk.PhotoImage(resized_image5)
                        canvas5.create_image(0,0, anchor=NW, image=new_image5)


                        canvas6 = Canvas(self.poker_screen, width = 70, height = 100)
                        canvas6.place(x=755,y=130)
                        img6 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player3.cards[1]}.png'))
                        resized_image6 = img6.resize((75,110))
                        new_image6 = ImageTk.PhotoImage(resized_image6)
                        canvas6.create_image(0,0, anchor=NW, image=new_image6)


                    if self.player4 in winners:
                        canvas7 = Canvas(self.poker_screen, width = 70, height = 100)
                        canvas7.place(x=1305,y=290)
                        img7 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player4.cards[0]}.png'))
                        resized_image7 = img7.resize((75,110))
                        new_image7 = ImageTk.PhotoImage(resized_image7)
                        canvas7.create_image(0,0, anchor=NW, image=new_image7)


                        canvas8 = Canvas(self.poker_screen, width = 70, height = 100)
                        canvas8.place(x=1385,y=290)
                        img8 =(Image.open(f'{ROUTETOIMAGES}cards/{self.player4.cards[1]}.png'))
                        resized_image8 = img8.resize((75,110))
                        new_image8 = ImageTk.PhotoImage(resized_image8)
                        canvas8.create_image(0,0, anchor=NW, image=new_image8)
                        


            # update chip counts and player info 
            self.update_user_details()


            # give user option to play another game
            new_game_label = Label(self.poker_screen, text = "Do you want to play another game?", bg = self.colour_scheme, font = ("Calibri",25))
            new_game_label.place(x=1100, y=650)
            yes_button = Button(self.poker_screen, text = "Yes", bg = self.colour_scheme, width = 8, height = 2, command = self.play_again)
            yes_button.place(x=1200, y=700)
            no_button = Button(self.poker_screen, text = "No", bg= self.colour_scheme, width = 8, height = 2, command = self.dont_play_again)
            no_button.place(x=1300, y = 700)


        self.poker_screen.mainloop()


    def create_game_events_window(self):
        self.game_events_window = Tk()
        self.game_events_window.geometry("200x800")
        self.game_events_window.title('Game Events')
        self.game_events_window.configure(bg = self.colour_scheme)


        Label(self.game_events_window, text = "Preflop Stage", bg = self.colour_scheme, font = ("Calibri",15)).pack()






    def game_flow(self):
        self.check_current_players()
        # self.check_chips_of_players()


        # this is a line for testing purposes as it will allow me to see the hands of the players
        self.update_player_hand()


        if len(self.current_players) == 1:
            # set the round to be 9 so that when updating the game window it displays the winning algorithm
            self.game_round = 9


        else:
            # betting staged
            if self.game_round in [2,4,6,8]:
                self.betting()
                self.update_stakes()


                # if user has folded, run the betting again to ensure bots have bet same amount
                if self.player1.fold or self.player1.all_in:
                    self.check_current_players()
                    stake_gaps = []
                    for player in self.current_players:
                        if player != self.player1:
                            stake_gaps.append(player.stake_gap)
                    if max(stake_gaps) != 0:
                        for player in self.current_players:
                            player.check = False
                        self.betting()
                        self.check_current_players()
                    
                self.update_game_window()


            # deal flop
            elif self.game_round == 3:
                self.deck.deal_flop()


                for player in (self.player1, self.player2, self.player3, self.player4):
                    self.deck.add_community_cards_to_hand_after_flop(player)
                    self.update_player_hand()


                self.reset_player_stakes()
                self.update_game_window()


            # deal turn
            elif self.game_round == 5:
                self.deck.deal_turn_or_river()


                for player in (self.player1, self.player2, self.player3, self.player4):
                    self.deck.add_community_card_to_hand_after_turn(player)
                    self.update_player_hand()


                self.reset_player_stakes()
                self.update_game_window()


            # deal river
            elif self.game_round == 7:
                self.deck.deal_turn_or_river()


                for player in (self.player1, self.player2, self.player3, self.player4):
                    self.deck.add_community_card_to_hand_after_turn(player)
                    self.update_player_hand()


                self.reset_player_stakes()
                self.update_game_window()


            # check for winner
            else:
                # set game round to 9 so that it updates the board with the winner
                self.game_round = 9
                self.player1.turn = False
                self.update_game_window()


    def reset_player_stakes(self):
        for player in (self.player1, self.player2, self.player3, self.player4):
            player.check = False
            player.stake = 0
            player.stake_gap = 0


    def update_user_details(self):
        with open (USERDATABASE, 'r') as f:
            accounts = json.load(f)


        for i in accounts:
            if i[0] == self.player1.name:
                i[2]= self.player1.chips


        with open (USERDATABASE, 'w') as f:
            json.dump(accounts, f)
            
    def update_stakes(self):
        required_stake = max(self.player1.stake, self.player2.stake, self.player3.stake, self.player4.stake)
        for player in (self.player1, self.player2, self.player3, self.player4):
            if player.stake != required_stake and not player.fold and not player.all_in:
                player.stake_gap = required_stake - player.stake


    def play_again(self):
        self.poker_screen.destroy()
        new_game = Game(self.player1.chips, self.tips_enabled, self.colour_scheme, self.player1.name)


    def dont_play_again(self):
        self.poker_screen.destroy()
        self.game_events_window.destroy()
                
            
    def betting(self):
        # user has no action to do
        if self.player1.fold == True or self.player1.check == True or (self.player1.all_in == True and self.player1.chips == 0):
            pass


        # user decides to bet
        elif self.player1.stake_gap == 0:
            # adds the user bet to the pot
            self.pot_size += self.player1.stake
            self.player1.chips -= self.player1.stake


            # ensures that the other players will have to put in at least that many chips
            self.player2.stake_gap = self.player1.stake
            self.player3.stake_gap = self.player1.stake
            self.player4.stake_gap = self.player1.stake


            
        # bot has raised and user adds more chips
        else:
            current_stake = self.player1.stake
            if self.player1.stake_gap >= self.player1.chips:
                self.player1.all_in = True
                extra_stake = self.player1.chips
            else:
                extra_stake = self.player1.stake_gap


            self.pot_size += extra_stake
            self.player1.chips -= extra_stake
            self.player1.stake = current_stake + extra_stake
            self.player1.stake_gap = 0


        for player in (self.player2, self.player3, self.player4):
            self.bot_betting(player)
            self.update_stakes()


        if not self.player1.all_in or not self.player1.fold:
            self.player1.turn = True


    def bot_betting(self, player):
        bet = 0
        if player.fold == True:
            pass


        elif player.all_in == True:
            pass


        else:
            # this strength rating will be a percentage of hands that the player beats
            hand_strength = StatsCalc(player.cards)
            strength = hand_strength.get_stats()
            print(f'{player.name}: {strength}')
            
            if strength > 0.9:
                # if current bet is less than 15% of their chips, they will raise to 30% if they haven't bet already
                if player.stake_gap <= player.chips * 0.15 and player.stake == 0:
                    bet = player.chips * 0.3
                
                # if they already bet and they don't need to make another action, they will check
                elif player.stake_gap == 0 and player.stake != 0:
                    player.check = True


                # if they have already bet and someone raises then they will always call the raise
                else:
                    if player.stake_gap >= player.chips:
                        bet = player.chips
                        player.all_in = True
                    else:
                        bet = player.stake_gap


            elif strength > 0.8:
                # if current bet is less than 10% of their chips, they will raise to 15% if they haven't bet already
                if player.stake_gap <= player.chips * 0.1 and player.stake == 0:
                    bet = player.chips * 0.15


                # if they have already bet and they don't need to make another action, they will check
                elif player.stake_gap == 0 and player.stake != 0:
                    player.check = True


                # if they have already bet and someone raises,then they will call up to 60% of their chips
                elif player.stake_gap <= player.chips * 0.6:
                    bet = player.stake_gap


                # they will fold if they don't want to call the bet
                else:
                    player.fold = True


            elif strength > 0.7:
                # if current bet is 0, they will raise to 10% if they haven't bet already
                if player.stake_gap == 0 and player.stake == 0:
                    bet = player.chips * 0.1


                # if they have already bet and they don't need to make another action, they will check
                elif player.stake_gap == 0 and player.stake != 0:
                    player.check = True


                # if they have already bet and someone raises,then they will call up to 40% of their chips
                elif player.stake_gap <= player.chips * 0.4:
                    bet = player.stake_gap


                # they will fold if they don't want to call the bet
                else:
                    player.fold = True


            elif strength > 0.5: 
                # if they dont need to make an action, they will check
                if player.stake_gap == 0:
                    player.check = True


                # if they have to make an action, then they will call up to 30% of their chips
                elif player.stake_gap <= player.chips * 0.3:
                    bet = player.stake_gap


                # they will fold if they don't want to call the bet
                else:
                    player.fold = True


            else:
                # if they dont need to make an action, they will check
                if player.stake_gap == 0:
                    player.check = True


                # they will fold if they need to bet chips
                else:
                    player.fold = True


            if bet != 0:
                player.check = False


            if not player.check and not player.fold:
                player.stake_gap = 0
                bet = round(bet)


                if bet <0:
                    bet = bet * -1


                Label(self.game_events_window, text = f'{player.name} has bet {bet}', bg = self.colour_scheme, font = ("Calibri",15)).pack()


                player.stake += bet
                player.chips -= bet
                self.pot_size += bet


    def check(self):
        # removes the option buttons once they have pressed one
        self.bet_button.destroy()
        self.check_button.destroy()
        self.fold_button.destroy()


        self.player1.turn = False
        self.player1.check = True


        Label(self.game_events_window, text = f'{self.player1.name} has checked', bg = self.colour_scheme, font = ("Calibri",15)).pack()






        self.game_round += 1
        self.game_flow()


    def fold(self): 
        self.bet_button.destroy()
        self.check_button.destroy()
        self.fold_button.destroy()


        self.player1.turn = False
        self.player1.fold = True


        Label(self.game_events_window, text = f'{self.player1.name} has folded', bg = self.colour_scheme, font = ("Calibri",15)).pack()






        self.check_current_players()
        if len(self.current_players) == 1:
            self.game_round = 9
            self.update_game_window()
        else:
            self.game_round += 1
            self.game_flow()


    def bet(self):
        self.bet_button.destroy()
        self.check_button.destroy()
        self.fold_button.destroy()


        self.player1.turn = False


        self.bet_screen = Toplevel(self.poker_screen)
        self.bet_screen.geometry("200x150")
        self.bet_screen.configure(bg = self.colour_scheme)


        self.bet_amount = StringVar()
        Label(self.bet_screen, text = "Please enter bet amount below", bg = self.colour_scheme).pack()
        self.bet_entry = Entry(self.bet_screen, textvariable=self.bet_amount)
        self.bet_entry.pack()


        Button(self.bet_screen, text = "Enter", width = 10, height = 1,command = self.place_bet).pack()
            
    def place_bet(self):
        self.bet_screen.destroy()


        if int(self.bet_amount.get()) >= self.player1.chips:
            self.player1.all_in = True
            self.player1.stake = self.player1.chips


        else:
            self.player1.stake = int(self.bet_amount.get())


        Label(self.game_events_window, text = f'{self.player1.name} has bet {self.player1.stake}', bg = self.colour_scheme, font = ("Calibri",15)).pack()
        
        self.game_round += 1
        self.game_flow()


    def call_bet(self):
        self.bet_button.destroy()
        self.fold_button.destroy()
        self.required_chips.destroy()


        self.player1.turn = False


        Label(self.game_events_window, text = f'{self.player1.name} has bet {self.player1.stake_gap}', bg = self.colour_scheme, font = ("Calibri",15)).pack()






        self.betting()
        self.update_game_window()


    def dont_call_bet(self):
        self.bet_button.destroy()
        self.fold_button.destroy()
        self.required_chips.destroy()


        self.player1.turn = False
        self.player1.fold = True


        Label(self.game_events_window, text = f'{self.player1.name} has folded', bg = self.colour_scheme, font = ("Calibri",15)).pack()


        self.betting()
        self.update_game_window()


    def update_player_hand(self):
        with open (ROUTETOPLAYERHANDS, 'w') as f:
            info = []
            for player in self.current_players:
                info.append(player.name)
                info.extend(player.cards)


            json.dump(info, f)


    def check_current_players(self):
        for i in self.current_players:
            if i.fold == True:
                self.current_players.remove(i)


    def check_chips_of_players(self):
        # if the user runs out of chips, this will top them back up to 5000, instead of having to create a new account
        if self.player1.chips == 0:
            self.player1.chips += 5000
        
        # if a bot runs out of chips, they will be assinged new chips depening on the user's chip count
        for player in (self.player2, self.player3, self.player4):
            if player.chips == 0:
                player.chips += self.player1.chips + random.randint(-int((self.player1.chips * 0.4)),int((self.player1.chips * 0.4)))
