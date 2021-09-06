import sqlite3
import random
import string
import sys
from tkinter import *
from tkinter import font as tkfont


questions = ["What high school did you attend?", "What’s your favorite movie?",
             "What is the name of your favorite pet?", "What is your favorite food?",
             "What was your favorite childhood toy?", "What was the make of your first car?",
             "In what city were you born?"]
CLEAR_ALL = ['label1', 'label2', 'enter', 'code_entry', 'welcome_text', 'broad_security', 'spec_security1',
             'ans_entry1', 'spec_security2', 'ans_entry2', 'enter_secq2', 'enter_secq1', 'shiftcreateacc', 'save',
             'createacc_invalid_message', 'invalid_code_message', 'code_text', 'code_warning', 'name_entry',
             'enter_name', 'invalid_name', 'next1', 'next2', 'sqmenu', 'sqanswer', 'set_answer', 'back', 'select',
             'done', 'CreateAccEndMessage1', 'CreateAccEndMessage2', 'LoggedInMessage', 'ViewPasswordMessage', 'search',
             'savewebsite', 'WebsiteNameMessage', 'AlreadySavedMessage', 'savepassword1', 'EnterPasswordMessage1',
             'PasswordSavedMessage', 'retrn', 'new', 'view', "savePasswordAnywayBt", "saveAnywayBt", 'savepassword2',
             'savePasswordBt', 'EnterPasswordMessage2', 'savedmessage', 'SearchInsteadBt', 'enterwebsite', 'website',
             'password', 'websites', 'passwords', 'NewPasscode', 'NoneSavedYet']

BUTTON_COLOR = "DodgerBlue4"
root = Tk()
BUTTON_FONT = tkfont.Font(family='Helvetica', size="20")
WELCOME_FONT = tkfont.Font(family='helvetica', size="40")

root.geometry("900x513")
root.wm_attributes('-transparent', True)
background = PhotoImage(file="BGImageLightTech.png")

canvas = Canvas(root, width=900, height=504)

canvas.create_text(450, 200, text="Welcome to Password Saver!\nHere, you can save passwords\nand"
                                  " access them with\nthe press of a button!",
                   font=WELCOME_FONT, fill='#00008B')

counter = 0


def init():
    global curs, database
    database = sqlite3.connect("hackathon_database.db")
    curs = database.cursor()

    curs.execute("""CREATE TABLE IF NOT EXISTS users_answers
    (
    question text, 

    answer text)""")

    curs.execute("""CREATE TABLE IF NOT EXISTS users
    (
    name text,
    code text
    )""")  # This creates a users table if it doesn't exist already.

    query = """CREATE TABLE IF NOT EXISTS users_joins
    (user_id integer references users,
    answers_id integer references users_answers)
    """
    curs.execute(query)
    start()


def createacc():
    clearCanvas([])
    canvas.create_text(450, 100, text='Create New Account', font=('Helvetica', 40), fill='#00008B', tags="label1")
    canvas.create_text(450, 200, text='Enter Your Name', font=('Helvetica', 20), fill='#00008B', tags="label2")
    name_entry = Entry(root)
    canvas.create_window(450, 300, window=name_entry, tags="name_entry")
    name_entry.config(highlightbackground='black')

    def EnterName():
        name = name_entry.get().strip()
        if name == '':
            canvas.create_text(450, 350, text='please enter a name in the field above',
                               font=('Helvetica', 20), tags='invalid_name')
            return
        got_a_unique_code = False
        while not got_a_unique_code:
            code = code_generator()  # Generates unique code for him as long as the code is not already in "users" table
            curs.execute("SELECT * FROM users WHERE code = :code", {'code': code})
            result = curs.fetchall()

            if not result:
                with database:
                    curs.execute("INSERT INTO users VALUES (:name, :code)", {"name": name, "code": code})

                user_id = curs.lastrowid
                got_a_unique_code = True
                clearCanvas([])
                print(code)
                canvas.create_text(450, 100, text='Your unique code is {}'.format(code), font=('Helvetica', 40),
                                   fill='#00008B', tags='code_text')
                canvas.create_text(450, 200, text='Please remember this, as all your saved passwords can only be viewe'
                                                  'd\nwhen you login in using your name and code. The code has been\n'
                                                  'printed in the console as well for you to copy.',
                                   font=('Helvetica', 20), tags='code_warning')

                def SecuritySetExlp():
                    clearCanvas([])
                    canvas.create_text(450, 100, text="Since this is your first time using this program,\n"
                                                      "you will need to set up some security questions",
                                       font=('Helvetica', 40),
                                       fill='#00008B', tags='code_text')

                    canvas.create_text(450, 200, text="Click the drop-down menu to\n"
                                                      "select a question you want to answer",
                                       font=('Helvetica', 20),
                                       fill='#00008B', tags='code_text')
                    canvas.create_text(450, 300, text="Make sure you answer at least 2!",
                                       font=('Helvetica', 20),
                                       fill='#00008B', tags='code_text')

                    def SetSecurityQ():
                        clearCanvas([])
                        variable = StringVar(root)
                        variable.set(questions[0])
                        sqmenu = OptionMenu(root, variable, *questions)
                        canvas.create_window(450, 200, window=sqmenu, tags='sqmenu')

                        def AskAnswer():
                            clearCanvas([])
                            q = variable.get().strip()
                            sqanswer = Entry(root)
                            canvas.create_window(450, 300, window=sqanswer, tags='sqanswer')
                            updated_list(questions, q)

                            def SetAnswer():
                                answer = sqanswer.get()
                                with database:
                                    curs.execute("INSERT INTO users_answers VALUES (:question, :answer)",
                                                      {"question": q, "answer": answer.lower()})
                                    last_id_answer = curs.lastrowid
                                    curs.execute("INSERT INTO users_joins VALUES (:user_id, :answers_id)",
                                                      {"user_id": user_id, "answers_id": last_id_answer})
                                SetSecurityQ()

                            set_answer = Button(text="Set As Answer", command=SetAnswer)
                            canvas.create_window(400, 350, window=set_answer, tags='set_answer')

                        def CreateAccEnd():
                            if len(questions) > 5:
                                SetSecurityQ()
                            else:
                                for i in CLEAR_ALL:
                                    canvas.delete(i)
                                    canvas.create_text(450, 100, text="Great! You're all set now.", font=WELCOME_FONT,
                                                       tags='CreateAccEndMessage1')
                                    canvas.create_text(450, 200, text="You can go login and begin your journey of havi"
                                                                      "ng\nto remember only one password from now.",
                                                       font=('Helvetica', 20),
                                                       tags='CreateAccEndMessage2')

                        done = Button(text='Done', command=CreateAccEnd)
                        canvas.create_window(480, 350, window=done, tags='done')

                        select = Button(text='Select', command=AskAnswer)
                        canvas.create_window(420, 350, window=select, tags='select')
                        start()
                    next2 = Button(text='Next', command=SetSecurityQ)
                    canvas.create_window(450, 350, window=next2, tags='next2')

                next1 = Button(text='Next', command=SecuritySetExlp)
                canvas.create_window(450, 350, window=next1, tags='next1')

    enter_name = Button(text='Enter', command=EnterName)
    canvas.create_window(520, 300, window=enter_name, tags='enter_name')


def home():
    for i in CLEAR_ALL:
        canvas.delete(i)
    canvas.create_text(450, 200, text="Welcome to Password Saver!\nHere, you can save passwords\nand"
                                      " access them with\nthe press of a button!",
                       font=WELCOME_FONT, fill='#00008B', tags="welcome_text")


def login():
    for i in CLEAR_ALL:
        canvas.delete(i)
    canvas.create_text(450, 100, text='Login', font=('Helvetica', 40), fill='#00008B', tags="label1")
    canvas.create_text(450, 200, text='Enter Your Code', font=('Helvetica', 20), fill='#00008B', tags="label2")
    code_entry = Entry(root)
    canvas.create_window(450, 300, window=code_entry, tags="code_entry")
    code_entry.config(highlightbackground='black')

    def EnterCode():
        global result, code
        code = code_entry.get().strip()
        curs.execute("SELECT * FROM users WHERE code =:code", {'code': code})
        result = curs.fetchall()

        if result:
            code = result[0][1]
            clearCanvas([])
            curs.execute("SELECT rowid FROM users WHERE code = :code", {"code": code})
            id_of_our_user = curs.fetchall()[0][0]

            curs.execute("SELECT answers_id FROM users_joins WHERE user_id = :id_of_our_user",
                         {"id_of_our_user": id_of_our_user})
            answer_ids = curs.fetchall()

            canvas.create_text(450, 200, text="You will only be logged in if you\n"
                                              "answer your security questions correctly.", font=('Helvetica', 40),
                               fill="#00008B", tags="broad_security")
            global counter
            if counter == 0:
                clearCanvas(['broad_security'])
                ids = answer_ids[0]
                qid = ids[0]
                curs.execute("SELECT * FROM users_answers WHERE rowid = :qid", {"qid": qid})
                question_answer_is = curs.fetchone()
                canvas.create_text(450, 300, text="Answer the security question: {}".format(question_answer_is[0]),
                                   font=('Helvetica', 20),
                                   fill="#00008B", tags="spec_security1")
                ans_entry1 = Entry(root)
                canvas.create_window(450, 350, window=ans_entry1, tags='ans_entry1')

                def verifyQ1():
                    clearCanvas([])
                    global counter
                    given_ans = ans_entry1.get()
                    if given_ans.lower() == question_answer_is[1].lower():
                        print(given_ans, question_answer_is[1])
                        print(type(given_ans), type(question_answer_is[1]))
                        counter += 1
                        EnterCode()

                enter_secq1 = Button(text='Enter', command=verifyQ1)
                canvas.create_window(520, 350, window=enter_secq1, tags='enter_secq1')

            if counter == 1:
                clearCanvas(['broad_security'])
                ids = answer_ids[1]
                qid = ids[0]
                curs.execute("SELECT * FROM users_answers WHERE rowid = :qid", {"qid": qid})
                question_answer_is = curs.fetchone()
                canvas.create_text(450, 300, text="Answer the security question: {}".format(question_answer_is[0]),
                                   font=('Helvetica', 20),
                                   fill="#00008B", tags="spec_security2")
                ans_entry2 = Entry(root)
                canvas.create_window(450, 350, window=ans_entry2, tags='ans_entry2')

                def verifyQ2():
                    clearCanvas([])
                    global counter
                    given_ans = ans_entry2.get()
                    if given_ans.lower() == question_answer_is[1]:
                        counter += 1
                        EnterCode()

                enter_secq2 = Button(text='Enter', command=verifyQ2)
                canvas.create_window(520, 350, window=enter_secq2, tags='enter_secq2')
            if counter == 2:
                canvas.delete('login', 'createacc')
                Logout = Button(root, text='Logout',
                                fg='black',
                                bd=10, highlightthickness=4,
                                highlightcolor=BUTTON_COLOR,
                                highlightbackground=BUTTON_COLOR,
                                borderwidth=4,
                                font=BUTTON_FONT,
                                command=start)
                Logout_canvas = canvas.create_window(70, 5,
                                                     anchor="nw",
                                                     window=Logout, tags='logout')

                counter = 0
                clearCanvas([])
                # canvas.create_text(450, 100, text="You are now logged in as {}".format(result[0][0]),
                #                    font=WELCOME_FONT)
                query = """CREATE TABLE IF NOT EXISTS {} 
                    (
                    website text,
                    password text
                    )""".format(code
                                )

                curs.execute(query)
                users_powers(
                    code)

        else:
            clearCanvas([])
            canvas.create_text(450, 100, text="This code is not valid",
                               font=('Helvetica', 40),
                               fill="#00008B", tags="invalid_code_message")
            canvas.create_text(450, 200, text="Create a new account to join",
                               font=('Helvetica', 20),
                               fill="#00008B", tags="createacc_invalid_message")
    enter = Button(text='Enter', command=EnterCode)
    canvas.create_window(520, 300, window=enter, tags='enter')


def users_powers(table_name):
    clearCanvas([])
    canvas.create_text(450, 100, text="You are now logged in as {}".format(result[0][0]),
                       font=('Helvetica', 40), fill='#00008B', tags='LoggedInMessage')
    canvas.create_text(450, 200, text="You can now view your passwords or create a new one",
                       font=('Helvetica', 20), fill='#00008B', tags='ViewPasswordMessage')

    def Save():
        save_a_password(code)
    SaveButton = Button(text='New +', command=Save)
    canvas.create_window(400, 250, window=SaveButton, tags='save')

    def Search():
        search_for_a_password(code)
    SearchButton = Button(text='View', command=Search)
    canvas.create_window(500, 250, window=SearchButton, tags='search')


def save_a_password(table_name):
    clearCanvas([])
    website_entry = Entry(root)
    canvas.create_window(450, 200, window=website_entry, tags='savewebsite')
    canvas.create_text(450, 150, text="The name of the website (Enter like Facebook, Google, Youtube, meaning only the"
                                      " first letter capital and no urls): ", font=('Helvetica', 15),
                       tags='WebsiteNameMessage')

    def SavePass():
        website = website_entry.get()
        curs.execute("SELECT * FROM {} WHERE website=:website".format(table_name), {"website": website})
        result = curs.fetchall()
        if not result == []:
            canvas.create_text(450, 250, text="Your already have a password saved for this website.\n",
                               font=('Helvetica', 15), tags='AlreadySavedMessage')

            def saveAnyway():
                password_entry = Entry(root)
                canvas.create_window(450, 400, window=password_entry, tags='savepassword1')
                canvas.create_text(450, 350, text="Enter the password you want to save",
                                   font=('Helvetica', 15), tags='EnterPasswordMessage1')

                def savePasswordAnyway():
                    password = password_entry.get()
                    with database:
                        curs.execute("INSERT INTO {} VALUES (:website, :password)".format(table_name),
                                          {"website": website, "password": password})
                    canvas.create_text(450, 400, text='Your password has been saved. It will show up when you search fo'
                                                      'r the passwords.',
                                       font=('Helvetica', 15), tags='PasswordSavedMessage')

                    def Return():
                        users_powers(code)

                    def New():
                        save_a_password(code)

                    def View():
                        search_for_a_password(code)
                    retrn = Button(text='Return to Profile', command=Return)
                    canvas.create_window(300, 450, window=retrn, tags='retrn')
                    new = Button(text='New+', command=New)
                    canvas.create_window(400, 450, window=new, tags='new')
                    view = Button(text='View Passwords', command=View)
                    canvas.create_window(500, 450, window=view, tags='view')
                savePasswordAnywayBt = Button(text='Enter', command=savePasswordAnyway)
                canvas.create_window(513, 350, window=savePasswordAnywayBt, tags="savePasswordAnywayBt")

            saveAnywayBt = Button(text='Save For Different Account', command=saveAnyway)
            canvas.create_window(350, 300, window=saveAnywayBt, tags="saveAnywayBt")

            def SearchInstead():
                search_for_a_password(table_name)

            SearchInsteadBt = Button(text='Search for Password', command=SearchInstead)
            canvas.create_window(550, 300, window=SearchInsteadBt, tags="SearchInsteadBt")
        else:
            password_entry = Entry(root)
            canvas.create_window(450, 300, window=password_entry, tags='savepassword2')
            canvas.create_text(450, 250, text="Enter the password you want to save",
                               font=('Helvetica', 15), tags='EnterPasswordMessage2')

            def savePassword():
                password = password_entry.get()
                with database:
                    curs.execute("INSERT INTO {} VALUES (:website, :password)".format(table_name),
                                 {"website": website, "password": password})
                canvas.create_text(450, 350,
                                   text='Your password has been saved. It will show up when you search for the passwo'
                                        'rds.',
                                   font=('Helvetica', 15), tags='savedmessage')

                def Return():
                    users_powers(code)

                def New():
                    save_a_password(code)

                def View():
                    search_for_a_password(code)

                retrn = Button(text='Return to Profile', command=Return)
                canvas.create_window(300, 450, window=retrn, tags='retrn')
                new = Button(text='New+', command=New)
                canvas.create_window(400, 450, window=new, tags='new')
                view = Button(text='View Passwords', command=View)
                canvas.create_window(500, 450, window=view, tags='view')
            savePasswordBt = Button(text='Enter', command=savePassword)
            canvas.create_window(513, 300, window=savePasswordBt, tags='savePasswordBt')
    enterWeb = Button(text='Enter', command=SavePass)
    canvas.create_window(513, 200, window=enterWeb, tags='enterwebsite')


def search_for_a_password(table_name):
    clearCanvas([])
    curs.execute("SELECT * FROM {}".format(table_name))
    result = curs.fetchall()
    if not result:
        clearCanvas([])
        canvas.create_text(450, 200, text="You don't have any passwords saved yet.", font=('Helvetica', 20),
                           fill='#00008B', tags='NoneSavedYet')

        def New():
            save_a_password(code)
        new = Button(text="New +", command=New)
        canvas.create_window(450, 250, window=new, tags='NewPasscode')
    else:
        clearCanvas([])
        canvas.create_text(200, 100, text="Websites", font=('Helvetica', 40),
                           fill='#00008B', tags='website')
        canvas.create_text(700, 100, text="Passwords", font=('Helvetica', 40),
                           fill='#00008B', tags='password')
        y_coord = 150
        for tups in result:
            canvas.create_text(200, y_coord, text=str(tups[0]), font=('Helvetica', 20),
                               fill='#00008B', tags='websites')
            canvas.create_text(700, y_coord, text=str(tups[1]), font=('Helvetica', 20),
                               fill='#00008B', tags='passwords')
            # print(f"{tups[0]}\t{tups[1]}")
            y_coord += 50

        def Return():
            users_powers(code)

        def New():
            save_a_password(code)

        retrn = Button(text='Return to Profile', command=Return)
        canvas.create_window(300, 450, window=retrn, tags='retrn')
        new = Button(text='New+', command=New)
        canvas.create_window(400, 450, window=new, tags='new')


def update_a_password(table_name):
    pass


def code_generator():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str


def select_security_questions(updated_q):
    q1 = 1
    q2 = 1
    while q1 == q2:
        q1 = random.randint(0, len(updated_q) - 1)
        q2 = random.randint(0, len(updated_q) - 1)

    return [updated_q[q1], updated_q[q2]]


def updated_list(questions, question_used):
    Questions_Updated = questions
    Questions_Updated.remove(question_used)
    return Questions_Updated


def clearCanvas(exceptions):
    for i in CLEAR_ALL:
        if i in exceptions:
            pass
        else:
            canvas.delete(i)


def start():
    global Home, Login, CreateAcc
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=background,
                        anchor="nw")
    Home = Button(root, text='Home',
                  fg='black',
                  bd=10, highlightthickness=4,
                  highlightcolor=BUTTON_COLOR,
                  highlightbackground=BUTTON_COLOR,
                  borderwidth=4,
                  font=BUTTON_FONT,
                  command=home)

    Login = Button(root, text='Login',
                   fg='black',
                   bd=10, highlightthickness=4,
                   highlightcolor=BUTTON_COLOR,
                   highlightbackground=BUTTON_COLOR,
                   borderwidth=4,
                   font=BUTTON_FONT,
                   command=login)
    CreateAcc = Button(root, text='Create Account',
                       fg='black',
                       bd=10, highlightthickness=4,
                       highlightcolor=BUTTON_COLOR,
                       highlightbackground=BUTTON_COLOR,
                       borderwidth=4,
                       font=BUTTON_FONT,
                       command=createacc)

    Home_canvas = canvas.create_window(5, 5,
                                       anchor="nw",
                                       window=Home, tags='home')

    Login_canvas = canvas.create_window(70, 5,
                                        anchor="nw",
                                        window=Login, tags='login')

    CreateAcc_canvas = canvas.create_window(130, 5,
                                            anchor="nw",
                                            window=CreateAcc, tags='createacc')

    root.mainloop()
    QUIT = Button(root, text="Exit Program", command=root.quit)
    QUIT.pack()
    root.mainloop()


if __name__ == '__main__':
    init()
