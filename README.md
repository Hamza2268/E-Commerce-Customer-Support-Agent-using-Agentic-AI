## Quick Start Guide

1 - Start Virtual Environmnet
python -m venv venv
.\venv\Scripts\activate

2 - install Dependencies

```
  pip install -r requirements.txt
```

3 - Test the Application
(Create .env file and add Groq key "GROQ_API_KEY = the your key")

3.1 - Start the Server, In your first terminal window, run:

```
  python main.py
```

3.2.1 - Open a second terminal window, activate your virtual environment, and run the testing suites

```
  .\venv\Scripts\activate
  python test_agent.py
```

3.2.2 - 2. Test Session Management & Memory Isolation, This script simulates two different customers talking to the agent simultaneously, proving that memory is isolated and sessions can be successfully wiped.

```
   python test_sessions.py
```

3.2.3 - Interactive conversation, If you want to chat with the agent yourself directly from the terminal, run:

```
   python chat_test.py
```
