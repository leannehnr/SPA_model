# Behavior Tree Demo

This directory contains a demonstration of a reactive behavior tree that manages battery levels before executing tasks.

## Files

- `battery_reactive_bt.png` - Visual representation of the behavior tree structure
- `battery_reactive_bt.md` - Mermaid diagram documentation of the behavior tree
- `battery_reactive_bt_demo.py` - Python implementation using py_trees library

## Installation

Install the required dependencies using uv:

```bash
cd /Users/giodegas/ISRLAB/SPA_model
uv sync
```

Or using pip:

```bash
uv pip install -r requirements.txt
```

## Running the Demo

Execute the demonstration using uv:

```bash
cd /Users/giodegas/ISRLAB/SPA_model
uv run bt/battery_reactive_bt_demo.py
```

Or directly with Python:

```bash
python bt/battery_reactive_bt_demo.py
```

## What the Demo Does

The demo simulates a robot that must:

1. Check its battery level before executing tasks
2. Go to charge if battery is low (below 20%)
3. Execute a task sequence if battery is sufficient:
   - Move to target object
   - Close gripper to grasp object
   - Return to home position

The behavior tree runs for 5 ticks, demonstrating how the reactive behavior automatically manages the battery:

- **Tick 1**: Battery starts at 15% (low) → Robot goes to charge
- **Tick 2**: Battery now at 45% → Robot executes full task sequence
- **Subsequent ticks**: Continue task execution while battery permits

## Behavior Tree Structure

```text
Root (Sequence)
├── Battery Manager (Selector)
│   ├── BatteryOK (Condition)
│   └── GoCharge (Action)
└── Task Sequence (Sequence)
    ├── MoveToObj (Action)
    ├── CloseGrip (Action)
    └── MoveHome (Action)
```

## Customization

You can modify the behavior by adjusting parameters in `battery_reactive_bt_demo.py`:

- `battery_threshold`: Minimum battery level to proceed with tasks (default: 20%)
- `charge_rate`: How much battery is restored per charge action (default: 30%)
- `battery_cost`: How much each action consumes (MoveToObj: 5%, CloseGrip: 2%, MoveHome: 5%)
- `initial_battery`: Starting battery level for the demo (default: 15%)

## Understanding the Output

The demo displays:

1. Initial battery level
2. Tree structure with node status indicators
3. For each tick:
   - Current battery level
   - Actions being executed
   - Updated tree state
   - Final battery level after tick

Status indicators:

- `✓` - Success
- `✗` - Failure
- `*` - Running
- `-` - Invalid/Not executed
