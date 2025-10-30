# Battery Reactive Behavior Tree

This document visualizes the battery reactive behavior tree structure.

## Behavior Tree Diagram

```mermaid
graph TD
    Root["→<br/>Sequence"]
    
    Selector["?<br/>Selector"]
    BatteryOK(["BatteryOK<br/>Condition"])
    GoCharge["GoCharge<br/>Action"]
    
    SeqTask["→<br/>Sequence"]
    MoveToObj["MoveToObj<br/>Action"]
    CloseGrip["CloseGrip<br/>Action"]
    MoveHome["MoveHome<br/>Action"]
    
    Root --> Selector
    Root --> SeqTask
    
    Selector --> BatteryOK
    Selector --> GoCharge
    
    SeqTask --> MoveToObj
    SeqTask --> CloseGrip
    SeqTask --> MoveHome
    
    style Root fill:#e1f5ff,stroke:#333,stroke-width:2px,color:#000
    style Selector fill:#fff4e6,stroke:#333,stroke-width:2px,color:#000
    style BatteryOK fill:#e8f5e9,stroke:#333,stroke-width:2px,color:#000
    style GoCharge fill:#f3e5f5,stroke:#333,stroke-width:2px,color:#000
    style SeqTask fill:#e1f5ff,stroke:#333,stroke-width:2px,color:#000
    style MoveToObj fill:#f3e5f5,stroke:#333,stroke-width:2px,color:#000
    style CloseGrip fill:#f3e5f5,stroke:#333,stroke-width:2px,color:#000
    style MoveHome fill:#f3e5f5,stroke:#333,stroke-width:2px,color:#000
```

## Node Description

### Control Nodes

- **Root Sequence (→)**: Main sequence node that executes children from left to right. Succeeds if all children succeed.
- **Selector (?)**: Fallback node that tries children until one succeeds. Used for battery management.
- **Task Sequence (→)**: Sequence node that executes the main task workflow.

### Condition Nodes

- **BatteryOK**: Checks if the battery level is sufficient to continue operations.

### Action Nodes

- **GoCharge**: Directs the robot to go to the charging station.
- **MoveToObj**: Moves the robot to the target object.
- **CloseGrip**: Closes the gripper to grasp the object.
- **MoveHome**: Returns the robot to the home position.

## Behavior Flow

1. The root sequence starts execution
2. First, the selector checks battery status:
   - If **BatteryOK** succeeds → continue to task sequence
   - If **BatteryOK** fails → execute **GoCharge** action
3. If battery is OK, the task sequence executes:
   - **MoveToObj**: Navigate to target object
   - **CloseGrip**: Grasp the object
   - **MoveHome**: Return to home position

This reactive behavior ensures the robot always maintains sufficient battery before attempting task execution.
