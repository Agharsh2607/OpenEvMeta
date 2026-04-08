import requests
import time

BASE_URL = "http://localhost:8000"

def main():
    print("Resetting environment...")
    res = requests.post(f"{BASE_URL}/reset")
    print(f"Initial: {res.json()}")
    
    for _ in range(5):
        action = {"action_type": "resolve"}
        res = requests.post(f"{BASE_URL}/step", json=action)
        print(f"Step: {res.json()}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
