from poker import *

# This module employs a Genetic Algorithm to generate royal flush poker hands


def mate(hand0, hand1, card_pool):
    child_hand = []
    dominant_trait = None

    hand0_traits = look_for_best(hand0)
    hand1_traits = look_for_best(hand1)

    if hand0_traits == None and hand1_traits == None:
        dominant_trait = None
    elif hand0_traits == None and hand1_traits != None:
        dominant_trait = 1
    elif hand0_traits != None and hand1_traits == None:
        dominant_trait = 0
    elif len(hand0_traits) > len(hand1_traits):
        dominant_trait = 0
    elif len(hand0_traits) < len(hand1_traits):
        dominant_trait = 1
    elif len(hand0_traits) == len(hand1_traits):
        dominant_trait = random.choice([0, 1])

    if dominant_trait == 0:
        child_hand = hand0_traits
        for i in range(5):
            if len(child_hand) == 5:
                break
            if hand1[i] not in child_hand:
                child_hand.append(hand1[i])
    elif dominant_trait == 1:
        child_hand = hand1_traits
        for i in range(5):
            if len(child_hand) == 5:
                break
            if hand0[i] not in child_hand:
                child_hand.append(hand0[i])
    else:
        sub_hand0 = random.randint(1, 4)
        child_hand = hand0[:sub_hand0+1]
        for i in range(5):
            if len(child_hand) == 5:
                break
            if hand1[i] not in child_hand:
                child_hand.append(hand1[i])

    if len(child_hand) < 5:
        while len(child_hand) < 5:
            rand_card = random.choice(card_pool)
            if rand_card not in child_hand:
                child_hand.append(rand_card)

    return child_hand


def crossoverStage(hand_list, card_pool):
    # selection
    nextGen = []
    nextGen.append(hand_list[0])
    nextGen.append(hand_list[1])
    # crossover
    for i in range(2,len(hand_list)):
        child = mate(hand_list[i-1], hand_list[i], card_pool)
        nextGen.append(child)
    return nextGen


def mutate(hand, card_pool):
    mutated = []
    gene_swap = random.randint(0,5)

    for i in range(5):
        if i != gene_swap:
            mutated.append(hand[i])

    while len(mutated) < 5:
        rand_card = random.choice(card_pool)
        if rand_card not in mutated:
            mutated.append(rand_card)
    return mutated


def mutationStage(hand_list, card_pool):
    post_mutation = []
    post_mutation.append(hand_list[0])
    for hand in hand_list[1:]:
        fitness = evaluate_fitness(hand)
        naturalSelection = random.randint(0, 10)
        if naturalSelection > fitness:
            post_mutation.append(mutate(hand, card_pool))
        else: post_mutation.append(hand)
    return post_mutation


def evaluate_fitness(hand):
    suit_str = suit_strength(hand)
    card_str = card_strength(hand)
    fitness = suit_str + card_str
    return fitness


def sort_by_fitness(hand_list):
    hand_tuples = []
    for i in range(len(hand_list)):
        t = (hand_list[i], evaluate_fitness(hand_list[i]))
        hand_tuples.append(t)
    sorted_hands = sorted(hand_tuples, key=lambda x: x[1])
    sorted_hands.reverse()

    just_hands = []
    for hand in sorted_hands:
        just_hands.append(hand[0])
    return just_hands


def genetic(generation, random_hands_cards, card_pool):
    #evaluate fitness
    sorted_hands = []
    for hand in sort_by_fitness(random_hands_cards):
        sorted_hands.append(hand)

    #selection/crossover
    post_crossover_hands = crossoverStage(sorted_hands, card_pool)
    post_crossover_hands = sort_by_fitness(post_crossover_hands)

    #mutation
    post_mutation_hands = mutationStage(post_crossover_hands, card_pool)
    post_mutation_hands = sort_by_fitness(post_mutation_hands)

    found_flush = False
    for hand in post_mutation_hands:
        if check_royal_flush(hand):
            found_flush = True
            print("it took {0} generations to make a royal flush".format(generation))

    if not found_flush:
        genetic(generation+1, post_mutation_hands, card_pool)

    return post_mutation_hands
