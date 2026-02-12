class LoginPage:
    EN = {
        "base_url": "https://api.homewoodhealth.io/en/login",
        "elements": {
            "inputs": {
                "email_address": "//input[@id='emailAddress']",
                "password": "//input[@id='password']",
            },
            "buttons": {
                "next": "//button[@type='submit']",
            }
        },
        "paths": {
            "buttons": {
                "sign_in": "/en/login"
            }
        }
    }

    FR = {
        "base_url": "https://api.homewoodhealth.io/fr/login",
        "elements": {
            "inputs": {
                "email_address": "//input[@id='emailAddress']",
                "password": "",
            },
            "buttons": {
                "next": "//button[@type='submit']",
                "sign_in": ""
            }
        },
        "paths": {
            "buttons": {
                "sign_in": "/fr/login"
            }
        }
    }
