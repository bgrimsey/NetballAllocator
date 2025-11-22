# NetballAllocator

## Overview
Python program that automatically generates netball team line-ups based on:
- Player position preferences
- Team size
- Gender balance constraints (The fabled 'rule 7')

It helps us quickly create fair and balanced teams! Saving time and avoiding Ava using pen & paper

---

## Input CSV Format
The program reads a CSV file of players with the following:


| Name   | Gender | Preferred Positions |
|--------|--------|-------------------|
| Jeff   | M      | GA;GS             |
| Annie  | F      | GD;GK             |
| Britta | M      | WA;C              |
| Troy   | F      | GD                |

Make sure you have a header row pls