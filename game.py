import random
import time


HUMAN_TYPE = 'h'
AI_TYPE = 'a'
PLAYER_TYPES = [HUMAN_TYPE, AI_TYPE]

PLAYER_ONE = 1
PLAYER_TWO = 2
MARKERS = {
    PLAYER_ONE: 'X',
    PLAYER_TWO: 'O'
}

class Game():
    player_one = None
    player_two = None
    current_player = None
    running = True

    width = 3
    board = [i for i in range(1, 10)]

    def __init__(self):
        self.winning_lines = self._create_win_conditions()

    def _create_win_conditions(self):
        winning_lines = []
        # horizontal
        for i in range(self.width):
            line = []
            for j in range(self.width):
                line.append((i * self.width) + j)
            winning_lines.append(line)

        # vertical
        for i in range(self.width):
            line = []
            for j in range(self.width):
                line.append((j * self.width) + i)
            winning_lines.append(line)

        # forward diagonal
        line = [i * (self.width + 1) for i in range(self.width)]
        winning_lines.append(line)

        # backward diagonal
        line = [i * (self.width - 1) + self.width - 1 for i in range(self.width)]
        winning_lines.append(line)
        return winning_lines

    def build_board(self):
        line_no = 0
        for i in range(self.width):
            start = line_no * self.width
            line = self.board[start:start + self.width]
            line = '|'.join(map(str, line))
            if i < self.width - 1:
                line = line + '\n\t %s' % ('-' * (self.width + self.width - 1))
            line_no += 1
            print('\t', line)

    def run(self):
        print("Let's play a game!")
        self.setup()
        self._decide_first_turn()
        self.take_turn()

    def _decide_first_turn(self):
        self.current_player = self.player_one

    def take_turn(self):
        while self.running is True:
            print("\nIt's %s's turn now." % self.current_player)
            self.build_board()
            if self.current_player.player_type == HUMAN_TYPE:
                turn = self.human_turn()
            else:
                turn = self.ai_turn()
            self.board[turn - 1] = self.current_player.symbol
            if self.check_win_conditions():
                self.running = False
                self.end()
            if self.current_player == self.player_one:
                self.current_player = self.player_two
            else:
                self.current_player = self.player_one

    def check_win_conditions(self):
        if sum(isinstance(space, str) for space in self.board) < 3:
            return
        win = None
        for line in self.winning_lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]]:
                win = True
        return win

    def _get_available_spaces(self):
        return [space for space in self.board if isinstance(space, int)]

    def human_turn(self):
        turn_choice = int(input('\nChoose an unused square from the board.'))
        if turn_choice not in self._get_available_spaces():
            print('\nI said an unused square\n')
            self.human_turn()
        return turn_choice

    def ai_turn(self):
        print('\nThinking...\n') # For dramatic effect
        time.sleep(1)
        return random.choice(self._get_available_spaces())

    def setup(self):
        # for player_number in range(1, 3):
        #     player_type = input('Is player %s a Human or AI? h/a' % player_number).lower()
        #     if player_type not in PLAYER_TYPES:
        #         print('No you loser.')
        #         break
            # self.create_player(player_number, player_type)
        self.create_player(1, HUMAN_TYPE)
        self.create_player(2, AI_TYPE)

    def create_player(self, player_number, player_type):
        if player_type == HUMAN_TYPE:
            if player_number == 1:
                self.player_one = HumanPlayer(player_number)
            else:
                self.player_two = HumanPlayer(player_number)
        if player_type == AI_TYPE:
            if player_number == 2:
                self.player_two = AIPlayer(player_number)
            else:
                self.player_one = AIPlayer(player_number)

    def end(self):
        print('\n%s Wins!' % self.current_player)
        if input('\nWould you like to play again? Y/N?').lower() == 'y':
            self.run()
        else:
            print('\nThanks for playing!')


class Player():
    player_type = None
    player_number = None
    name = None

    def __init__(self, player_number):
        self.player_number = player_number
        self.symbol = MARKERS[player_number]

    def __str__(self):
        return self.name


class HumanPlayer(Player):
    def __init__(self, player_number):
        super().__init__(player_number)
        self.player_type = HUMAN_TYPE
        self.name = input("What is this player's name?")


class AIPlayer(Player):
    def __init__(self, player_number):
        super().__init__(player_number)
        self.player_type = AI_TYPE
        self.name = 'AI %s' % player_number


if __name__ == "__main__":
    if input('Would you like to play a game? Y/N').lower() == 'y':
        game = Game()
        game.run()
