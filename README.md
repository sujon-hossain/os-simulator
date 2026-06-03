# Integrated OS Simulator

## Overview

Integrated OS Simulator is a desktop application developed in Python that demonstrates fundamental Operating System concepts through an interactive graphical user interface (GUI). The simulator allows users to experiment with process scheduling algorithms, semaphore operations, and deadlock avoidance techniques in a visual and educational environment.

## Features

### Process Scheduling

* First Come First Serve (FCFS)
* Round Robin Scheduling
* Process configuration with:

  * Process ID (PID)
  * Arrival Time
  * Burst Time
  * Priority
  * Time Quantum

### Synchronization

* Semaphore Demonstration
* Process synchronization visualization
* Critical section management concepts

### Deadlock Management

* Banker's Algorithm implementation
* Safe state checking
* Resource allocation simulation
* Deadlock avoidance demonstration

### User Interface

* Interactive GUI built with Python
* Easy process creation and management
* Real-time output display
* Clear and reset functionality

## Technologies Used

* Python
* Tkinter (GUI)
* Operating System Algorithms
* Data Structures

## Project Structure

```text
Integrated-OS-Simulator/
│
├── main.py
├── scheduler.py
├── semaphore.py
├── banker.py
├── utils.py
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd Integrated-OS-Simulator
```

3. Run the application:

```bash
python main.py
```

## How to Use

1. Enter Process Information:

   * PID
   * Arrival Time
   * Burst Time
   * Priority
   * Quantum (for Round Robin)

2. Click **Add Process** to add a process.

3. Select the desired algorithm:

   * FCFS
   * Round Robin
   * Semaphore Demo
   * Banker's Algorithm

4. View the results and simulation output in the display area.

5. Use **Clear** to reset all data.

## Educational Objectives

This project helps students understand:

* CPU Scheduling Algorithms
* Process Management
* Semaphores
* Critical Sections
* Deadlocks
* Banker's Algorithm
* Resource Allocation
* Operating System Fundamentals

## Future Improvements

* Priority Scheduling
* Shortest Job First (SJF)
* Shortest Remaining Time First (SRTF)
* Multilevel Queue Scheduling
* Gantt Chart Visualization
* Memory Management Simulation
* Page Replacement Algorithms

## Author

Md Sujon

## License

This project is developed for educational and academic purposes.
