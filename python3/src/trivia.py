#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    place: int = 0

    def move_to(self, place):
        self.place = place

class Game:
    def __init__(self):
        self.players = []
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player_index = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append("Rock Question %s" % i)

    def is_playable(self):
        return self.player_count >= 2

    def add(self, player: Player):
        self.players.append(player)
        self.purses[self.player_count] = 0
        self.in_penalty_box[self.player_count] = False

        print(player.name + " was added")
        print("They are player number %s" % len(self.players))

        return True

    @property
    def player_count(self):
        return len(self.players)

    def roll(self, die_roll):
        print("%s is the current player" % self._current_player_name)
        print("They have rolled a %s" % die_roll)

        if not self._current_player_in_penalty_box() or self._is_allowed_to_leave_the_penalty_box(die_roll):
            self._move_current_player(die_roll)
            self._ask_question()

    def _move_current_player(self, die_roll):
        new_place = (self._current_player_place + die_roll) % 12
        self.players[self.current_player_index].move_to(new_place)

        print(self._current_player_name + \
                            '\'s new location is ' + \
                            str(self._current_player_place))

    def _is_allowed_to_leave_the_penalty_box(self, die_roll):
        if self._is_die_roll_odd(die_roll):
            self.is_getting_out_of_penalty_box = True

            print("%s is getting out of the penalty box" % self._current_player_name)
            return True
        else:
            print("%s is not getting out of the penalty box" % self._current_player_name)
            self.is_getting_out_of_penalty_box = False
            return False

    def _is_die_roll_odd(self, die_roll):
        return die_roll % 2 != 0

    def _current_player_in_penalty_box(self):
        return self.in_penalty_box[self.current_player_index]

    def _ask_question(self):
        print("The category is %s" % self._current_category)
        if self._current_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self._current_player_place == 0: return 'Pop'
        if self._current_player_place == 4: return 'Pop'
        if self._current_player_place == 8: return 'Pop'
        if self._current_player_place == 1: return 'Science'
        if self._current_player_place == 5: return 'Science'
        if self._current_player_place == 9: return 'Science'
        if self._current_player_place == 2: return 'Sports'
        if self._current_player_place == 6: return 'Sports'
        if self._current_player_place == 10: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player_index]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player_index] += 1
                print(self._current_player_name + \
                    ' now has ' + \
                    str(self.purses[self.current_player_index]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self._advance_to_next_player()

                return winner
            else:
                self._advance_to_next_player()
                return True



        else:

            print("Answer was corrent!!!!")
            self.purses[self.current_player_index] += 1
            print(self._current_player_name + \
                ' now has ' + \
                str(self.purses[self.current_player_index]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self._advance_to_next_player()

            return winner

    def _advance_to_next_player(self):
        self.current_player_index += 1
        if self.current_player_index == len(self.players): self.current_player_index = 0

    @property
    def _current_player_name(self):
        return self.players[self.current_player_index].name
    
    @property
    def _current_player_place(self):
        return self.players[self.current_player_index].place

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self._current_player_name + " was sent to the penalty box")
        self.in_penalty_box[self.current_player_index] = True

        self._advance_to_next_player()
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player_index] == 6)


from random import randrange
import random

def play_game():
    random.seed(1)


    not_a_winner = False

    game = Game()

    game.add(Player('Chet'))
    game.add(Player('Pat'))
    game.add(Player('Sue'))

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break


if __name__ == '__main__':
    play_game()
