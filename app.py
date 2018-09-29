import os
import sys
import nltk
nltk.download('punkt')

from flask import * 
from summarizer import Summary
import parser
import classifier


app = Flask(__name__)# application object created or constructor

reload(sys)
sys.setdefaultencoding("utf-8")

# GLOBAL VARIABLES
s = Summary()
I = 0.3 # threshold for sentiment
J = 0.5 # threshold for readability
K = 0.5 # summary lenght
sentilyzer = classifier.get_sentilyzer() # classifier for getting sentiment
sn_classifier = classifier.get_sn_classifier() # classifier for suitable / non-suitable
# GLOBAL ends

def set_params():
    """
    set the three sliders values
    """
    global I, J, K
    try:
        I = float(request.args["I"])
        J = float(request.args["J"])
        K = float(request.args["K"])
    except:
        pass

def get_res(db):
    
    res = []
    for url in db:
        title, text = db[url]
        if classifier.predict(sn_classifier, text) == "suitable":
            # only if it is suitable
            pos_sents = []
            sents = nltk.sent_tokenize(text)
            for sent in sents:
                # select the sentences with positive sentiments
                feat = classifier.extract_features(sent)
                out = sentilyzer.prob_classify(feat)
                if out.prob('pos') >= I:
                    pos_sents.append(sent)

            if len(pos_sents) == 0:
                # ignore the news if there are no positive sentences
                continue
            pos_text = " ".join(pos_sents)

            summ_text = s.get_summary(pos_text, k=int(K * len(sents)) + 1)

            read_score = classifier.get_readability(summ_text)
            if read_score >= J:
                res.append((title, summ_text))
    return res

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/latest")
def latest():
    set_params()
    db = parser.get_db()
    res = get_res(db["latest"])
    return render_template("latest.html", res=res, I=I, J=J, K=K)

@app.route("/world")
def world():
    set_params()
    db = parser.get_db()
    res = get_res(db["world"])
    return render_template("world.html", res=res, I=I, J=J, K=K)
@app.route("/uk")
def uk():
    set_params()
    db = parser.get_db()
    res = get_res(db["uk"])
    return render_template("uk.html", res=res, I=I, J=J, K=K)

@app.route("/africa")
def africa():
    set_params()
    db = parser.get_db()
    res = get_res(db["africa"])
    return render_template("africa.html", res=res, I=I, J=J, K=K)

@app.route("/ent")
def ent():
    set_params()
    db = parser.get_db()
    res = get_res(db["ent"])
    return render_template("ent.html", res=res, I=I, J=J, K=K)

@app.route("/sci")
def sci():
    set_params()
    db = parser.get_db()
    res = get_res(db["sci"])
    return render_template("sci.html", res=res, I=I, J=J, K=K)

@app.route("/nature")
def nature():
    set_params()
    db = parser.get_db()
    res = get_res(db["nature"])
    return render_template("nature.html", res=res, I=I, J=J, K=K)

@app.route("/tech")
def tech():
    set_params()
    db = parser.get_db()
    res = get_res(db["tech"])
    return render_template("tech.html", res=res, I=I, J=J, K=K)

@app.route("/allsports")
def allsports():
    set_params()
    db = parser.get_db()
    res = get_res(db["allsports"])
    return render_template("allsports.html", res=res, I=I, J=J, K=K)

@app.route("/football")
def football():
    set_params()
    db = parser.get_db()
    res = get_res(db["football"])
    return render_template("football.html", res=res, I=I, J=J, K=K)

@app.route("/tennis")
def tennis():
    set_params()
    db = parser.get_db()
    res = get_res(db["tennis"])
    return render_template("tennis.html", res=res, I=I, J=J, K=K)

@app.route("/info")
def info():
    set_params()
    db = parser.get_db()
    res = get_res(db["info"])
    return render_template("info.html")

def questionaire():
    return render_template("questionaire.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port, debug=False)
