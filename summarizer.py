# coding=UTF-8

from __future__ import division
import nltk
nltk.download('punkt')
import string

PUNCT_MAP = dict((ord(char), None) for char in string.punctuation)

class Summary(object):

    def __init__(self, sw_fname='data/stopwords.txt'):
        """
        Constructor which loads the stemmer and stopwords
        """
        self.stemmer = nltk.PorterStemmer()
        self.sent_tokenize = nltk.sent_tokenize
        with open(sw_fname) as f:
            self.stopwords = set([w.lower().strip() for w in f.readlines()])

    def clean_sent(self, s):
        """
        clean the sentence, convert to lowercase, remove punctuations
        """
        clean_s = " ".join(s.split()) # remove white spaces
        if type(clean_s) == unicode:
            clean_s = clean_s.translate(PUNCT_MAP)
        else:
            clean_s = clean_s.translate(None, string.punctuation) # remove punctuations

        return clean_s

    def format_sent(self, sent):
        """
        return list of formatted sentences
        format sentence -> remove stop words and stem the remaining words
        """
        format_sent = []
        for s in sent:
            format_s = []
            s = self.clean_sent(s)
            for word in s.split(" "):
                if word.lower() not in self.stopwords:
                    format_word = self.stemmer.stem(word.lower())
                    format_s.append(format_word)
            format_sent.append(format_s)
        return format_sent

    def intersection(self, sent1, sent2):
        """
        function to find interesection of two sentences
            i.e. no. of common words / length
        """
        s1 = set(sent1)
        s2 = set(sent2)
        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0
        
        # We normalize the result by the average number of words
        
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    def get_scores(self, sent):
        """
        calculate score of sentence
            based on no of intersection with other sentences
            higher the intersection with other sentences, more is the content covered,
            more is the score of that sentence
        """
        format_sent = self.format_sent(sent)
        n = len(format_sent)
        assert n == len(sent)
        #print "Number of sentencesin test",len(sent)

        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.intersection(format_sent[i], format_sent[j])

        scores = []
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
                #score2 = score/len(sent)
            scores.append(score)
            #print scores
        return scores

    def get_summary(self, text, k=0.5):
        """
        return summary by
        calculate score of each sentence
        return the top_k sentences in order
        """
        sent = self.sent_tokenize(text)
        if k > len(sent):
            k = len(sent)

        scores = self.get_scores(sent)
	#print scores
        order = sorted(enumerate(scores), key=lambda x:x[1], reverse=True)
        order = order[:k]
        order = sorted(order, key=lambda x:x[0])
        summ_sent = []
        for index, _ in order[:k]:
            summ_sent.append(sent[index])

        summary = " ".join(summ_sent)
        return summary
