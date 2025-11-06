from constraint import Problem

teams = ["MI", "CSK", "RCB", "KKR"]

dates = ["Apr1", "Apr2", "Apr3", "Apr4", "Apr5"]

venues = ["Mumbai", "Chennai", "Pune", "Ahmedabad"]

matches = []
for i in range(len(teams)):
    for j in range(i + 1, len(teams)):
        matches.append((teams[i], teams[j]))

problem = Problem()

for match in matches:
    possible_slots = []
    for d in dates:
        for v in venues:
            possible_slots.append((d, v))
    problem.addVariable(str(match), possible_slots)
    
def no_team_twice_a_day(*chosen_slots):
    played = {}
    for match, (date, venue) in zip(matches, chosen_slots):
        for team in match:
            if (team, date) in played:
                return False
            played[(team, date)] = True
    return True

problem.addConstraint(no_team_twice_a_day, [str(m) for m in matches])

solution = problem.getSolution()

print("IPL Match Schedule:")
for match, slot in solution.items():
    print(f"{match} -> Date: {slot[0]}, Venue: {slot[1]}")
