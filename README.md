# Web Automation Testing - DEMO

#### Selenium - Python

MDG 2026

---

# Environment Versions

- macOS Tahoe Version 26.3.1 (25D2128)
- Google Chrome Version 146.0.7680.72 
- ChromeDriver 146.0.7680.72
- Homebrew 5.0.16
- node v25.7.0
- Python 3.14.3

---

# Set up

1. Install python on machine
    - brew install python
    - python --version
    - python3 --verison
2. Navigate to root project directory
3. Set up virtual environment
    - python3 -m venv .venv
4. Activate virtual environment
    - source .venv/bin/activate
5. Install requirements
    - pip3 install -r requirements.txt

---

# Tests


## Build Acceptance Test Suite
- pytest tests/test_bat_web.py
- LANGUAGE=fr pytest tests/test_bat_web.py
- for i in {1..1}; do pytest tests/test_bat_web.py; LANGUAGE=fr pytest tests/test_bat_web.py; done

### Homeweb Sub Suite
- pytest tests/test_homeweb.py
- LANGUAGE=fr pytest tests/test_homeweb.py

### Customer Portal Sub Suite
- pytest tests/test_customer_porta;.py
- LANGUAGE=fr pytest tests/test_customer_porta;.py

### Sentio Beta - Client Sub Suite
- pytest tests/test_sentio_beta_client.py
- LANGUAGE=fr pytest tests/test_sentio_beta_client.py

### Sentio Beta - Provider Sub Suite
- pytest tests/test_sentio_beta_provider.py
- LANGUAGE=fr pytest tests/test_sentio_beta_provider.py