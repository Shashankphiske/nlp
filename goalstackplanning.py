# --- Simple Goal Stack Planner for Block World ---

# Initial and Goal States
initial_state = ["ONTABLE(A)", "ONTABLE(B)", "CLEAR(A)", "CLEAR(B)"]
goal_state = ["ON(A,B)"]

# Actions: Preconditions and Effects
actions = {
    "STACK(x,y)": {
        "pre": ["HOLDING(x)", "CLEAR(y)"],
        "add": ["ON(x,y)", "CLEAR(x)", "ARMEMPTY"],
        "del": ["CLEAR(y)", "HOLDING(x)"]
    },
    "UNSTACK(x,y)": {
        "pre": ["ON(x,y)", "CLEAR(x)", "ARMEMPTY"],
        "add": ["HOLDING(x)", "CLEAR(y)"],
        "del": ["ON(x,y)", "CLEAR(x)", "ARMEMPTY"]
    },
    "PICKUP(x)": {
        "pre": ["ONTABLE(x)", "CLEAR(x)", "ARMEMPTY"],
        "add": ["HOLDING(x)"],
        "del": ["ONTABLE(x)", "CLEAR(x)", "ARMEMPTY"]
    },
    "PUTDOWN(x)": {
        "pre": ["HOLDING(x)"],
        "add": ["ONTABLE(x)", "CLEAR(x)", "ARMEMPTY"],
        "del": ["HOLDING(x)"]
    }
}


# Goal Stack Planning Algorithm
def goal_stack_planning(initial, goal):
    stack = goal.copy()
    current = initial.copy()
    plan = []

    print("Initial State:", current)
    print("Goal State:", goal, "\n")

    while stack:
        top = stack.pop()

        if top in current:
            continue

        elif top in actions:
            act = top
            action_name = act.split("(")[0]
            args = act[act.find("(")+1:act.find(")")].split(",")
            template = actions[action_name + "(x,y)"] if "y" in actions[action_name + "(x,y)"]["pre"][0] else actions[action_name + "(x)"]
            preconds = [p.replace("x", args[0]) if "x" in p else p for p in template["pre"]]
            preconds = [p.replace("y", args[1]) if len(args) > 1 and "y" in p else p for p in preconds]
            for p in reversed(preconds):
                if p not in current:
                    stack.append(p)
            plan.append(act)

        elif "(" in top and ")" in top:
            predicate = top.split("(")[0]
            args = top[top.find("(")+1:top.find(")")].split(",")

            # Determine which action can achieve this condition
            if predicate == "ON":
                stack.append(f"STACK({args[0]},{args[1]})")
            elif predicate == "HOLDING":
                stack.append(f"PICKUP({args[0]})")
            elif predicate == "CLEAR" and args[0] == "B":
                stack.append(f"UNSTACK(A,B)")

        else:
            continue

    print("Generated Plan:")
    for step in plan:
        print("→", step)


# --- Run the Planner ---
goal_stack_planning(initial_state, goal_state)
