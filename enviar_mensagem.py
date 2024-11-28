import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

def get_text_message_input(recipient , text) -> str:
    
    """
    Returns a JSON-formatted string representing a WhatsApp Business API text message input.

    Args:
        recipient (str): The phone number of the recipient in the E.164 format.
        text (str): The text of the message.

    Returns:
        str: A JSON-formatted string representing the message input.
    """

    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    """
    Sends a message to a recipient using the WhatsApp Business API.

    Args:
        data (str): A JSON-formatted string representing the message input.

    Returns:
        requests.Response: The response from the API.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response
