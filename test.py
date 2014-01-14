# coding=latin-1
'''
Created on 14 Jan 2014

@author: Andrew
'''

print "NLP test"
from java.sql import *
from java.lang import Class
from java.lang import Math
from com.mysql.jdbc import Driver

from java.io import FileInputStream

from opennlp.tools.sentdetect import SentenceModel
from opennlp.tools.sentdetect import SentenceDetectorME
from opennlp.tools.tokenize import TokenizerModel
from opennlp.tools.tokenize import TokenizerME
from opennlp.tools.namefind import TokenNameFinderModel
from opennlp.tools.namefind import NameFinderME
from opennlp.tools.util import Span

sentenceModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-sent.bin")
tokenModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-token.bin")
nameModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-ner-person.bin")
locationModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-ner-location.bin")
organizationModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-ner-organization.bin")
dateModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-ner-date.bin")
timeModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-ner-time.bin")
moneyModelIn = FileInputStream("c:\jython2.5.2\ext\opennlp\models\en-ner-money.bin")


def loadSentenceModel(modelIn):
    try:
        model = SentenceModel(modelIn)
    except Exception:
        print "Model Load failed"
    finally:
        if (modelIn != None):
            try:
                modelIn.close()
            except Exception:
                print "File close failed"
    return model

def loadTokenModel(modelIn):
    try:
        model = TokenizerModel(modelIn)
    except Exception:
        print "Model Load failed"
        model = None
    finally:
        if (modelIn != None):
            try:
                modelIn.close()
            except Exception:
                print "File close failed"
    return model
          

def loadNameModel(modelIn):
    try:
        model = TokenNameFinderModel(modelIn)
    except Exception:
        print "Model Load failed"
        model = None
    finally:
        if (modelIn != None):
            try:
                modelIn.close()
            except Exception:
                print "File close failed"
    return model
          


def getSentences(inputText):        
    sentenceDetector = SentenceDetectorME(sentenceModel)
    sentences = sentenceDetector.sentDetect(inputText)
    return sentences

def getTokens(inputSent):        
    tokenizer = TokenizerME(tokenModel)
    tokens = tokenizer.tokenize(inputSent)
    return tokens

def getNames(model, sentence):
    nameFinder = NameFinderME(model)
    nameSpans = nameFinder.find(sentence)
    nameFinder.clearAdaptiveData()
    return nameSpans



sentenceModel = loadSentenceModel(sentenceModelIn)
tokenModel = loadTokenModel(tokenModelIn)
personNameModel = loadNameModel(nameModelIn)
locationNameModel = loadNameModel(locationModelIn)
organizationNameModel = loadNameModel(organizationModelIn)
dateNameModel = loadNameModel(dateModelIn)
timeNameModel = loadNameModel(timeModelIn)
moneyNameModel = loadNameModel(moneyModelIn)


def anonymizeSentence(sentence):
    #print sentence
    tokens = getTokens(sentence)
    #for token in tokens:
    #    print token
    names = Span.spansToStrings(getNames(personNameModel, tokens), tokens)
    for name in names:
        sentence = sentence.replace(name, "{person}")
    locations = Span.spansToStrings(getNames(locationNameModel, tokens), tokens)
    for location in locations:
        sentence = sentence.replace(location, "{location}")
    orgs = Span.spansToStrings(getNames(organizationNameModel, tokens), tokens)
    for org in orgs:
        sentence = sentence.replace(org, "{organisation}")
    names = Span.spansToStrings(getNames(dateNameModel, tokens), tokens)
    for name in names:
        sentence = sentence.replace(name, "{date}")
    names = Span.spansToStrings(getNames(timeNameModel, tokens), tokens)
    for name in names:
        sentence = sentence.replace(name, "{time}")
    names = Span.spansToStrings(getNames(moneyNameModel, tokens), tokens)
    for name in names:
        sentence = sentence.replace(name, "{money}")
    return sentence

        
        
def anonymizeText(text):
    sentences = []
    for sentence in getSentences(text):
        sentences.append(anonymizeSentence(sentence))
    return sentences
    
    
    
#sampleText = "These are fragments. pretending.  To BE Sentences"

#sampleText = """
#I'm Martin from Gloucestershire. I'm currently playing a Martin Handcraft Committee, but think I'd like to get a modern instrument. I just got back into playing by joining the Jazz Band at the school where I teach Computing, so I signed up for lessons too. Loving it!
#"""

sampleText = """
Rudolph Agnew, 55 years old and former chairman of Consolidated Gold Fields PLC, based in London, was named
    a director of this British industrial conglomerate.  He succeeds Filipe Inglese, and his wife Mary is a pharmacist. He has two childen, Mark and Angela, and they live in Surrey"""

sampleText ="""With the passing of Arthur Wilson (21 June 1927 to 10 July 2010) after a long battle with Parkinson's Disease, the music profession has lost one of its finest symphonic trombone players and teachers. Arthur's career spanned more than 50 years. His loss will be deeply felt by hundreds of friends, colleagues and ex-students.
Arthur Wilson was a Londoner born and bred, a third generation professional trombonist whose father, Stanley, was a busy player in dance bands (Harry Davison's in particular), radio broadcasts and theatres between the Wars. His family, which consisted of five boys, lived in Battersea and when he was 16, his father lent him his spare instrument, a good quality medium-bore Courtois, to learn on. By today's norm, Arthur was a late starter, but within a short time he made good progress, his stylistic ambitions along the lines of Tommy Dorsey, whose popular recordings had been a strong influence on his father's playing. Only a matter of months after Arthur had taken up the trombone his father took back Arthur's instrument. Since money was short there was no hope of a replacement instrument of the same quality, and so visits to the local junk shops procured a bell in one, a slide in another and a mouthpiece in yet another - early evidence of the determination that was to be such a feature of Arthur's character. 
"""

sampleText = """
A shiver runs down my back, though the temperature in the car is fine. My mind is racing with the impact of her announcement. For the first time in my life, I'm speechless; no witty comeback, no sassy retort, nothing.

As I gawk at my mom, a hint of recognition is teasing my brain. Then, my junior high geography class comes back, full tilt! An island; it's an island somewhere between Hawaii and Japan. And, if memory serves, a very small island!

Mom, oblivious to my comatose state, carries on with her one sided conversation. She suggests after practice we look up Guam in our well worn set of encyclopedias.

You see, it's October 1979. No internet, computers or cell phones."""


sampleText = """
12:25pm - Douglas Fraser, Business and economy editor, Scotland tweets: Global Energy Group (Aberdeen, Inverness, Nigg etc) reports year to March sales +43% to 358m GBP, earnings double to $34m
"""

sampleText0 = """
The opportunity to interview Dr Tom Stuttaford came up thanks to a chance encounter at the Norfolk-and-Norwich University Hospital.

My colleague, photographer Bill Smith took a picture of Dr Tom Stuttaford just as he was leaving the hospital earlier this month.

He had spent a night in hospital after falling at his home in Elm Hill.

And his daughter-in-law, Jo Stuttaford is the great-granddaughter of Maria Pasqua, the little Italian peasant girl.

"""

sampleText0 = """
During October 1929, Jean-Paul Sartre and Simone de Beauvoir became a couple and Sartre asked her to marry him.[7] One day while they were sitting on a bench outside the Louvre, he said, "Let's sign a two-year lease".[8] Near the end of her life, Beauvoir said, "Marriage was impossible. I had no dowry." So they entered a lifelong relationship.[9] Beauvoir chose never to marry and did not set up a joint household with Sartre.[10] She never had children.[10] This gave her time to earn an advanced academic degree, to join political causes, to travel, to write, to teach, and to have lovers (both male and female – the latter often shared)."""


anonSentences =  anonymizeText(sampleText)    

for sentence in anonSentences:
    print repr(sentence)

print "that's all folks"