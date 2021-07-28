import numpy as np


class Game:
    OVERFLOW_MASK = 0x1020408102040

    def __init__(self):
        self.mask = 0
        self.position = 0
        self.ended = False
        self.round_no = 0
        self.log = ["Game started"]

    @property
    def status(self):
        return self.log[-1]

    @property
    def current_player(self):
        return self.round_no%2 + 1

    @property
    def winner(self):
        return None if not self.ended else self.current_player

    def make_move(self, move_idx): 
        if self.ended:
            self.log.append("Cannot make move in a finished game!")
            return False
        
        # Get opponent's perspective
        opponents_position = self.position ^ self.mask

        token_at_idx = (self.mask + (1 << (move_idx*7)))
        if (token_at_idx & Game.OVERFLOW_MASK):
            self.log.append("This column is full!")
            return False

        # Drop the token
        self.mask = self.mask | token_at_idx
        
        if Game.connected_four(opponents_position ^ self.mask):
            self.log.append(f"Player: {self.current_player}, Winning move: {move_idx}")
            self.ended = True
        else:
            self.position = opponents_position
            self.round_no += 1
            self.log.append(f"Player: {self.current_player}, Move: {move_idx}")
            # Change player
        return True

    @classmethod
    def connected_four(cls, pos):

        # Horizontal check
        m = pos & (pos >> 7)
        if m & (m >> 14):
            return True

        # Diagonal \
        m = pos & (pos >> 6)
        if m & (m >> 12):
            return True

        # Diagonal /
        m = pos & (pos >> 8)
        if m & (m >> 16):
            return True

        # Vertical
        m = pos & (pos >> 1)
        if m & (m >> 2):
            return True

        # Nothing found
        return False
    
    @classmethod
    def position_to_grid(cls,pos) -> np.array:
        a = [0]*49
        for i in range(48,-1,-1):
            a[i] = pos % 2
            pos >>= 1
        e=np.flip(np.array(a).reshape((7,7)).T,axis=1)
        return np.delete(e, 0, axis=0)

    @property
    def grid(self):
        a, b = (self.current_player, 3-self.current_player)
        r = a * Game.position_to_grid(self.position) + b * Game.position_to_grid(self.position^self.mask)
        return r

if __name__ == "__main__":
    g = Game()
    print(g.grid)
    g.make_move(2)
    g.make_move(2)
    g.make_move(3)
    g.make_move(3)
    g.make_move(4)
    g.make_move(4)
    g.make_move(5)
    print(g.winner)
    print(g.grid)