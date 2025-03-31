"""CSC111 Project 2 - Movie Recommendation System
Last Updated: 29/3/25
Edited by: Ozzie, Aiden
"""
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
import uuid
from api import BackendInstance


def create_window(dataset_path: str) -> None:
    """  Initialize the backend instance using the dataset path, And starts the interface once called.

    Preconditions:
    - dataset_path is a valid directory containing "movies.csv" and "ratings.csv"
    """

    movies_file_path = dataset_path + "/movies.csv"
    ratings_file_path = dataset_path + "/ratings.csv"

    backend = BackendInstance(movies_file_path, ratings_file_path)

    main_window = Tk()

    custom_font = tkfont.Font(family="Times New Roman", size=28, weight="bold")
    custom_font2 = tkfont.Font(family="Times New Roman", size=14)
    main_window.geometry("1000x550+240+150")
    main_window.title("Welcome Page")

    def login() -> None:
        '''
        Open a login window where users can enter their username and password.
        '''
        global login_screen
        login_screen = Toplevel(main_window)
        login_screen.title("Login")
        login_screen.geometry("1000x550+240+150")
        Label(login_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()

        username = StringVar()
        password = StringVar()

        lable = Label(login_screen, text="Username:")
        lable.pack()

        username_entry = Entry(login_screen, fg="black", textvariable=username)
        username_entry.pack()

        lable = Label(login_screen, text="Password:")
        lable.pack()

        password_entry = Entry(login_screen, fg="black", show='*', textvariable=password)
        password_entry.pack()
        Label(login_screen, text="").pack()

        def _button() -> None:
            """
            Retrieve entered username and password and attempt login.
            """
            entered_username = username.get()
            entered_password = password.get()
            login2(entered_username, entered_password)

        Button(login_screen, text="Login", width=20, height=2, bg="grey", command=_button).pack()

        def _back() -> None:
            login_screen.destroy()

        back = Button(login_screen, text="Back", fg="black", highlightbackground="grey", width=10, height=2,
                      command=_back)
        back.place(relx=0.08, rely=0.08, anchor="center")

    def login2(entered_username: str, entered_password: str) -> None:
        '''
        This function checks if verify_login returns true or false, resulting in a successful login vs unsuscsessful

        Preconditions:
            - isintance(entered_username, str) == true
            - isintance(enetered_password, str) == true

        '''
        if verify_login(entered_username, entered_password):
            Label(login_screen, text="Login successful!").pack()
            login_success()

        else:
            Label(login_screen, text="Login failed. Incorrect username or password.").pack()

    def verify_login(entered_username: str, entered_password: str) -> None:
        '''
        This function cycles through the file holding all the usernames and passwords, comparing them to the
        entered username and entered password. If any matches appear the function returns true, indicating a successful
        login, and if not, it means the user does not exist.

        Preconditions:
            - isintance(entered_username, str) == true
            - isintance(enetered_password, str) == true

        '''
        global _id

        with open("user.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2 or len(parts) == 3:
                    user_id, stored_username, stored_password = parts[0], parts[1], parts[2]
                    if entered_username == stored_username and entered_password == stored_password:
                        _id = user_id
                        return True
        return False

    def login_success() -> None:
        '''
        Display a success message and transition to the main menu.
        '''
        global success_screen
        success_screen = Toplevel(main_window)
        success_screen.geometry("150x100+200+100")
        success_screen.title("Sucsess")
        Label(success_screen, text="Login successful").pack()
        Button(success_screen, text="Ok", width=5, height=2, bg="grey", command=success_screen.destroy).pack()
        login_screen.destroy()
        menu()

    def register() -> None:
        '''
        This function allows the user to create a account, by submitting a username and password.
        '''
        global register_screen
        register_screen = Toplevel(main_window)
        register_screen.title("Register")
        register_screen.geometry("1000x550+240+150")
        Label(register_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()

        username = StringVar()
        password_var = StringVar()
        confirm_var = StringVar()

        lable = Label(register_screen, text="Username:")
        lable.pack()

        username_entry = Entry(register_screen, fg="black", textvariable=username)
        username_entry.pack()

        lable = Label(register_screen, text="Password:")
        lable.pack()

        password_entry = Entry(register_screen, fg="black", show='*', textvariable=password_var)
        password_entry.pack()

        lable = Label(register_screen, text="Confirm Password:")
        lable.pack()

        confirm_entry = Entry(register_screen, fg="black", show='*', textvariable=confirm_var)
        confirm_entry.pack()

        lable = Label(register_screen, text="")
        lable.pack()

        def _button() -> None:
            entered_username = username.get()
            entered_password = password_var.get()
            confirm = confirm_var.get()
            user_id = str(uuid.uuid4())[:2]
            signup(user_id, entered_username, entered_password, confirm)

        Button(register_screen, text="Register", width=20, height=2, bg="grey", command=_button).pack()

        back = Button(register_screen, text="Back", fg="black", highlightbackground="grey", width=10, height=2,
                      command=destroy_signup)
        back.place(relx=0.08, rely=0.08, anchor="center")

    def destroy_signup() -> None:
        """
        Deletes register_screen window
        """
        register_screen.destroy()

    def signup(user_id: int, username: str, password: str, confirm: str) -> None:
        """
        Validate registration details and store them in user.txt if valid.
        """
        global _id
        with open("user.txt", "r") as file:
            usernames = [line.strip().split() for line in file]
            if username in usernames:
                Label(register_screen, text="Username already exists").pack()
            elif password != confirm:
                Label(register_screen, fg="white", text="The passwords do not match, try again.").pack()
            else:
                with open("user.txt", "a") as file:
                    file.write(user_id + " " + username + " " + password + "\n")
                file.close()
                _id = user_id
                register_success()
                menu()

    def register_success() -> None:
        """
        Notify the user that registration was successful.
        """
        global success_screen
        success_screen = Toplevel(main_window)
        success_screen.geometry("150x100+200+100")
        success_screen.title("Sucsess")
        Label(success_screen, text="Sign in successful").pack()
        Button(success_screen, text="Ok", width=5, height=2, bg="grey", command=success_screen.destroy).pack()
        register_screen.destroy()

    def menu() -> None:
        """
        Display the main menu with options to get recommendations or view watched movies.
        """
        global menu_screen

        menu_screen = Toplevel(main_window)
        menu_screen.title("Menu")
        menu_screen.geometry("1000x550+240+150")
        Label(menu_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()
        Label(menu_screen, text="").pack()
        try:
            added_screen.destroy()
        except:
            pass

        def combined() -> None:
            menu_destroy()
            preferences()

        reco = Button(menu_screen, text="Recomendations", fg="black", highlightbackground="grey", width=30, height=5,
                      command=combined)
        reco.place(relx=0.5, rely=0.3, anchor="center")

        watch = Button(menu_screen, text="Watched Movies", fg="black", highlightbackground="grey", width=30, height=5,
                       command=watched_movies)
        watch.place(relx=0.5, rely=0.5, anchor="center")

        back = Button(menu_screen, text="Log Out", fg="black", highlightbackground="grey", width=10, height=2,
                      command=menu_destroy)
        back.place(relx=0.08, rely=0.08, anchor="center")

    def menu_destroy() -> None:
        menu_screen.destroy()

    def preferences() -> None:
        """
        Display genre selection options for personalized movie recommendations.
        """

        global preference_screen
        preference_screen = Toplevel(main_window)
        preference_screen.title("Game")
        preference_screen.geometry("1000x550+240+150")

        quest = Label(preference_screen, text="Select your favorite Genres", font=custom_font)
        quest.place(relx=0.5, rely=0.2, anchor="center")

        frame = Frame(preference_screen, width=200, height=150)
        frame.place(relx=0.5, rely=0.4, anchor="center")

        vert_scroll = Scrollbar(frame, orient=VERTICAL)

        genres = Listbox(frame, selectmode='multiple', yscrollcommand=vert_scroll.set, width=20, height=8)
        genres.grid(row=0, column=0, sticky="nsew")

        vert_scroll.config(command=genres.yview)
        vert_scroll.grid(row=0, column=1, sticky="ns")

        available_genres = backend.get_genres()

        for genre in available_genres:
            genres.insert(END, genre)

        vert_scroll.config()

        def _reco() -> None:
            selected_indices = genres.curselection()
            selected_genres = [genres.get(i) for i in selected_indices]
            p_destroy()
            recomendation(selected_genres)

        submit = Button(preference_screen, text="Submit", font=custom_font, command=_reco)
        submit.place(relx=0.5, rely=0.65, anchor="center")

        def _return() -> None:
            p_destroy()
            menu()

        back = Button(preference_screen, text="Back", fg="black", highlightbackground="grey", width=10,
                      height=2, command=_return)
        back.place(relx=0.08, rely=0.08, anchor="center")

    def p_destroy() -> None:
        preference_screen.destroy()

    def recomendation(answer: list[str]) -> None:
        """
        Show movie recommendations based on selected genres.

        Precondtion:
            - len(answer) > 0
        """
        global reco_screen, tree
        reco_screen = Toplevel(main_window)
        reco_screen.title("Game")
        reco_screen.geometry("1000x550+240+150")
        Label(reco_screen, text="Movie Reco", width=30, height=5, font=custom_font).pack()
        Label(reco_screen, text="").pack()

        recommended_movie = backend.get_recs_from_genres(answer, 10)

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
            tree.insert("", "end", values=(title, year, round(rating, 2), genres))

        tree.pack()

        def _return() -> None:
            reco_destroy()
            preferences()

        tree.bind("<ButtonRelease-1>", on_row_selected)

        back = Button(reco_screen, text="Back", fg="black", highlightbackground="grey", width=10,
                      height=2, command=_return)
        back.place(relx=0.08, rely=0.08, anchor="center")

    def reco_destroy() -> None:
        reco_screen.destroy()

    def on_row_selected(e: Event) -> None:
        """
        Retrieve data from the selected movie row.
        """

        selected_item = tree.focus()
        if selected_item:
            row_data = tree.item(selected_item, "values")
            add(row_data)

    def add(select_row: list[tuple[str, int, float, set[str]]]) -> None:
        """
        Display confirmation that a movie has been added to the watched list.
        """
        global added_screen
        added_screen = Toplevel(main_window)
        added_screen.title("Game")
        added_screen.geometry("1000x550+240+150")
        reco_screen.destroy()

        label = Label(added_screen, text="The following will be added to your profile as watched:", width=60,
                      height=5, font=custom_font2)
        label.place(relx=0.5, rely=0.1, anchor="center")

        row = Label(added_screen, text=f"{select_row}", width=100,
                    height=5, font=custom_font2)
        row.place(relx=0.5, rely=0.3, anchor="center")

        save(select_row)

        rerun = Button(added_screen, text="Return to Menu", font=custom_font, command=menu)
        rerun.place(relx=0.5, rely=0.7, anchor="center")

    def save(row: list[tuple[str, int, float, set[str]]]) -> None:
        """
        Save the selected movie to the watched movies file.

        Preconditions:
        - len(row) > 3
        """
        with open("watched_movies.txt", "a") as file:
            file.write(f"{_id},{row[0]}\n")
        file.close()

    def get_watched_movies() -> list[tuple[str, int, float, set[str]]]:
        """
        Gather a list of all movies watched by the user with _id

        Precondition:
            -isinstance(_id, str) == True
            -_id is not None
        """

        movies = []
        with open("watched_movies.txt", "r") as file:
            for line in file:
                userid = line.strip().split(",")
                if userid[0] == _id:
                    movies.append(f"{userid[1]}")
        return movies

    def watched_movies() -> None:
        """
        Displays a scrolable list of all movies watched by user, in order.
        """
        global watched_screen
        menu_destroy()
        watched_screen = Toplevel(main_window)
        watched_screen.title("Watched Movies")
        watched_screen.geometry("1000x550+240+150")

        Label(watched_screen, text="Movie History:", font=custom_font).pack(pady=10)

        frame = Frame(watched_screen, width=200, height=150)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        vert_scroll = Scrollbar(frame, orient=VERTICAL)

        movies = Listbox(frame, selectmode='none', yscrollcommand=vert_scroll.set, width=50, height=20)
        movies.grid(row=0, column=0, sticky="nsew")

        vert_scroll.config(command=movies.yview)
        vert_scroll.grid(row=0, column=1, sticky="ns")

        watched_movies = get_watched_movies()

        if not watched_movies:
            movies.insert(END, "No movies watched yet.")
        else:
            for watched in watched_movies:
                movies.insert(END, watched)

        vert_scroll.config()

        def _return() -> None:
            watched_screen.destroy()
            menu()

        back = Button(watched_screen, text="Back", fg="black", highlightbackground="grey", width=10,
                      height=2, command=_return)
        back.place(relx=0.08, rely=0.08, anchor="center")

    label = Label(main_window, text="Recomendations", font=custom_font,
                  bg="lightblue")
    label.place(relx=0.5, rely=0.1, anchor="center")
    login = Button(main_window, text="Login", fg="black", highlightbackground="grey", width=30, height=5,
                   command=login)
    login.place(relx=0.5, rely=0.3, anchor="center")
    register = Button(main_window, text="Register", fg="black", highlightbackground="grey", width=30, height=5,
                      command=register)
    register.place(relx=0.5, rely=0.5, anchor="center")

    main_window.mainloop()


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['tkinter, uuid, api']
    })
