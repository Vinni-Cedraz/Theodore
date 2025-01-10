import sys
import requests
import json

# Define the base URL for the Flask app
BASE_URL = "http://127.0.0.1:5000/generate-card"

# Define the test cases
test_cases = {
    "1": {
        "name": "Alice",
        "relationship": "friend",
        "memory": "the time we went hiking in the mountains and watched the sunrise together"
    },
    "2": {
        "name": "Bob",
        "relationship": "brother",
        "memory": "the day we built a treehouse in our backyard and spent the night camping in it"
    },
    "3": {
        "name": "Catherine",
        "relationship": "mother",
        "memory": "the countless evenings we spent baking cookies and sharing stories in the kitchen"
    },
    "4": {
        "name": "David",
        "relationship": "girlfriend",
        "memory": "our romantic getaway to the beach where we collected seashells and watched the sunset"
    },
    "5": {
        "name": "Emma",
        "relationship": "colleague",
        "memory": "the successful project we completed together and celebrated with a team dinner"
    }
}

def main(test_case_number):
    if test_case_number not in test_cases:
        print("Invalid test case number. Please provide a number between 1 and 5.")
        return

    data = test_cases[test_case_number]
    response = requests.post(BASE_URL, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    if response.status_code == 200:
        print("Test case executed successfully.")
        print("Response:", response.json())
    else:
        print("Failed to execute test case.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_cases.py <test_case_number>")
    else:
        main(sys.argv[1])