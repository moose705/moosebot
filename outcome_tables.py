def action_outcomes(i):
    if i == 0:
        return "ERROR"
    elif i == 1:
        return "Overwhelming failure"
    elif i < 4:
        return "Failure"
    elif i < 8:
        return "Failure, but not completely"
    elif i < 12:
        return "Neutral outcome."
    elif i < 15:
        return "Success, but with a twist..."
    elif i < 20:
        return "Success!"
    elif i == 20:
        return "Overwhelming success!"

def combat_outcomes(i):
    if i == 0:
        return "ERROR"
    elif i == 1:
        return "Damage yourself"
    elif i < 4:
        return "Miss"
    #elif i < 8:
        #return "Grazed enemy"
    elif i < 12:
        return "Damaged enemy, but there is a downside..."
    elif i < 15:
        return "Successfully damaged enemy"
    elif i < 20:
        return "Critical hit!"
    elif i == 20:
        return "Overwhelming damage!"

def item_outcomes(i):
    if i == 0:
        return "ERROR"
    elif i == 1:
        return "Extremely cursed item"
    elif i < 4:
        return "Cursed item"
    elif i < 8:
        return "Mostly useless item"
    elif i < 12:
        return "Mediocre item"
    elif i < 15:
        return "Good item"
    elif i < 20:
        return "Great item"
    elif i == 20:
        return "OP item"