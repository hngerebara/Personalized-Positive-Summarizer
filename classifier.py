
from __future__ import division

import nltk
nltk.download('punkt')
import glob
import time
from summarizer import Summary
import cPickle as pickle

def load_spache_words(fname="data/spache_words.txt"):
    spache_words = []
    with open(fname) as f:
        words = []
        for line in f.readlines():
            words += line.split("|")
    words = [w.strip().lower() for w in words]
    spache_words += words
    return set(spache_words)

def load_stopwords(fname="data/stopwords.txt"):
    with open(fname) as f:
        stop_words = [w.lower().strip() for w in f.readlines()]
    return set(stop_words)

def load_neg_words(fname="data/neg_words.txt"):
    with open(fname) as f:
        neg_words = [w.lower().strip() for w in f.readlines()]
    return set(neg_words)

def get_readability(text):
    sents = nltk.sent_tokenize(text)
    words = []
    for s in sents:
        words += s.split()
    n_sents = len(sents)
    n_words = len(words)
    try:
        asl = n_words / n_sents
    except ZeroDivisionError:
        asl = 0
    uniq_words = [w for w in words if w not in spache_words]
    try:
        pdw = (len(uniq_words) / len(words)) * 100
    except ZeroDivisionError:
        pdw = 0
    score = 0.121 * asl + 0.082 * pdw + 0.659
    return score

def clean_text(text):
    """
    cleans the text
    """
    allowed_spec_chars = [" "]
    clean_text = " "
    for char in text.lower():
        if char.isalpha() or char in allowed_spec_chars:
            clean_text += char
        else:
            clean_text += " "

    clean_text = " ".join(clean_text.split())
    return clean_text

def extract_features(text):
    """
    Extract features from the text
    """

    feat_dict = {}

    text = clean_text(text)
    words = text.split()

    for word in words:
        if word not in stop_words and len(word) > 2:
            feat_dict[stem(word)] = True

    return feat_dict

def train(train_set):
    """
    Train the naive bayes classifier
    """
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print "Naive Bayes Training completed."
    return classifier

def predict(classifier, text):
    """
    Predict the label of the text
    """
    if len(neg_words.intersection(set(text.lower().split()))) > 0:
        return "non_suitable"
    features = extract_features(text)
    return classifier.classify(features)

def get_sentilyzer():
    """
    train and return the sentiment analyzer
    """
    from nltk.corpus import movie_reviews

    try:
        classifier = pickle.load(open("data/sentilyzer.pickle"))
        return classifier
    except:
        print "Unable to load sentilyzer, so training it again"

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(extract_features(movie_reviews.raw(fileids=[f])), 'neg') for f in negids]
    posfeats = [(extract_features(movie_reviews.raw(fileids=[f])), 'pos') for f in posids]
    
    print "Length of Negative Features", len(negfeats)
    print "Length of Positive Features", len(posfeats)

    negcutoff = int(len(negfeats) * 3 / 4)
    poscutoff = int(len(posfeats) * 3 / 4)

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

    classifier = nltk.NaiveBayesClassifier.train(trainfeats)
    print 'accuracy of sentiment analysis:', nltk.classify.util.accuracy(classifier, testfeats)
    pickle.dump(classifier, open("data/sentilyzer.pickle", "w"))
    return classifier


def _test():
    """
    A test case to make sure code is right
    """
    train_set = []

    suitable = ["Nice, this is good and so I am very happy",
         "I am happy",
         "Happiness is good for health"]

    non_suitable = ["Rape, violence not for life",
         "Violence is always bad"]

    for s in suitable:
        train_set.append((extract_features(s), 'suitable'))

    for n in non_suitable:
        train_set.append((extract_features(n), 'non_suitable'))

    classifier = train(train_set)

    assert "non_suitable" == predict(classifier, "Violent attack")
    assert "suitable" == predict(classifier, "I am happy")

def load_train_data(d="data/"):
    """
    A function to load the training data
    """
    train_data = []
    for fname in glob.glob(d + "suitable/*"):
        with open(fname) as f:
            doc = f.read()
        feat = extract_features(doc)
        train_data.append((feat, "suitable"))

    for fname in glob.glob(d + "non_suitable/*"):
        with open(fname) as f:
            doc = f.read()
        feat = extract_features(doc)
        train_data.append((feat, "non_suitable"))

    print "Training data loaded"
    return train_data

def print_accuracy(classifier, test_set):
    print(nltk.classify.accuracy(classifier, test_set))

def load_demo(classifier, sentilyzer, s):
    """
    A function to demo the classifier
    """
    print "Loading demo...."
    time.sleep(1)
    while 1:
        print "Enter news article's text or press 'q' to quit:"
        text = raw_input()
        if text == "q":
            return

        print "Category:", predict(classifier, text)
        print "Sentiment: %s" % sentilyzer.classify(extract_features(text))
        summary = s.get_summary(text, k=5)
        read_score = get_readability(summary)
        print "Summary:",summary
        print "\n"
        print "Readability:", read_score
        print "\n\n"

def get_sn_classifier():
    """
    returns the classifier for
    suitable / non-suitable
    """
    
    train_data = load_train_data()
    sentilyzer = get_sentilyzer()
    classifier = train(train_data)
    print_accuracy(classifier, train_data)
    return classifier

def main():
    # _test()
    sn_classifier = get_sn_classifier()
    sentilyzer = get_sentilyzer()
    s = Summary()
    load_demo(sn_classifier, sentilyzer, s)


stem = nltk.PorterStemmer().stem
stop_words = load_stopwords()
neg_words = load_neg_words()
spache_words = load_spache_words()

if __name__ == '__main__':
    main()
