import random

# This module includes methods needed for using the Markov Chain and Genetic Algorithm to generate royal flushes


def make_deck():
    deck_points = {}
    for i in range(2, 11):
        for type in ["H", "D", "C", "S"]:
            if i ==10:
                deck_points["{0}-{1}".format(i, type)] = i
            else:
                deck_points["0{0}-{1}".format(i, type)] = i
    i = 11
    for face in ["JA", "QN", "KG", "AC"]:
        for type in ["H", "D", "C", "S"]:
            deck_points["{0}-{1}".format(face, type)] = i
        i += 1

    card_to_number_lookup = {}
    num = 0
    for card in [2, 3, 4, 5, 6, 7, 8, 9, 10, "JA", "QN", "KG", "AC"]:
        for type in ["H", "D", "C", "S"]:
            if num < 32:
                card_to_number_lookup["0{0}-{1}".format(card, type)] = num
            else:
                card_to_number_lookup["{0}-{1}".format(card, type)] = num
            num += 1

    number_to_card_lookup = {}
    for i in card_to_number_lookup:
        number_to_card_lookup[card_to_number_lookup[i]] = i

    card_pool = []
    for i in card_to_number_lookup:
        card_pool.append(i)

    return deck_points, card_to_number_lookup, number_to_card_lookup, card_pool


def get_random_hands(n):
    deck_points, card_to_number_lookup, number_to_card_lookup, card_pool = make_deck()
    random_hand_sample_cards = []
    random_hand_sample_nums = []
    for i in range(n):
        random_hand = random.sample(range(52), 5)
        random_hand_sample_nums.append(random_hand)
        hand_translated = []
        for j in range(5):
            hand_translated.append(number_to_card_lookup[random_hand_sample_nums[i][j]])
        random_hand_sample_cards.append(hand_translated)
    return random_hand_sample_cards, random_hand_sample_nums


def suit_strength(hand):
    spades = 0
    diamonds = 0
    hearts = 0
    clubs = 0
    for i in range(5):
        if hand[i][-1] == "S":
            spades += 1
        elif hand[i][-1] == "D":
            diamonds += 1
        elif hand[i][-1] == "H":
            hearts += 1
        elif hand[i][-1] == "C":
            clubs += 1

    strength = max(spades, diamonds, hearts, clubs)

    return strength


def card_strength(hand):
    strength = 0
    for face in ["AC", "KG", "QN", "JA", "10"]:
        for i in range(5):
            if face in hand[i]:
                strength += 1

    return strength


def look_for_suit(sub_hand):
    spades = 0
    diamonds = 0
    hearts = 0
    clubs = 0
    for i in range(len(sub_hand)):
        if sub_hand[i][-1] == "S":
            spades += 1
        elif sub_hand[i][-1] == "D":
            diamonds += 1
        elif sub_hand[i][-1] == "H":
            hearts += 1
        elif sub_hand[i][-1] == "C":
            clubs += 1

    strength = max(spades, diamonds, hearts, clubs)

    if strength == spades:
        suit = "S"
    elif strength == diamonds:
        suit = "D"
    elif strength == hearts:
        suit = "H"
    elif strength == clubs:
        suit = "C"

    best_subhand = []
    for i in range(len(sub_hand)):
        if sub_hand[i][-1] == suit:
            best_subhand.append(sub_hand[i])

    return best_subhand


def look_for_best(hand):
    best = []
    for i in range(5):
        if "AC" in hand[i]:
            best.append(hand[i])
        if "KG" in hand[i]:
            best.append(hand[i])
        if "QN" in hand[i]:
            best.append(hand[i])
        if "JA" in hand[i]:
            best.append(hand[i])
        if "10" in hand[i]:
            best.append(hand[i])
    best = look_for_suit(best)
    if len(best) == 0:
        return None
    else:
        return best


def check_royal_flush(hand):
    royal_flush = False
    royal_flush_suit = hand[0][-1]
    for i in range(5):
        if "AC" in hand[i] and hand[i][-1] == royal_flush_suit:
            royal_flush = True
            break
    if royal_flush:
        for i in range(5):
            if "KG" in hand[i] and hand[i][-1] == royal_flush_suit:
                royal_flush = True
                break
            royal_flush = False
    if royal_flush:
        for i in range(5):
            if "QN" in hand[i] and hand[i][-1] == royal_flush_suit:
                royal_flush = True
                break
            royal_flush = False
    if royal_flush:
        for i in range(5):
            if "JA" in hand[i] and hand[i][-1] == royal_flush_suit:
                royal_flush = True
                break
            royal_flush = False
    if royal_flush:
        for i in range(5):
            if "10" in hand[i] and hand[i][-1] == royal_flush_suit:
                royal_flush = True
                break
            royal_flush = False
    if royal_flush:
        print(hand, "is a royal flush")
        return True


def check_duplicates(hand):
    dupe = False
    for i in range(5):
        check = hand[i]
        for j in range(5):
            if i == j:
                dupe = False
            else:
                if hand[j] == check:
                    print(hand, "has a duplicate")
                    return True
