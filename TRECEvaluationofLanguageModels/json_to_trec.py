# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should
import urllib.request
import urllib
import re
import string

# import urllib2

core_list = ['BM25', 'DFR', 'LanguageModel']


def manipulate_string(s):
    whitelist = string.ascii_letters + string.digits + ' '
    new_s = ''
    for char in s:
        if char in whitelist:
            new_s += char
        else:
            new_s += ' '
    return new_s


def main():
    for core_name in core_list:
        # change the url according to your own core name and query
        outfn = '/Users/sriparnachakraborty/Desktop/IR_project/Project3/JSON to TREC/' + core_name + '.txt'
        outf = open(outfn, 'a+')
        # inputfile = open('queries.txt', "r")
        counter = 0

        with open('queries.txt', encoding="utf-8") as inputfile:
            for query in inputfile:
                counter += 1
                in_query = query[4:]
                in_query = in_query.strip('\n').replace(':', '')
                print(in_query)
                encoded_query = urllib.parse.quote(in_query)
                inurl = 'http://localhost:8983/solr/' + core_name + '/select?fl=id%2Cscore&q=text_en%3A(' + encoded_query + ')%20or%20text_de%3A(' + encoded_query + ')%20or%20' \
                                                                                                                                                                     'text_ru%3A(' + encoded_query + ')' + '&rows=20&wt=json'
                print(inurl)

                # if you're using python 3, you should use
                data = urllib.request.urlopen(inurl)

                docs = json.load(data)['response']['docs']
                # change query id and IRModel name accordingly
                if counter < 10:
                    qid = '00' + str(counter)
                elif counter > 100:
                    qid = str(counter)
                else:
                    qid = '0' + str(counter)
                # the ranking should start from 1 and increase
                rank = 1
                for doc in docs:
                    outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                        doc['score']) + ' ' + core_name + '\n')
                    rank += 1
            inputfile.close()
            outf.close()


if __name__ == '__main__':
    main()
