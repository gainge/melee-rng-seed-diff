# Taken from savestate's reddit post explaining Melee's RNG System
# All credit goes to savestate and their hard work!

#@804d5f90
seed = 0x00000001

#Gets inlined in both functions
#This one is egregious because it ends up being called twice in each
def get_seed():
    global seed
    return seed

#Gets inlined in both functions
#Uses a Linear Congruential Generator with a = 214013, c = 2531011, m = 2**32
#Has a period of 2**32 which is optimal considering the modulus
def next_seed():
    global seed
    seed = ((seed * 214013) + 2531011) % 2**32

def advance_seed(seed):
    return ((seed * 214013) + 2531011) % 2**32

#@80380580
#Returns a value between 0 and max_val-1
def get_random_int(max_val):
    next_seed()
    top_bits = get_seed() // 2**16
    return (max_val * top_bits) // 2**16

#@80380528
#Returns an evenly spaced value between 0 and 65535/65536
def get_random_float():
    next_seed()
    top_bits = get_seed() // 2**16
    return top_bits / 65536


def find_seed_difference(startSeed, targetSeed):
    if startSeed == targetSeed: return 0

    # Establish pointers at both start and target to handle case
    # where start is ahead of target
    seedFromStart = startSeed
    seedFromTarget = targetSeed
    rollCount = 0

    while True:
        seedFromStart = advance_seed(seedFromStart)
        seedFromTarget = advance_seed(seedFromTarget)
        rollCount += 1
        
        if seedFromStart == targetSeed or seedFromTarget == startSeed: break

    # check if target was reached from start
    if seedFromStart == targetSeed:
        return rollCount
    else:
        # Starting seed was ahead of target, return negative offset
        return -1 * rollCount


def is_quit(userInput):
    return userInput == 'x' or userInput == 'X'


def get_user_hex(prompt='Please Enter Seed'):
    while True:
        userSeed = input(prompt)
        userSeed = userSeed.replace(' ', '')

        # Return if quit sentinel is entered
        if is_quit(userSeed): return userSeed

        # Otherwise, validate the hex input
        try:
            intVal = int(userSeed, 16)
            return intVal
        except ValueError:
            print()
            print('!----- Please enter a hex value -----!')
            

def display_hex_from_int(val):
    hexString = "{0:#0{1}x}".format(val,10).upper()

    return f'0x{hexString[2:]}'

print('=======================')
print('SSBM RNG Seed Diff Calc')
print('=======================')
while True:
    print('Please Supply Seeds (x to quit)')
    # Grab hex seeds from the user
    startSeed = get_user_hex('Please Enter First Seed: ')
    if is_quit(startSeed): break

    endSeed = get_user_hex('Please Enter Second Seed: ')
    if is_quit(endSeed): break

    print()

    diff = find_seed_difference(startSeed, endSeed)

    if diff == -1:
        print('Seed wraparound, please check input and try again')
    else:
        print(f'{display_hex_from_int(startSeed)} => {display_hex_from_int(endSeed)}')
        print(f'Seed Diff: {diff}')
        print('========================================')

print('Exiting....')


