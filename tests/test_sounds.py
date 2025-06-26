#!/usr/bin/env python3
"""
Test script to demonstrate the two different notification sounds.
Run this to hear the difference between threshold and movement alerts.
"""

import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from src.notifier.runner import notify

def test_notification_sounds():
    """Test both notification sounds with a 3-second delay between them."""
    
    print("Testing notification sounds...")
    print("You should hear two different sounds:")
    print("1. Threshold alert (more urgent sound)")
    print("2. Movement alert (standard sound)")
    print()
    
    # Test threshold alert (initial crossing)
    print("Playing threshold alert sound...")
    notify("Test Threshold Alert", "This is a threshold crossing notification", "threshold")
    
    # Wait 3 seconds
    time.sleep(3)
    
    # Test movement alert (subsequent price movement)
    print("Playing movement alert sound...")
    notify("Test Movement Alert", "This is a price movement notification", "movement")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_notification_sounds() 