import requests
import re

URL = "http://127.0.0.1:8000/query"

def load_npl_tests():
    queries = open("npl/query", "rb")
    queries = str(queries.read().decode("UTF-8", "ignore"))
    queries = queries.split("/")[:-1]
    new_queries = {}
    for q in queries:
        new_q = [t for t in q.split("\n") if t != '']
        new_queries[new_q[0]] = new_q[1]
    
    responses = open("npl/response", "rb")
    responses = str(responses.read().decode("UTF-8", "ignore"))
    responses = responses.split("/")[:-1]
    new_responses = {}
    for r in responses:
        new_r = " ".join(r.split("\n"))
        new_r = [t for t in new_r.split(" ") if t != '']
        new_responses[new_r[0]] = new_r[:-1]
    
    return new_queries, new_responses

def load_lisa_tests():
    queries = open("lisa/query", "rb")
    queries = str(queries.read().decode("UTF-8", "ignore"))
    queries = queries.split("#")[:-1]
    new_queries = {}
    for q in queries:
        new_q = " ".join(q.split("\n"))
        new_q = [t.strip() for t in new_q.split("\r")]
        new_q = [t for t in new_q if t != ""]
        new_queries[new_q[0]] = " ".join(new_q[1:])
   

    responses = open("lisa/response", "rb")
    responses = str(responses.read().decode("UTF-8", "ignore"))
    responses = responses.split("Query")[1:]
    new_responses = {}
    for r in responses:
        new_r = r.split("\n")
        while(new_r[-1] == ""):
            new_r = new_r[:-1]
        _id = new_r[0].replace("\r", "").strip()
        nums = [arr.replace("\r", "").replace("-1", "").strip() for arr in new_r[2:]]
        nums = " ".join([t for t in nums if t != ""])
        nums = nums.split(" ")
        
        new_responses[_id] = nums
    
    return new_queries, new_responses

def load_tests(choosed):
    if(choosed == "npl"):
        return load_npl_tests()
    elif(choosed == "lisa"):
        return load_lisa_tests()

    return None, None


def f_measure(precision, recall):
    beta = 0.5
    return (1 + (beta**2)) / ((1 / precision) + (beta**2 / recall))

def f1_measure(precision, recall):
    return (2) / ((1 / precision) + (1 / recall))

def init():
    doc_collections = ["lisa", "npl"]
    print("Choose one:")
    for index, doc_collection in enumerate(doc_collections):
        print(index, doc_collection)

    try:
        a = int(input())
        choosed = doc_collections[a]
    except:
        choosed = doc_collections[0]

    print(f"Collection choosed: {choosed}")

    queries, responses = load_tests(choosed)
    if(queries is None or responses is None):
        raise Exception("Wrong test")


    sum_precision = 0
    sum_recall = 0
    sum_f = 0
    sum_f1 = 0
    cant = 0
    for q in queries:
        if(responses.__contains__(q) == False):
            continue

        ids = []
        request = requests.get(url = URL + "?value=" + queries[q])
        data = request.json()
        count = 0
        for doc in data:
            ids.append([num for num in re.findall('[0-9]*', doc["text"].split("\n")[0]) if num != ""][0])
            
        for _id in ids:
            if(_id in responses[q]):
                count += 1

        # relevants
        REL = len(responses[q])
        # retrieved
        RET = len(data)
        # relevants retireved
        RR = count

        if(len(data) > 0):
            precision = RR / RET
            sum_precision += precision

            recall = RR / REL
            sum_recall += recall

            if(precision != 0 and recall != 0):
                sum_f += f_measure(precision, recall)
                sum_f1 += f1_measure(precision, recall)

        cant += 1

    print(f"Tests: {cant}")
    print(f"Precision average: {sum_precision / cant}")
    print(f"Recall average :{sum_recall / cant}")
    print(f"F measure average: {sum_f / cant}")
    print(f"F1 measure average: {sum_f1 / cant}")
    print()

init()
