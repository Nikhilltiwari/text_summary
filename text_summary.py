import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation 
from heapq import nlargest

text ="Apple Inc. had its genesis in the lifelong dream of Stephen G. Wozniak to build his own computer—a dream that was made suddenly feasible with the arrival in 1975 of the first commercially successful microcomputer, the Altair 8800, which came as a kit and used the recently invented microprocessor chip. Encouraged by his friends at the Homebrew Computer Club, a San Francisco Bay area group centred around the Altair, Wozniak quickly came up with a plan for his own microcomputer. In 1976, when the Hewlett-Packard Company, where Wozniak was an engineering intern, expressed no interest in his design, Wozniak, then 26 years old, together with a former high-school classmate, 21-year-old Steve Jobs, moved production operations to the Jobs family garage. Jobs and Wozniak named their company Apple. For working capital, Jobs sold his Volkswagen minibus and Wozniak his programmable calculator. Their first model was simply a working circuit board, but at Jobs’s insistence the 1977 version was a stand-alone machine in a custom-molded plastic case, in contrast to the forbidding steel boxes of other early machines. This Apple II also offered a colour display and other features that made Wozniak’s creation the first microcomputer that appealed to the average person."
def summarizer(rawdocs): 

   stopwords=list(STOP_WORDS)
   #print(stopwords) 
   nlp=spacy.load('en_core_web_sm')
   doc=nlp(rawdocs)
   #print(doc)
   tokens= [token.text for token in doc]
   #print(tokens)
   word_freq={}
   for word in doc:
    if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
        if word.text not in word_freq.keys():
            word_freq[word.text]=1
        else:
            word_freq[word.text]+=1

   #print(word_freq)

   max_freq=max(word_freq.values())
   #print(max_freq)
   for word in word_freq.keys():
    word_freq[word]=word_freq[word]/max_freq

    #print(word_freq)

    sent_token= [sent for sent in doc.sents]
    #print(sent_token)
    sent_score={}
    for sent in sent_token:
     for word in sent:
        if word.text in word_freq.keys():
            if sent not in sent_score.keys():
                sent_score[sent]=word_freq[word.text]
            else:
                sent_score[sent]+=word_freq[word.text]
                 
     #print(sent_score)
     select_len=int(len(sent_token)*0.33)
     #print(select_len)
     summary= nlargest(select_len,sent_score,key=sent_score.get)
     final_summary=[word.text for word in summary]
     summary=  ''.join(final_summary)
     #print(summary)
     #print("****Length of original text",len(text.split(' ')))
     #print("****Length of summary text",len(summary.split(' ')))
   return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))
summarizer(text)