import requests
import json

app_id = '25b51a25'
app_key = '22990bfcc0e232e45d7a891b399d3ee4'
baseURL = 'https://od-api.oxforddictionaries.com:443/api/v1/'
choice = -1

def lambda_handler(event, context):
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
		GetDefinitionIntent(intent)
	elif intent_name == "WordAgain":
		WordAgain(intent)
	elif intent_name == "GetPronounciationIntent":
		GetPronounciationIntent(intent)
	elif intent_name == "GetExamplesIntent":
		GetExamplesIntent(intent)
	elif intent_name == "GetDomainsIntent":
		GetDomainsIntent(intent)
	elif intent_name == "GetEtomologiesIntent":
		GetEtomologiesIntent(intent)
	elif intent_name == "GetRegionsIntent":
		GetRegionsIntent(intent)
	elif intent_name == "GetSynonymsIntent":
		GetSynonymsIntent(intent)
	elif intent_name == "GetAntonymsIntent":
		GetAntonymsIntent(intent)
	elif intent_name == "SearchIntent":
		SearchIntent(intent)
	elif intent_name == "SpellingIntent":
		SpellingIntent(intent)
	elif intent_name == "GetTranslationsIntent":
		GetTranslationsIntent(intent)
	elif intent_name == "AMAZON.HelpIntent":
		do_help()
	elif intent_name == "AMAZON.StopIntent":
		do_stop()
	elif intent_name == "AMAZON.CancelIntent":
		do_stop()
	else:
		print("Invalid Intent reply with help")
		do_help()

def GetDefinitionIntent(intent):
	word = getWord(intent, GetDefinitionIntent)
	language = getLanguage(intent, GetDefinitionIntent)
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

	print defs
	if len(defs) > 1:
		outputSpeech = "The definitions of the word " + word + " are "
	else:
		outputSpeech = "The definition of the word " + word + " is "
	i = 0
	for definition in defs:
		outputSpeech = outputSpeech + definition
		i = i + 1
		if i < len(defs):
			outputSpeech += " or "
	print outputSpeech
	response_plain_text(outputSpeech, False)


def GetSynonymsIntent(intent):
	word, language = getWordnLanguage(intent, GetSynonymsIntent)
	url = baseURL + 'entries/' + language + '/' + word + '/synonyms'
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetAntonymsIntent(intent):
	word, language = getWordnLanguage(intent, GetAntonymsIntent)
	url = baseURL + 'entries/' + language + '/' + word + '/antonyms'
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetPronounciationIntent(intent):
	word, language = getWordnLanguage(intent, GetPronounciationIntent)
	url = baseURL + 'entries/' + language + '/' + word.lower()
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetExamplesIntent(intent):
	word, language = getWordnLanguage(intent, GetExamplesIntent)
	if language == 'en' or language == 'es':
		url = baseURL + 'entries/' + language + '/' + word + '/sentences'
	else:
		response_plain_text(getLanguageNotSupportedMessage(), false, GetExamplesIntent)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetDomainsIntent(intent):
	word, language = getWordnLanguage(intent, GetDomainsIntent)
	url = baseURL + 'entries/' + language + '/' + word.lower()
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetEtomologiesIntent(intent):
	word, language = getWordnLanguage(intent, GetEtomologiesIntent)
	url = baseURL + 'entries/' + language + '/' + word.lower()
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetRegionsIntent(intent):
	word, language = getWordnLanguage(intent, GetRegionsIntent)
	url = baseURL + 'entries/' + language + '/' + word.lower()
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def SearchIntent(intent):
	word, language = getWordnLanguage(intent, GetAntonymsIntent)
	url = baseURL + 'search/' + language + '?q=' + word + ',limit=5'
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def SpellingIntent(intent):
	word, language = getWordnLanguage(intent, GetEtomologiesIntent)
	url = baseURL + 'entries/' + language + '/' + word.lower()
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))


def GetTranslationsIntent(intent):
	word = getWord(intent, GetTranslationsIntent)
	language1 = getLanguage(intent, GetTranslationsIntent)
	language2 = getLanguage(intent, GetTranslationsIntent)
	url = baseURL + 'entries/' + language1 + '/' + word + '/translations=' + language2
	print(word, language, url)

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("json \n" + json.dumps(r.json()))



def getWordnLanguage(intent, callback):
	return getWord(intent, callback), getLanguage(intent)


def WordAgain(intent, callback):
	response_plain_text(getWordAgainMessage(), False)
	callback(intent)


def do_help():
	response_plain_text(getHelpMessage(), False)


def do_stop():
	response_plain_text(getStopMessage(), True)


def getWord(intent, callback):
	if intent['slots']['WORD'] != None:
		return intent['slots']['WORD']['value']
	return WordAgain(intent, callback)


def getLanguage(intent, callback):
	if intent['slots'].has_key('LANGUAGE') :
		lan = intent['slots']['LANGUAGE']['value']
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
			return response_plain_text(getLanguageNotSupportedMessage(), false, callback)
	else:
		return 'en'


def response_plain_text(output, endsession):
    """ create a simple json plain text response  """
    return {
    	'version'	: '1.0',
        'response'	: {
			'shouldEndSession'	: endsession,
	        'outputSpeech'	: {
	        	'type'		: 'PlainText',
	        	'text'		: output
	        }
        },
		'sessionAttributes'	:{}
    }


def getWelcomeMessage():
	return ""


def getWelcomeMessage():
	Messages = [
		"Welcome to Protone Dictionary!",
		"This is Protone Dictionary!",
		""
	];
	return "Welcome"


def getWordAgainMessage():
	return "Please repeat the word again"


def getHelpMessage():
	return 	"You can say what is the definition of the word YOUR WORD" \
			" or you can say give me the synonyms of the word YOUR WORD "


def getStopMessage():
	return "Nice meeting you. Please visit again"
