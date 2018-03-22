import requests
import json

app_id = '25b51a25'
app_key = '22990bfcc0e232e45d7a891b399d3ee4'
baseURL = 'https://od-api.oxforddictionaries.com:443/api/v1/'
choice = -1

def GetDefinitionIntent():
	# word = getWord(intent, GetDefinitionIntent)
	# language = getLanguage(intent, GetDefinitionIntent)
    word = 'peculiar'
    language = 'en'
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

GetDefinitionIntent()
