import json
import urllib.request
import urllib


def main():
    model_name = 'BM25'
    count = 1

    with open('test_queries.txt', encoding="utf-8") as inputfile:
        for line in inputfile:
            query = line.strip('\n').replace(':', '')
            query = urllib.parse.quote(query)
            inurl = 'http://localhost:8983/solr/' + model_name + '/select?fl=id%2Cscore&q=text_en%3A(' + query + \
                    ')%20or%20text_de%3A(' + query + ')%20or%20text_ru%3A(' + query + ')' + '&rows=20&wt=json'
            qid = str(count).zfill(3)

            outf = open(str(count) + '.txt', 'a+')
            data = urllib.request.urlopen(inurl).read()
            docs = json.loads(data.decode('utf-8'))['response']['docs']
            rank = 1

            for doc in docs:
                outf.write(str(qid) + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                    doc['score']) + ' ' + model_name + '\n')
                rank += 1
            outf.close()
            count += 1


if __name__ == '__main__':
    main()
