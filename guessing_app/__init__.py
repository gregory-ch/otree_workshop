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
    difference = models.IntegerField()
    final_payoff = models.CurrencyField()


class Instructions(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Generate random number when leaving instructions
        player.computer_number = random.randint(C.MIN_NUMBER, C.MAX_NUMBER)


class MyPage(Page):
    form_model = 'player'
    form_fields = ['guess']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Calculate difference and final payoff
        player.difference = abs(player.computer_number - player.guess)
        player.final_payoff = C.ENDOWMENT - player.difference


class Results(Page):
    pass


page_sequence = [Instructions, MyPage, Results]
