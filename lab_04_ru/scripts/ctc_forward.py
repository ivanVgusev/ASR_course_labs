"""CTC forward recursion in probability space."""
from scripts.ctc_core import BLANK, validate


def extended_target(target, blank=BLANK):
    if not isinstance(target, str) or not isinstance(blank, str) or not blank:
        raise ValueError('target and blank must be strings')
    states = [blank]
    for symbol in target:
        if symbol == blank:
            raise ValueError('target cannot contain blank')
        states.extend([symbol, blank])
    return states


def incoming_sum(previous, extended, state, blank):
    stay_prob = 0
    if state < len(previous):
        stay_prob = previous[state]

    back_one_prob = 0
    if state >= 1:
        back_one_prob = previous[state - 1]

    back_two_prob = 0
    if state >= 2:
        if extended[state] != blank:
            if extended[state] != extended[state - 2]:
                back_two_prob = previous[state - 2]

    return stay_prob + back_one_prob + back_two_prob


def terminal_sum(last_row):
    if len(last_row) == 1:
        return last_row[0]
    return last_row[-2] + last_row[-1]


def forward_table(emissions, target, blank=BLANK):
    states = extended_target(target, blank)
    if not isinstance(emissions, list):
        raise ValueError('emissions must be a list')
    if not emissions:
        return []
    if not isinstance(emissions[0], dict):
        raise ValueError('emission row must be a dictionary')
    alphabet = list(emissions[0])
    validate(emissions, alphabet, blank)
    if any(symbol not in alphabet for symbol in target):
        raise ValueError('target symbol missing from emissions')
    first = [0.0] * len(states)
    first[0] = emissions[0][blank]
    if len(states) > 1:
        first[1] = emissions[0][states[1]]
    table = [first]
    for row in emissions[1:]:
        previous = table[-1]
        table.append([row[symbol] * incoming_sum(previous, states, state_index, blank) for state_index, symbol in enumerate(states)])
    return table


def transcript_probability(table):
    return terminal_sum(table[-1]) if table else 0.0
