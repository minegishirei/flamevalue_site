
import MeCab
import collections


def getMeishiList(text):
    #読み込んだtextファイルで形態素解析を行う
    tagger =MeCab.Tagger()
    tagger.parse('')
    node = tagger.parseToNode(text)

    #取り出す品詞を決めている.今回は名詞
    word_list=[]
    while node:
        word_type = node.feature.split(',')[0]
        #名詞の他にも動詞や形容詞なども追加できる
        if word_type in ["名詞"]:
            word_list.append(node.surface)
        node=node.next
    word_chain=' '.join(word_list)

    #collections.counterでword_list内に含まれている名詞をカウント
    c=collections.Counter(word_list)

    #printでよく使われている単語top20を出力
    list_dict = []
    for row in c.most_common():
        if row[1] == 1:
            continue
        list_dict.append({
            "word" : row[0],
            "count" : row[1]
        })
    return list_dict



