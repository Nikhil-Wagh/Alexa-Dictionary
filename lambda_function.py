import requests
import json
import random
import re

app_id = '25b51a25'
app_key = '22990bfcc0e232e45d7a891b399d3ee4'
baseURL = 'https://od-api.oxforddictionaries.com:443/api/v1/'
choice = -1

# python-lambda-local -f lambda_handler -t 10 lambda_function.py ./events/event.json

# TODO:// add if len(results) <= 0 condition in every intent

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return response(getWelcomeMessage(), False)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])


def on_intent(request):
    intent = request['intent']
    intent_name = intent['name']

    if 'dialogState' in request:
        if request['dialogState'] == "STARTED" or request['dialogState'] == "IN_PROGRESS":
            return dialog_response(request['dialogState'], False)

    if intent_name == "GetDefinitionIntent":
        return GetDefinitionIntent(intent)
    elif intent_name == "GetSynonymsIntent":
        return GetSynonymsIntent(intent)
    elif intent_name == "GetAntonymsIntent":
        return GetAntonymsIntent(intent)
    elif intent_name == "GetExamplesIntent":
        return GetExamplesIntent(intent)
    elif intent_name == "GetDomainsIntent":
        return GetDomainsIntent(intent)
    elif intent_name == "GetEtomologiesIntent":
        return GetEtomologiesIntent(intent)
    elif intent_name == "GetSpellingIntent":
        return SpellingIntent(intent)
    elif intent_name == "TranslationIntent":
        return GetTranslationsIntent(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return do_help()
    elif intent_name == "AMAZON.StopIntent":
        return do_stop()
    elif intent_name == "AMAZON.CancelIntent":
        return do_stop()
    else:
        print ("Invalid Intent reply with help")
        do_help()

def GetDefinitionIntent(intent):
    word = getWord(intent)
    language = getLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)
    
    defs = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    if m.has_key('definitions') : 
                        for n in m['definitions']:
                            defs.append(n)

    if len(defs) > 0 : 
        starters = [
            "The definition" + ("s" if n > 1 else "") + " of the word " + word + (" are" if n > 1 else " is") + " as follows, ",
            "Here's what I found, ",
            "The word " + word + " means, ",
            "According to oxford Dictionary, the meaning of the word " + word +" is ",
            "The word " + word + " defines as follows, ",
            word + " is defined as, ", 
            "The denotion of the word " + word + " is, ",
            "the exposition of the word " + word + " means, ",
        ]
        starter = getRandom (starters)
        rest = getFromArray(defs)
        outputSpeech = starter + rest
        return response(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find any definitions for " + word, True)


def GetSynonymsIntent(intent):
    word, language = getWordnLanguage(intent)
    print (word, language)
    url = baseURL + 'entries/' + language + '/' + word + '/synonyms'
    print(word, language, url)

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)
    
    syms = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    if m.has_key('synonyms') : 
                        for n in m['synonyms']:
                            if n.has_key('text') and n['text'] not in syms: 
                                syms.append(n['text'])

    if len(syms) > 0 :
        starters = [
            "Here's what I've found, "
        ]
        starter = getRandom (starters)
        rest = getFromArray(syms)
        # print(starter, rest)
        outputSpeech = starter + rest
        return response(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find any synonyms for " + word, True)


def GetAntonymsIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word + '/antonyms'
    print(word, language, url)

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)

    antyms = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    if m.has_key('antonyms') : 
                        for n in m['antonyms']:
                            if n.has_key('text') and n['text'] not in antyms: 
                                antyms.append(n['text'])

    if len(antyms) > 0 :
        starters = [
            "Here's what I've found, "
        ]
        starter = getRandom (starters)
        rest = getFromArray(antyms)
        # print(starter, rest)
        outputSpeech = starter + rest
        return response(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find any antonyms for " + word, True)
    

def GetExamplesIntent(intent):
    word, language = getWordnLanguage(intent)
    if language != 'en' and language != 'es':
        return response("Sorry only english and spanish are supported for examples", True)
    
    url = baseURL + 'entries/' + language + '/' + word + '/sentences'

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)

    examples = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            if i.has_key('sentences') : 
                for sent in i['sentences']:
                    if sent.has_key('text'):    
                        examples.append(sent['text'])

    if len(examples) > 0 :
        starters = [
            "Here's what I've found, "
        ]
        starter = getRandom (starters)
        rest = ""
        i = 0
        random.shuffle(examples)
        print("\n")
        for e in examples :
            print(e)
            e = e[ : e.find(",")]
            index = e.find(word) 
            if index == -1 : 
                continue
            _next = e.find(" ", index + 1)
            if index != -1: 
                rest += e[:index] + '<emphasis level="moderate">' + e[index : (_next if _next != -1 else len(e))] + '</emphasis>' + e[(_next if _next != -1 else len(e)) : ] + ". "
            if i > 1:
                break
            i += 1
        # print(starter, rest)
        outputSpeech = starter + rest
        return response_SSML(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find any examples for " + word, True)

def GetDomainsIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)

    domains = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    if m.has_key('domains'):
                        for d in m['domains']:
                            if d not in domains : 
                                domains.append(d)

    if len(domains) > 0 :
        starters = [
            "Here's what I've found, "
        ]
        starter = getRandom (starters)
        rest = getFromArray(domains)
        # print(starter, rest)
        outputSpeech = starter + rest
        return response(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find the domains of " + word, True)


def GetEtomologiesIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)
    
    etymologies = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                if j.has_key('etymologies'):
                    for etms in j['etymologies']:
                        if etms not in etymologies : 
                            etymologies.append(etms)

    if len(etymologies) > 0 :
        starters = [
            "The word " + word +" is derived from "
        ]
        starter = getRandom (starters)
        rest = getFromArray(etymologies)
        # print(starter, rest)
        outputSpeech = starter + rest
        return response(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find any history related to " + word, True)
    

def SpellingIntent(intent):
    word, language = getWordnLanguage(intent)
    outputSpeech = "The spelling of the word " + word + " is <say-as interpret-as=\"spell-out\">" + word + "</say-as>."
    
    return response_SSML(outputSpeech, True)


def GetTranslationsIntent(intent):
    word = getWord(intent)
    lan1 = getSlotValue(intent, 'LANGUAGE_O')
    lan2 = getSlotValue(intent, 'LANGUAGE_T')
    if lan1 != -1:
        language1 = checkLanguage(lan1)
    else : 
        language1 = 'en'

    if lan2 != -1:
        language2 = checkLanguage(lan2)
        
    if language1 == language2:
        return response("You cannot translate to the same language. It will be the same, obviously. Please try again for different languages.", True)

    available_languages = ['en', 'es', 'nso', 'zu', 'ms', 'id', 'tn', 'ur', 'pt', 'de']
    if language1 not in available_languages or language2 not in available_languages:
        return response("Sorry, for translation only these languages are supported, English, Spanish, Northern Sotho, isiZulu, Malay, Indonesian, Setswana, Urdu, Portuguese and German.", True)

    url = baseURL + 'entries/' + language1 + '/' + word + '/translations=' + language2
    print(word, language1, language2, url)

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        rjson = json.loads(r.text)
    except Exception as e:
        return response("Sorry, I couldn't find anything for " + word + ". Please try again.", True)

    translations = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for sense in j['senses']:
                    if sense.has_key('translations'):
                        for tra in sense['translations']:
                            if tra.has_key('text') and tra['text'] not in translations: 
                                translations.append(tra['text'])

    if len(translations) > 0 : 

        starter = "The " + lan2 + " translation of " + lan1 + " word " + word + " is, " 

        rest = getFromArray(translations)
        # print(starter, rest)
        outputSpeech = starter + rest
        return response(outputSpeech, True)
    else : 
        return response("Sorry, I couldn't find any translation of the " + word + " to " + lan2 + ". Please try again", True)




def getWordnLanguage(intent):
    return [getWord(intent), getLanguage(intent)]


def puten(lan):
    if lan != -1 :
        return lan
    return 'en'


def do_help():
    Features = "The Protone dictionary supports multiple features like definitions, synonyms, antonyms, examples, domains in which your word is spoken, etomologies, spellings and translations. For example, "
    Messages = [
        "to get the definition of the word 'change', you can say, tell me the definition of the word 'change'. ",
        "to get the synonyms of the word 'change', you can say, tell me the synonyms of the word 'change'. ",
        "to get the antonyms of the word 'change', you can say, tell me the antonyms of the word 'change'. ",
        "to get some examples of using the word 'change', you can say, tell me the examples of the word 'change'. ",
        "to know the domains in which a particular word is used, you can say, tell me the domains in which the word 'change' is used. ",
        "to know the history behind the word 'change', you can say, what is the etomology of the word 'change'. ",
        "to get the spelling of word change, you can say, what is the spelling of the word 'change'. "
    ]
    rest = [
        "There are some more examples of using protone dictionary. Ask for help again to know all of them.",
        "What can I do for you?",
        "Is there anything I can do for you?",
        "Hope that I helped."
    ]
    return response(Features + getRandom(Messages) + getRandom(rest), False)


def do_stop():
    Messages = [
        "Good Bye!!!",
        "Aloha",
        "Ciao",
        "Bon Voyage",
        "We'll meet again.",
        "Hope that I helped.",
        "Sayonara"
    ]
    return response(getRandom(Messages), True)


def getWord(intent):
    word = getSlotValue(intent, 'WORD')
    if word != -1:
        return word.lower()
    else:
        return WordAgain(intent)


def getSlotValue(intent, slot):
    if intent['slots'].has_key(slot):
        if intent['slots'][slot].has_key('value') :
            return intent['slots'][slot]['value'].lower()
        else:
            return -1
    else:
        return -1


def getLanguage(intent):
    lan = getSlotValue(intent, 'LANGUAGE')
    if lan != -1:
        return checkLanguage(lan)
    else:
        return 'en'


def checkLanguage(lan):
    if lan == 'english':
        return 'en'
    elif lan == 'spanish':
        return 'es'
    elif lan == 'malay':
        return 'ms'
    elif lan == 'swahili':
        return 'sw'
    elif lan == 'setswana':
        return 'tn'
    elif lan == 'northern sotho':
        return 'nso'
    elif lan == 'latvian':
        return 'lv'
    elif lan == 'indonesian':
        return 'id'
    elif lan == 'urdu':
        return 'ur'
    elif lan == 'isizulu':
        return 'zu'
    elif lan == 'romanian':
        return 'ro'
    elif lan == 'hindi':
        return 'hi'
    elif lan == 'german':
        return 'de'
    elif lan == 'portuguese':
        return 'pt'
    elif lan == 'tamil':
        return 'ta'
    elif lan == 'gujarati':
        return 'gu'
    else:
        return -1


def getRandom(starters):
    return starters[random.randint(0, len(starters) - 1)] 


def getFromArray(array):
    output = ""
    i = 0
    random.shuffle(array)
    for value in array:
        if value.find(";") != -1:
            output += value[:value.find(";")]
        else : 
            output += value
        if i <= len(array) - 2 and i < 5:
            output += ", "
        if i == len(array) - 2 or i == 4:
            output += "and, "
        if i == len(array) - 1 or i == 5: 
            output += "."
        if i >= 5:
            break
        i += 1
    output = output.replace(";", " and")
    output = re.sub('[^A-Za-z0-9,. ]+', '', output)
    return output


def response_plain_text(output, endsession, attributes, title, cardContent, repromt):
    print("\n")
    print(output)
    print("\n")
    """ create a simple json plain text response  """
    return {
        'version'   : '1.0',
        'response'  : {
            'shouldEndSession'  : endsession,
            'outputSpeech'  : {
                'type'      : 'PlainText',
                'text'      : output
            },
            'card' : {
                'type' : 'Simple',
                'title' : title,
                'content' : cardContent    
            },
            'repromt' : {
                'outputSpeech' : {
                    'type' : 'PlainText',
                    'text' : repromt
                }
            }
        },
        'sessionAttributes' : attributes
    }


def response(outputSpeech, shouldEndSession):
    print("\n")
    print(outputSpeech)
    print("\n")
    return {
        'version'   : '1.0',
        'response'  : {
            'shouldEndSession'  : shouldEndSession,
            'outputSpeech'  : {
                'type'      : 'PlainText',
                'text'      : outputSpeech
            }
        },
        'sessionAttributes' :{
            'Value' : 1
        }
    }


def getWelcomeMessage():
    Messages = [
        "Welcome to Protone Dictionary!",
        "This is Protone Dictionary!",
        "Hello there, How may I help you?",
        "Welcome to Protone Dictionary, What should I do for you today?",
        "Welcome, What can I do for you?",
        "Hello there, shall we get started?",
        "Welcome, What should I look for today?",
        "Welcome, did you find any new words?",
        "Welcome, hop on to the world of words",
        "I'm soo happy to see you.",
        "Hello, nice to meet you.",
        "Hello, let's find meaning of some interesting words."
    ];
    return getRandom(Messages)


def dialog_response(attributes, endsession):

    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
}

def response_SSML(outputSpeech, shouldEndSession):
    return {
        'version'   : '1.0',
        'response'  : {
            'shouldEndSession'  : shouldEndSession,
            'outputSpeech'  : {
                'type'      : 'SSML',
                'ssml'      : '<speak> ' + outputSpeech + '</speak>'
            }
        }
    }

"""
TODO:// make responses to show cards as well
"""

