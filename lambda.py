from __future__ import print_function
from urllib2 import urlopen
import re
import json

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        recipe = get_recipe("beef+pie")
        return build_response("Here is the recipe for {}. Ready for the ingredients?".format(recipe["name"]),
                              {"recipe": recipe, "stage": "ingredients", "step_number": 0})

    elif event['request']['type'] == "IntentRequest" and event['request']['intent']['name'] == 'AMAZON.YesIntent':
        return next_step(event['session']['attributes'])

def get_recipe(keyword):
    search_results = urlopen('http://www.taste.com.au/search-recipes/?q=beef+pie').read()
    recipe_links = re.findall('(sort-by)|(http://www.taste.com.au/recipes/\d+)',search_results)
    results_index = recipe_links.index((u'sort-by', u'')) + 1 #skip the featured recipes
    recipe_link = recipe_links[results_index][1]
    recipe_page = urlopen(recipe_link).read()
    recipe_json = re.search('({"@context":.*?)</script>', recipe_page).group(1)
    recipe = json.loads(recipe_json)
    #we want to make the recipe instructions one sentance each.
    recipe['recipeInstructions'] = [s for t in recipe['recipeInstructions'] for s in t.split('. ')]

    return recipe

def next_step(state):
    if state['stage'] == 'ingredients':
        if state["step_number"] < len(state["recipe"]["recipeIngredient"]) - 1:
            response_text = state["recipe"]["recipeIngredient"][state["step_number"]]
            state["step_number"] += 1
            return build_response(response_text, state)
        else:
            response_text = u"The last ingredient is {}. Ready to start the recipe?".format(state["recipe"]["recipeIngredient"][state["step_number"]])
            state["stage"] = "method"
            state["step_number"] = 0
            return build_response(response_text, state)

    if state['stage'] == 'method':
        if state["step_number"] < len(state["recipe"]["recipeInstructions"]) - 1:
            response_text = state["recipe"]["recipeInstructions"][state["step_number"]]
            state["step_number"] += 1
            return build_response(response_text, state)
        else:
            response_text = u"{}. That's the end of the recipe.".format(state["recipe"]["recipeInstructions"][state["step_number"]])
            return build_response(response_text, state)

def build_response(speech, session_attributes):
    return {
        'sessionAttributes': session_attributes,
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech
            },
            'shouldEndSession': False
        }
    }

