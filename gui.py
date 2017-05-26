from collections import defaultdict

from tkinter import *

from game import Game


class GamePainter:
    # Peg geometry
    width = 30
    height = 30
    x_pad = 10
    y_pad = 10
    y0 = 20
    x0 = 20

    colors = defaultdict(lambda: 'black',
    {
        0: 'white',
        1: 'red',
        2: 'yellow',
        3: 'green',
        4: 'blue',
        5: 'orange',
        6: 'purple',
    })

    def __init__(self, game, frame):
        self.frame = frame
        self.game = game

        h, w = self._compute_canvas_size()
        self.canvas = Canvas(frame, width=w, height=h)
        self.canvas.pack()

        self.current_guess = [0] * self.game.n
        self.show_solution = False

    def _compute_canvas_size(self):
        mini = (self.game.n // 4) + 1
        cv_height = 2 * self.y0 + (self.height + self.y_pad) * (self.game.tries + 1)
        cv_width = 2 * self.x0 + (self.width + self.x_pad) * (self.game.n + mini)
        return cv_height, cv_width

    def set_game(self, game):
        self.game = game
        self.current_guess = [0] * self.game.n
        self.show_solution = False

    def reset_canvas(self):
        self.canvas.destroy()
        h, w = self._compute_canvas_size()
        self.canvas = Canvas(self.frame, width=w, height=h)
        self.canvas.pack()

    def paint_peg(self, row, col, color):
        """ Paint a peg at given position. """
        x0 = self.x0 + (self.width + self.x_pad) * col
        x1 = x0 + self.width
        y0 = self.y0 + (self.height + self.y_pad) * row
        y1 = y0 + self.height
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def paint_mini_pegs(self, row, col, colors):
        """ Paint a mini-peg at given position. """
        pass

    def paint_hline(self, row, col0, col1, color):
        pass

    def paint_vline(self, row, col0, col1, color):
        pass

    def paint(self):
        self.canvas.delete('all')

        # Paint guesses
        for i in range(len(self.game.guesses)):
            guess = self.game.guesses[i][0]
            for j in range(len(guess)):
                self.paint_peg(i, j, self.colors[guess[j]])

        # Paint entry
        i = len(self.game.guesses)
        for j in range(len(self.current_guess)):
            self.paint_peg(i, j, self.colors[self.current_guess[j]])

        # Paint empty guesses left
        for i in range(len(self.game.guesses) + 1, self.game.tries):
            for j in range(self.game.n):
                self.paint_peg(i, j, 'grey')

        self.paint_hline(self.game.tries, 0, self.game.n, 'black')

        # Paint solution
        sol = self.show_solution
        i = self.game.tries
        for j in range(self.game.n):
            color = self.colors[self.game.solution[j]] if sol else 'grey'
            self.paint_peg(i, j, color)


if __name__ == '__main__':
    root = Tk()
    game = Game()

    # For testing
    game.guess([1, 2, 3, 4])
    game.guess([4, 3, 2, 1])

    # Game display
    game_frame = Frame(root)
    game_painter = GamePainter(game, game_frame)
    game_painter.paint()

    def new_game():
        game_painter.set_game(Game())
        game_painter.reset_canvas()
        game_painter.paint()

    def show_solution():
        game_painter.show_solution = True
        game_painter.paint()

    # Menu
    menu = Frame(root)
    button_new_game = Button(menu, text='New Game', width=20, command=new_game)
    button_quit = Button(menu, text='Quit', width=20, command=quit)
    button_solution = Button(menu, text='Show Solution', width=20, command=show_solution)

    # Layout
    menu.grid(row=0, column=0, sticky=N+W, pady=20, padx=20)
    button_new_game.grid(row=0, column=0, sticky=N+W)
    button_solution.grid(row=1, column=0, sticky=N+W)
    button_quit.grid(row=2, column=0, sticky=N+W)
    game_frame.grid(row=0, column=1)

    root.mainloop()