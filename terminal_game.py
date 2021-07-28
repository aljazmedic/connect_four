from game import Game
import numpy as np

RED="\u001b[31m"
BLUE="\u001b[34m"
RESET="\u001b[0m"
CHARACTER="O"

map_obj = {
    1:f"{RED}{CHARACTER}{RESET}|",
    2:f"{BLUE}{CHARACTER}{RESET}|"
}

@np.vectorize
def colorize(i):
    return map_obj.get(i, " |")

class TerminalGame(Game):
    def __init__(self):
        super().__init__()

    def output(self):
        TerminalGame.clear_terminal()
        colored=np.array(list(map(colorize, self.grid)))
        colored=np.append(colored,[[f"{x} " for x in range(0,7)]],axis=0) # Index columns
        colored=np.insert(colored,0,["|"]*6+[' '],axis=1) # Left guard
        print('\n'.join([''.join(row) for row in colored]))

    @classmethod
    def clear_terminal(cls):
        print(chr(27) + "[2J")
    
    def ask_for_input(self):
        idxs = input(f"On move: Player {self.current_player} [0-6] >")
        try:
            if idxs == '': return self.ask_for_input()
            idx = int(idxs)
            return idx
        except ValueError:
            print("Invalid input!")
            return self.ask_for_input()
    
    def begin(self):
        while not self.ended:
            try:
                self.output()
                idx = self.ask_for_input()
                self.make_move(idx)
            except KeyboardInterrupt:
                break
        if self.ended:
            print(f"Player {self.current_player} won!")
        print()
if __name__=="__main__":
    TerminalGame().begin()