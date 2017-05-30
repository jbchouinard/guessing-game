from collections import defaultdict

from game import Game
from solver import Solver
from tkinter import *


XSCALE = 1
YSCALE = 1

def sx(x):
    return int(XSCALE * x)

def sy(y):
    return int(YSCALE * y)


options = {
    'colors': 6,
    'n': 4,
    'tries': 10,
}


class GameWidget:
    # Peg geometry
    width = sx(30)
    height = sy(30)
    x_pad = sx(10)
    y_pad = sy(10)
    y0 = sy(10)
    x0 = sx(10)

    colors = defaultdict(
        lambda: 'black',
        {
            # Pegs
            0: 'white',
            1: 'red',
            2: 'yellow',
            3: 'green',
            4: 'blue',
            5: 'orange',
            6: 'purple',
            # Mini pegs
            'correct': 'black',
            'incorrect': 'white',
            'missing': 'grey',
        }
    )

    def __init__(self, game, frame, legend):
        self.frame = frame
        self.game = game

        mini = ((self.game.n-1) // 4) + 1
        ncols = self.game.n + mini
        nrows = self.game.tries + 1
        h, w = self._compute_canvas_size(nrows, ncols)
        self.canvas = Canvas(frame, width=w, height=h)
        self.canvas.pack()

        h, w = self._compute_canvas_size(self.game.colors + 1, 1)
        self.canvas_legend = Canvas(legend, width=w, height=h)
        self.canvas_legend.pack()

        self.current_guess = [0] * self.game.n
        self.cursor_color = 0
        self.show_solution = False
        self.button_ok = None
        self.entries = {}

    def _compute_canvas_size(self, rows, cols):
        cv_height = 2 * self.y0 + (self.height + self.y_pad) * rows
        cv_width = 2 * self.x0 + (self.width + self.x_pad) * cols
        return cv_height, cv_width

    def set_game(self, game):
        self.game = game
        self.current_guess = [0] * self.game.n
        self.show_solution = False

    def reset_canvas(self):
        self.canvas.destroy()
        mini = ((self.game.n-1) // 4) + 1
        ncols = self.game.n + mini
        nrows = self.game.tries + 1
        h, w = self._compute_canvas_size(nrows, ncols)
        self.canvas = Canvas(self.frame, width=w, height=h)
        self.canvas.pack()

    def get_coords(self, row, col):
        """ Get x, y coords for peg at position row, column """
        x = self.x0 + (self.width + self.x_pad) * col
        y = self.y0 + (self.height + self.y_pad) * row
        return x, y

    def draw_peg(self, row, col, color, canvas=None):
        """ draw a peg at given position. """
        if canvas is None:
            canvas = self.canvas
        x0, y0 = self.get_coords(row, col)
        x1 = x0 + self.width
        y1 = y0 + self.height
        return canvas.create_oval(x0, y0, x1, y1, fill=color)

    def draw_mini_pegs(self, row, col, values):
        """ draw mini-pegs at given position. """
        x0, y0 = self.get_coords(row, col)
        x_pad = self.width * 0.2
        y_pad = self.height * 0.2
        w = self.width * 0.4
        h = self.height * 0.4
        n = len(values)
        ncol = (n+1) // 2
        for i in range(n):
            row = i % ncol
            col = i // ncol
            x = x0 + (w + x_pad) * row
            y = y0 + (h + y_pad) * col
            col = self.colors[values[i]]
            self.canvas.create_oval(x, y, x+w, y+h, fill=col)

    def draw_legend(self):
        for i in range(self.game.colors):
            id = self.draw_peg(i, 0, self.colors[i+1], canvas=self.canvas_legend)
            self.canvas_legend.tag_bind(id, '<ButtonPress-1>', self.on_legend_click)

    def submit_guess(self):
        self.game.guess(self.current_guess)
        self.current_guess = [0] * self.game.n
        self.draw()

    def draw_hline(self, row, col0, col1, color):
        x0, y0 = self.get_coords(row, col0)
        y0 -= self.y_pad / 2
        x1 = x0 + (self.width + self.x_pad) * (col1 - col0)
        self.canvas.create_line(x0, y0, x1, y0, fill=color)

    def draw_entries(self):
        if self.entries:
            for entry in self.entries.keys():
                self.canvas.delete(entry)
        self.entries = {}
        i = len(self.game.guesses)
        for j in range(self.game.n):
            color = self.colors[self.current_guess[j]]
            id = self.draw_peg(i, j, color)
            self.canvas.tag_bind(id, '<ButtonPress-1>', self.on_entry_click)
            self.entries[id] = j

    def draw_ok_button(self):
        if self.button_ok:
            self.button_ok.destroy()
        i = len(self.game.guesses)
        j = self.game.n
        x, y = self.get_coords(i, j)
        y += self.y_pad / 3
        self.button_ok = Button(self.frame, text='OK', command=self.submit_guess)
        self.canvas.create_window(x, y, anchor=N+W, window=self.button_ok)

    def draw(self):
        self.canvas.delete('all')

        # draw previous guesses
        for i in range(len(self.game.guesses)):
            guess, response = self.game.guesses[i]
            for j in range(len(guess)):
                self.draw_peg(i, j, self.colors[guess[j]])
            a1 = response[0]
            a2 = response[1]
            a3 = self.game.n - a1 - a2
            vals = ['correct'] * a1 + ['incorrect'] * a2 + ['missing'] * a3
            self.draw_mini_pegs(i, self.game.n, vals)

        # draw current guess
        i = len(self.game.guesses)
        if self.game.state != 'open':
            self.show_solution = True

        if i < self.game.tries:
            if self.show_solution:
                for j in range(self.game.n):
                    self.draw_peg(i, j, 'grey')
                self.draw_mini_pegs(i, self.game.n, ['missing'] * self.game.n)
            else:
                self.draw_entries()
                self.draw_ok_button()

        # draw empty guesses remaining
        for i in range(len(self.game.guesses) + 1, self.game.tries):
            for j in range(self.game.n):
                self.draw_peg(i, j, 'grey')
            self.draw_mini_pegs(i, self.game.n, ['missing'] * self.game.n)

        self.draw_hline(self.game.tries, 0, self.game.n, 'black')

        # draw solution
        sol = self.show_solution
        i = self.game.tries
        for j in range(self.game.n):
            color = self.colors[self.game.solution[j]] if sol else 'grey'
            self.draw_peg(i, j, color)

    def on_legend_click(self, event):
        w = event.widget.find_closest(event.x, event.y)
        self.cursor_color = w[0]

    def on_entry_click(self, event):
        entry_id = event.widget.find_closest(event.x, event.y)[0]
        self.current_guess[self.entries[entry_id]] = self.cursor_color
        self.draw_entries()


if __name__ == '__main__':
    root = Tk()
    game = Game(**options)

    # Game display
    game_frame = Frame(root)
    legend_frame = Frame(root)
    game_widget = GameWidget(game, game_frame, legend_frame)
    game_widget.draw()
    game_widget.draw_legend()

    def new_game():
        game_widget.set_game(Game(**options))
        game_widget.reset_canvas()
        game_widget.draw()

    def restart():
        game_widget.game.restart()
        game_widget.show_solution = False
        game_widget.draw()

    def show_solution():
        game_widget.show_solution = True
        game_widget.draw()

    def solve(treshold):
        def solve_f():
            game = game_widget.game
            if game_widget.button_ok:
                game_widget.button_ok.destroy()
            solver = Solver(game)
            while game.state == 'open':
                solver.guess(treshold)
                game_widget.draw()
        return solve_f

    # Menu
    menu = Frame(root)
    button_new_game = Button(menu, text='New Game', width=sx(20), command=new_game)
    button_restart = Button(menu, text='Restart', width=sx(20), command=restart)
    button_solution = Button(menu, text='Show Solution', width=sx(20), command=show_solution)
    button_solve_fast = Button(menu, text='Solve (Fast)', width=sx(20), command=solve(0.5))
    button_solve_best = Button(menu, text='Solve (Best)', width=sx(20), command=solve(0))
    button_quit = Button(menu, text='Quit', width=sx(20), command=quit)

    # Frames Layout
    menu.grid(row=0, column=0, sticky=N+W, pady=sy(20), padx=sx(20))
    legend_frame.grid(row=1, column=0, sticky=N+E, pady=sy(20), padx=sx(20))
    game_frame.grid(row=0, column=1, rowspan=2)

    # Menu Layout
    button_new_game.grid(row=0, column=0, sticky=N+W)
    button_restart.grid(row=1, column=0, sticky=N+W)
    button_solution.grid(row=2, column=0, sticky=N+W)
    button_solve_fast.grid(row=3, column=0, sticky=N+W)
    button_solve_best.grid(row=4, column=0, sticky=N+W)
    button_quit.grid(row=5, column=0, sticky=N+W)

    root.mainloop()
