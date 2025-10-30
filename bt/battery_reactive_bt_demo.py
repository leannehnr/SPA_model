#!/usr/bin/env python3
"""
Battery Reactive Behavior Tree Demo

This module demonstrates a reactive behavior tree that manages battery levels
before executing tasks. It uses the py_trees library to implement the behavior
tree structure shown in battery_reactive_bt.png.
"""

import time
import py_trees
from py_trees.composites import Sequence, Selector
from py_trees.common import Status


class BatteryOK(py_trees.behaviour.Behaviour):
    """
    Condition node that checks if the battery level is sufficient.
    """
    
    def __init__(self, name="BatteryOK", battery_threshold=20.0):
        """
        Initialize the battery condition checker.
        
        Args:
            name: Name of the behavior
            battery_threshold: Minimum battery level required (percentage)
        """
        super(BatteryOK, self).__init__(name)
        self.battery_threshold = battery_threshold
        self.feedback_message = ""
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key(
            key="battery_level",
            access=py_trees.common.Access.READ
        )
    
    def setup(self, **kwargs):
        """Setup the behavior (called once before first tick)."""
        _ = kwargs  # Unused but required by interface
        self.logger.debug(f"  {self.name} [BatteryOK::setup()]")
    
    def update(self):
        """
        Check the battery level.
        
        Returns:
            Status.SUCCESS if battery is OK, Status.FAILURE otherwise
        """
        battery_level = self.blackboard.get("battery_level")
        self.logger.info(f"  {self.name} [Checking battery: {battery_level:.1f}%]")
        
        if battery_level >= self.battery_threshold:
            self.feedback_message = f"Battery OK: {battery_level:.1f}%"
            return Status.SUCCESS
        else:
            self.feedback_message = f"Battery low: {battery_level:.1f}%"
            return Status.FAILURE


class GoCharge(py_trees.behaviour.Behaviour):
    """
    Action node that simulates going to the charging station.
    """
    
    def __init__(self, name="GoCharge", charge_rate=10.0):
        """
        Initialize the charging action.
        
        Args:
            name: Name of the behavior
            charge_rate: Battery charge rate per tick (percentage)
        """
        super(GoCharge, self).__init__(name)
        self.charge_rate = charge_rate
        self.feedback_message = ""
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key(
            key="battery_level",
            access=py_trees.common.Access.WRITE
        )
    
    def setup(self, **kwargs):
        """Setup the behavior (called once before first tick)."""
        _ = kwargs  # Unused but required by interface
        self.logger.debug(f"  {self.name} [GoCharge::setup()]")
    
    def update(self):
        """
        Simulate charging the battery.
        
        Returns:
            Status.SUCCESS after charging
        """
        battery_level = self.blackboard.get("battery_level")
        self.logger.info(f"  {self.name} [Going to charging station...]")
        
        # Charge the battery
        new_level = min(100.0, battery_level + self.charge_rate)
        self.blackboard.set("battery_level", new_level)
        
        self.feedback_message = f"Charged battery to {new_level:.1f}%"
        self.logger.info(f"  {self.name} [Battery charged to {new_level:.1f}%]")
        
        return Status.SUCCESS


class MoveToObj(py_trees.behaviour.Behaviour):
    """
    Action node that simulates moving to the target object.
    """
    
    def __init__(self, name="MoveToObj", battery_cost=5.0):
        """
        Initialize the move to object action.
        
        Args:
            name: Name of the behavior
            battery_cost: Battery consumption for this action (percentage)
        """
        super(MoveToObj, self).__init__(name)
        self.battery_cost = battery_cost
        self.feedback_message = ""
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key(
            key="battery_level",
            access=py_trees.common.Access.WRITE
        )
    
    def setup(self, **kwargs):
        """Setup the behavior (called once before first tick)."""
        _ = kwargs  # Unused but required by interface
        self.logger.debug(f"  {self.name} [MoveToObj::setup()]")
    
    def update(self):
        """
        Simulate moving to the target object.
        
        Returns:
            Status.SUCCESS after moving
        """
        battery_level = self.blackboard.get("battery_level")
        self.logger.info(f"  {self.name} [Moving to target object...]")
        
        # Consume battery
        new_level = max(0.0, battery_level - self.battery_cost)
        self.blackboard.set("battery_level", new_level)
        
        self.feedback_message = f"Moved to object (battery: {new_level:.1f}%)"
        
        return Status.SUCCESS


class CloseGrip(py_trees.behaviour.Behaviour):
    """
    Action node that simulates closing the gripper.
    """
    
    def __init__(self, name="CloseGrip", battery_cost=2.0):
        """
        Initialize the close grip action.
        
        Args:
            name: Name of the behavior
            battery_cost: Battery consumption for this action (percentage)
        """
        super(CloseGrip, self).__init__(name)
        self.battery_cost = battery_cost
        self.feedback_message = ""
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key(
            key="battery_level",
            access=py_trees.common.Access.WRITE
        )
    
    def setup(self, **kwargs):
        """Setup the behavior (called once before first tick)."""
        _ = kwargs  # Unused but required by interface
        self.logger.debug(f"  {self.name} [CloseGrip::setup()]")
    
    def update(self):
        """
        Simulate closing the gripper.
        
        Returns:
            Status.SUCCESS after gripping
        """
        battery_level = self.blackboard.get("battery_level")
        self.logger.info(f"  {self.name} [Closing gripper...]")
        
        # Consume battery
        new_level = max(0.0, battery_level - self.battery_cost)
        self.blackboard.set("battery_level", new_level)
        
        self.feedback_message = f"Gripper closed (battery: {new_level:.1f}%)"
        
        return Status.SUCCESS


class MoveHome(py_trees.behaviour.Behaviour):
    """
    Action node that simulates moving back to home position.
    """
    
    def __init__(self, name="MoveHome", battery_cost=5.0):
        """
        Initialize the move home action.
        
        Args:
            name: Name of the behavior
            battery_cost: Battery consumption for this action (percentage)
        """
        super(MoveHome, self).__init__(name)
        self.battery_cost = battery_cost
        self.feedback_message = ""
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key(
            key="battery_level",
            access=py_trees.common.Access.WRITE
        )
    
    def setup(self, **kwargs):
        """Setup the behavior (called once before first tick)."""
        _ = kwargs  # Unused but required by interface
        self.logger.debug(f"  {self.name} [MoveHome::setup()]")
    
    def update(self):
        """
        Simulate moving back to home position.
        
        Returns:
            Status.SUCCESS after returning home
        """
        battery_level = self.blackboard.get("battery_level")
        self.logger.info(f"  {self.name} [Returning to home position...]")
        
        # Consume battery
        new_level = max(0.0, battery_level - self.battery_cost)
        self.blackboard.set("battery_level", new_level)
        
        self.feedback_message = f"Returned home (battery: {new_level:.1f}%)"
        
        return Status.SUCCESS


def create_battery_reactive_tree():
    """
    Create the battery reactive behavior tree structure.
    
    Returns:
        The root node of the behavior tree
    """
    # Root sequence
    root = Sequence(name="Root", memory=False)
    
    # Battery management selector
    battery_selector = Selector(name="Battery Manager", memory=False)
    battery_ok = BatteryOK(name="BatteryOK", battery_threshold=20.0)
    go_charge = GoCharge(name="GoCharge", charge_rate=30.0)
    
    battery_selector.add_children([battery_ok, go_charge])
    
    # Task sequence
    task_sequence = Sequence(name="Task Sequence", memory=False)
    move_to_obj = MoveToObj(name="MoveToObj", battery_cost=5.0)
    close_grip = CloseGrip(name="CloseGrip", battery_cost=2.0)
    move_home = MoveHome(name="MoveHome", battery_cost=5.0)
    
    task_sequence.add_children([move_to_obj, close_grip, move_home])
    
    # Build the tree
    root.add_children([battery_selector, task_sequence])
    
    return root


def main():
    """
    Main function to demonstrate the battery reactive behavior tree.
    """
    print("=" * 60)
    print("Battery Reactive Behavior Tree Demo")
    print("=" * 60)
    print()
    
    # Create the behavior tree
    root = create_battery_reactive_tree()
    
    # Initialize blackboard with battery level
    blackboard = py_trees.blackboard.Client(name="Demo")
    blackboard.register_key(
        key="battery_level",
        access=py_trees.common.Access.WRITE
    )
    
    # Start with low battery to demonstrate charging
    initial_battery = 15.0
    blackboard.set("battery_level", initial_battery)
    print(f"Initial battery level: {initial_battery:.1f}%")
    print()
    
    # Setup the tree
    root.setup_with_descendants()
    
    # Display the tree structure
    print("Behavior Tree Structure:")
    print(py_trees.display.unicode_tree(root, show_status=True))
    print()
    
    # Run multiple ticks to demonstrate the behavior
    num_ticks = 5
    print(f"Running {num_ticks} behavior tree ticks...")
    print("-" * 60)
    
    for i in range(num_ticks):
        print(f"\n{'=' * 60}")
        print(f"Tick {i + 1}/{num_ticks}")
        print(f"{'=' * 60}")
        
        current_battery = blackboard.get("battery_level")
        print(f"Current battery: {current_battery:.1f}%")
        print()
        
        # Tick the tree
        root.tick_once()
        
        # Display the tree state
        print("\nTree State:")
        print(py_trees.display.unicode_tree(root, show_status=True))
        
        # Show final battery level
        final_battery = blackboard.get("battery_level")
        print(f"\nBattery after tick: {final_battery:.1f}%")
        
        time.sleep(0.5)  # Small delay for readability
    
    print(f"\n{'=' * 60}")
    print("Demo completed!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

