import copy
import sys
import re


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def set_next(self, new_next):
        self.next_node = new_next

    def get_data(self):
        return self.data


class LinkedList:
    def __init__(self):
        self.head = None

    def printList(self):
        temp = self.head
        doclist = []
        try:
            while temp is not None:
                d = temp.data
                doclist.append(d['docID'])
                temp = temp.next
            return doclist
        except Exception as e:
            print(e)

    '''def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            currdict = current.get_data()
            nextdict = data

            while (current.next is not None and
                   int(nextdict['docID']) > int(currdict['docID'])):
                current = current.next

            new_node.next = current.next
            current.next = new_node'''
    def insert(self,data):
        current = self.head
        if current is None:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
            self.size = 1
            return True
        if current.data['docID'] > data['docID']:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return True
        while current.next is not None:
            if current.next.data['docID'] > data['docID']:
                break
            current = current.next
        new_node = Node(data)
        new_node.next = current.next
        current.next = new_node
        return True

    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
            if current.data == data:
                found = True
            else:
                current = current.next
        if current is None:
            raise ValueError("Data not in list")
        return current


def Remove(duplicate):
    final_list = []
    tf_list = {}
    for num in duplicate:
        key = num
        tf_list[key] = duplicate.count(num)
        if num not in final_list:
            final_list.append(num)
    return final_list, tf_list


def read_data():
    #filepath = '/Users/sriparnachakraborty/Desktop/IR/Project2_Dryrun_Corpus.txt'
    filepath = sys.argv[1]
    input_file = open(filepath, 'r+')
    str_dict = {}
    for line in input_file:
        line = line.replace('\t',' ').replace('\n','')
        arr = line.split(" ")
        key = arr[0]
        str_dict[key] = arr[1:]
    return str_dict


def create_inverted_index():
    str_dict = read_data()
    term_dict = {}
    for key in str_dict.keys():
        token_list = str_dict[key]
        token_list_trimmed, tf_dict = Remove(token_list)

        for token in token_list_trimmed:
            term_pair_dict = {'doc_freq': 0, 'postings': LinkedList()}
            tmp = {'docID': 0, 'term_freq': 0}
            if token not in term_dict:
                term_pair_dict['doc_freq'] = 1
                tmp['docID'] = key
                tmp['term_freq'] = tf_dict[token]
                docID_dict = tmp
                term_pair_dict['postings'].insert(docID_dict)
                term_dict[token] = term_pair_dict
            else:

                temp = term_dict[token]
                temp['doc_freq'] += 1
                tmp['docID'] = key
                tmp['term_freq'] = tf_dict[token]
                docID_dict = tmp
                temp['postings'].insert(docID_dict)
                term_dict[token] = temp

    return term_dict


'''method retrieves the postings lists for each of the given query terms. 
Input of this method will be a set of terms: term0, term1,..., termN. It should output the postings for each term in the following format:'''


def GetPostings(query):
    try:
        collection_list = []
        token_query = query.split(" ")
        inverted_index = create_inverted_index()
        for i in range(0, len(token_query)):
            token_query[i] = token_query[i].replace(' ', '')
            write_file("GetPostings")
            write_file(token_query[i])
            postings = inverted_index[token_query[i]]
            postingslist = postings['postings']
            doclist = postingslist.printList()
            plist = ''
            for item in doclist:
                plist += str(item) + ' '
            write_file('Postings list: ' + plist)
            collection_list.append(doclist)
        return collection_list
    except KeyError:
        write_file('ERROR: No term found in the document')
    except Exception as e:
        write_file(e)


'''function to implement multi-term boolean AND query on the index using document-at-a-time (DAAT) strategy.
Input of the function will be a set of query terms: term0, term1, ..., termN'''


def DaatAnd(query, compare_count):
    try:
        query_dict = create_inverted_index()
        query_token_list = query.split(" ")
        query_list = []
        for i in range(0, len(query_token_list)):
            token_query = query_token_list[i].replace(' ', '')
            if token_query in query_dict.keys():
                query_list.append(query_dict[token_query])

        query_list = sort(query_list)

        intersect_list = None
        single_list = []
        if (len(query_list)) == 1:
            # intersect_list, cc = intersection(intersect_list, query_list[i], compare_count)
            write_file('DaatAnd')
            write_file(query_token_list[0])
            single_dict = query_list[0]['postings']
            p = single_dict.head
            while p:
                single_list.append(p.data['docID'])
                p = p.next
            single_str = ''
            for item in single_list:
                single_str = single_str + ' ' + item
            write_file('Results: ' + single_str)
            write_file('Number of documents in results: ' + str(len(single_list)))
            write_file('Number of comparisons: 0')
            return single_list
        count = 0
        for i in range(1, len(query_list)):
            if intersect_list:
                intersect_list, compare_count = intersection(intersect_list, query_list[i], compare_count)

            else:
                intersect_list, compare_count = intersection(query_list[i - 1], query_list[i], compare_count)
            count = compare_count
        final_list = intersect_list['postings'].printList()
        if len(final_list) == 0:
            write_file('DaatAnd')
            out_str = ''
            for item in query_token_list:
                out_str = out_str + item + ' '
            write_file(out_str)
            write_file('Results: empty')
            write_file('Number of documents in results: ' + str(len(final_list)))
            write_file('Number of comparisons: ' + str(compare_count))
        else:
            write_file('DaatAnd')
            out_str = ''
            for item in query_token_list:
                out_str = out_str + item + ' '
            write_file(out_str)
            results = ''
            for item in final_list:
                results = results + item + ' '
            write_file('Results: ' + results)
            write_file('Number of documents in results: ' + str(len(final_list)))
            write_file('Number of comparisons: ' + str(count))
        return final_list
    except Exception as e:
        write_file(e)


def intersection(p1_list, p2_list, compare_count):
    intersect_list = LinkedList()
    intersect_dict = {}
    pl1 = copy.deepcopy(p1_list['postings'])
    pl2 = copy.deepcopy(p2_list['postings'])
    if pl1 is not None and pl2 is not None:
        p1 = pl1.head
        p2 = pl2.head
        while p1 and p2:
            if p1.data['docID'] == p2.data['docID']:
                intersect_list.insert(p1.data)
                compare_count += 1
                p1 = p1.next
                p2 = p2.next
            elif p1.data['docID'] < p2.data['docID']:
                compare_count += 1
                p1 = p1.next
            else:
                compare_count += 1
                p2 = p2.next
    intersect_dict['postings'] = intersect_list
    return intersect_dict, compare_count


'function is used to implement multi-term boolean OR query on the index using DAAT. ' \
'Input of this function will be a set of query terms: term0, term1, ..., termN'


def DaatOR(query, compare_count):
    try:
        query_dict = create_inverted_index()
        query_token_list = query.split(" ")
        query_list = []
        for i in range(0, len(query_token_list)):
            token_query = query_token_list[i].replace(' ', '')
            if token_query in query_dict.keys():
                query_list.append(query_dict[token_query])

        query_list = sort(query_list)

        union_list = None
        single_list = []
        if (len(query_list)) == 1:
            write_file('DaatOR')
            write_file(query_token_list[0])
            single_dict = query_list[0]['postings']
            p = single_dict.head
            while p:
                single_list.append(p.data['docID'])
                p = p.next
            single_str = ''
            for item in single_list:
                single_str = single_str + ' ' + item
            write_file('Results: ' + single_str)
            write_file('Number of documents in results: ' + str(len(single_list)))
            write_file('Number of comparisons: 0')
            return single_list
        count = 0
        for i in range(1, len(query_list)):
            if union_list:
                union_list, compare_count = union(union_list, query_list[i], compare_count)

            else:
                union_list, compare_count = union(query_list[i - 1], query_list[i], compare_count)
            count = compare_count
        final_list = union_list['postings'].printList()
        if len(final_list) == 0:
            write_file('DaatOr')
            out_str = ''
            for item in query_token_list:
                out_str = out_str + item + ' '
            write_file(out_str)
            write_file('Results: empty')
            write_file('Number of documents in results: ' + str(len(final_list)))
            write_file('Number of comparisons: ' + str(compare_count))
        else:
            write_file('DaatOr')
            out_str = ''
            for item in query_token_list:
                out_str = out_str + item + ' '
            write_file(out_str)
            results = ''
            for item in final_list:
                results = results + item + ' '
            write_file('Results: ' + results)
            write_file('Number of documents in results: ' + str(len(final_list)))
            write_file('Number of comparisons: ' + str(count))
        return final_list
    except Exception as e:
        write_file(e)


def union(p1_list, p2_list, compare_count):
    union_list = LinkedList()
    union_dict = {}
    pl1 = copy.deepcopy(p1_list['postings'])

    pl2 = copy.deepcopy(p2_list['postings'])
    if pl1 is not None and pl2 is not None:
        p1 = pl1.head
        p2 = pl2.head
        while p1 and p2:
            if p1.data['docID'] == p2.data['docID']:
                union_list.insert(p1.data)
                compare_count += 1
                p1 = p1.next
                p2 = p2.next
            elif p1.data['docID'] < p2.data['docID']:
                union_list.insert(p1.data)
                compare_count += 1
                p1 = p1.next
            else:
                union_list.insert(p2.data)
                compare_count += 1
                p2 = p2.next
    elif pl1 is not None and pl2 is None:
        p1 = pl1.head
        while p1:
            union_list.insert(p1.data)
            p1 = p1.next
    else:
        p2 = pl2.head
        while p2:
            union_list.insert(p2.data)
            p2 = p2.next
    if p1 and not p2:
        while p1:
            union_list.insert(p1.data)
            p1 = p1.next
    else:
        while p2:
            union_list.insert(p2.data)
            p2 = p2.next

    union_dict['postings'] = union_list
    return union_dict, compare_count


def TF_IDF_Ranking(query, daat_list):
    query_dict = create_inverted_index()
    query_token_list = query.split(" ")
    doc_dict = read_data()
    query_idf_dict = {}
    rank_docid_dict = {}
    rank_list = []
    total_no_docs = len(doc_dict.keys())
    for query_term in query_token_list:
        query_term = query_term.replace(' ', '')
        query_term_dict = query_dict[query_term]
        query_term_postings = query_term_dict['postings']
        doc_freq = query_term_dict['doc_freq']
        idf = total_no_docs / doc_freq
        query_idf_dict[query_term] = idf
        if query_term_postings is not None:
            q1 = query_term_postings.head
            while q1:
                doc_id = q1.data['docID']
                total_terms = len(doc_dict[doc_id])
                term_freq = int(q1.data['term_freq'])

                net_term_freq = term_freq / total_terms
                q1.data['term_freq'] = net_term_freq
                q1 = q1.next
    for docid in daat_list:
        if docid in doc_dict.keys():
            rank_sum = 0.0
            for term in doc_dict[docid]:
                tf_idf = 0.0
                if term in query_token_list and term in query_dict.keys():
                    term_obj = query_dict[term]
                    posting_list = term_obj['postings']
                    p = posting_list.head
                    while p:
                        if p.data['docID'] == docid:
                            term_node = p
                            break
                        else:
                            p = p.next
                    tf = term_node.data['term_freq']
                    idf = query_idf_dict[term]
                    tf_idf = tf * idf
                    rank_sum = float(rank_sum) + float(tf_idf)
        rank_docid_dict[docid] = float(rank_sum)
    final_rank_list = []
    sorted_list = sorted(rank_docid_dict.items(), key=lambda kv: kv[1], reverse=True)
    for item in sorted_list:
        final_rank_list.append(item[0])
    write_file('TF-IDF')
    ranked_doc = ''
    for item in final_rank_list:
        ranked_doc = ranked_doc + ' ' + item
    if ranked_doc == '':
        write_file('Results: empty')
    else:
        write_file('Results:' + ranked_doc)


def sort(input_list):
    temp_list = copy.deepcopy(input_list)

    for i in range(0, len(temp_list)):
        for j in range(0, len(temp_list) - i - 1):
            if temp_list[j]['doc_freq'] > temp_list[j + 1]['doc_freq']:
                temp_list[j]['doc_freq'], temp_list[j + 1]['doc_freq'] = \
                    temp_list[j + 1]['doc_freq'], temp_list[j]['doc_freq']
    return temp_list


def write_file(input_str):
    #outfilepath = '/Users/sriparnachakraborty/Desktop/IR/Output.txt'
    outfilepath = sys.argv[2]
    with open(outfilepath, 'a') as f1:
        if f1:
            f1.writelines(input_str + '\n')


def main():
    #inputfile = '/Users/sriparnachakraborty/Desktop/IR/input.txt'
    inputfile = sys.argv[3]
    query_file = open(inputfile, 'r+')
    for query in query_file:
        query = query.replace('\t', ' ').replace('\n', '')
        GetPostings(query)
        AND_list = DaatAnd(query, 0)
        TF_IDF_Ranking(query, AND_list)
        OR_list = DaatOR(query, 0)
        TF_IDF_Ranking(query, OR_list)
        write_file('')
    query_file.close()


if __name__ == '__main__':
    main()
