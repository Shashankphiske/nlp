import random
from collections import deque, defaultdict

DIRS = [(0,1),(1,0),(0,-1),(-1,0)]

def in_bounds(x,y,n):
    return 0 <= x < n and 0 <= y < n

def neighbors(x,y,n):
    for dx,dy in DIRS:
        nx,ny = x+dx, y+dy
        if in_bounds(nx,ny,n):
            yield nx,ny

class WumpusEnv:
    def __init__(self, n=4, pit_prob=0.15, place_wumpus=True, seed=None):
        if seed is not None:
            random.seed(seed)
        self.n = n
        self.pits = set()
        self.wumpus = None
        self.wumpus_alive = place_wumpus
        self.gold = None
        cells = [(i,j) for i in range(n) for j in range(n) if not (i==0 and j==0)]
        # place wumpus
        if place_wumpus:
            self.wumpus = random.choice(cells)
            cells.remove(self.wumpus)
        # place pits
        for c in list(cells):
            if random.random() < pit_prob:
                self.pits.add(c)
                if c in cells: cells.remove(c)
        # place gold
        if cells:
            self.gold = random.choice(cells)
        else:
            self.gold = (n-1,n-1)

    def percept(self, pos):
        x,y = pos
        stench = False
        if self.wumpus_alive and self.wumpus is not None:
            wx,wy = self.wumpus
            stench = abs(wx-x) + abs(wy-y) == 1
        breeze = any(abs(px-x)+abs(py-y)==1 for px,py in self.pits)
        glitter = (pos == self.gold)
        return {"stench":stench, "breeze":breeze, "glitter":glitter}

    def is_deadly(self, pos):
        if pos in self.pits: return True
        if self.wumpus_alive and self.wumpus == pos: return True
        return False

    def display(self, reveal=False):
        n = self.n
        print("Environment ({}x{}):".format(n,n))
        for i in range(n):
            row = []
            for j in range(n):
                c = "."
                if (i,j) == (0,0): c = "A"  # start
                if reveal:
                    if (i,j) == self.wumpus and self.wumpus_alive: c = "W"
                    if (i,j) in self.pits: c = "P"
                    if (i,j) == self.gold: c = "G"
                row.append(c)
            print(" ".join(row))
        print()

class AgentKB:

    def __init__(self, n):
        self.n = n
        self.visited = set()
        self.safe = set()
        self.unsafe = set()  # definitely unsafe (pit or wumpus)
        self.possible_pit = defaultdict(set)    
        self.possible_wumpus = defaultdict(set)
        self.percepts = {}  # pos -> percept dict

    def mark_visited(self, pos, percept):
        self.visited.add(pos)
        self.percepts[pos] = percept
        # visited pos is safe
        self.safe.add(pos)

    def infer_from(self, pos):
        
        p = self.percepts.get(pos, {"stench":False,"breeze":False,"glitter":False})
   
        if not p["breeze"] and not p["stench"]:
            for nb in neighbors(pos[0], pos[1], self.n):
                if nb not in self.visited:
                    self.safe.add(nb)

        if p["breeze"]:
            for nb in neighbors(pos[0], pos[1], self.n):
                if nb not in self.safe:
                    self.possible_pit[pos].add(nb)

        if p["stench"]:
            for nb in neighbors(pos[0], pos[1], self.n):
                if nb not in self.safe:
                    self.possible_wumpus[pos].add(nb)

    def consolidate_possibilities(self):
        for pos in list(self.possible_pit.keys()):
            self.possible_pit[pos] = {c for c in self.possible_pit[pos] if c not in self.safe}
            if not self.possible_pit[pos]:
                del self.possible_pit[pos]
        for pos in list(self.possible_wumpus.keys()):
            self.possible_wumpus[pos] = {c for c in self.possible_wumpus[pos] if c not in self.safe}
            if not self.possible_wumpus[pos]:
                del self.possible_wumpus[pos]

        if self.possible_pit:
            all_sets = list(self.possible_pit.values())

            inter = set.intersection(*all_sets) if len(all_sets) > 0 else set()
            if len(inter) == 1:

                cell = next(iter(inter))
                self.unsafe.add(cell)

        if self.possible_wumpus:
            all_sets = list(self.possible_wumpus.values())
            inter = set.intersection(*all_sets) if len(all_sets) > 0 else set()
            if len(inter) == 1:
                cell = next(iter(inter))
                self.unsafe.add(cell)

    def is_known_safe(self, pos):
        return pos in self.safe

    def is_known_unsafe(self, pos):
        return pos in self.unsafe

    def get_safe_unvisited_neighbors(self, pos):
        res = []
        for nb in neighbors(pos[0], pos[1], self.n):
            if nb not in self.visited and nb in self.safe:
                res.append(nb)
        return res

    def all_known_safe_unvisited(self):
        return [s for s in self.safe if s not in self.visited]

def shortest_path(start, goal, n, allowed):
    if start == goal: return [start]
    q = deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        for nb in neighbors(u[0], u[1], n):
            if nb in parent: continue
            if nb not in allowed: continue
            parent[nb] = u
            if nb == goal:
                # reconstruct
                path = []
                cur = nb
                while cur:
                    path.append(cur)
                    cur = parent[cur]
                return list(reversed(path))
            q.append(nb)
    return None

class Agent:
    def __init__(self, n):
        self.n = n
        self.pos = (0,0)
        self.kb = AgentKB(n)
        # mark start safe/visited
        self.kb.mark_visited(self.pos, {"stench":False,"breeze":False,"glitter":False})
        self.kb.safe.add(self.pos)

    def perceive_and_update(self, env):
        percept = env.percept(self.pos)
        self.kb.mark_visited(self.pos, percept)
        self.kb.infer_from(self.pos)
        self.kb.consolidate_possibilities()
        # if current pos safe, neighbors from no-percepts could be added already
        return percept

    def choose_next(self):
        # 1) any adjacent known safe unvisited neighbor
        for nb in neighbors(self.pos[0], self.pos[1], self.n):
            if nb not in self.kb.visited and self.kb.is_known_safe(nb):
                return nb
        # 2) any known safe unvisited cell anywhere -> path plan to it using only known-safe cells
        targets = self.kb.all_known_safe_unvisited()
        if targets:
            # choose nearest by BFS distance on allowed safe cells
            allowed = set(self.kb.safe) | set(self.kb.visited)
            best_path = None
            best_len = None
            for t in targets:
                path = shortest_path(self.pos, t, self.n, allowed)
                if path:
                    if best_len is None or len(path) < best_len:
                        best_len = len(path)
                        best_path = path
            if best_path and len(best_path) >= 2:
                return best_path[1]  # step toward target
        # 3) No known safe frontier -> be conservative: do not step into possible unsafe cells.
        return None

    def move_to(self, nxt):
        self.pos = nxt

def run_simulation(n=4, pit_prob=0.15, seed=None, verbose=True, max_steps=200):
    env = WumpusEnv(n=n, pit_prob=pit_prob, place_wumpus=True, seed=seed)
    agent = Agent(n)
    step = 0
    found_gold = False
    if verbose:
        print("Initial environment (hidden):")
        env.display(reveal=False)
        print("Agent starts at (0,0). Running simulation...\n")
    while step < max_steps:
        percept = agent.perceive_and_update(env)
        if verbose:
            print(f"Step {step}: Agent at {agent.pos}, percept={percept}")
        # If glitter -> found gold
        if percept["glitter"]:
            if verbose: print("Agent found the gold at", agent.pos)
            found_gold = True
            break
        # choose next move
        nxt = agent.choose_next()
        if nxt is None:
            # stuck — no known safe move
            if verbose: print("Agent has no known safe moves left; stopping.")
            break
        # if the chosen next is actually deadly according to env (KB was wrong), agent dies
        if env.is_deadly(nxt):
            # agent attempted to move into deadly cell; mark as unsafe and continue
            if verbose:
                print("Agent attempted to step into deadly cell", nxt, "- marking unsafe and backtracking.")
            agent.kb.unsafe.add(nxt)
            # remove from safe if incorrectly marked
            if nxt in agent.kb.safe:
                agent.kb.safe.remove(nxt)
            agent.kb.consolidate_possibilities()
            step += 1
            continue
        # move agent
        agent.move_to(nxt)
        step += 1

    if verbose:
        print("\nFinal environment (reveal):")
        env.display(reveal=True)
        print("Visited cells:", sorted(agent.kb.visited))
        print("Known safe cells:", sorted(agent.kb.safe))
        print("Known unsafe cells (deduced):", sorted(agent.kb.unsafe))
        print("Found gold?" , found_gold)
    return found_gold

if __name__ == "__main__":
    # Example runs
    print("=== Wumpus World Simulator ===\n")
    # run a few random seeds to see behavior
    for s in [1, 7, 42]:
        print(f"---- Run with seed={s} ----")
        run_simulation(n=4, pit_prob=0.18, seed=s, verbose=True, max_steps=200)
        print("\n")
