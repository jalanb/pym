try:
    1 / 0
finally:
    print("Duh")

try:
    1 / 0
except ZeroDivisionError:
    print("D'oh!")
finally:
    print("Damn")
