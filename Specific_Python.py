import nltk
from nltk.tag.stanford import StanfordNERTagger


PATH_TO_JAR='/Users/josemuniz/Desktop/stanford-ner-2020-11-17/stanford-ner.jar'
PATH_TO_MODEL = '/Users/josemuniz/Desktop/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'

tagger = StanfordNERTagger(model_filename=PATH_TO_MODEL,
                          path_to_jar=PATH_TO_JAR, 
                          encoding='utf-8')

words = nltk.word_tokenize("Corporate governance For the year ended 31 March 2022, under The Companies (Miscellaneous Reporting) Regulations 2019, the company has adopted the Wates principles for large private companies as an appropriate framework when making disclosure about its corporate governance arrangements. Each of the 6 Wates Principles has been considered individually within the context of the company's operations. A supporting statement is set out below how the Opportunity & Risk and Executive Remuneration principles have been applied. The principles of Purpose & Leadership, Board Composition, Directors Responsibilities and Stakeholder Relationships & Engagement are set out within the section 172 statements within the Strategic Report. Opportunity & Risk A Board should promote the long-term sustainable success oj the company by identifying opportunities to create and preserve value and establishing oversight for the identification and mitigation of risks. The company operates within an NRC contract with the Department for Transport. The Company acts to comply with the obligations of these agreements and act as a Good and Efficient Operator. A risk register is updated regularly, quantifying the biggest internal and external risk factors facing the company. This register is approved by the Executive Committee of the company and the Board. Each risk is assigned an owner and mitigating actions are taken to either manage the risk or eradicate it entirely, where possible.    Executive remuneration A Board should promote executive remuneration structures aligned to the long-term sustainable success of the company, taking into account pay and conditions elsewhere in the company. The group remuneration committee considers the pay and incentive structures for senior management across the group, including the executive directors of the company. The renumeration of the executive directors of the company is established through a process which takes into account the same factors as the group executives. These include: • Alignment of pay with the purpose, values and strategy of the business. • The relationship between the directors' pay and that of the wider workforce. The Board is committed to creating an environment at all levels in the company which enables people to perform and develop their abilities and potential. The Board strives to ensure that company has a diverse workplace which does not attach specific importance to age, community background or country of origin, disability, gender, nationality, political opinion, religious belief, or sexuality - that ensures that we are able to attract talented employees who will contribute to the success of the company."")


import stanza                    
stanza.download('en') # download English model
nlp = stanza.Pipeline('en') # initialize English neural pipeline
doc = nlp("Barack Obama was born in Hawaii.") # run annotation over a sentence
print(doc)
print(doc.entities)


# Main Example
doc = nlp("As a private company with NWL's ownership structure, we believe it is consistent with good corporate governance for there to be significant shareholder representation on the Board, including the Chairmanship. We also accept that there needs to be an appropriate balance. As I explain at page 68, we have taken the opportunity to continue to refresh the Board this year. We have five newly appointed INEDs, and four further Non-Executive Directors (NEDs), including me as Chairman, which makes INEDs the largest single group on the Board. ") # run annotation over a sentence
print(doc)
print(doc.entities)
doc.sentences[3].print_dependencies()




# NLP Stanford
stanza.install_corenlp() #Initiate CoreNLP Stanford
import stanza
from stanza.server import CoreNLPClient
import os

text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
        timeout=30000,
        memory='6G') as client:
    ann = client.annotate(text)
# get the first sentence
sentence = ann.sentence[0]
# get the constituency parse of the first sentence
constituency_parse = sentence.parseTree
print(constituency_parse)
print(sentence.basicDependencies)   

## Option B
# Construct a CoreNLPClient with some basic annotators, a memory allocation of 4GB, and port number 9001
client = CoreNLPClient(
    annotators=['tokenize','ssplit', 'pos', 'lemma', 'ner'], 
    memory='4G', 
    endpoint='http://localhost:9001',
    be_quiet=True)
print(client)

# Start the background server and wait for some time
# Note that in practice this is totally optional, as by default the server will be started when the first annotation is performed
client.start()
import time; time.sleep(10)
    
# Annotate some text
text = "Albert Einstein was a German-born theoretical physicist. He developed the theory of relativity in 1999. He had 10% stocks that he sold 10 times"
text = "As a private company with NWL's ownership structure, we believe it is consistent with good corporate governance for there to be significant shareholder representation on the Board, including the Chairmanship. We also accept that there needs to be an appropriate balance. As I explain at page 68, we have taken the opportunity to continue to refresh the Board this year. We have five newly appointed INEDs, and four further Non-Executive Directors (NEDs), including me as Chairman, which makes INEDs the largest single group on the Board. "
document = client.annotate(text)
document

# Access Annotations
# Iterate over all tokens in all sentences, and print out the word, lemma, pos and ner tags
print("{:12s}\t{:12s}\t{:6s}\t{}".format("Word", "Lemma", "POS", "NER"))

for i, sent in enumerate(document.sentence):
    print("[Sentence {}]".format(i+1))
    for t in sent.token:
        print("{:12s}\t{:12s}\t{:6s}\t{}".format(t.word, t.lemma, t.pos, t.ner))
    print("")

# Iterate over all detected entity mentions
print("{:30s}\t{}".format("Mention", "Type"))

for sent in document.sentence:
    for m in sent.mentions:
        print("{:30s}\t{}".format(m.entityMentionText, m.entityType)) 
    
# Print annotations of a token
print(document.sentence[0].token[0])

# Print annotations of a mention
print(document.sentence[0].mentions[0])

# Shut down the background CoreNLP server
client.stop()
time.sleep(10)






