#!/usr/bin/env python3
def trans_part(row):
    newrow = ""
    left = 0
    right = len(row) - 1
    inside = False
    while left <= right and row[left] == " ": left += 1
    while right >= 0 and row[right] == " ": right -= 1
    for i, c in enumerate(row):
        if i >= left and i <= right:
            if inside:
                if c != " ": inside = False
            else:
                if c == " ": c = "e"
                if c == chr(0):
                    inside = True
                    c = " "
        newrow += c
    return newrow
