# Test Suite: Build Acceptance
from dotenv import load_dotenv
import os


# 1: Set up Credentials
# 1.1: Loads variables from .env
load_dotenv()
CREDENTIALS = {
    "personal": {
        "email": os.getenv("PERSONAL_EMAIL"),
        "password": os.getenv("PERSONAL_PASSWORD")
    },
    "demo": {
        "email": os.getenv("DEMO_EMAIL"),
        "password": os.getenv("DEMO_PASSWORD")
    },
}

def test_bat_web_001(homeweb):
    # 1: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    homeweb.set_landing(True)
    assert "homeweb" in homeweb.current_url.lower()
    assert homeweb.title

def test_bat_web_002(homeweb):
    assert homeweb.is_landing()
    resources = homeweb.landing["elements"]["resources"]
    paths = homeweb.landing["paths"]["resources"]

    # 1: Test - Resource 1
    homeweb.click_element("xpath", resources["emotional_intelligence"])
    assert paths["emotional_intelligence"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 2: Test - Resource 2
    homeweb.click_element("xpath", resources["anxiety"])
    assert paths["anxiety"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 3: Test - Resource 3
    homeweb.click_element("xpath", resources["letting_go"])
    assert paths["letting_go"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 4: Test - Resource 4
    homeweb.click_element("xpath", resources["toolkit"])
    assert paths["toolkit"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

def test_bat_web_003(homeweb, quantum):
    assert homeweb.is_landing()
    buttons = homeweb.landing["elements"]["buttons"];
    paths = homeweb.landing["paths"]["buttons"];
    inputs = quantum.login["elements"]["inputs"]

    # 1: Test - Sign In - Button
    homeweb.click_element("xpath", buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Email field
    quantum.input(inputs["email_address"], CREDENTIALS["personal"]["email"])
    quantum.submit()
    password_input = quantum.wait_for_password()
    assert password_input.is_displayed()

    # 3: Test - Password field
    quantum.input(inputs["password"], CREDENTIALS["personal"]["password"])
    quantum.submit()

    # 4: Test - Login
    assert homeweb.wait_for_dashboard()
    homeweb.set_authenticated(True)

def test_bat_web_004(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = "https://homeweb.ca/en/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content()

def test_bat_web_005(homeweb):
    assert homeweb.is_authenticated

    # 1: Navigate to sentio resource
    sentio_resource_target = "https://homeweb.ca/app/en/resources/62c5a1e929ed9c1608d0434b"
    homeweb.driver.get(sentio_resource_target)
    assert homeweb.wait_for_resource_content()

    # 2: Test - Sentio transfer kickout
    homeweb.click_element("class name", "btn-primary")
    assert homeweb.wait_for_sentio_transfer()
    homeweb.go_back()

def test_bat_web_006(homeweb):
    assert homeweb.is_authenticated()
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 1: Test - Menu dropdown
    header.click_element("class name", header_buttons["menu"])
    assert header.wait_for_dropdown()

    # 2: Test - Logout
    header.click_element("css selector", header_buttons["sign_out"])
    assert "https://homeweb.ca/" in homeweb.current_url.lower()
    assert homeweb.is_landing()
    homeweb.set_authenticated(False)

def test_bat_web_007(homeweb, quantum):
    assert homeweb.is_landing()
    header = homeweb.header
    header_buttons = header.elements["buttons"]
    paths = header.paths["buttons"]
    inputs = quantum.login["elements"]["inputs"]

    # 1: Test - Sign In - Header
    header.click_element("class name", header_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Email field
    quantum.input(inputs["email_address"], CREDENTIALS["demo"]["email"])
    quantum.submit()
    password_input = quantum.wait_for_password()
    assert password_input.is_displayed()

    # 3: Test - Password field
    quantum.input(inputs["password"], CREDENTIALS["demo"]["password"])
    quantum.submit()

    # 4: Test - Login
    assert homeweb.wait_for_dashboard()
    homeweb.set_authenticated(True)

def test_bat_web_008(homeweb):
    assert homeweb.is_authenticated()
    childcare_resource_target = "https://homeweb.ca/app/en/resources/579ba4db88db7af01fe6ddd4"
    eldercare_resource_target = "https://homeweb.ca/app/en/resources/579ba49a88db7af01fe6ddc8"
    hra_resource_target = "https://homeweb.ca/app/en/resources/579ba53088db7af01fe6dde6"

    # 1: Test - ChildCare - Lifestage transfer kickout
    homeweb.driver.get(childcare_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element("class name", "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()
    homeweb.go_back()

    # 2: Test - ElderCare - Lifestage transfer kickout
    homeweb.driver.get(eldercare_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element("class name", "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()
    homeweb.go_back()

    # 3: Test - HRA - LifeStyles transfer kickout
    homeweb.driver.get(hra_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element("class name", "btn-primary")
    assert homeweb.wait_for_lifestyle_transfer()
    homeweb.go_back()

# TODO: BAT-WEB-009
# TODO: BAT-WEB-010
# TODO: BAT-WEB-011