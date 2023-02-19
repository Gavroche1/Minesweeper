""" The main file of the minesweeper """

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messsagebox
import game
import const


def validate(user_input, min_val, max_val):
    """
        Check that a user_input is a number
        and min_val <= user_input <= max_val
    """

    if  user_input.isdigit():
        if min_val <= int(user_input) <= max_val:
            return True

        return False

    return False


class ModalParameter(tk.Toplevel):
    """ This is class is the modal where the user changes the parameters """

    def __init__(self, *args, callback=None, landmine=10, row=10, col=10, **kwargs):
        """ Initialize """

        super().__init__(*args, **kwargs)

        self.resizable(0, 0)
        self.title(const.TITLE_WINDOW)
        self.iconphoto(False, tk.PhotoImage(file=const.IMG_LOGO))

        self.callback = callback
        self.spinbox_landmine = ttk.Entry(self, "ttk::spinbox", from_=1, to=const.MAX_LANDMINE)
        self.spinbox_row = ttk.Entry(self, "ttk::spinbox", from_=1, to=const.MAX_ROW)
        self.spinbox_col = ttk.Entry(self, "ttk::spinbox", from_=1, to=const.MAX_COL)

        self.spinbox_landmine.insert(0, landmine)
        self.spinbox_row.insert(0, row)
        self.spinbox_col.insert(0, col)

        self.create_components()
        self.focus()
        self.grab_set()

    def create_components(self):
        """ Create and display the components """

        label_landmine = ttk.Label(self, text="Number of landmines : ")
        label_row = ttk.Label(self, text="Number of rows : ")
        label_col = ttk.Label(self, text="Number of cols : ")

        btn_valid = ttk.Button(self, text="Valid", command=self.btn_valid_action)

        label_landmine.grid(row=0, column=0, pady=5, padx=5, sticky="W")
        label_row.grid(row=1, column=0, pady=5, padx=5, sticky="W")
        label_col.grid(row=2, column=0, pady=5, padx=5, sticky="W")
        self.spinbox_landmine.grid(row=0, column=1, pady=5, padx=5)
        self.spinbox_row.grid(row=1, column=1, pady=5, padx=5)
        self.spinbox_col.grid(row=2, column=1, pady=5, padx=5)
        btn_valid.grid(row=3, column=1, pady=5, padx=5, sticky="E")

    def btn_valid_action(self):
        """ When the user wants to valid the datas """

        landmine = self.spinbox_landmine.get()
        col = self.spinbox_col.get()
        row = self.spinbox_row.get()

        if validate(landmine, 1, const.MAX_LANDMINE) and \
           validate(row, 1, const.MAX_ROW) and \
           validate(col, 1, const.MAX_COL) and \
           int(landmine) < int(col) * int(row):
            self.callback(int(landmine), int(col), int(row))
            self.destroy()


class Window(tk.Tk):
    """ This class is the window of the program """

    def __init__(self):
        """ Initialize """

        tk.Tk.__init__(self)

        self.game = game.Game(10, 10, 10)
        self.resizable(0, 0)
        self.title(const.TITLE_WINDOW)
        self.iconphoto(False, tk.PhotoImage(file=const.IMG_LOGO))

        self.grid_btn = []
        self.dict_imgs = {
            "1": tk.PhotoImage(file="imgs/1.png"),
            "2": tk.PhotoImage(file="imgs/2.png"),
            "3": tk.PhotoImage(file="imgs/3.png"),
            "4": tk.PhotoImage(file="imgs/4.png"),
            "5": tk.PhotoImage(file="imgs/5.png"),
            "6": tk.PhotoImage(file="imgs/6.png"),
            "7": tk.PhotoImage(file="imgs/7.png"),
            "8": tk.PhotoImage(file="imgs/8.png"),
            "flat": tk.PhotoImage(file="imgs/flag.png"),
            "empty": tk.PhotoImage(file="imgs/empty.png"),
            "red-landmine": tk.PhotoImage(file="imgs/red-landmine.png"),
        }
        self.create_components()
        self.display_grid()

    def create_components(self):
        """ Create and display the components """

        # Remove all the components
        for widget in self.winfo_children():
            widget.destroy()

        # Frame button
        frame_btn = tk.Frame()

        style = ttk.Style()
        style.configure("my.TButton", font=(None, 20))

        btn_replay = ttk.Button(frame_btn, text="Replay", style="my.TButton", command=self.replay)
        btn_replay.pack(side=tk.LEFT, padx=20)

        btn_parameter = ttk.Button(frame_btn, text="Parameter", \
            style="my.TButton", command=self.display_modal_parameter)
        btn_parameter.pack(padx=20)

        frame_btn.pack(pady=10)

        # Frame grid
        self.grid_btn = []
        frame_grid = tk.Frame()

        for i in range(self.game.row):
            row = []

            for j in range(self.game.col):
                btn = ttk.Button(frame_grid)
                btn.grid(row=i, column=j)
                btn.bind("<Button>", lambda evt, i=i, j=j: self.click_btn_grid(evt, i, j))
                btn.configure(image=self.dict_imgs["empty"])

                row.append(btn)

            self.grid_btn.append(row)

        frame_grid.pack(padx=2, pady=2)

    def display_grid(self):
        """ Change the buttons with the new version of the grid """

        game_grid = self.game.grid

        for i in range(len(self.grid_btn)):
            for j in range(len(self.grid_btn[0])):
                self.grid_btn[i][j].configure(state=tk.NORMAL)

                if game_grid[i][j] in ("h", "f"):
                    self.grid_btn[i][j].configure(image=self.dict_imgs["flat"])
                elif game_grid[i][j] == "0":
                    self.grid_btn[i][j].configure(state=tk.DISABLED)
                    self.grid_btn[i][j].configure(image=self.dict_imgs["empty"])
                elif game_grid[i][j] == "l":
                    self.grid_btn[i][j].configure(image=self.dict_imgs["red-landmine"])
                elif game_grid[i][j] != " ":
                    self.grid_btn[i][j].configure(image=self.dict_imgs[game_grid[i][j]])
                else:
                    self.grid_btn[i][j].configure(image=self.dict_imgs["empty"])

    def replay(self):
        """ When the user wants to replay """

        self.game.replay()
        self.display_grid()

    def click_btn_grid(self, evt, i, j):
        """ When the user clicks on a button of the grid """

        if evt.num == 1:
            self.game.click_user(j, i)
        elif evt.num == 3:
            self.game.add_flag(j, i)

        self.display_grid()

        if self.game.test_win():
            messsagebox.showinfo(const.TITLE_WINDOW, "You won !")
        elif self.game.is_lost:
            messsagebox.showinfo(const.TITLE_WINDOW, "You lost !")

    def display_modal_parameter(self):
        """ Display the modal where the user can change the parameters """

        ModalParameter(
            callback=self.change_size_grid,
            landmine=self.game.nb_landmine,
            col=self.game.col,
            row=self.game.row
        )

    def change_size_grid(self, landmine, row, col):
        """ When the user valide the modalParameter """

        self.game = game.Game(landmine, col, row)
        self.game.replay()
        self.create_components()


def main():
    """ The main function of the game """

    app = Window()
    app.mainloop()

if __name__ == "__main__":
    main()
