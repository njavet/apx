

def estimate_orm(weight, reps):
    if int(reps) < 1:
        return 0
    elif int(reps) == 1:
        return weight
    elif int(reps) == 2:
        return weight / 0.97
    elif int(reps) == 3:
        return weight / 0.94
    elif int(reps) == 4:
        return weight / 0.92
    elif int(reps) == 5:
        return weight / 0.89
    elif int(reps) == 6:
        return weight / 0.86
    elif int(reps) == 7:
        return weight / 0.83
    elif int(reps) == 8:
        return weight / 0.81
    elif int(reps) == 9:
        return weight / 0.78
    elif int(reps) == 10:
        return weight / 0.75
    elif int(reps) == 11:
        return weight / 0.73
    elif int(reps) == 12:
        return weight / 0.71
    elif int(reps) == 13:
        return weight / 0.70
    elif int(reps) == 14:
        return weight / 0.68
    elif int(reps) == 15:
        return weight / 0.67
    elif int(reps) == 16:
        return weight / 0.65
    elif int(reps) == 17:
        return weight / 0.64
    elif int(reps) == 18:
        return weight / 0.63
    elif int(reps) == 19:
        return weight / 0.61
    elif int(reps) == 20:
        return weight / 0.60
    elif int(reps) == 21:
        return weight / 0.59
    elif int(reps) == 22:
        return weight / 0.58
    elif int(reps) == 23:
        return weight / 0.57
    elif int(reps) == 24:
        return weight / 0.56
    elif int(reps) == 25:
        return weight / 0.55
    elif int(reps) == 26:
        return weight / 0.54
    elif int(reps) == 27:
        return weight / 0.53
    elif int(reps) == 28:
        return weight / 0.52
    elif int(reps) == 29:
        return weight / 0.51
    elif int(reps) == 30:
        return weight / 0.50
    else:
        return weight

