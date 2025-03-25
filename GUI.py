import tkinter
from tkinter import *
from tkinter import PhotoImage, ttk
import tkinter as tk
from tkinter import font as tkfont
from api import BackendInstance
import os

def rest():
    global main_window
    main_window = Tk()

rest()

custom_font = tkfont.Font(family="Times New Roman", size=28, weight="bold")
main_window.geometry("1000x550+240+150")
main_window.title("Welcome Page")

# background_image = PhotoImage(file="skaterboy.png")
# background_image = background_image.subsample(1, 1)
# background_label = tk.Label(image=background_image)
# background_label.place(relwidth=1, relheight=1)

#def text_colors:


def login() -> None:
    global login_screen
    login_screen = Toplevel(main_window)  # makes the login screen the new main
    login_screen.title("Login")
    login_screen.geometry("1000x550+240+150")
    Label(login_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()

    username = StringVar()  # creates username variable as a string
    password = StringVar()  # creates passowrd variable as a string

    lable = Label(login_screen, text="Username:")
    lable.pack()

    username_entry = Entry(login_screen, fg="black", textvariable=username)
    username_entry.pack()

    lable = Label(login_screen, text="Passowrd:")
    lable.pack()

    password_entry = Entry(login_screen, fg="black", show='*', textvariable=password)
    password_entry.pack()
    Label(login_screen, text="").pack()  # creates a buffer space

    def _button():
        entered_username = username.get()
        entered_password = password.get()
        login2(entered_username, entered_password)

    Button(login_screen, text="Login", width=20, height=2, bg="grey", command=_button).pack()

    def _back() -> None:
        login_screen.destroy()

    back = Button(login_screen, text="Back", fg="black", highlightbackground="grey", width=10, height=2, command=_back)
    back.place(relx=0.08, rely=0.08, anchor="center")


def login2(entered_username: str, entered_password: str) -> None:
    if verify_login(entered_username, entered_password):
        Label(login_screen, text="Login successful!").pack()
        login_sucsess()

    else:
        Label(login_screen, text="Login failed. Incorrect username or password.").pack()

def verify_login(entered_username: str, entered_password: str) -> None:
    try:
        with open(os.path.join(os.path.dirname(__file__), "user.txt"), "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2 or len(parts) == 3:
                    stored_username, stored_password = parts[0], parts[1]
                    if entered_username == stored_username and entered_password == stored_password:
                        return True
        return False
    except FileNotFoundError:
        return False

def login_sucsess() -> None:
    global sucsess_screen
    sucsess_screen = Toplevel(main_window)
    sucsess_screen.geometry("150x100+200+100")
    sucsess_screen.title("Sucsess")
    Label(sucsess_screen, text="Login sucsessful").pack()
    Button(sucsess_screen, text="Ok", width=5, height=2, bg="grey", command=sucsess_screen.destroy).pack()
    login_screen.destroy()
    menu()


def register() -> None:
    global register_screen
    register_screen = Toplevel(main_window)
    register_screen.title("Register")
    register_screen.geometry("1000x550+240+150")
    Label(register_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()

    username = StringVar()  # creates username variable as a string
    password_var = StringVar()  # creates passowrd variable as a string
    confirm_var = StringVar()

    lable = Label(register_screen, text="Username:")
    lable.pack()

    username_entry = Entry(register_screen, fg="white",textvariable=username)  # Creates username box to enter username
    username_entry.pack()

    lable = Label(register_screen, text="Passowrd:")
    lable.pack()

    password_entry = Entry(register_screen, fg="black", show='*', textvariable=password_var)
    password_entry.pack()

    lable = Label(register_screen, text="Confirm Passowrd:")
    lable.pack()

    confirm_entry = Entry(register_screen, fg="black", show='*', textvariable=confirm_var)
    confirm_entry.pack()

    lable = Label(register_screen, text="")
    lable.pack()

    def _button():
        entered_username = username.get()
        entered_password = password_var.get()
        confirm = confirm_var.get()
        signup(entered_username, entered_password, confirm)

    Button(register_screen, text="Register", width=20, height=2, bg="grey", command=_button).pack()

    back = Button(register_screen, text="Back", fg="black", highlightbackground="grey", width=10, height=2,
                  command=destroy_signup)
    back.place(relx=0.08, rely=0.08, anchor="center")


def destroy_signup() -> None:
    register_screen.destroy()


def signup(username: str, password: str, confirm: str) -> None:
    global signup
    with open("user.txt", "r") as file:
        usernames = [line.strip().split() for line in file]
        if username in usernames:
            Label(register_screen, text="Username already exists").pack()
        elif password != confirm:
            Label(register_screen, fg="white", text="The passwords do not match, try again.").pack()
        else:
            file = open("user.txt", "a")
            file.write(username + " " + password + "\n")
            file.close()  # closes file
            register_sucsess()
            menu()


def register_sucsess() -> None:
    global sucsess_screen
    sucsess_screen = Toplevel(main_window)
    sucsess_screen.geometry("150x100+200+100")
    sucsess_screen.title("Sucsess")
    Label(sucsess_screen, text="Sign in sucsessful").pack()
    Button(sucsess_screen, text="Ok", width=5, height=2, bg="grey", command=sucsess_screen.destroy).pack()
    register_screen.destroy()


def menu() -> None:
    global menu_screen

    menu_screen = Toplevel(main_window)
    menu_screen.title("Menu")
    menu_screen.geometry("1000x550+240+150")
    Label(menu_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()
    Label(menu_screen, text="").pack()

    gam = Button(menu_screen, text="Recomendations", fg="black", highlightbackground="grey", width=30, height=5, command=preferences)
    gam.place(relx=0.5, rely=0.3, anchor="center")

    back = Button(menu_screen, text="Log Out", fg="black", highlightbackground="grey", width=10, height=2, command=menu_destroy)
    back.place(relx=0.08, rely=0.08, anchor="center")

def menu_destroy() -> None:
    menu_screen.destroy()

def preferences():
    global preference_screen
    menu_screen.destroy()
    preference_screen = Toplevel(main_window)
    preference_screen.title("Game")
    preference_screen.geometry("1000x550+240+150")
    Label(preference_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()
    Label(preference_screen, text="").pack()

    query = "What is your favorite genre?"

    quest = Label(preference_screen, text=query, font=custom_font)
    quest.place(relx=0.5, rely=0.3, anchor="center")

    answer = Entry(preference_screen, width=10, font=custom_font)
    answer.place(relx=0.5, rely=0.4, anchor="center")

    def _reco():
        _answer = answer.get().strip().lower()
        recomendation(_answer)

    submit = Button(preference_screen, text="Submit", font=custom_font, command=_reco)
    submit.place(relx=0.5, rely=0.5, anchor="center")

    back = Button(preference_screen, text="Back", fg="black", highlightbackground="grey", width=10, height=2,command=p_destroy)
    back.place(relx=0.08, rely=0.08, anchor="center")

def p_destroy() -> None:
    preference_screen.destroy()

def recomendation(answer: str) -> None:
    global reco_screen
    menu_screen.destroy()
    reco_screen = Toplevel(main_window)
    reco_screen.title("Game")
    reco_screen.geometry("1000x550+240+150")
    Label(reco_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()
    Label(reco_screen, text="").pack()

    extract = BackendInstance()
    print("All available genres:", extract.get_genres())
    print(answer)

    recommended_movie = extract.get_recommendations_from_genres([answer], 5)
    print("Recommended movies:", recommended_movie)
    print("All available genres:", extract.get_genres())

    tree = ttk.Treeview(reco_screen, columns=("Title", "Year", "Rating", "Genre"), show="headings", height=10)

    tree.heading("Title", text="Title")
    tree.heading("Year", text="Year")
    tree.heading("Rating", text="Rating")
    tree.heading("Genre", text="Genre")

    tree.column("Title", anchor=CENTER)
    tree.column("Year", anchor=CENTER)
    tree.column("Rating", anchor=CENTER)
    tree.column("Genre", anchor=CENTER)

    for movie in recommended_movie:
        title, year, rating, genres = movie
        tree.insert("", "end", values=(title, year, rating, genres))

    tree.pack()

    back = Button(reco_screen, text="white", fg="black", highlightbackground="grey", width=10, height=2,command=reco_destroy)  # creates interactive login button
    back.place(relx=0.08, rely=0.08, anchor="center")

def reco_destroy() -> None:
    reco_screen.destroy()

label = Label(main_window, text="Reco", font=custom_font,
              bg="lightblue")  # sets up the Label with the background image, transparent text background, and higher-aligned text
label.place(relx=0.5, rely=0.1, anchor="center")  # Manually adjust where the text is
login = Button(main_window, text="Login", fg="black", highlightbackground="grey", width=30, height=5,
               command=login)  # creates interactive login button
login.place(relx=0.5, rely=0.3, anchor="center")
register = Button(main_window, text="Register", fg="black", highlightbackground="grey", width=30, height=5,
                  command=register)
register.place(relx=0.5, rely=0.5, anchor="center")

main_window.mainloop()  # continuously loops the main window, which prevents window from closing
