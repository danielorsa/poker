from poker import *

# This module employs a markov chain to generate royal flush poker hands


def number_to_card(hand, lookup):
    translation = []
    for i in range(5):
        translation.append(lookup[hand[i]])
    return translation


def display_transitions(starts, trans, random_hands_cards, card_pool, number_to_card_lookup):
    for i in range(len(card_pool)):
        print(card_pool[i], end="\t")
    print("")

    for i in range(len(starts)):
        print(starts[i], end="\t")
    print("")

    print("\t", end="  ")
    for i in range(len(card_pool)):
        print(card_pool[i], end="\t")
    print("")

    for i in range(len(trans)):
        print(card_pool[i], end="\t")
        for j in range(len(trans[i])):
            print(trans[i][j], end="\t")
        print("")


def get_transitions(hand_list_nums):
    starts = [0] * 52
    for hand in hand_list_nums:
        starts[hand[0]] += 1

    row_sum = sum(starts)
    for i in range(52):
        starts[i] = (starts[i] / row_sum)

    transitions = []
    for i in range(52):
        transitions.append([0] * 52)

    for hand in hand_list_nums:
        for i in range(1, len(hand)):
            transitions[hand[i - 1]][hand[i]] += 1

    for i in range(len(transitions)):
        row_sum = sum(transitions[i])
        for k in range(len(transitions[0])):
            if row_sum > 0:
                transitions[i][k] = (transitions[i][k] / row_sum)

    return starts, transitions

def readjust_transitions(card_num, transitions):
    for i in range(52):
        transitions[i][card_num] = 0

    for i in range(len(transitions)):
        row_sum = sum(transitions[i])
        for k in range(len(transitions[0])):
            if row_sum > 0:
                transitions[i][k] = (transitions[i][k] / row_sum)
    return transitions


def markov(starts, transitions, number_to_card_lookup):
    #### FIRST CARD ####
    random_chance = random.random()
    new_hand = []
    chance_sum = 0
    for i in range(52):
        chance_sum += starts[i]
        if chance_sum >= random_chance:
            start_card = i
            new_hand.append(start_card)
            # transitions = readjust_transitions(start_card, transitions)
            break

    ### REST OF HAND ####
    while len(new_hand) < 5:
        last_card = new_hand[-1]
        random_chance = random.random()
        chance_sum = 0
        for i in range(52):
            chance_sum += transitions[last_card][i]
            if chance_sum >= random_chance:
                next_card = i
                new_hand.append(next_card)
                # transitions = readjust_transitions(next_card, transitions)
                break

    cards = []
    for i in range(5):
        cards.append(number_to_card_lookup[new_hand[i]])

    return cards
