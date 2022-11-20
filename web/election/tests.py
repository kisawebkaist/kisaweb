from django.test import TestCase
from election.expression_parser import evaluate
from random import randint

# Create your tests here.


# to test the adjusted votes formula
def test_adjusted_votes_formula(formula):
    
    # basically generates 10 random election vote instance
    # that obeys the constraints (e.g. ...-votes-me <= ...-votes-all)
    # then tests the formula through the evaluator

    def generate_random_votes():
        votes = {
            'kiva': randint(1, 1000),
            'kova': randint(1, 1000),
            'nkva': randint(1, 1000),
        }
        votes['kivm'] = randint(1, votes['kiva'])
        votes['kovm'] = randint(1, votes['kova'])
        votes['nkvm'] = randint(1, votes['nkva'])
        return votes

    test_cases = [
        generate_random_votes() for _ in range(10)
    ]

    for case in test_cases:
        status, result = evaluate(formula, **case)
        if not status:
            return result
    
    return 'OK'