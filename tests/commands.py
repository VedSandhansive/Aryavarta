# auto_rigveda.py
# Automates sending "next and mind" commands to AI after each response

import pyautogui
import time
import keyboard
import threading
import sys

class RigvedaAutomator:
    def __init__(self):
        self.running = True
        self.waiting_for_response = False
        self.response_received = False
        
    def send_command(self):
        """Send 'next and mind' command"""
        print("\n🤖 Sending: 'next and mind'")
        pyautogui.write("next and mind")
        pyautogui.press("enter")
        self.waiting_for_response = True
        self.response_received = False
        
    def monitor_for_response_start(self):
        """Monitor for AI response start (checks screen for typing indicators)"""
        # This is a simplified version
        # In practice, you'd need to detect when AI starts/stops typing
        time.sleep(3)  # Wait for response to begin
        return True
        
    def monitor_for_response_end(self):
        """Monitor for AI response completion"""
        # Look for "now next and mind" or similar indicators that response is complete
        # For now, use a timer based on typical response length
        print("⏳ Waiting for response to complete...")
        
        # Estimate based on typical response length (adjust as needed)
        # 3-5 minutes for 5 suktas with examples
        wait_time = 240  # 4 minutes
        
        # Countdown
        for i in range(wait_time, 0, -10):
            if not self.running:
                return False
            print(f"   Waiting... {i} seconds remaining", end="\r")
            time.sleep(10)
        
        print("\n✅ Response likely complete")
        self.waiting_for_response = False
        self.response_received = True
        return True
    
    def run(self):
        """Main loop"""
        print("=" * 60)
        print("RIGVEDA AUTOMATOR - Sends 'next and mind' repeatedly")
        print("=" * 60)
        print("\n⚠️  Instructions:")
        print("   1. Place cursor in the chat input box")
        print("   2. Press Ctrl+C to stop")
        print("   3. Keep the chat window active")
        print("\nStarting in 5 seconds...\n")
        
        time.sleep(5)
        
        # Send first command
        self.send_command()
        
        while self.running:
            try:
                # Monitor for response completion
                if self.waiting_for_response:
                    if self.monitor_for_response_end():
                        # Send next command
                        time.sleep(5)  # Small delay before next command
                        if self.running:
                            self.send_command()
                else:
                    # If not waiting, start monitoring
                    self.waiting_for_response = True
                    self.monitor_for_response_end()
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping...")
                self.running = False
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                time.sleep(10)
        
        print("\n✅ Automation stopped")


class ScreenBasedAutomator:
    """More reliable version using screen detection"""
    
    def __init__(self):
        self.running = True
        self.consecutive_no_change = 0
        self.last_screen_hash = None
        
    def capture_screen_region(self):
        """Capture the chat area where AI types"""
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        
        # Define chat region (adjust based on your screen)
        # DeepSeek chat is typically center-right
        region = (screen_width // 3, 50, screen_width // 2, screen_height - 100)
        
        try:
            screenshot = pyautogui.screenshot(region=region)
            return hash(screenshot.tobytes())
        except:
            return None
    
    def wait_for_response_complete(self, timeout=300):
        """Wait until screen stops changing (AI finished typing)"""
        print("⏳ Monitoring for response completion...")
        stable_count = 0
        last_hash = None
        
        start_time = time.time()
        
        while time.time() - start_time < timeout and self.running:
            current_hash = self.capture_screen_region()
            
            if current_hash == last_hash:
                stable_count += 1
            else:
                stable_count = 0
                last_hash = current_hash
            
            # If stable for 10 checks (about 10-15 seconds), assume complete
            if stable_count >= 10:
                print("✅ Response complete (screen stable)")
                return True
            
            time.sleep(1.5)
        
        print("⚠️ Timeout waiting for response")
        return True
    
    def run(self):
        """Main loop"""
        print("=" * 60)
        print("RIGVEDA AUTOMATOR (Screen-Based)")
        print("=" * 60)
        print("\n⚠️  Instructions:")
        print("   1. Position chat window so AI response area is visible")
        print("   2. Press Ctrl+C to stop")
        print("\nStarting in 5 seconds...\n")
        
        time.sleep(5)
        
        # Send first command
        pyautogui.write("next and mind")
        pyautogui.press("enter")
        print("🤖 Sent: 'next and mind'")
        
        iteration = 1
        
        while self.running:
            try:
                # Wait for response to complete
                self.wait_for_response_complete()
                
                # Small delay to ensure everything is settled
                time.sleep(3)
                
                # Send next command
                iteration += 1
                print(f"\n🔄 Iteration {iteration}")
                pyautogui.write("next and mind")
                pyautogui.press("enter")
                print("🤖 Sent: 'next and mind'")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping...")
                self.running = False
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                time.sleep(10)
        
        print(f"\n✅ Completed {iteration} iterations")


class SimpleTimerAutomator:
    """Simplest version - uses fixed timer for each batch"""
    
    def __init__(self, minutes_per_batch=4):
        self.minutes_per_batch = minutes_per_batch
        self.running = True
        self.iteration = 0
        
    def run(self):
        """Main loop"""
        print("=" * 60)
        print("RIGVEDA AUTOMATOR (Timer-Based)")
        print("=" * 60)
        print(f"\n⏱️  Waiting {self.minutes_per_batch} minutes between commands")
        print("\n⚠️  Instructions:")
        print("   1. Place cursor in the chat input box")
        print("   2. Press Ctrl+C to stop")
        print("\nStarting in 5 seconds...\n")
        
        time.sleep(5)
        
        # Send first command
        pyautogui.write("next and mind")
        pyautogui.press("enter")
        self.iteration = 1
        print(f"\n🔄 Iteration {self.iteration}: Sent 'next and mind'")
        
        while self.running:
            try:
                # Wait for specified time
                for remaining in range(self.minutes_per_batch * 60, 0, -10):
                    if not self.running:
                        break
                    mins = remaining // 60
                    secs = remaining % 60
                    print(f"⏳ Waiting {mins:02d}:{secs:02d}...", end="\r")
                    time.sleep(10)
                
                if not self.running:
                    break
                
                # Send next command
                self.iteration += 1
                print(f"\n🔄 Iteration {self.iteration}: Sent 'next and mind'")
                pyautogui.write("next and mind")
                pyautogui.press("enter")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping...")
                self.running = False
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                time.sleep(10)
        
        print(f"\n✅ Completed {self.iteration} iterations")


if __name__ == "__main__":
    print("Choose automation mode:")
    print("1. Timer-based (simple, 4 minutes per batch)")
    print("2. Screen-based (more reliable, needs screen)")
    print("3. Quick (2 minutes per batch)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        automator = SimpleTimerAutomator(minutes_per_batch=4)
    elif choice == "2":
        print("\n⚠️ Screen-based requires pyautogui and screen visibility")
        automator = ScreenBasedAutomator()
    elif choice == "3":
        automator = SimpleTimerAutomator(minutes_per_batch=2)
    else:
        automator = SimpleTimerAutomator(minutes_per_batch=4)
    
    automator.run()