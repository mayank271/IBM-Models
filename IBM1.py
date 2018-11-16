"""
Implementation of IBM Model 1 and EM algorithm
"""


def not_converged(p_prob, curr_prob, h_words, e_words):
    """
    Method to check whether the values in the
    translation table have converged or not
    :param p_prob: Previous values in the translation table (dictionary)
    :param curr_prob: Current translation table (dictionary)
    :param h_words: Foreign language words (list)
    :param e_words: English language words (list)
    :return:
    """
    # First call of this function when the
    # previous table is empty
    if p_prob == {}:
        return 1
    val = 0
    for ew in e_words:
        for hw in h_words:
            t = (p_prob[ew][hw] - curr_prob[ew][hw])**2
            val += t

    val = val**0.5
    # Condition for convergence
    if val < 0.0005:
        return 0
    else:
        return 1


def get_alignments(sen1, sen2, prob):
    """
    Method to get the alignment given two sentences and the word
    to word translation probabilities
    :param sen1: List of words in sentence 1 in order
    :param sen2: List of words in sentence 2 in order
    :param prob: Probabilities of word to word translations
    :return: alignment for the translation of sentence 1 to sentence 2
    """
    alignment = []

    e = 0
    while e < len(sen1):
        # List of words in sen2 having max probability
        # for the current word in sen1
        al = []
        p_val = 0
        f = 0
        while f < len(sen2):
            if p_val < prob[sen1[e]][sen2[f]]:
                p_val = prob[sen1[e]][sen2[f]]
                al.clear()
                al.append(f)
            else:
                if p_val == prob[sen1[e]][sen2[f]]:
                    al.append(f)
            f += 1
        # Appending the tuples to the alignment list
        for f in al:
            alignment.append((e, f))

        e += 1

    return alignment


def run(flag):
    """
    :param flag: True if the texts need to be printed
    :return:
    """
    # Importing Data
    translations = []
    try:
        file = open("data\\hin.txt", 'r', encoding='utf-8')
        text = file.read()
        translations = text.split("\n")
    except:
        pass

    # Corpus maintains a list of 2 lists (english words list
    # and the corresponding foreign language words list) for
    # each sentence extracted from the dataset
    corpus = []
    # Unique english words in the dataset
    eng_words = []
    # Unique foreign language words in the dataset
    hin_words = []
    # List of sentence pairs of english and the foreign language
    sentence_pairs = []
    # Processing data
    for i in translations:
        s = i.split('\t')
        if len(s) < 2:
            pass
        else:
            sen = []
            eng = s[0]
            hin = s[1]
            sen.append(eng)
            sen.append(hin)
            sentence_pairs.append(sen)
            eng = eng.split('.')
            eng = eng[0].split('!')
            eng = eng[0].split(',')
            eng = eng[0].split('?')
            eng = eng[0].split(' ')
            hin = hin.split('?')
            hin = hin[0].split('!')
            hin = hin[0].split(',')
            hin = hin[0].split('।')
            hin = hin[0].split(' ')
            for h in hin:
                if h != '':
                    hin_words.append(h)
            hin_words = list(set(hin_words))
            for e in eng:
                if e != '':
                    eng_words.append(e)
            eng_words = list(set(eng_words))
            temp = []
            temp.append(eng)
            temp.append(hin)
            corpus.append(temp)

    # Initializing Translational Probabilities (Considering all possible alignments)
    t_prob = {}
    for eng in eng_words:
        t_prob[eng] = {hin: 1 / len(eng_words) for hin in hin_words}

    prev_prob = {}
    s_total = {}
    # Looping through this loop till the
    # probabilities do not converge
    while not_converged(prev_prob, t_prob, hin_words, eng_words):
        count = {}
        for eng in eng_words:
            count[eng] = {hin: 0 for hin in hin_words}

        total = {}
        for hin in hin_words:
            total[hin] = 0

        for pair in corpus:
            for e_word in pair[0]:
                s_total[e_word] = 0
                for h_word in pair[1]:
                    s_total[e_word] += t_prob[e_word][h_word]

            for e_word in pair[0]:
                for h_word in pair[1]:
                    count[e_word][h_word] += (t_prob[e_word][h_word]) / s_total[e_word]
                    total[h_word] += (t_prob[e_word][h_word]) / s_total[e_word]

        prev_prob = t_prob
        for hin in hin_words:
            for eng in eng_words:
                t_prob[eng][hin] = count[eng][hin] / total[hin]

    alignments = []

    for c in corpus:
        align = get_alignments(c[0], c[1], t_prob)
        alignments.append(align)

    if flag is True:
        i = 0
        while i < len(alignments):
            print('English Text : {}'.format(sentence_pairs[i][0]))
            print('Foreign Text : {}'.format(sentence_pairs[i][1]))
            print('Alignment : {}'.format(alignments[i]))
            print()
            i += 1

    return alignments


if __name__ == '__main__':
    run(flag=True)
