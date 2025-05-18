from queue import PriorityQueue, Queue
from collections import deque, defaultdict
from copy import deepcopy
import heapq
import time
import random
import math
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QLabel, QGridLayout
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



MOVES = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}
initial = ((2, 6, 5), (0, 8, 7), (4, 3, 1))
goal = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

special_states = [
    ((1, 2, 3), (4, 5, 6), (7, 0, 8)),
    ((1, 2, 3), (4, 5, 6), (0, 7, 8)),
    ((2, 5, 3), (1, 6, 8), (4, 0, 7)),
    ((5, 1, 3), (4, 2, 6), (0, 7, 8)),
    ((2, 5, 3), (0, 4, 6), (7, 1, 8)),
    ((1, 2, 3), (7, 4, 0), (8, 6, 5)),
    ((1, 2, 0), (4, 5, 3), (7, 8, 6)),
    ((4, 1, 2), (0, 5, 3), (7, 8, 6)),
    ((1, 0, 2), (4, 5, 3), (7, 8, 6)),
    ((1, 2, 3), (4, 8, 5), (7, 6, 0)),
    ((1, 5, 0), (4, 8, 2), (7, 6, 3)),
    ((2, 7, 3), (0, 4, 6), (1, 5, 8))
]

def get_goal_positions(goal):
    return {val: (i, j) for i, row in enumerate(goal) for j, val in enumerate(row)}

def heuristic(state, goal_positions):
    return sum(abs(i - goal_positions[val][0]) + abs(j - goal_positions[val][1]) 
               for i, row in enumerate(state) for j, val in enumerate(row) if val)

def get_valid_actions(state):
    x, y = next((i, j) for i, row in enumerate(state) for j, v in enumerate(row) if v == 0)
    valid = []
    if x > 0: valid.append("U")
    if x < 2: valid.append("D")
    if y > 0: valid.append("L")
    if y < 2: valid.append("R")
    return valid
    
def apply_action(state, action, move, uncertain_actions):
    results = set()
    valid_dirs = get_valid_actions(state)
    found = False
    for actual_dir in uncertain_actions.get(action, []):
        if actual_dir in valid_dirs:
            new_state = move(state, actual_dir)
            if new_state:
                results.add(new_state)
                found = True
    if not found:
        results.add(state)  # Nếu không move được thì giữ nguyên
    return list(results)


class InputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Puzzle State")
        self.layout = QtWidgets.QVBoxLayout()
        self.inputs = []
        
        grid_layout = QtWidgets.QGridLayout()
        for i in range(3):
            row_inputs = []
            for j in range(3):
                line_edit = QtWidgets.QLineEdit()
                line_edit.setFixedSize(40, 40)
                grid_layout.addWidget(line_edit, i, j)
                row_inputs.append(line_edit)
            self.inputs.append(row_inputs)
        
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        
        self.layout.addLayout(grid_layout)
        self.layout.addWidget(self.ok_button)
        self.setLayout(self.layout)
    
    def get_state(self):
        try:
            return tuple(tuple(int(self.inputs[i][j].text()) for j in range(3)) for i in range(3))
        except ValueError:
            return None
    
class Puzzle(QtWidgets.QMainWindow):
    def __init__(self, initial, goal):
        super().__init__()
        uic.loadUi("giaodienPUzz.ui", self)
        self.start_state = initial
        self.goal_state = goal
        self.goal_positions = get_goal_positions(goal)
        self.uncertain_actions = {
            "U": ["U", "L", "R"],
            "D": ["D", "L", "R"],
            "L": ["L", "U", "D"],
            "R": ["R", "U", "D"]
        }
        
        self.algorithm_stats = {
            "Uninformed": [],
            "Informed": [],
            "Local": [],
            "Complex": [],
            "CSPs": [],
            "Reinforcement": []
        }
        self.chart_btn.clicked.connect(self.draw_all_charts)
        self.Uninformed = self.uninformed_grb
        self.Informed = self.informed_grb
        self.Local = self.local_grb
        self.Complex_Environments = self.complex_grb
        self.CSPs = self.csps_grb
        self.Reinforcement_Learning = self.rein_grb
        
        self.is_paused = False
        self.is_running = False
        self.play_pause_btn.clicked.connect(self.toggle_animation)
        self.search_prB.setValue(0)
        
        self.labels = [self.n1_lbl, self.n2_lbl, self.n3_lbl, 
                       self.n4_lbl, self.n5_lbl, self.n6_lbl,
                       self.n7_lbl, self.n8_lbl, self.n9_lbl]
        
        self.uninformed_cmb.currentIndexChanged.connect(self.solve_combo)
        self.informed_cmb.currentIndexChanged.connect(self.solve_combo)
        self.local_cmb.currentIndexChanged.connect(self.solve_combo)
        self.complex_cmb.currentIndexChanged.connect(self.solve_combo)
        self.csps_cmb.currentIndexChanged.connect(self.solve_combo)
        self.reinforcement_cmb.currentIndexChanged.connect(self.solve_combo)

        self.input_btn.clicked.connect(self.get_user_input)
        self.random_btn.clicked.connect(self.set_random_state)
        self.special_btn.clicked.connect(self.special_state)
        
        self.update_puzzle(self.start_state)
        
        self.reset_btn.clicked.connect(lambda: self.solve("reset"))
        
    def get_user_input(self):
        dialog = InputDialog(self)
        if dialog.exec_():
            self.start_state = dialog.get_state()
            self.update_puzzle(self.start_state)
    
    def set_random_state(self):
        nums = list(range(9))
        random.shuffle(nums)
        self.start_state = tuple(tuple(nums[i * 3:(i + 1) * 3]) for i in range(3))
        self.update_puzzle(self.start_state)
        
    def special_state(self):
        self.start_state = random.choice(special_states)
        self.update_puzzle(self.start_state)
        
    def update_puzzle(self, state):
        flat_state = [num for row in state for num in row]
        for lbl, num in zip(self.labels, flat_state):
            lbl.setText(str(num) if num != 0 else "")
            
    def clear_all_comboboxes(self):
        self.uninformed_cmb.setCurrentIndex(-1)
        self.informed_cmb.setCurrentIndex(-1)
        self.local_cmb.setCurrentIndex(-1)
        self.complex_cmb.setCurrentIndex(-1)
        self.csps_cmb.setCurrentIndex(-1)
        self.reinforcement_cmb.setCurrentIndex(-1)

    def solve_combo(self):
        self.solve("combo")

            
    def solve(self, method):
        uninformed = self.uninformed_cmb.currentText()
        informed = self.informed_cmb.currentText()
        local = self.local_cmb.currentText()
        complex = self.complex_cmb.currentText()
        csps = self.csps_cmb.currentText()
        rein = self.reinforcement_cmb.currentText()

        start_time = time.time()
        path = []

        if method == "reset":
            if hasattr(self, 'timer') and self.timer.isActive():
                self.timer.stop()
            self.is_running = False
            self.is_paused = False
            self.search_prB.setValue(0)
            self.play_pause_btn.setEnabled(True)
            self.update_puzzle(self.start_state)
            self.road_list.clear()
            self.name_lbl.setText("Algorithm_Name")
            self.step_lbl.setText("Steps:")
            self.time_lbl.setText("Time:")
            self.uninformed_cmb.setCurrentIndex(-1)
            self.informed_cmb.setCurrentIndex(-1)
            self.local_cmb.setCurrentIndex(-1)
            self.complex_cmb.setCurrentIndex(-1)
            self.csps_cmb.setCurrentIndex(-1)
            self.reinforcement_cmb.setCurrentIndex(-1)
            return

        #uninformed
        if uninformed == "Breath-first Search (BFS)":
            path = self.bfs(self.start_state, self.goal_state)
            self.name_lbl.setText(uninformed)
            
        elif uninformed == "Depth-first Search (DFS)":
            path = self.dfs(self.start_state, self.goal_state)
            self.name_lbl.setText(uninformed)
        elif uninformed == "Iterative Deepening (IDDFS)":
            path = self.iddfs(self.start_state, self.goal_state)
            self.name_lbl.setText(uninformed)
        elif uninformed == "Uniform Cost Search (UCS)":
            path = self.ucs(self.start_state, self.goal_state)
            self.name_lbl.setText(uninformed)
            
        ##informed
        elif informed == "Greedy Search":
            path = self.greedy(self.start_state, self.goal_state)
            self.name_lbl.setText(informed)
        elif informed == "A*":
            path = self.a_star(self.start_state, self.goal_state)
            self.name_lbl.setText(informed)
        elif informed == "IDA*":
            path = self.ida_star(self.start_state, self.goal_state)
            self.name_lbl.setText(informed)
            
        ##local
        elif local == "Simple Hill Climbing (SHC)":
            path = self.shc(self.start_state, self.goal_state)
            self.name_lbl.setText(local)
        elif local == "Steepest Ascent Hill Climbing (SAHC)":
            path = self.sahc(self.start_state, self.goal_state)
            self.name_lbl.setText(local)
        elif local == "Stochastic Hill Climbing (StHC)":
            path = self.sthc(self.start_state, self.goal_state)
            self.name_lbl.setText(local)
        elif local == "Simulated Annealing (SA)":
            path = self.sa(self.start_state, self.goal_state)
            self.name_lbl.setText(local)
        elif local == "Beam Search":
            path = self.bs(self.start_state, self.goal_state)
            self.name_lbl.setText(local)
        elif local == "Genetic Algorithm (GA)":
            path = self.ga(self.start_state, self.goal_state)
            self.name_lbl.setText(local)
            
        ##complex
        elif complex == "And-Or":
            path = self.and_or(self.start_state, self.goal_state)
            self.name_lbl.setText(complex)
        elif complex == "Sensorless":
            path = self.sensorless(self.start_state, self.goal_state)
            self.name_lbl.setText(complex)
        
        ##csps
        elif csps == "Backtracking":
            path = self.backtracking(self.start_state, self.goal_state)
            self.name_lbl.setText(csps)
        elif csps == "Forward Checking":
            path = self.forward_checking(self.start_state, self.goal_state)
            self.name_lbl.setText(csps)
        elif csps == "Min-Conflicts":
            path = self.min_conflicts(self.start_state, self.goal_state)
            self.name_lbl.setText(csps)
            
        ##reinforcement learning
        elif rein == "Q-Learning":
            path = self.q_learning()
            self.name_lbl.setText(rein)

        if path is not None:
            if uninformed:
                self.informed_cmb.setCurrentIndex(-1)
                self.local_cmb.setCurrentIndex(-1)
                self.complex_cmb.setCurrentIndex(-1)
                self.csps_cmb.setCurrentIndex(-1)
                self.reinforcement_cmb.setCurrentIndex(-1)
            elif informed:
                self.uninformed_cmb.setCurrentIndex(-1)
                self.local_cmb.setCurrentIndex(-1)
                self.complex_cmb.setCurrentIndex(-1)
                self.csps_cmb.setCurrentIndex(-1)
                self.reinforcement_cmb.setCurrentIndex(-1)
            elif local:
                self.uninformed_cmb.setCurrentIndex(-1)
                self.informed_cmb.setCurrentIndex(-1)
                self.complex_cmb.setCurrentIndex(-1)
                self.csps_cmb.setCurrentIndex(-1)
                self.reinforcement_cmb.setCurrentIndex(-1)
            elif complex:
                self.uninformed_cmb.setCurrentIndex(-1)
                self.informed_cmb.setCurrentIndex(-1)
                self.local_cmb.setCurrentIndex(-1)
                self.csps_cmb.setCurrentIndex(-1)
                self.reinforcement_cmb.setCurrentIndex(-1)
            elif csps:
                self.uninformed_cmb.setCurrentIndex(-1)
                self.informed_cmb.setCurrentIndex(-1)
                self.local_cmb.setCurrentIndex(-1)
                self.complex_cmb.setCurrentIndex(-1)
                self.reinforcement_cmb.setCurrentIndex(-1)
            elif rein:
                self.uninformed_cmb.setCurrentIndex(-1)
                self.informed_cmb.setCurrentIndex(-1)
                self.local_cmb.setCurrentIndex(-1)
                self.csps_cmb.setCurrentIndex(-1)
                self.complex_cmb.setCurrentIndex(-1)
        end_time = time.time()

        if path:
            elapsed = end_time - start_time
            steps = len(path)
            self.save_algorithm_result(self.name_lbl.text(), elapsed, steps)
            self.road_list.addItem(f"Path: {path}")
            self.step_lbl.setText(f"Steps: {steps}")
            self.time_lbl.setText(f"Time: {elapsed:.4f} sec")
            self.animate_solution(path)
        else:
            self.road_list.addItem("No solution found")
            elapsed = 0
            steps = 0
            self.save_algorithm_result(self.name_lbl.text(), elapsed, steps)

##Vẽ biểu đồ theo từng nhóm thuật toán
    def draw_all_charts(self):
        self.plot_group_chart("Uninformed", self.Uninformed)
        self.plot_group_chart("Informed", self.Informed)
        self.plot_group_chart("Local", self.Local)
        self.plot_group_chart("Complex", self.Complex_Environments)
        self.plot_group_chart("CSPs", self.CSPs)
        self.plot_group_chart("Reinforcement", self.Reinforcement_Learning)

    
    def save_algorithm_result(self, name, time_val, step_val):
        if "BFS" in name or "DFS" in name or "IDDFS" in name or "UCS" in name:
            group = "Uninformed"
        elif "Greedy" in name or "A*" in name:
            group = "Informed"
        elif "Hill Climbing" in name or "Beam" in name or "SA" in name or "GA" in name:
            group = "Local"
        elif "And-Or" in name or "Sensorless" in name:
            group = "Complex"
        elif "Backtracking" in name or "Forward" in name or "Min-Conflicts" in name:
            group = "CSPs"
        elif "Q-Learning" in name:
            group = "Reinforcement"
        else:
            return
        
        for i, (alg_name, _, _) in enumerate(self.algorithm_stats[group]):
            if alg_name == name:
                self.algorithm_stats[group][i] = (name, time_val, step_val)
                break
        else:
            self.algorithm_stats[group].append((name, time_val, step_val))
        
    def plot_group_chart(self, group_name, widget):
        data = self.algorithm_stats[group_name]
        if not data:
            return

        names, times, steps = zip(*data)
        x = range(len(names))

        fig, ax1 = plt.subplots(figsize=(3.8, 2.5))
        ax2 = ax1.twinx()

        bar1 = ax1.bar([i - 0.2 for i in x], times, width=0.4, label="Time (s)", color='skyblue')
        bar2 = ax2.bar([i + 0.2 for i in x], steps, width=0.4, label="Steps", color='green')

        # Cấu hình trục
        ax1.set_ylabel("Time (s)", fontsize=8)
        ax2.set_ylabel("Steps", fontsize=8)
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=15, ha='right', fontsize=5)
        ax1.set_title(group_name + " Comparison", fontsize=8)

        # Hiển thị giá trị trên cột
        for i in x:
            ax1.text(i - 0.2, times[i] + 0.01, f"{times[i]:.4f}", ha='center', va='bottom', fontsize=3)
            ax2.text(i + 0.2, steps[i] + 0.05, f"{steps[i]}", ha='center', va='bottom', fontsize=5)

        # Chú thích
        ax1.legend(loc='upper left', fontsize=5)
        ax2.legend(loc='upper right', fontsize=5)

        max_time = max(times)
        max_step = max(steps)

        if max_time < 0.1:
            ax1.set_ylim(0, max_time * 1.5 + 0.01)

        if max_step < 100:
            ax2.set_ylim(0, max_step * 1.5 + 1)
    
        fig.tight_layout()

        canvas = FigureCanvas(fig)

        # Xử lý layout cũ
        layout = widget.layout()
        if layout is None:
            layout = QtWidgets.QVBoxLayout()
            widget.setLayout(layout)
        else:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        layout.addWidget(canvas)
    
    def animate_solution(self, path):
        self.index = 0
        self.path = path
        self.search_prB.setValue(0)
        self.is_paused = False
        self.is_running = True
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_move)
        self.timer.start(300)
    
    def next_move(self):
        if self.is_paused or not self.is_running:
            return
        
        if self.index < len(self.path):
            self.update_puzzle(self.path[self.index])
            self.index += 1
            progress = int((self.index / len(self.path)) * 100)
            self.search_prB.setValue(progress)
        else:
            self.timer.stop()
            self.is_running = False
            self.search_prB.setValue(100)
            
    def toggle_animation(self):
        if not hasattr(self, 'path') or not self.path:
            return  # chưa có gì để chạy

        # Nếu đang chạy → Pause
        if self.timer.isActive():
            self.timer.stop()
            self.is_paused = True

        # Nếu đang tạm dừng → Resume
        elif self.is_paused:
            self.timer.start(300)
            self.is_paused = False
    
    def get_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return None
    
    def move(self, state, direction):
        x, y = self.get_blank(state)
        dx, dy = MOVES[direction]
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            return tuple(tuple(row) for row in new_state)
        return None
    
    
    def get_neighbors_action(self, state):
        neighbors = []
        for action in ['L', 'R', 'U', 'D']:
            new_state = self.move(state, action)
            if new_state:
                neighbors.append((action, new_state))
        return neighbors
    
    def get_neighbors(self, state):
        neighbors = []
        N = len(state)
        state = [list(row) for row in state]
        # Tìm vị trí ô trống
        for i in range(N):
            for j in range(N):
                if state[i][j] == 0:
                    x, y = i, j
                    break

        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(tuple(tuple(row) for row in new_state))
        return neighbors
    
    def reconstruct_path(self, parent, end_state):
        path = [end_state]
        while end_state in parent:
            end_state = parent[end_state]
            path.append(end_state)
        path.reverse()
        return path

########Search_Algorithms
###Uninformed Search  
    #Breath-first Search
    def bfs(self, start, goal):
        queue = Queue()
        queue.put([start])
        visited = set()
        
        while not queue.empty():
            path = queue.get()
            state = path[-1]
            
            if state == goal:
                return path
            
            if state not in visited:
                visited.add(state)
                for neighbor in self.get_neighbors(state):
                    queue.put(path + [neighbor])
        return []
    
    #Depth-first Search
    def dfs(self, start, goal, limit=50):
        stack = [ [start] ]
        visited = set()
        
        while stack:
            path = stack.pop()
            state = path[-1]
            
            if state == goal:
                return path
            
            if state not in visited and len(path) < limit:
                visited.add(state)
                for neighbor in self.get_neighbors(state):
                    stack.append(path + [neighbor])
        return []
    
    #Iterative Deepening
    def iddfs(self, start, goal, max_depth=100):
        def dls(state, depth, visited, path):
            if state == goal and depth == 0:
                return path
            if depth <= 0:
                return []

            visited.add(state)

            for neighbor in self.get_neighbors(state):
                if neighbor not in visited:
                    result = dls(neighbor, depth - 1, visited, path + [neighbor])
                    if result:
                        return result

            visited.remove(state)  # backtrack
            return []

        for depth in range(max_depth):
            visited = set()
            result = dls(start, depth, visited, [start])
            if result:
                return result
        return []

    #Uniform Cost Search
    def ucs(self, start, goal):
        queue = PriorityQueue()
        queue.put((0, [start]))
        visited = {}
        
        while not queue.empty():
            cost, path = queue.get()
            state = path[-1]
            
            if state == goal:
                return path
            
            if state not in visited or cost < visited[state]:
                visited[state] = cost
                for neighbor in self.get_neighbors(state):
                    queue.put((cost + 1, path + [neighbor]))
        return []

###Informed Search
    #Greedy Search
    def greedy(self, start, goal):
        from queue import PriorityQueue
        def is_goal(state):
            return state == goal or (isinstance(goal, list) and state in goal)

        goal_positions = get_goal_positions(goal)
        visited = set()
        pq = PriorityQueue()

        pq.put((heuristic(start, goal_positions), [start]))
        in_frontier = set()
        in_frontier.add(start)

        while not pq.empty():
            heuristic_val, path = pq.get()
            current_state = path[-1]
            in_frontier.discard(current_state)

            if current_state in visited:
                continue
            visited.add(current_state)

            if is_goal(current_state):
                return path

            for neighbor in self.get_neighbors(current_state):
                if neighbor not in visited and neighbor not in in_frontier:
                    new_path = path + [neighbor]
                    h = heuristic(neighbor, goal_positions)
                    pq.put((h, new_path))
                    in_frontier.add(neighbor)

        return []
    
    #A*
    def a_star(self, start, goal):
        goal_pos = get_goal_positions(goal)
        open_set = []
        heapq.heappush(open_set, (heuristic(start, goal_pos), 0, [start]))
        g_cost = {start: 0}

        while open_set:
            _, cost, path = heapq.heappop(open_set)
            current = path[-1]
            if current == goal:
                return path

            for neighbor in self.get_neighbors(current):
                new_g = g_cost[current] + 1
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    f = new_g + heuristic(neighbor, goal_pos)
                    heapq.heappush(open_set, (f, new_g, path + [neighbor]))

        return []

    #IDA*
    def ida_star(self, start, goal):
        goal_pos = get_goal_positions(goal)

        def dfs(path, g, bound):
            node = path[-1]
            f = g + heuristic(node, goal_pos)
            if f > bound:
                return None, f
            if node == goal:
                return path, f
            min_bound = float('inf')
            for neighbor in self.get_neighbors(node):
                if neighbor in path:
                    continue
                result, temp = dfs(path + [neighbor], g + 1, bound)
                if result:
                    return result, temp
                min_bound = min(min_bound, temp)
            return None, min_bound

        bound = heuristic(start, goal_pos)
        while True:
            result, bound = dfs([start], 0, bound)
            if result:
                return result
            if bound == float('inf'):
                return []

###Local Search
    #Simple Hill Climbing
    def shc(self, start, goal):
        path = [start]
        goal_pos = get_goal_positions(goal)

        while path[-1] != goal:
            current = path[-1]
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return path

            next_node = min(neighbors, key=lambda s: heuristic(s, goal_pos))
            if heuristic(next_node, goal_pos) >= heuristic(current, goal_pos):
                return path  # kẹt
            path.append(next_node)
        return path

    #Steepest_Ascent Hill Climbing
    def sahc(self, start, goal):
        path = [start]
        goal_pos = get_goal_positions(goal)

        while path[-1] != goal:
            current = path[-1]
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return path

            neighbors.sort(key=lambda s: heuristic(s, goal_pos))
            best = neighbors[0]
            if heuristic(best, goal_pos) >= heuristic(current, goal_pos):
                return path

            if random.random() < 0.9:
                path.append(best)
            else:
                path.append(random.choice(neighbors[1:]) if len(neighbors) > 1 else best)
        return path

    #Stochastic Hill Climbing
    def sthc(self, start, goal, max_restarts=30, max_steps=1000):
        import random, math

        goal_pos = get_goal_positions(goal)
        directions = ['L', 'R', 'U', 'D']

        for _ in range(max_restarts):
            current = start
            path = [current]
            visited = set()
            visited.add(current)

            T = 100
            alpha = 0.99
            steps = 0

            while T > 1e-3 and steps < max_steps:
                if current == goal:
                    return path

                neighbors = self.get_neighbors(current)
                neighbors = [n for n in neighbors if n not in visited]
                if not neighbors:
                    break

                weighted = []
                for n in neighbors:
                    h = heuristic(n, goal_pos)
                    weight = math.exp(-h / T)
                    weighted.append((n, weight))

                total = sum(w for _, w in weighted)
                if total == 0:
                    break

                probs = [w / total for _, w in weighted]
                next_node = random.choices([n for n, _ in weighted], weights=probs, k=1)[0]

                current = next_node
                path.append(current)
                visited.add(current)

                T *= alpha
                steps += 1

        return []
    
    #Simulated Annealing
    def sa(self, start, goal):
        import random, math

        goal_pos = get_goal_positions(goal)
        T = 500           
        alpha = 0.995    
        max_steps = 30000  

        current = start
        current_h = heuristic(current, goal_pos)
        path = [current]

        best = current
        best_h = current_h
        best_path = list(path)

        steps = 0
        while T > 1e-4 and steps < max_steps:
            if current == goal:
                return path

            neighbors = self.get_neighbors(current)
            if not neighbors:
                break

            # Ưu tiên chọn hàng xóm có heuristic tốt hơn trung bình
            neighbors.sort(key=lambda x: heuristic(x, goal_pos))
            candidate_pool = neighbors[:max(1, len(neighbors)//2)]
            next_node = random.choice(candidate_pool)

            next_h = heuristic(next_node, goal_pos)
            delta = current_h - next_h

            if delta > 0 or random.random() < math.exp(delta / T):
                current = next_node
                current_h = next_h
                path.append(current)

                if current_h < best_h:
                    best = current
                    best_h = current_h
                    best_path = list(path)

            T *= alpha
            steps += 1

        return best_path if best == goal else None
    
    #Beam Search
    def bs(self, start, goal, beam_width=2):
        goal_pos = get_goal_positions(goal)
        frontier = [[start]]

        while frontier:
            candidates = []
            for path in frontier:
                current = path[-1]
                if current == goal:
                    return path
                for neighbor in self.get_neighbors(current):
                    if neighbor not in path:
                        candidates.append(path + [neighbor])
            if not candidates:
                return None
            candidates.sort(key=lambda p: heuristic(p[-1], goal_pos))
            frontier = candidates[:beam_width]
        return []
    
    #Genetic Algorithm
    def ga(self, start, goal, population_size=50, generations=200):
        directions = ['L', 'R', 'U', 'D']
        goal_pos = get_goal_positions(goal)

        def move(state, direction):
            row, col = next((r, c) for r in range(3) for c in range(3) if state[r][c] == 0)
            new_state = [list(r) for r in state]
            if direction == 'L' and col > 0:
                new_state[row][col], new_state[row][col-1] = new_state[row][col-1], new_state[row][col]
            elif direction == 'R' and col < 2:
                new_state[row][col], new_state[row][col+1] = new_state[row][col+1], new_state[row][col]
            elif direction == 'U' and row > 0:
                new_state[row][col], new_state[row-1][col] = new_state[row-1][col], new_state[row][col]
            elif direction == 'D' and row < 2:
                new_state[row][col], new_state[row+1][col] = new_state[row+1][col], new_state[row][col]
            return tuple(tuple(r) for r in new_state)

        def apply_moves(state, moves):
            for m in moves:
                state = move(state, m)
            return state

        def random_individual(length=30):
            return [random.choice(directions) for _ in range(length)]

        def fitness(individual):
            final = apply_moves(start, individual)
            return -heuristic(final, goal_pos)

        def crossover(p1, p2):
            cut = random.randint(1, len(p1) - 1)
            return p1[:cut] + p2[cut:]

        def mutate(ind):
            i = random.randint(0, len(ind) - 1)
            ind[i] = random.choice(directions)
            return ind

        population = [random_individual() for _ in range(population_size)]

        for _ in range(generations):
            population.sort(key=fitness, reverse=True)
            best = population[0]
            final_state = apply_moves(start, best)
            if final_state == goal:
                # reconstruct path
                path = [start]
                current = start
                for mov in best:
                    next_state = move(current, mov)
                    if next_state != current:
                        path.append(next_state)
                        current = next_state
                    if current == goal:
                        break
                return path

            next_gen = population[:5]  # elitism
            while len(next_gen) < population_size:
                p1, p2 = random.sample(population[:20], 2)
                child = crossover(p1, p2)
                if random.random() < 0.3:
                    child = mutate(child)
                next_gen.append(child)

            population = next_gen

        return []

###Complex Environments
    #And-Or    
    def and_or(self, start, goal, max_depth=50):
        cache = {}

        def or_search(state, depth, path):
            if state == goal:
                return []
            if depth >= max_depth or state in path:
                return None
            if state in cache:
                return cache[state]

            for action in get_valid_actions(state):
                result_states = apply_action(state, action, self.move, self.uncertain_actions)
                if not result_states:
                    continue
                subplan = and_search(result_states, depth + 1, path + [state])
                if subplan is not None:
                    plan = [(action, subplan)]
                    cache[state] = plan
                    return plan

            cache[state] = None
            return None

        def and_search(states, depth, path):
            plan = []
            for s in states:
                subplan = or_search(s, depth, path)
                if subplan is None:
                    return None
                plan.append(subplan)
            return plan

        return or_search(start, 0, [])
    
    #Sensorless
    def generate_initial_belief(state_with_blank_known):
        """Sinh tất cả trạng thái có thể bằng cách giữ nguyên thứ tự ô số và hoán vị vị trí ô trống (0)."""
        tiles = [num for row in state_with_blank_known for num in row if num != 0]
        belief = set()

        for i in range(3):
            for j in range(3):
                new_state = []
                idx = 0
                for x in range(3):
                    row = []
                    for y in range(3):
                        if (x, y) == (i, j):
                            row.append(0)
                        else:
                            row.append(tiles[idx])
                            idx += 1
                    new_state.append(tuple(row))
                belief.add(tuple(new_state))
        return belief

    def sensorless(self, start, goal):
        belief = Puzzle.generate_initial_belief(start)
        self.belief_state = [belief.copy()]
        path = []

        def avg_heuristic(states):
            goal_pos = get_goal_positions(goal)
            return sum(heuristic(s, goal_pos) for s in states) / len(states)

        for _ in range(10):
            if len(belief) == 1 and goal in belief:
                return path

            possible_dirs = set()
            for s in belief:
                possible_dirs.update(get_valid_actions(s))

            best_action = None
            best_new_belief = None
            if best_new_belief == belief:
                continue
            best_score = float('inf')

            for action in possible_dirs:
                possible_new_states = set()
                for state in belief:
                    for actual_dir in self.uncertain_actions.get(action, []):
                        if actual_dir in get_valid_actions(state):
                            new_state = self.move(state, actual_dir)
                            if new_state:
                                possible_new_states.add(new_state)

                if not possible_new_states or possible_new_states == belief:
                    continue

                score = avg_heuristic(possible_new_states) + len(possible_new_states) * 0.5
                if score < best_score:
                    best_score = score
                    best_action = action
                    best_new_belief = possible_new_states

            if best_action is None:
                break

            path.append(best_action)
            belief = best_new_belief
            self.belief_state.append(belief.copy())

            if len(belief) == 1 and goal in belief:
                return path

        return None
                            
###CSPs
    #Backtracking
    def backtracking(self, start, goal, max_depth=50):
        path = []
        visited = set()

        def serialize(state):
            return tuple(cell for row in state for cell in row)

        def solve(state, depth):
            if depth > max_depth:
                return False
            if serialize(state) in visited:
                return False
            visited.add(serialize(state))
            path.append(state)

            if state == goal:
                return True

            for neighbor in self.get_neighbors(state):
                if solve(neighbor, depth + 1):
                    return True

            path.pop()  # backtrack
            return False

        solve(start, 0)
        return path
        
    #forward
    def forward_checking(self, start, goal):
        def is_valid(state):
            return state not in visited

        visited = set()
        parent = dict()
        queue = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            if current == goal:
                return self.reconstruct_path(parent, current)

            for neighbor in self.get_neighbors(current):
                if is_valid(neighbor):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None  # Không tìm thấy
        
    #min-conflicts
    def min_conflicts(self, start, goal, max_steps=10000, restarts=10):
        # if start is None:
        #     start = self.start_state
        # if goal is None:
        #     goal = self.goal_state
        goal_pos = get_goal_positions(goal)
        best_path = None
        best_cost = float("inf")

        for _ in range(restarts):
            current = start
            path = [current]
            visited = set([current])

            for step in range(max_steps):
                if current == goal:
                    return path

                neighbors = self.get_neighbors(current)
                neighbors = [n for n in neighbors if n not in visited]
                if not neighbors:
                    break

                next_state = min(neighbors, key=lambda s: heuristic(s, goal_pos))
                visited.add(next_state)
                path.append(next_state)
                current = next_state

                h = heuristic(current, goal_pos)
                if h < best_cost:
                    best_cost = h
                    best_path = list(path)

                if h == 0:
                    return path

        return best_path if best_path and best_cost == 0 else None
        
###Reinforcement Learning
    #q_learning
    def q_learning(self, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.2):
        def count_correct_positions(state):
            return sum(
                1 for i in range(3) for j in range(3)
                if state[i][j] == self.goal_state[i][j] and state[i][j] != 0
            )

        Q = defaultdict(lambda: defaultdict(float))
        best_path = []
        best_score = -float('inf')

        for ep in range(episodes):
            state = self.start_state
            visited = set()
            path = [state]
            prev_correct = count_correct_positions(state)
            total_reward = 0

            for _ in range(100):
                actions = self.get_neighbors_action(state)
                if not actions:
                    break

                # Exploration vs Exploitation
                if random.random() < epsilon:
                    action, next_state = random.choice(actions)
                else:
                    action, next_state = max(actions, key=lambda a: Q[state][a[0]])

                curr_correct = count_correct_positions(next_state)

                if next_state == self.goal_state:
                    reward = 100
                elif next_state in visited:
                    reward = -20
                elif curr_correct > prev_correct:
                    reward = 5
                elif curr_correct == prev_correct:
                    reward = -1
                else:
                    reward = -5

                total_reward += reward
                visited.add(next_state)

                next_actions = self.get_neighbors_action(next_state)
                max_q_next = max([Q[next_state][a[0]] for a in next_actions], default=0)

                Q[state][action] += alpha * (reward + gamma * max_q_next - Q[state][action])
                state = next_state
                path.append(state)
                prev_correct = curr_correct

                if state == self.goal_state:
                    break

            if total_reward > best_score and state == self.goal_state:
                best_score = total_reward
                best_path = list(path)

            # Giảm epsilon dần theo từng episode
            epsilon *= 0.995

        return best_path if best_path else None

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Puzzle(initial, goal)
    window.show()
    sys.exit(app.exec_())
