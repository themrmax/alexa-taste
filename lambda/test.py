import unittest
from index import *

START_SESSION={
  "session": {
    "new": True,
     "sessionId": "session1234",
    "attributes": {},
    "user": {
       "userId": None 
    },
    "application": {
       "applicationId": "amzn1.echo-sdk-ams.app.[unique-value-here]"
    }
   },
  "version": "1.0",
  "request": {
    "type": "LaunchRequest",
    "requestId": "request5678"
  }
}

def test_launch_request():
    response = lambda_handler(START_SESSION, None)
    assert response['response']['outputSpeech']['text'].startswith(
        "Ask me to find you a recipe.")
 

def test_get_recipe_request():
    response = lambda_handler({"request":{"type":"IntentRequest", 
                                         "intent":
                                         {"name": "GetRecipeIntent"}}}, None)
    assert response['response']['outputSpeech']['text'].startswith(
        "Here is the recipe for")
