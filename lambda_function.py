import requests
import json
from random import randint

app_id = '25b51a25'
app_key = '22990bfcc0e232e45d7a891b399d3ee4'
baseURL = 'https://od-api.oxforddictionaries.com:443/api/v1/'
choice = -1

def lambda_handler(event, context):
    # if 'attributes' in event['session']:
    #     if event['session']['attributes']['Value']:
    #         print "Value in attributes is :: " + event['session']['attributes']['Value']

    if event['request']['type'] == "LaunchRequest":
        return response_plain_text(getWelcomeMessage(), False)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])


def on_intent(request):
    intent = request['intent']
    intent_name = intent['name']

    if intent_name == "GetDefinitionIntent":
        return GetDefinitionIntent(intent)
    elif intent_name == "WordAgain":
        return WordAgain(intent)
    elif intent_name == "GetPronounciationIntent":
        return GetPronounciationIntent(intent)
    elif intent_name == "GetExamplesIntent":
        return GetExamplesIntent(intent)
    elif intent_name == "GetDomainsIntent":
        return GetDomainsIntent(intent)
    elif intent_name == "GetEtomologiesIntent":
        return GetEtomologiesIntent(intent)
    elif intent_name == "GetRegionsIntent":
        return GetRegionsIntent(intent)
    elif intent_name == "GetSynonymsIntent":
        return GetSynonymsIntent(intent)
    elif intent_name == "GetAntonymsIntent":
        return GetAntonymsIntent(intent)
    elif intent_name == "SearchIntent":
        return SearchIntent(intent)
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
    starter = getRandomStarters (starters, n)
    rest = getFromArray(defs)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)


def GetSynonymsIntent(intent):
    word, language = getWordnLanguage(intent)
    print (word, language)
    url = baseURL + 'entries/' + language + '/' + word + '/synonyms'

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
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(syms)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)


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
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(antyms)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)



def GetPronounciationIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    pronounciation_files = []
    rjson = json.loads(r.text)
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            pronounciation_files.append(i['pronounciations'][0]['audioFile'])

    n = len(pronounciation_files)
    starters = [
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(pronounciation_files)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)
    

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

    n = len(examples)
    starters = [
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(examples)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)

def GetDomainsIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    rjson = json.loads(r.text)
    domains = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    if m.has_key('domains'):
                        for d in m['domains']:
                            domains.append(d)

    n = len(domains)
    starters = [
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(domains)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)


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
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(etymologies)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)
    


def GetRegionsIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    rjson = json.loads(r.text)
    regions = []
    for k in rjson['results']:
        for i in k['lexicalEntries']:
            for j in i['entries']:
                for m in j['senses']:
                    for region in m['regions']:
                        regions.append(region)

    n = len(regions)
    starters = [
        
    ]
    starter = getRandomStarters (starters, n)
    rest = getFromArray(regions)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)



def SearchIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'search/' + language + '?q=' + word + ',limit=5'
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    rjson = json.loads(r.text)

    words = []
    for result in rjson['results']:
        words.append({
            'word': result['word'],
            'matchType': result['matchType']
            })


    outputSpeech = "Found these words which might be similar to the word " + word + ". "
    for word in words:
        outputSpeech += word['word'] + " of type " + word['matchType'] + " "

    return response_plain_text(outputSpeech, True)


def SpellingIntent(intent):
    word, language = getWordnLanguage(intent)
    url = baseURL + 'entries/' + language + '/' + word.lower()
    print(word, language, url)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    rjson = json.loads(r.text)

    outputSpeech = "The Spelling of the word " + word + " is <speak><say-as interpret-as=\"spell-out\">" + word + "</say-as>.</speak>"
    
    return response_plain_text(outputSpeech, True)


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


    n = len(syms)
    starters = [
        
    ]
    # TODO:// In the following format
    outputSpeech = "The translations of the word " + word + " in language " + language2 + " are "

    starter = getRandomStarters (starters, n)
    rest = getFromArray(syms)
    # print(starter, rest)
    outputSpeech = starter + rest
    return response_plain_text(outputSpeech, True)



def getWordnLanguage(intent):
    return [getWord(intent), getLanguage(intent)]


def puten(lan):
    if lan != -1 :
        return lan
    return 'en'

def WordAgain(intent):
    return response_plain_text(getWordAgainMessage(), False)


def do_help():
    return response_plain_text(getHelpMessage(), False)


def do_stop():
    return response_plain_text(getStopMessage(), True)


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


def getRandomStarters(starters, n):
    return starters[randint(0, n - 1)]  


def getFromArray(array):
    output = ""
    i = 0
    for value in array:
        output += value
        if i < len(array) - 1:
            output += ", "
        else :
            output += "."
        if i >= 5:
            break
    return output.replace(";", " or ")


def response_plain_text(output, endsession, attributes, title, cardContent, repromt):
    print(output)
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


def response():
    return {
        'version'   : '1.0',
        'response'  : {
            'shouldEndSession'  : False,
            'outputSpeech'  : {
                'type'      : 'PlainText',
                'text'      : "How can I help you?"
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
        "I'm soo happy to see you."
        "Hello, nice to meet you.",
        "Hello, let's find meaning of some interesting words."
    ];
    return Messages[randint(0, len(Message) - 1)]


def getWordAgainMessage():
    return "Please repeat the word again"


def getHelpMessage():
    return  "You can say what is the definition of the word YOUR WORD" \
            " or you can say give me the synonyms of the word YOUR WORD "


def getStopMessage():
    return "Nice meeting you. Please visit again"


def getLanguageNotSupportedMessage():
    return "Sorry the given language is not supported for this operation"
