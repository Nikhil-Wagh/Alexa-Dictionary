import requests
import json
import random
import re

app_id = '25b51a25'
app_key = '22990bfcc0e232e45d7a891b399d3ee4'
baseURL = 'https://od-api.oxforddictionaries.com:443/api/v1/'
choice = -1

# python-lambda-local -f lambda_handler -t 10 lambda_function.py ./events/event.json

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

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    rjson = json.loads(r.text)
    defs = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    for n in m['definitions']:
                        defs.append(n)

    n = len(defs)
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


def GetSynonymsIntent(intent):
    word, language = getWordnLanguage(intent)
    print (word, language)
    url = baseURL + 'entries/' + language + '/' + word + '/synonyms'
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    rjson = json.loads(r.text)
    syms = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    for n in m['synonyms']:
                        syms.append(n['text'])

    n = len(syms)
    starters = [
        "Here's what I've found, "
    ]
    starter = getRandom (starters)
    rest = getFromArray(syms)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response(outputSpeech, True)


def GetAntonymsIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word + '/antonyms'
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    rjson = json.loads(r.text)
    antyms = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    for n in m['antonyms']:
                        antyms.append(n['text'])

    n = len(antyms)
    starters = [
        "Here's what I've found, "
    ]
    starter = getRandom (starters)
    rest = getFromArray(antyms)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response(outputSpeech, True)
    

def GetExamplesIntent(intent):
    word, language = getWordnLanguage(intent)
    if language == 'en' or language == 'es':
        url = baseURL + 'entries/' + language + '/' + word + '/sentences'
    else:
        response_plain_text(getLanguageNotSupportedMessage(), false, GetExamplesIntent)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    
    rjson = json.loads(r.text)
    examples = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for sent in i['sentences']:
                examples.append(sent['text'])

    starters = [
        "Here's what I've found, "
    ]
    starter = getRandom (starters)
    rest = ""
    i = 0
    for e in examples :
        index = e.find(word) 
        e = e[ : e.find(",")]
        if index != -1: 
            rest += e[:index] + '<emphasis level="strong">' + e[index : e.find(" ", index)] + '</emphasis>' + e[e.find(" ", index) : ] + ". "
        if i > 1:
            break
        i += 1
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_SSML(outputSpeech, True)

def GetDomainsIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    rjson = json.loads(r.text)

    domains = set()
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    if m.has_key('domains'):
                        for d in m['domains']:
                            domains.add(d)

    n = len(domains)
    starters = [
        "Here's what I've found, "
    ]
    starter = getRandom (starters)
    rest = getFromArray(domains)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response(outputSpeech, True)


def GetEtomologiesIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    rjson = json.loads(r.text)

    etymologies = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                if j.has_key('etymologies'):
                    for etms in j['etymologies']:
                        etymologies.append(etms)

    n = len(etymologies)
    starters = [
        "Here's what I've found, "
    ]
    starter = getRandom (starters)
    rest = getFromArray(etymologies)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response(outputSpeech, True)
    

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
    else:
        language1 = 'en'

    if lan2 != -1:
        language2 = checkLanguage(lan2)
    else:
        language2 = 'en'

    if language1 == language2:
        # TODO:// return correct response 
        return "You cannot translate to same language."
    available_languages = ['en', 'es', 'nso', 'zu', 'ms', 'id', 'tn', 'ur', 'pt', 'de']
    if language1 not in available_languages or language2 not in available_languages:
        return response("Sorry, for translation only these languages are supported, English, Spanish, Northern Sotho, isiZulu, Malay, Indonesian, Setswana, Urdu, Portuguese and German.", True)

    url = baseURL + 'entries/' + language1 + '/' + word + '/translations=' + language2
    print(word, language1, language2, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    print(r.status_code)
    rjson = json.loads(r.text)

    translations = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for sense in j['senses']:
                    if sense.has_key('translations'):
                        for tra in sense['translations']:
                          translations.append(tra['text'])

    starter = "The " + lan2 + " translation of " + lan1 + " word " + word + " is, " 

    rest = getFromArray(translations)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response(outputSpeech, True)



def getWordnLanguage(intent):
    return [getWord(intent), getLanguage(intent)]


def puten(lan):
    if lan != -1 :
        return lan
    return 'en'


def do_help():
    Message = "You can ask for definitions, synonyms, antonyms, examples, domains in which your word is spoken, etomologies, spellings and translations" \
            "you can say, tell me the definition of the word 'change', "\
            "or you can say, tell me the synonyms of the word 'change', "\
            "or you can say, tell me the examples of the word 'change', "\
            "or you can say, tell me the domains in which the word 'change' is used, "\
            "or you can say, what is the etomology of the word 'change', "\
            "or you can say, what is the spelling of the word 'change'. "\
            "What can I do for you?"
    return response(Message, False)


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
        return response_plain_text(getLanguageNotSupportedMessage(), False)


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
        "Welcome, hope on to the world of words",
        "I'm soo happy to see you.",
        "Hello, nice to meet you.",
        "Hello, let's find meaning of some interesting words."
    ];
    return getRandom(Messages)


def getHelpMessage():
    return  "You can say what is the definition of the word YOUR WORD" \
            " or you can say give me the synonyms of the word YOUR WORD "


def getStopMessage():
    return "Nice meeting you. Please visit again"


def getLanguageNotSupportedMessage():
    return "Sorry the given language is not supported for this operation"


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
I didn't catch the last word, can you please repeat it for me.
I'm sorry I wasn't paying attention, can you please repeat the last word
Please repeat the word you are looking for
I'm not sure I know that word. Can you repeat the word please?
please provide me the word you are looking for


I'm looking for the word {WORD}
the word was {WORD}
the word is {WORD}


TODO:// add try catch block in every api call
TODO:// make responses to show cards as well
"""

