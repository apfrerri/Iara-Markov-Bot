import os, re, json, random
from collections import defaultdict

class Chatbot:
    def __init__(self):
        self.start_key = "<start>"
        self.stop_key = "<response>"

    def train_data(self, data, data_markov):
        outputs = []
        new_data = self.tree()
        num = 0

        for key in range(0, len(data), 2):
            self.add(new_data, re.sub("\\W+", " ", data[key].lower()).split() + [self.stop_key, str(num)])
            outputs.append(data[key + 1])
            num += 1

        self.database = json.loads(json.dumps(new_data))
        self.response_data = outputs
        self.markov_chain = self.new_chain(data_markov)

        #print(json.dumps(self.database, indent=4))

    def get_answer(self, inp=""):
        if not inp:
            return None
        
        not_answer = self.generate_text(inp)
        inp = re.sub("\\W+", " ", inp.lower()).split()

        if not inp:
            return None
        
        path = self.database.get(inp[0], {})

        if not path or not inp:
            return None
        
        num = 1
        while not path.get(self.stop_key) and not num >= len(inp) or not num >= len(inp):
            if path.keys():
                path = path.get(inp[num % len(inp)], path[random.choice(list(path.keys()))])
                num += 1
            else:
                break
        
        if path.get(self.stop_key):
            return self.response_data[int(random.choice(list(path.get(self.stop_key).keys())))]
        else:
            return None
    
    def get_answer_with_return(self, inp=""):
        if not inp:
            return self.generate_text()
        
        not_answer = self.generate_text(inp)
        inp = re.sub("\\W+", " ", inp.lower()).split()

        if not inp:
            return not_answer
        
        path = self.database.get(inp[0], {})

        if not path or not inp:
            return not_answer
        
        num = 1
        while not path.get(self.stop_key) and not num >= len(inp) or not num >= len(inp):
            if path.keys():
                path = path.get(inp[num % len(inp)], path[random.choice(list(path.keys()))])
                num += 1
            else:
                break
        
        if path.get(self.stop_key):
            return self.response_data[int(random.choice(list(path.get(self.stop_key).keys())))]
        else:
            return not_answer
        
    def new_chain(self, data):
        new_data = {}

        for phrase in data:
            phrase = [self.start_key] + phrase.split() + [0]

            for key in range(0, len(phrase) - 1):
                if not new_data.get(phrase[key]):
                    new_data[phrase[key]] = [phrase[key + 1]]
                else:
                    new_data[phrase[key]].append(phrase[key + 1])
        
        return new_data
    
    def generate_text(self, base_text=""):
        if base_text:
            words = []
            for word in base_text.split():
                if self.markov_chain.get(word):
                    words.append(word)
            
            if words:
                start = random.choice(words)
            else:
                start = self.start_key
        else:
            start = self.start_key

        answer = [start, random.choice(self.markov_chain.get(start))]

        while answer[-1]:
            answer.append(random.choice(self.markov_chain.get(answer[-1])))
        
        return re.sub(self.start_key, "", " ".join(answer[:-1]))

    def tree(self):
        return defaultdict(self.tree)
    
    def add(self, t, path):
        for node in path:
            t = t[node]
