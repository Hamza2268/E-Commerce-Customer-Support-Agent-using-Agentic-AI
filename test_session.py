import requests
import time
import uuid

BASE_URL = "http://127.0.0.1:8000"

def print_divider(title):
    print(f"\n{'='*10} {title} {'='*10}")

def test_session_management():
    # 1. Simulating Customer A (Session 1)
    id = str(uuid.uuid4())
    print_divider("Turn 1: Customer A gives context")
    payload_a1 = {"message": "Hi, my name is Hamza and I am asking about ORD-10001.", "session_id": id}
    res_a1 = requests.post(f"{BASE_URL}/chat", json=payload_a1).json()
    print(f"Customer A: {payload_a1['message']}")
    print(f"Agent: {res_a1.get('reply')}")
    time.sleep(2)

    # 2. Testing Memory for Customer A
    print_divider("Turn 2: Testing Customer A Memory")
    payload_a2 = {"message": "What was my name, and which order was I asking about?", "session_id": id}
    res_a2 = requests.post(f"{BASE_URL}/chat", json=payload_a2).json()
    print(f"Customer A: {payload_a2['message']}")
    print(f"Agent (Should remember): {res_a2.get('reply')}")
    time.sleep(2)

    # 3. Simulating Customer B (Session 2)
    print_divider("Turn 3: Customer B joins (Testing Isolation)")
    payload_b1 = {"message": "Hi! Do you know what my name is?", "session_id": "session-guest"}
    res_b1 = requests.post(f"{BASE_URL}/chat", json=payload_b1).json()
    print(f"Customer B: {payload_b1['message']}")
    print(f"Agent (Should NOT know): {res_b1.get('reply')}")
    time.sleep(2)

    ####################################### 4. Fetching the Session History via API ##############################################
    print_divider("Turn 4: Retrieving Session History")
    history_res = requests.get(f"{BASE_URL}/history/{id}")
    if history_res.status_code == 200:
        history = history_res.json().get("history", [])
        print(f"Successfully retrieved {len(history)} messages for Session A.")
        for idx, msg in enumerate(history):
            print(f"Message {idx + 1} ({msg['role'].capitalize()}): {msg['content']} \n")
    else:
        print("Failed to retrieve history.")
    time.sleep(1)

    ############################################## 5. Clearing the Session ##############################################
    print_divider("Turn 5: Wiping the Session")
    reset_res = requests.delete(f"{BASE_URL}/reset/{id}")
    print(f"Reset Response: {reset_res.json()}")
    
    ############################################## 6. Verifying the wipe ##############################################
    print_divider("Turn 6: Verifying Wipe")
    history_check = requests.get(f"{BASE_URL}/history/{id}")
    print(f"History Check after wipe (Should be 404): {history_check.status_code}")

if __name__ == "__main__":
    test_session_management()