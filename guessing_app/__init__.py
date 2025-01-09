from otree.api import *
import random


doc = """
A guessing game where players try to guess a number between 0 and 100
"""


class C(BaseConstants):
    NAME_IN_URL = 'guessing_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    ENDOWMENT = cu(100)
    MIN_NUMBER = 0
    MAX_NUMBER = 90


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    computer_number = models.IntegerField()
    guess = models.IntegerField(
        min=C.MIN_NUMBER, 
        max=C.MAX_NUMBER,
        label="Please, insert any number from {} to {}".format(C.MIN_NUMBER, C.MAX_NUMBER),
    )


class Instructions(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.computer_number = random.randint(
            C.MIN_NUMBER, C.MAX_NUMBER
        )


class MyPage(Page):
    form_model = 'player'
    form_fields = ['guess']

    @staticmethod
    def before_next_page(player, timeout_happened):
        difference = abs(player.computer_number - player.guess)
        player.payoff = C.ENDOWMENT - difference

    @staticmethod
    def vars_for_template(player):
        guess = player.field_maybe_none('guess')
        if guess is None:
            return {}
        return {
            'difference': abs(player.computer_number - guess)
        }


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        guess = player.field_maybe_none('guess')
        difference = abs(player.computer_number - guess) if guess is not None else 0
        return {
            'difference': difference
        }


page_sequence = [Instructions, MyPage, Results]
