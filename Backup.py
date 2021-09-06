import sqlite3
import random
import string
import sys
from tkinter import *
from tkinter import font as tkFont


class PasswordSaver:

    def __init__(self):
        self.database = sqlite3.connect("hackathon_database.db")
        self.curs = self.database.cursor()

        self.curs.execute("""CREATE TABLE IF NOT EXISTS users_answers
        (
        question text, 

        answer text)""")

        self.curs.execute("""CREATE TABLE IF NOT EXISTS users
        (
        name text,
        code text
        )""")  # This creates a users table if it doesn't exist already.

        query = """CREATE TABLE IF NOT EXISTS users_joins
        (user_id integer references users,
        answers_id integer references users_answers)
        """
        self.curs.execute(query)
        self.start()

    def start(self):
        first_time = input("If you are a current user, type 'User' or type 'New' if you are a new user: ").strip()
        if first_time == "New":
            self.first_time_users()
        elif first_time == "User":
            self.current_user()
        else:
            print("You can only answer 'User' or 'New': ")
            self.start()

    def first_time_users(self):
        name = input("Please Enter your name: ").strip()  # Asks user for name.
        got_a_unique_code = False
        while not got_a_unique_code:
            code = self.code_generator()  # Generates unique code for him as long as the code is not already in "users" table
            self.curs.execute("SELECT * FROM users WHERE code = :code", {'code': code})
            result = self.curs.fetchall()

            if not result:
                with self.database:
                    self.curs.execute("INSERT INTO users VALUES (:name, :code)", {"name": name, "code": code})

                user_id = self.curs.lastrowid
                got_a_unique_code = True
                print(
                    f"Your unique code is {code} \nPlease remember this, as all your saved passwords can only be viewed"
                    f" when you login in using your name and code.")
                print()
                print(
                    "Since this is your first time using this program, you will need to set up some security questions")
                qs = self.select_security_questions()
                for q in qs:
                    answer = input(q).strip()
                    with self.database:
                        self.curs.execute("INSERT INTO users_answers VALUES (:question, :answer)",
                                          {"question": q, "answer": answer.lower()})
                        last_id_answer = self.curs.lastrowid
                        self.curs.execute("INSERT INTO users_joins VALUES (:user_id, :answers_id)",
                                          {"user_id": user_id, "answers_id": last_id_answer})

                print("Great! You're all set now.")
                print()
                print("You can go login and begin your journey of having to remember only one password from now.")
                self.start()

    def current_user(self):
        code = input("Please enter your code: ").strip()
        self.curs.execute("SELECT * FROM users WHERE code =:code", {'code': code})
        result = self.curs.fetchall()

        if result:
            code = result[0][1]
            print("You will only be logged in if you answer your security questions correctly.")
            self.curs.execute("SELECT rowid FROM users WHERE code = :code", {"code": code})
            id_of_our_user = self.curs.fetchall()[0][0]

            self.curs.execute("SELECT answers_id FROM users_joins WHERE user_id = :id_of_our_user",
                              {"id_of_our_user": id_of_our_user})
            answer_ids = self.curs.fetchall()
            count = 0
            for ids in answer_ids:
                qid = ids[0]
                self.curs.execute("SELECT * FROM users_answers WHERE rowid = :qid", {"qid": qid})
                question_answer_is = self.curs.fetchone()
                given_ans = input(question_answer_is[0])
                if given_ans.lower() == question_answer_is[1]:
                    count += 1

            if count == 2:
                print("You are now logged in as ", result[0][0])
                query = """CREATE TABLE IF NOT EXISTS {} 
                (
                website text,
                password text
                )""".format(code)

                self.curs.execute(query)
                self.users_powers(
                    code)  # We pass in the code because it is the table's name which stores our users information.

        else:
            print("You arenot a current user")
            self.start()

    def users_powers(self, table_name):
        print()
        print("You can now search, save, or update your passwords")
        get_input = input(
            "Type 'Search' to search for a password, 'Update' to update a password, 'Save' to save a new password, or '"
            "Q' to exit: ").strip()
        if get_input == "Save":
            self.save_a_password(table_name)
        elif get_input == "Search":
            self.search_for_a_password(table_name)
        elif get_input == "Update":
            self.update_a_password(table_name)
        elif get_input == 'Q':
            sys.exit()
        else:
            print("Please only input the accepted values.")
            self.users_powers(table_name)

    def save_a_password(self, table_name):
        website = input(
            "The name of the website (Enter like Facebook, Google, Youtube, meaning only the first letter capital and n"
            "o urls): ").strip()
        self.curs.execute("SELECT * FROM {} WHERE website=:website".format(table_name), {"website": website})
        result = self.curs.fetchall()
        if not result == []:
            what_to_do = (
                "Your already have a password saved for this website. Go ahead and save if it's for a different account"
                ".\nType 'g' to go ahead and save, 'u' to update, 's' to search for the password, or 'q' to quit: ")
            if what_to_do == 'g':
                password = input("Your password of the account in the website: ").strip()
                with self.database:
                    self.curs.execute("INSERT INTO {} VALUES (:website, :password)".format(table_name),
                                      {"website": website, "password": password})

                print("Your password has been saved. It will show up when you search for the passwords.")
                self.users_powers(table_name)
            elif what_to_do == 'u':
                self.update_a_password(table_name)
            elif what_to_do == 's':
                self.search_for_a_password(table_name)
            elif what_to_do == 'q':
                sys.exit()

        password = input("Your password of the account in the website: ").strip()
        with self.database:
            self.curs.execute("INSERT INTO {} VALUES (:website, :password)".format(table_name),
                              {"website": website, "password": password})

        print("Your password has been saved. It will show up when you search for the passwords.")
        self.users_powers(table_name)

    def search_for_a_password(self, table_name):
        self.curs.execute("SELECT * FROM {}".format(table_name))
        result = self.curs.fetchall()
        if not result:
            print("You have no passwords saved yet. Let's get started with that.")
            self.users_powers(table_name)
        else:
            print("Website\t\tPassword")
            print("--------\t\t--------")
            for tups in result:
                print(f"{tups[0]}\t{tups[1]}")

            self.users_powers(table_name)

    def update_a_password(self, table_name):
        pass

    @staticmethod
    def code_generator():
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(12))
        return result_str

    def select_security_questions(self):
        security_qs = ["What is your pet's name? ", "What is the name of the town you were born in? ",
                       "What is your first babysitter's name? "]
        q1 = 1
        q2 = 1
        while q1 == q2:
            q1 = random.randint(0, len(security_qs) - 1)
            q2 = random.randint(0, len(security_qs) - 1)

        return [security_qs[q1], security_qs[q2]]


if __name__ == '__main__':
    ins1 = PasswordSaver()
