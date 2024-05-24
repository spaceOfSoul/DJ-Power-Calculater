import numpy as np
# This function uses mathematical formulas obtained from the website below.
# Source: https://gall.dcinside.com/mgallery/board/view/?id=djmaxrespect&no=626587
# Please refer to the above link for more detailed information on the formula.
def calculate_power(x, c):
    if x < 90:
        t = 0.0
    elif x <= 94.5:
        t = (24 / 135 * np.exp(8 / 9 * (x - 95)) + 0.125)
    elif x <= 95:
        t = calculate_power(94.5, 1) + (calculate_power(95.5, 1) - calculate_power(94.5, 1)) * (x - 94.5) * (x - 94.5) * (x - 95.5) / 30
    elif x <= 95.5:
        t = (24 / 135 * np.exp(2 / 3 * (x - 95)) + 0.125)
    elif x < 96:
        t = calculate_power(96, 1) + 2 * (calculate_power(96.5, 1) - calculate_power(96, 1)) * (x - 96)
    elif x < 97.5:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (3 * x - 250.5) / 40
    elif x < 98:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (x - 76.5) / 20
    elif x < 98.5:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (3 * x - 186.5) / 100
    elif x < 99:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (x - 44) / 50
    elif x < 100:
        t = 8 / 27 * (np.log(x - 95) - np.log(5)) + 1
    elif x == 100:
        t = 1
    else:
        t = 0
    return t * c
