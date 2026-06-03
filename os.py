import tkinter as tk
from tkinter import messagebox

# ================= PROCESS =================
class Process:
    def __init__(self, pid, at, bt, priority):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.priority = priority
        self.remaining = bt
        self.wt = 0
        self.tat = 0

# ================= SCHEDULER =================
class Scheduler:
    @staticmethod
    def fcfs(processes):
        procs = sorted([p for p in processes], key=lambda x: x.at)
        if not procs: return [], [0]
        
        timeline = [procs[0].at]
        time = timeline[0]
        gantt = []

        for p in procs:
            if time < p.at:
                gantt.append("IDLE")
                time = p.at
                timeline.append(time)
            p.wt = time - p.at
            time += p.bt
            p.tat = time - p.at
            gantt.append(f"P{p.pid}")
            timeline.append(time)
        return gantt, timeline

    @staticmethod
    def rr(processes, q):
        procs = sorted([p for p in processes], key=lambda x: x.at)
        if not procs: return [], [0]
        
        time = procs[0].at
        queue, gantt, timeline = [], [], [time]
        i, n = 0, len(procs)

        while i < n or queue:
            while i < n and procs[i].at <= time:
                queue.append(procs[i])
                i += 1
            if not queue:
                if i < n:
                    gantt.append("IDLE")
                    time = procs[i].at
                    timeline.append(time)
                    continue
                else: break
            p = queue.pop(0)
            run = min(q, p.remaining)
            gantt.append(f"P{p.pid}")
            time += run
            p.remaining -= run
            timeline.append(time)
            while i < n and procs[i].at <= time:
                queue.append(procs[i])
                i += 1
            if p.remaining > 0: queue.append(p)
            else:
                p.tat = time - p.at
                p.wt = p.tat - p.bt
        return gantt, timeline

# ================= SEMAPHORE =================
class Semaphore:
    def __init__(self, value=1):
        self.value = value

    def wait(self):
        if self.value > 0:
            self.value -= 1
            return True
        return False

    def signal(self):
        self.value += 1

# ================= GUI =================
class OSSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated OS Simulator - All Features Restored")
        self.root.geometry("1100x850")
        self.processes = []

        # --- INPUT SECTION ---
        input_frame = tk.LabelFrame(root, text=" Process Configuration (Enter to Move/Add) ", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        self.labels = ["PID", "Arrival", "Burst", "Priority", "Quantum"]
        self.entries = []
        for idx, text in enumerate(self.labels):
            tk.Label(input_frame, text=f"{text}:").grid(row=0, column=idx*2, padx=5)
            ent = tk.Entry(input_frame, width=10)
            ent.grid(row=0, column=idx*2+1, padx=5)
            ent.bind('<Return>', lambda e, i=idx: self.handle_enter(i))
            self.entries.append(ent)

        self.pid_ent, self.at_ent, self.bt_ent, self.pr_ent, self.q_ent = self.entries
        self.q_ent.insert(0, "2")
        self.pid_ent.focus_set()

        # --- BUTTONS ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Add Process", command=self.add, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="FCFS", command=self.run_fcfs).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Round Robin", command=self.run_rr).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Semaphore Demo", command=self.sync_demo).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Banker's Algorithm", command=self.banker).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_all, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

        # --- OUTPUT ---
        self.output = tk.Text(root, height=18, width=130, font=("Courier", 10))
        self.output.pack(pady=10, padx=10)

        # --- GANTT CANVAS ---
        self.canvas = tk.Canvas(root, height=120, width=1050, bg="white", highlightthickness=1)
        self.canvas.pack(pady=10)

    def handle_enter(self, index):
        if index < 3:
            self.entries[index+1].focus_set()
        elif index == 3:
            self.add()

    def add(self):
        try:
            p_id, at, bt, pr = int(self.pid_ent.get()), int(self.at_ent.get()), int(self.bt_ent.get()), int(self.pr_ent.get())
            if any(p.pid == p_id for p in self.processes):
                messagebox.showerror("Error", "PID exists!")
                return
            self.processes.append(Process(p_id, at, bt, pr))
            self.output.insert(tk.END, f"P{p_id} added.\n")
            for i in range(4): self.entries[i].delete(0, tk.END)
            self.pid_ent.focus_set()
        except ValueError:
            messagebox.showwarning("Warning", "Fill PID, AT, BT, and Priority!")

    def reset_procs(self):
        for p in self.processes:
            p.remaining = p.bt
            p.wt = p.tat = 0

    def run_fcfs(self):
        if not self.processes: return
        self.reset_procs()
        g, t = Scheduler.fcfs(self.processes)
        self.display_results("FCFS", g, t)

    def run_rr(self):
        if not self.processes: return
        try:
            q = int(self.q_ent.get())
            self.reset_procs()
            g, t = Scheduler.rr(self.processes, q)
            self.display_results("Round Robin", g, t)
        except ValueError: pass

    def display_results(self, name, g, t):
        self.output.delete(1.0, tk.END)
        header = f"{'PID':<8}{'AT':<8}{'BT':<8}{'PRIO':<8}{'WT':<8}{'TAT':<8}\n"
        self.output.insert(tk.END, f"--- {name} Results ---\n{header}{'-'*55}\n")
        tw, tt = 0, 0
        for p in sorted(self.processes, key=lambda x: x.pid):
            self.output.insert(tk.END, f"{p.pid:<8}{p.at:<8}{p.bt:<8}{p.priority:<8}{p.wt:<8}{p.tat:<8}\n")
            tw, tt = tw + p.wt, tt + p.tat
        n = len(self.processes)
        self.output.insert(tk.END, f"{'-'*55}\nAvg WT: {tw/n:.2f} | Avg TAT: {tt/n:.2f}\n")
        self.draw_gantt(g, t)

    def draw_gantt(self, g, t):
        self.canvas.delete("all")
        x, scale = 30, min(900 / max(t[-1]-t[0], 1), 40)
        for i in range(len(g)):
            w = (t[i+1] - t[i]) * scale
            color = "#f0f0f0" if g[i] == "IDLE" else "#e1f5fe"
            self.canvas.create_rectangle(x, 20, x+w, 70, fill=color)
            self.canvas.create_text(x + w/2, 45, text=g[i], font=("Arial", 8))
            self.canvas.create_text(x, 85, text=str(t[i]), font=("Arial", 7))
            x += w
        self.canvas.create_text(x, 85, text=str(t[-1]), font=("Arial", 7))

    def sync_demo(self):
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "--- Semaphore Demo ---\n")
        sem = Semaphore(1)
        for i in range(5):
            if sem.wait():
                self.output.insert(tk.END, f"Process {i}: Entered Critical Section\n")
                sem.signal()
                self.output.insert(tk.END, f"Process {i}: Released Semaphore\n")
            else:
                self.output.insert(tk.END, f"Process {i}: Blocked (Waiting)\n")

    def banker(self):
        self.output.delete(1.0, tk.END)
        alloc = [[0,1,0],[2,0,0],[3,0,2]]
        maxm = [[7,5,3],[3,2,2],[9,0,2]]
        avail = [3,3,2]
        n, m = len(alloc), len(avail)
        need = [[maxm[i][j]-alloc[i][j] for j in range(m)] for i in range(n)]
        finish = [False]*n
        safe = []
        while len(safe) < n:
            found = False
            for i in range(n):
                if not finish[i] and all(need[i][j] <= avail[j] for j in range(m)):
                    for j in range(m): avail[j] += alloc[i][j]
                    safe.append(i); finish[i] = True; found = True
            if not found: break
        if len(safe) == n:
            self.output.insert(tk.END, "SAFE STATE FOUND\nSequence: " + " -> ".join(f"P{i}" for i in safe))
        else:
            self.output.insert(tk.END, "UNSAFE STATE: Potential Deadlock\n")

    def clear_all(self):
        self.processes = []
        self.output.delete(1.0, tk.END)
        self.canvas.delete("all")
        self.pid_ent.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = OSSimulator(root)
    root.mainloop()