let sample_articles = [
    {
        "id": "1111.6201",
        "authors": "Yi-Hao Kao and Benjamin Van Roy",
        "abstract": "  We consider the problem of learning a linear factor model. We propose a\nregularized form of principal component analysis (PCA) and demonstrate through\nexperiments with synthetic and real data the superiority of resulting estimates\nto those produced by pre-existing factor analysis approaches. We also establish\ntheoretical results that explain how our algorithm corrects the biases induced\nby conventional approaches. An important feature of our algorithm is that its\ncomputational requirements are similar to those of PCA, which enjoys wide use\nin large part due to its efficiency.\n",
        "categories": "cs.LG,stat.ML",
        "pk": "01GGJASA6X2ZFRSB21116PG4H7",
        "year": "2013",
        "title": "Learning a Factor Model via Regularized PCA"
    },
    {
        "id": "1204.1564",
        "authors": "Paulo F. C. Tilles and Jose F. Fontanari",
        "abstract": "An explanation for the acquisition of word-object mappings is the associative\nlearning in a cross-situational scenario. Here we present analytical results of\nthe performance of a simple associative learning algorithm for acquiring a\none-to-one mapping between $N$ objects and $N$ words based solely on the\nco-occurrence between objects and words. In particular, a learning trial in our\nlearning scenario consists of the presentation of $C + 1 < N$ objects together\nwith a target word, which refers to one of the objects in the context. We find\nthat the learning times are distributed exponentially and the learning rates\nare given by $\\ln{[\\frac{N(N-1)}{C + (N-1)^{2}}]}$ in the case the $N$ target\nwords are sampled randomly and by $\\frac{1}{N} \\ln [\\frac{N-1}{C}] $ in the\ncase they follow a deterministic presentation sequence. This learning\nperformance is much superior to those exhibited by humans and more realistic\nlearning algorithms in cross-situational experiments. We show that introduction\nof discrimination limitations using Weber\"s law and forgetting reduce the\nperformance of the associative algorithm to the human level.\n",
        "categories": "q-bio.NC,cs.LG",
        "pk": "01GGJASA71SSAEH2GFW67B4XK2",
        "year": "2012",
        "title": "Minimal model of associative learning for cross-situational lexicon\n  acquisition"
    },
    {
        "id": "1203.2507",
        "authors": "Dong Dai, Philippe Rigollet, Tong Zhang",
        "abstract": "  Given a finite family of functions, the goal of model selection aggregation\nis to construct a procedure that mimics the function from this family that is\nthe closest to an unknown regression function. More precisely, we consider a\ngeneral regression model with fixed design and measure the distance between\nfunctions by the mean squared error at the design points. While procedures\nbased on exponential weights are known to solve the problem of model selection\naggregation in expectation, they are, surprisingly, sub-optimal in deviation.\nWe propose a new formulation called Q-aggregation that addresses this\nlimitation; namely, its solution leads to sharp oracle inequalities that are\noptimal in a minimax sense. Moreover, based on the new formulation, we design\ngreedy Q-aggregation procedures that produce sparse aggregation models\nachieving the optimal rate. The convergence and performance of these greedy\nprocedures are illustrated and compared with other standard methods on\nsimulated examples.\n",
        "categories": "math.ST,cs.LG,stat.ML,stat.TH",
        "pk": "01GGJASA70F4056V1FN28TVR0Z",
        "year": "2012",
        "title": "Deviation optimal learning using greedy Q-aggregation"
    },
    {
        "id": "0705.4485",
        "authors": "Edoardo M Airoldi, David M Blei, Stephen E Fienberg, Eric P Xing",
        "abstract": "  Observations consisting of measurements on relationships for pairs of objects\narise in many settings, such as protein interaction and gene regulatory\nnetworks, collections of author-recipient email, and social networks. Analyzing\nsuch data with probabilisic models can be delicate because the simple\nexchangeability assumptions underlying many boilerplate models no longer hold.\nIn this paper, we describe a latent variable model of such data called the\nmixed membership stochastic blockmodel. This model extends blockmodels for\nrelational data to ones which capture mixed membership latent relational\nstructure, thus providing an object-specific low-dimensional representation. We\ndevelop a general variational inference algorithm for fast approximate\nposterior inference. We explore applications to social and protein interaction\nnetworks.\n",
        "categories": "stat.ME,cs.LG,math.ST,physics.soc-ph,stat.ML,stat.TH",
        "pk": "01GGJASA6CBZRHQQEA3WKE636M",
        "year": "2014",
        "title": "Mixed membership stochastic blockmodels"
    }
]
class CircularBuffer {
    /*
    * A circular buffer that stores the last N elements.
    * When the buffer is full, the oldest element is overwritten.
    * 
    * methods: push, resize
    */
    constructor(size) {
        this.size = Number((size <= 0 || isNaN(size)) ? 1 : size);
        this.buffer = [];
        this.index = Number(0);
    }

    push(element) {
        if (this.buffer.length < this.size) {
            this.buffer.push(element);
        } else {
            this.buffer[this.index] = element;
        }
        this.index = Number((this.index + 1) % this.size);
    }

    resize(size) {
        // if size <= 0 or is not a number, do nothing
        if (size <= 0 || isNaN(size)) {
            return;
        }
        size = Number(size);
        let right = this.buffer.slice(
            Math.max(this.buffer.length - size + this.index, this.index), this.buffer.length
        )
        let left = this.buffer.slice(
            Math.max(this.index - size, 0), this.index
        )
        this.buffer = right.concat(left);
        this.index = Number(size > this.size ? this.size : 0);
        this.size = size;
    }

    to_string() {
        return this.buffer.slice(this.index, this.buffer.length).concat(this.buffer.slice(0, this.index)).join("");
    }
}

let buffer = new CircularBuffer(1);

chrome.storage.local.get({
    text_send_depth: "100",
}, (result) => {
    buffer.resize(result.text_send_depth);
});

class RecommandationService {
    constructor(text_buffer, text_trigger_depth, recommendation_service_url, recommendation_service_token) {
        this.text_buffer = text_buffer;
        this.nwords = 0;
        this.last_input = " ";
        this.text_trigger_depth = text_trigger_depth;
        this.recommendation_service_url = recommendation_service_url;
        this.recommendation_service_token = recommendation_service_token;
    }

    message_handler(request, sender, sendResponse) {
        if (request.key === undefined) {
            return;
        }
        let key = request.key.replace("Tab", "\t").replace("Enter", "\n").replace("Space", " ");
        if (key.match(/^.$/) === null && key.match(/^[ \t\n]$/) === null) {
            return;
        }
        buffer.push(key);
        let last_input = this.last_input;
        this.last_input = key;
        if (key.match(/^[ \n\t]$/) === null || last_input.match(/^[ \n\t]$/) !== null) {
            return;
        }
        this.nwords += 1;
        if (this.nwords < this.text_trigger_depth) {
            return;
        }
        this.nwords = 0;
        let url = encodeURI(this.recommendation_service_url);
        let body = JSON.stringify({
            "text": buffer.to_string()
        })
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'token ' + this.recommendation_service_token
        };
        fetch(
            url,
            {
                method: "POST",
                mode: 'cors',
                headers: headers,
                body: body
            }
        ).then((response) => {
            // get papers from response
            console.log(response);
            return response.json();
        }).then((data) => {
            console.log(data);
            for (let article of data["papers"]) {
                let notificationId = article.id;
                let options = {
                    type: "basic",
                    title: "Article that could interest you",
                    message: `${article.title}, written by ${article.authors}`,
                    iconUrl: "favicon.ico",
                    silent: true,
                };
    
                // update the notification if it already exists, otherwise create it
                chrome.notifications.update(notificationId, options, (wasUpdated) => {
                    if (!wasUpdated) {
                        chrome.notifications.create(notificationId, options, () => {
                            console.log("Notification created for article " + article.title);
                        });
                    } else {
                        console.log("Notification updated for article " + article.title);
                    }
                });
            } 
        });
    }
}

let recommandation_service = new RecommandationService(buffer, 10, 100, undefined);

chrome.storage.local.get({
    text_trigger_depth: "10",
    recommendation_service_url: "http://localhost:8080",
    recommendation_service_token: "token",
}, (result) => {
    console.log(result);
    recommandation_service.text_trigger_depth = result.text_trigger_depth;
    recommandation_service.recommendation_service_url = result.recommendation_service_url;
    recommandation_service.recommendation_service_token = result.recommendation_service_token;
});

chrome.runtime.onMessage.addListener(recommandation_service.message_handler.bind(recommandation_service));

// add notification click listener to open the article in a new tab
chrome.notifications.onClicked.addListener((notificationId) => {
    chrome.notifications.clear(notificationId);
    chrome.tabs.create({url: "https://arxiv.org/abs/" + notificationId});
});


// add storage change listener to resize buffer
chrome.storage.onChanged.addListener((changes, namespace) => {
    for (key in changes) {
        switch (key) {
            case "text_send_depth":
                buffer.resize(changes[key].newValue);
                break;
            case "text_trigger_depth":
                recommandation_service.text_trigger_depth = changes[key].newValue;
                break;
            case "recommendation_service_url":
                recommandation_service.recommendation_service_url = changes[key].newValue;
                break;
            case "recommendation_service_token":
                recommandation_service.recommendation_service_token = changes[key].newValue;
                break;
            default:
                break;
        }
    }
});