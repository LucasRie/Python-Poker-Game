import json
from tkinter import *
from config import *

class User:
    def __init__(self):
        self.loggedin = False
        while not self.loggedin:
            with open (USERDATABASE,'r') as f:
                self.accounts = json.load(f)
            self.create_login_screen()


    def create_login_screen(self):
        self.logging_screen = Tk()
        self.logging_screen.geometry("300x150")
        self.logging_screen.title("Log in Screen")


        Label(text="Welcome to my Poker Game",width = "300", height = "2",font = ("Calibir",20)).pack()
        Label(text='').pack
        Button(text = "Login", height = "2", width = "10", command = self.login).pack()
        Label(text='').pack
        Button(text = "Register", height = "2", width = "10", command = self.register).pack()
        self.logging_screen.mainloop()


    def login(self):
        self.login_screen = Toplevel(self.logging_screen)
        self.login_screen.title("Log In")
        self.login_screen.geometry("350x250")


        self.username = StringVar()
        self.password = StringVar()


        Label(self.login_screen, text= "Please enter details below").pack()
        Label(self.login_screen, text='').pack()


        Label(self.login_screen, text = "Username: *").pack()
        self.username_entry = Entry(self.login_screen, textvariable = self.username)
        self.username_entry.pack()
        Label(self.login_screen, text = "Password: *").pack()
        self.password_entry = Entry(self.login_screen, textvariable = self.password)
        self.password_entry.pack()


        Button(self.login_screen, text = "Log In", width = 10, height = 1, command = self.login_user).pack()


    def login_user(self):
        self.username_info = self.username.get()
        password_info = self.password.get()


        # hash password
        password = self.hash(password_info)


        exists = False
        for i in self.accounts:
            if self.username_info == i[0] and password == i[1]:
                exists = True
                self.chips = i[2]
                self.tips_enabled = i[3]
                self.colour_scheme = i[4]                
        
        if exists:
            self.loggedin = True
            Label(self.login_screen, text = "Log In Success", fg = "green", font = ("Calibri",11)).pack()
            Button(self.login_screen, text = "Close Window",width = 10, height = 1, command = self.login_screen.destroy and self.logging_screen.destroy).pack()


        else:
            Label(self.login_screen, text = "Incorrect username or password. \nPlease enter new details or register.").pack()


    def register(self):
        self.register_screen = Toplevel(self.logging_screen)
        self.register_screen.title("Register")
        self.register_screen.geometry("350x250")


        self.username = StringVar()
        self.password = StringVar()


        Label(self.register_screen, text= "Please enter details below").pack()
        Label(self.register_screen, text='').pack()


        Label(self.register_screen, text = "Username: *").pack()
        self.username_entry = Entry(self.register_screen, textvariable = self.username)
        self.username_entry.pack()
        Label(self.register_screen, text = "Password: *").pack()
        self.password_entry = Entry(self.register_screen, textvariable = self.password)
        self.password_entry.pack()


        Button(self.register_screen, text = "Register", width = 10, height = 1, command = self.register_user).pack()


    def register_user(self):
        self.username_info = self.username.get()
        password_info = self.password.get()


        valid_username = self.verify_username(self.username_info)
        valid_password = self.verify_password(password_info)


        if valid_username and valid_password:
            self.add_details(self.username_info,password_info)
                       
        elif not valid_username:
            Label(self.register_screen,text = 'Your username selected is not valid.\nPlease enter a new one or log in.').pack()


        elif not valid_password:
            Label(self.register_screen,text = 'Your password selected is not valid.\nPlease enter a new one.').pack()


    def verify_username(self,username):
        # verfiy length not longer than 18 characters
        if len(username) >= 18:
            return False


        # verify username not already in use
        for i in self.accounts:
            if i[0] == username:
                return False
        return True


    def verify_password(self,password):
        if len(password) >=8:
            upper, lower, number, special = 0,0,0,0
            for i in password:
                if i.isupper():
                    upper +=1
                elif i.islower():
                    lower += 1
                elif i.isdigit():
                    number +=1
                elif i in ['@','!','%','_','+','?']:
                    special += 1


            if upper >=1 and lower >=1 and number >= 1 and special >= 1 and upper + lower + number + special == len(password):
                return True
        return False


    def add_details(self, username, password):
        # hash the password
        password = self.hash(password)


        newAccount = [username, password, 5000, "False", 'green']
        self.accounts.append(newAccount)
        with open (USERDATABASE,'w') as f:
            json.dump(self.accounts,f)
        self.chips = 5000
        self.tips_enabled = "False"
        self.colour_scheme = 'green'
        self.loggedin = True


        self.username_entry.delete(0,END)
        self.password_entry.delete(0,END)


        Label(self.register_screen, text = "Registration Success", fg = "green", font = ("Calibri",11)).pack()
        Button(self.register_screen, text = "Close Window",width = 10, height = 1, command = self.register_screen.destroy and self.logging_screen.destroy).pack()


    def get_facts(self):
        return self.username_info, self.loggedin, self.chips, self.tips_enabled, self.colour_scheme  


    def update_player_info(self, new_chips, new_tips_status, new_colour):
        with open (USERDATABASE,'r') as f:
            accounts = json.load(f)


        for i in accounts:
            if i[0] == self.username.get():
                i[3], i[4] = new_tips_status, new_colour


                
        with open (USERDATABASE,'w') as f:
            json.dump(accounts,f)


    def hash(self, password):
        password = self.convert_to_binary_ASCII(password)
        password = self.add_padding(password)
        round1_output = self.operate_round_1(password)
        round2_output = self.operate_round_2(password)
        round3_output = self.operate_round_3(password)
        round4_output = self.operate_round_4(password)


        half1 = round1_output + round3_output
        half2 = round2_output + round4_output


        # Apply XOR on these two
        hashed_result = ''
        for i in range(256):
            if (half1[i] == '1' and half2[i] == '0') or (half1[i] == '0' and half2[i] == '1'):
                hashed_result += '1'
            else:
                hashed_result += '0'
        
        return self.convert_binary_to_character(hashed_result)
    
    def convert_to_binary_ASCII(self, password):
        new_pass = []
        for i in password:
            new_pass.append('{:08b}'.format((ord(i))))
        
        return new_pass
    
    def convert_binary_to_character(self, string):
        bytes = [string[n:n+8] for n in range(0,len(string), 8)]


        new_string = ''
        for i in bytes:
            if int(i,2) >= 0 and int(i,2) <= 32:
                character = chr(int(i,2) + 33)
            
            elif int(i,2) >=127 and int(i,2) <=160:
                character = chr(int(i,2) + 34)


            elif int(i,2) == 173:
                character = chr(174)


            else:
                character = chr(int(i,2))


            if int(i,2) == 34 or character == '"':
                character = chr(35)


            new_string += character


        return new_string
    
    def add_padding(self,password):
        total_bits = 0
        for i in password:
            total_bits += 8


        padding_bits = 448 - total_bits
        password.append('10000000')
        extra_bytes = (padding_bits - 8) // 8
        for i in range(extra_bytes):
            password.append('00000000')


        # add length of password to end
        length = '{:08b}'.format(total_bits)
        remaining_bits = 64 - len(length)
        length = '0' * remaining_bits + length
        length_as_bytes = [length[n:n+8] for n in range(0,len(length), 8)]
        password.extend(length_as_bytes)


        return password
    
    def operate_round_1(self,password):
        words = [password[n:n+4] for n in range(0,len(password), 4)]


        block1 = words[0] + words[1] + words[2] + words[3]
        block2 = words[4] + words[5] + words[6] + words[7]
        block3 = words[8] + words[9] + words[10] + words[11]
        block4 = words[12] + words[13] + words[14] + words[15]


        block1 = ''.join(block1)
        block2 = ''.join(block2)
        block3 = ''.join(block3)
        block4 = ''.join(block4)


        # apply funcion F
        left_bracket = ''
        for i in range(128):
            if block1[i] == '1' and block3[i] == '1':
                left_bracket += '1'
            else:
                left_bracket += '0'


        right_bracket = ''
        for i in range(128):
            if block2[i] == '0' and block4[i] == '1':
                right_bracket += '1'
            else:
                right_bracket += '0'


        output = ''
        for i in range(128):
            if left_bracket[i] == '1' or right_bracket[i] == '1':
                output += '1'
            else:
                output += '0'


        return output


    def operate_round_2(self,password):
        words = [password[n:n+4] for n in range(0,len(password), 4)]
        block1 = words[1] + words[6] + words[11] + words[0]
        block2 = words[5] + words[10] + words[15] + words[4]
        block3 = words[9] + words[14] + words[3] + words[8]
        block4 = words[13] + words[2] + words[7] + words[12]


        block1 = ''.join(block1)
        block2 = ''.join(block2)
        block3 = ''.join(block3)
        block4 = ''.join(block4)


        # apply function G
        left_bracket = ''
        for i in range(128):
            if block2[i] == '1' and block4[i] == '1':
                left_bracket += '1'
            else:
                left_bracket += '0'


        right_bracket = ''
        for i in range(128):
            if block3[i] == '1' and block1[i] == '0':
                right_bracket += '1'
            else:
                right_bracket += '0'


        output = ''
        for i in range(128):
            if left_bracket[i] == '1' or right_bracket[i] == '1':
                output += '1'
            else:
                output += '0'


        return output


    def operate_round_3(self,password):
        words = [password[n:n+4] for n in range(0,len(password), 4)]
        block1 = words[5] + words[8] + words[11] + words[14]
        block2 = words[1] + words[4] + words[7] + words[10]
        block3 = words[13] + words[0] + words[3] + words[6]
        block4 = words[9] + words[12] + words[15] + words[2]


        block1 = ''.join(block1)
        block2 = ''.join(block2)
        block3 = ''.join(block3)
        block4 = ''.join(block4)


        # apply function H
        left_bracket = ''
        for i in range(128):
            if (block1[i] == '1' and block2[i] == '0') or (block1[i] == '0' and block2[i] == '1'):
                left_bracket += '1'
            else:
                left_bracket += '0'


        right_bracket = ''
        for i in range(128):
            if (block3[i] == '1' and block4[i] == '0') or (block3[i] == '0' and block4[i] == '1'):
                right_bracket += '1'
            else:
                right_bracket += '0'


        output = ''
        for i in range(128):
            if left_bracket[i] == '1' or right_bracket[i] == '1':
                output += '1'
            else:
                output += '0'


        return output


    def operate_round_4(self,password):
        words = [password[n:n+4] for n in range(0,len(password), 4)]
        block1 = words[0] + words[7] + words[14] + words[5]
        block2 = words[12] + words[3] + words[10] + words[1]
        block3 = words[8] + words[15] + words[6] + words[13]
        block4 = words[4] + words[11] + words[2] + words[9]


        block1 = ''.join(block1)
        block2 = ''.join(block2)
        block3 = ''.join(block3)
        block4 = ''.join(block4)


        # apply function I
        B_OR_NOT_D = ''
        for i in range(128):
            if block2[i] == '1' or block4[i] == '0':
                B_OR_NOT_D += '1'
            else:
                B_OR_NOT_D += '0'


        left_bracket = ''
        for i in range(128):
            if (block1[i] == '1' and B_OR_NOT_D[i] == '0') or (block1[i] == '0' and B_OR_NOT_D[i] == '1'):
                left_bracket += '1'
            else:
                left_bracket += '0'


        right_bracket = ''
        for i in range(128):
            if (block3[i] == '1' and B_OR_NOT_D[i] == '0') or (block3[i] == '0' and B_OR_NOT_D[i] == '1'):
                right_bracket += '1'
            else:
                right_bracket += '0'


        output = ''
        for i in range(128):
            if (left_bracket[i] == '1' and right_bracket[i] == '0') or (left_bracket[i] == '0' and right_bracket[i] == '1'):
                output += '1'
            else:
                output += '0'
                
        return output
