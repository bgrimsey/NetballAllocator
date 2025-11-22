import csv
import random

input_file = 'C:/Users/billy/Desktop/Files/git-projects/NetballAllocator/sample_players.csv'

# Configuration
MEN_ON_COURT = 3
WOMEN_ON_COURT = 4
POSITIONS = ['GS','GA','WA','C','WD','GD','GK']
GENDERS = ['F', 'M']
QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
ATTACK_POS   = ['GS', 'GA']
MID_POS      = ['WA', 'C', 'WD']
DEFENCE_POS  = ['GD', 'GK']

women = 0
men = 0
players = []

# Read the CSV
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Gender'] == 'F':
            women += 1
        elif row['Gender'] == 'M':
            men += 1
        else:
            print("ERROR: incorrect gender in CSV file")
            exit()
        players.append({
            'name': row['Name'],
            'gender': row['Gender'],
            'positions': row['Preferred Positions'].split(';'),
            'quarters': 0,
            'Q1': False,
            'Q2': False,
            'Q3': False,
            'Q4': False

        })

men_quarters = min(4,MEN_ON_COURT/men * 4)
women_quarters = min(4,WOMEN_ON_COURT/women * 4)

print(men_quarters)
print(women_quarters)

team_allocations = []

#for quarter in quarters:
for quarter in QUARTERS:

    man_attack = False
    man_center = False
    man_defence = False


    # ---- Attack ----
    male_attack_candidates = [
        p for p in players
        if p['gender'] == 'M'
        and not p[quarter]
        and any(pos in ATTACK_POS for pos in p['positions'])
        and p['quarters'] < men_quarters
    ]

    if male_attack_candidates:
        chosen = random.choice(male_attack_candidates)
        pos_choices = [p for p in ATTACK_POS if p in chosen['positions']]
        assigned_position = random.choice(pos_choices)

        team_allocations.append({
            'Quarter': quarter,
            'Name': chosen['name'],
            'Assigned Position': assigned_position
        })
        chosen[quarter] = True
        chosen['quarters'] += 1
        man_attack = True


    # ---- Mid Court ----
    male_mid_candidates = [
        p for p in players
        if p['gender'] == 'M'
        and not p[quarter]
        and any(pos in MID_POS for pos in p['positions'])
        and p['quarters'] < men_quarters
    ]

    if male_mid_candidates:
        chosen = random.choice(male_mid_candidates)
        pos_choices = [p for p in MID_POS if p in chosen['positions']]
        assigned_position = random.choice(pos_choices)

        team_allocations.append({
            'Quarter': quarter,
            'Name': chosen['name'],
            'Assigned Position': assigned_position
        })
        chosen[quarter] = True
        chosen['quarters'] += 1
        man_center = True


    # ---- Defence ----
    male_def_candidates = [
        p for p in players
        if p['gender'] == 'M'
        and not p[quarter]
        and any(pos in DEFENCE_POS for pos in p['positions'])
        and p['quarters'] < men_quarters
    ]

    if male_def_candidates:
        chosen = random.choice(male_def_candidates)
        pos_choices = [p for p in DEFENCE_POS if p in chosen['positions']]
        assigned_position = random.choice(pos_choices)

        team_allocations.append({
            'Quarter': quarter,
            'Name': chosen['name'],
            'Assigned Position': assigned_position
        })
        chosen[quarter] = True
        chosen['quarters'] += 1
        man_defence = True


    for position in POSITIONS:

        # If that position has already been allocated by the above logic
        if any(t['Quarter'] == quarter and t['Assigned Position'] == position for t in team_allocations):
            continue

        assigned = False

        for player in players:

            # player already assigned this quarter
            if player[quarter]:
                continue 
            
            if (player['gender'] == 'M' and player['quarters'] >= men_quarters) or \
                (player['gender'] == 'F' and player['quarters'] >= women_quarters):
                continue

            # --- Gender balance rules ---
            if position in ['GS', 'GA'] and player['gender'] == 'M' and man_attack:
                continue
            if position in ['WA', 'C', 'WD'] and player['gender'] == 'M' and man_center:
                continue
            if position in ['GD', 'GK'] and player['gender'] == 'M' and man_defence:
                continue

            # Passed all checks → assign
            team_allocations.append({
                'Quarter': quarter,
                'Name': player['name'],
                'Assigned Position': position
            })
            player[quarter] = True
            player['quarters'] += 1

            # Update male position flags
            if position in ['GS', 'GA'] and player['gender'] == 'M':
                man_attack = True
            if position in ['WA', 'C', 'WD'] and player['gender'] == 'M':
                man_center = True
            if position in ['GD', 'GK'] and player['gender'] == 'M':
                man_defence = True

            assigned = True

            break

        if not assigned:
            # General fallback: assign anyone who is free
            for player in players:
                if not player[quarter]:
                    team_allocations.append({
                        'Quarter': quarter,
                        'Name': player['name'],
                        'Assigned Position': position  # even if not preferred
                    })
                    player[quarter] = True
                    player['quarters'] += 1
                    assigned = True
                    break



# Header
print("Quarter | " + " | ".join(POSITIONS))
print("-" * 80)

for q in QUARTERS:
    # Create a dict to hold assignments for this quarter
    row_positions = {p: "" for p in POSITIONS}

    # Fill in names
    for entry in team_allocations:
        if entry['Quarter'] == q:
            row_positions[entry['Assigned Position']] = entry['Name']
    
    # Print row
    print(
        q + " | " + " | ".join([row_positions[p] for p in POSITIONS])
    )