import tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import font as tkfont
from functools import partial
from pygments.lexer import combined

from api import BackendInstance

# Hey, also just gonna use comments for one other thing I noticed.
# When running the program, it at some points has like 4 or 5 different windows pop up,
# and most of them don't seem necessary. I think the new windows should either be
# replacing the old ones, or just have the old ones close when a new one pops up or smthn

def create_window(dataset_path: str) -> None:
    """ dataset_path should be a directory containing "movies.csv" and "ratings.csv"
    """
    movies_file_path = dataset_path + "/movies.csv"
    ratings_file_path = dataset_path + "/ratings.csv"

    backend = BackendInstance(movies_file_path, ratings_file_path)

    # TODO: Move the rest of this file's functionality into here
    # Since we've defined just one backend instance for the program, it can
    # be passed around to functions which need it.


def rest():
    global main_window
    main_window = Tk()

rest()

custom_font = tkfont.Font(family = "Times New Roman", size = 28, weight = "bold")
custom_font2 = tkfont.Font(family = "Times New Roman", size = 14)
main_window.geometry("1000x550+240+150")
main_window.title("Welcome Page")

#def text_colors:

def login() -> None:
    global login_screen
    login_screen = Toplevel(main_window)  # makes the login screen the new main
    login_screen.title("Login")
    login_screen.geometry("1000x550+240+150")
    Label(login_screen, text = "Movie Reco", width = 30, height = 5, font = custom_font).pack()

    username = StringVar()  # creates username variable as a string
    password = StringVar()  # creates passowrd variable as a string

    lable = Label(login_screen, text = "Username:")
    lable.pack()

    username_entry = Entry(login_screen, fg = "black", textvariable = username)
    username_entry.pack()

    lable = Label(login_screen, text = "Passowrd:")
    lable.pack()

    password_entry = Entry(login_screen, fg = "black", show = '*', textvariable = password)
    password_entry.pack()
    Label(login_screen, text = "").pack()

    def _button():
        entered_username = username.get()
        entered_password = password.get()
        login2(entered_username, entered_password)

    Button(login_screen, text = "Login", width = 20, height = 2, bg = "grey", command = _button).pack()

    def _back() -> None:
        login_screen.destroy()

    back = Button(login_screen, text = "Back", fg = "black", highlightbackground = "grey", width = 10, height = 2, command = _back)
    back.place(relx = 0.08, rely = 0.08, anchor = "center")


def login2(entered_username: str, entered_password: str) -> None:
    if verify_login(entered_username, entered_password):
        Label(login_screen, text = "Login successful!").pack()
        login_sucsess()

    else:
        Label(login_screen, text = "Login failed. Incorrect username or password.").pack()

def verify_login(entered_username: str, entered_password: str) -> None:
    try:
        with open("user.txt", "r") as file:
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
    Label(sucsess_screen, text = "Login sucsessful").pack()
    Button(sucsess_screen, text = "Ok", width = 5, height = 2, bg = "grey", command = sucsess_screen.destroy).pack()
    login_screen.destroy()
    menu()


def register() -> None:
    global register_screen
    register_screen = Toplevel(main_window)
    register_screen.title("Register")
    register_screen.geometry("1000x550+240+150")
    Label(register_screen, text = "Movie Reco", width = 30, height = 5, font = custom_font).pack()

    username = StringVar()  # creates username variable as a string
    password_var = StringVar()  # creates passowrd variable as a string
    confirm_var = StringVar()

    lable = Label(register_screen, text = "Username:")
    lable.pack()

    username_entry = Entry(register_screen, fg = "black",textvariable = username)  # Creates username box to enter username
    username_entry.pack()

    lable = Label(register_screen, text = "Passowrd:")
    lable.pack()

    password_entry = Entry(register_screen, fg = "black", show = '*', textvariable = password_var)
    password_entry.pack()

    lable = Label(register_screen, text = "Confirm Passowrd:")
    lable.pack()

    confirm_entry = Entry(register_screen, fg = "black", show = '*', textvariable = confirm_var)
    confirm_entry.pack()

    lable = Label(register_screen, text = "")
    lable.pack()

    def _button():
        entered_username = username.get()
        entered_password = password_var.get()
        confirm = confirm_var.get()
        signup(entered_username, entered_password, confirm)

    Button(register_screen, text = "Register", width = 20, height = 2, bg = "grey", command = _button).pack()

    back = Button(register_screen, text = "Back", fg = "black", highlightbackground = "grey", width = 10, height = 2,
                  command = destroy_signup)
    back.place(relx = 0.08, rely = 0.08, anchor = "center")


def destroy_signup() -> None:
    register_screen.destroy()

def signup(username: str, password: str, confirm: str) -> None:
    global signup
    with open("user.txt", "r") as file:
        usernames = [line.strip().split() for line in file]
        if username in usernames:
            Label(register_screen, text = "Username already exists").pack()
        elif password != confirm:
            Label(register_screen, fg = "white", text = "The passwords do not match, try again.").pack()
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
    Label(sucsess_screen, text = "Sign in sucsessful").pack()
    Button(sucsess_screen, text = "Ok", width = 5, height = 2, bg = "grey", command = sucsess_screen.destroy).pack()
    register_screen.destroy()

def menu() -> None:
    global menu_screen

    menu_screen = Toplevel(main_window)
    menu_screen.title("Menu")
    menu_screen.geometry("1000x550+240+150")
    Label(menu_screen, text = "Movie Reco", width = 30, height = 5, font = custom_font).pack()
    Label(menu_screen, text = "").pack()
    try:
        added_screen.destroy()
    except:
        pass

    def combined():
        menu_destroy()
        preferences()

    gam = Button(menu_screen, text = "Recomendations", fg = "black", highlightbackground = "grey", width = 30, height = 5, command = combined)
    gam.place(relx = 0.5, rely = 0.3, anchor = "center")

    back = Button(menu_screen, text = "Log Out", fg = "black", highlightbackground = "grey", width = 10, height = 2, command = menu_destroy)
    back.place(relx = 0.08, rely = 0.08, anchor = "center")

def menu_destroy() -> None:
    menu_screen.destroy()

def preferences():
    global preference_screen
    preference_screen = Toplevel(main_window)
    preference_screen.title("Game")
    preference_screen.geometry("1000x550+240+150")

    quest = Label(preference_screen, text="Select your favorite Genres", font= custom_font)
    quest.place(relx=0.5, rely=0.25, anchor="center")

    frame = Frame(preference_screen, width=200, height=150)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    vert_scroll = Scrollbar(frame, orient=VERTICAL)

    genres = Listbox(frame, selectmode='multiple', yscrollcommand=vert_scroll.set, width=20, height=8)
    genres.grid(row=0, column=0, sticky="nsew")

    vert_scroll.config(command=genres.yview)
    vert_scroll.grid(row=0, column=1, sticky="ns")

    list_genres = [
        'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Fantasy', 'Horror', 'Musical',
        'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War'
    ]

    for genre in list_genres:
        genres.insert(END, genre)

    vert_scroll.config()

    #def on_key_release(event: Event) -> None:
        #current_text = answer.get().lower()

        # TODO: Since the backend has a way to get all of the genre options,
        # I think we should have a dropdown menu or something of the sort
        # which shows the user the options they have. That way, we can also
        # gracefully handle any potential errors here instead of further down
        # the line.

        # Example idea:
        # Since the genres are static, they could be passed as an argument?
        # then, we can do something like:
        # for genre in genres
        #   if genre.startswith(current_text):
        #       Show the genre in a box under the text area
        #       potentially allow them to click it and have it auto-fill?

    # This has the on_key_release function be run whenever the user presses (releases) a key
    #answer.bind("<KeyRelease>", on_key_release)

    # Just one other quick note; I don't think nested functions are the best idea.
    # I believe PythonTA doesn't allow them, and even if, they can make the code
    # pretty hard to read. That said, I'm not super familiar w/ tkinter so if that's
    # the norm, then totally disreguard this :)

    def _reco():
        selected_indices = genres.curselection()
        selected_genres = [genres.get(i) for i in selected_indices]
        p_destroy()
        recomendation(selected_genres)

    submit = Button(preference_screen, text = "Submit", font = custom_font, command = _reco)
    submit.place(relx = 0.5, rely = 0.75, anchor = "center")

    def _return():
        p_destroy()
        menu()

    back = Button(preference_screen, text = "Back", fg = "black", highlightbackground = "grey", width = 10,
                  height = 2,command = _return)
    back.place(relx = 0.08, rely = 0.08, anchor = "center")

def p_destroy() -> None:
    preference_screen.destroy()

def recomendation(answer: list[str]) -> None:
    global reco_screen, tree
    reco_screen = Toplevel(main_window)
    reco_screen.title("Game")
    reco_screen.geometry("1000x550+240+150")
    Label(reco_screen, text = "Movie Reco", width = 30, height = 5, font = custom_font).pack()
    Label(reco_screen, text = "").pack()

    extract = BackendInstance()

    recommended_movie = extract.get_recommendations_from_genres(answer, 5)

    tree = ttk.Treeview(reco_screen, columns = ("Title", "Year", "Rating", "Genre"), show = "headings", height = 10)

    tree.heading("Title", text = "Title")
    tree.heading("Year", text = "Year")
    tree.heading("Rating", text = "Rating")
    tree.heading("Genre", text = "Genre")

    tree.column("Title", anchor = CENTER)
    tree.column("Year", anchor = CENTER)
    tree.column("Rating", anchor = CENTER)
    tree.column("Genre", anchor = CENTER)

    for movie in recommended_movie:
        title, year, rating, genres = movie
        tree.insert("", "end", values = (title, year, round(rating, 2), genres))

    tree.pack()

    def _return():
        reco_destroy()
        preferences()

    tree.bind("<ButtonRelease-1>", on_row_selected)

    back = Button(reco_screen, text = "Back", fg = "black", highlightbackground = "grey", width = 10,
                  height = 2,command = _return)
    back.place(relx = 0.08, rely = 0.08, anchor = "center")

def on_row_selected(event) -> list[any]:
    selected_item = tree.focus()
    if selected_item:
        row_data = tree.item(selected_item, "values")
    add(row_data)

def add(select_row) -> None:
    global added_screen
    added_screen = Toplevel(main_window)
    added_screen.title("Game")
    added_screen.geometry("1000x550+240+150")
    reco_screen.destroy()

    label = Label(added_screen, text=f"The following will be added to your profile as watched:", width=60,
          height=5, font = custom_font2)
    label.place(relx = 0.5, rely = 0.1, anchor = "center")

    row = Label(added_screen, text=f"{select_row}", width=100,
          height=5, font=custom_font2)
    row.place(relx=0.5, rely=0.3, anchor="center")

    rerun = Button(added_screen, text="Return to Menu", font=custom_font, command=menu)
    rerun.place(relx=0.5, rely=0.7, anchor="center")


def reco_destroy() -> None:
    reco_screen.destroy()

label = Label(main_window, text = "Reco", font = custom_font,
              bg = "lightblue")
label.place(relx = 0.5, rely = 0.1, anchor = "center")
login = Button(main_window, text = "Login", fg = "black", highlightbackground = "grey", width = 30, height = 5,
               command = login)
login.place(relx = 0.5, rely = 0.3, anchor = "center")
register = Button(main_window, text = "Register", fg = "black", highlightbackground = "grey", width = 30, height = 5,
                  command = register)
register.place(relx = 0.5, rely = 0.5, anchor = "center")

main_window.mainloop()
