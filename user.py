"""
Login/setup util for Navalii
"""
import sys
import os
import json
from time import sleep
import requests


def cls():
    """
    Clears the screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class NavaRequests:
    """
    Not to be mistaken with NavaRequestInterceptor.

    This class has a few useful methods for making API requests.
    """

    def __init__(self, authkey: str) -> None:
        self.API_BASE_LOCATION = "https://navalii_api-1-d8739263.deta.app/" # Url is bugged. This will not work.
        self.API_AUTH_KEY = authkey

    def makeAPIRequest(self, path: str, payload: dict | None = None) -> requests.Response:
        json = {
            "APIAUTH_KEY": self.API_AUTH_KEY
        }
        # Add the user payload if there is any.
        if payload:
            json.update(payload)

        try:
            r = requests.post(self.API_BASE_LOCATION + path, json=json)
        except requests.exceptions.ConnectionError as err:
            print("Unable to connect to the Navalii API. Make sure you're connected to the internet!")

        if r.status_code == 401 and r.json()["detail"] == "Access Denied: Invalid auth code!":
            raise self.APIAuthorizationError(f"Unable to authorize your client!")
        elif r.status_code == 500:
            raise self.APIServerError("The Navalii API encountered an expected error!")
        else:
            return r

    class APIAuthorizationError(BaseException):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    class APIServerError(BaseException):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)


def initNavalii():
    """
    Setup function for Navlii.
    :return:
    """
    req = NavaRequests("TMPKEY")

    if not os.path.isfile("./nava.json"):
        print("Unable to load Navalii config. Entering setup mode.")
        sleep(3)

        cls()

        print("Welcome!")
        print("This setup utility will get you ready for browsing on Navlii!")
        print()
        print("In order to use Navalii to its full power, you'll need to make an account. This is how we'll sync your "
              "data across devices.")

        sleep(5)

        print("\nOne moment...")

        r = req.makeAPIRequest("api")
        if r.status_code == 200:
            print("Connected to the Navalii API!")

        sleep(2)

        while True:
            print()
            userHasAccount = input("Do you have an account already? (y/N): ").lower()

            if userHasAccount not in ["y", "n"]:
                continue

            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if username == "" or password == "":
                cls()
                continue

            if userHasAccount == "n":
                # Create an account.

                print("\nSetting up your account...")
                r = req.makeAPIRequest("api/users/create", payload={
                    "username": username,
                    "password": password
                })

                status_code = r.status_code

                if status_code == 409:
                    print("\nAn account with that name already exists!")
                    sleep(3)
                    cls()
                    continue
                elif status_code == 200:
                    print("\nSuccess!")
                else:
                    print("\nWhoops! Something happened... Try again!")
                    sleep(3)
                    cls()
                    continue

            print("\nLogging in...")

            r = req.makeAPIRequest("api/users/auth", payload={
                "username": username,
                "password": password
            })

            if r.status_code == 200:
                print("Success!\n")
                sleep(4)
                break
            elif r.status_code == 404:
                print("We couldn't find an account with that name... Try again!")
                sleep(4)
                cls()

                continue
            elif r.status_code == 401:
                print("The password is incorrect! Try again...")
                sleep(4)
                cls()

                continue
            else:
                raise ConnectionError("what just happened.")

        # No idea why user has to be here. PyCharm is incredibly dumb and refuses to accept it anywhere else.
        user = r.json()

        cls()
        print("Give us a moment while we create some files...")
        sleep(1)

        with open("./nava.json", "w") as f:
            json.dump(
                {"user":
                    {
                        "tak_code": user["tak"]["code"],
                        "bookmarks": user["data"]["bookmarks"],
                        "name": user["key"]  # Different from username. Not used for auth.
                    }
                },
                f)

        with open("./config.json", "w") as f:
            json.dump({
                "browser": {
                    "home": None,
                    "s-engine": "google",
                    "default_search-non-valid": True,
                    "default_block-ad-urls": False
                }
            }, f)

        cls()
        print("\n\nDone!")
        print()
        print(f"Welcome, {user['key']}, to your Navalii.")
        sleep(4)
        cls()

    if not os.path.isfile("./config.json"):
        raise FileNotFoundError("nava config was found, but user config was not. Code: c:001")

    with open("./nava.json", "r") as f:
        navadat = json.load(f)
    with open("./config.json", "r") as f:
        configdat = json.load(f)

    initdata = {"nava": navadat, "config": configdat}

    # Normal log in.

    if initdata["nava"]["user"]["tak_code"]:
        print("Logging in...")

        r = req.makeAPIRequest("api/users/auth", payload={
            "tak": initdata["nava"]["user"]["tak_code"]
        })

        if r.status_code == 401:
            print("Session expired. Please log in to your account again.")
            sleep(4)

            cls()
            while True:
                username = input("Enter your username: ")
                password = input("Enter your password: ")

                if username == "" or password == "":
                    cls()
                    continue

                r = req.makeAPIRequest("api/users/auth", payload={
                    "username": username,
                    "password": password
                })

                if r.status_code == 200:
                    print("Success!\n")
                    sleep(4)
                    break
                elif r.status_code == 404:
                    print("We couldn't find an account with that name... Try again!")
                    sleep(4)
                    cls()

                    continue
                elif r.status_code == 401:
                    print("The password is incorrect! Try again...")
                    sleep(4)
                    cls()

                    continue
                else:
                    raise ConnectionError("what just happened.")

            user = r.json()
            with open("./nava.json", "r") as f:
                navadat = json.load(f)

            navadat["user"]["tak_code"] = user["tak"]["code"]

            with open("./nava.json", "w") as f:
                json.dump(navadat, f)

        return initdata
