def text_prepare(text):
    #https://cloud.yandex.ru/docs/speechkit/concepts/limits#speechkit-limits

    max_length = 4900

    sentences = text.split('.')
    text_reqest = []

    sentences_count = len(sentences)
    index_correct = 0
    for sentence_index in range(0, sentences_count):
        print(index_correct, sentence_index)
        index_summ = sentence_index+index_correct
        sentence = sentences[index_summ].strip(' \n\r\n')
        if len(sentence) >= max_length:
            for sub in sentence.split(','):
                sub = sentence_prepare(sub)
                if sub:
                    text_reqest.append(sub)
        else:
            try:
                sub_sentence = sentences[index_summ+1]
            except Exception as e:
                sub_sentence = sentences[index_summ]
            if len(sentence + sub_sentence) < max_length:
                sentence = sentence + '.' + sub_sentence + '.'
                sub = sentence_prepare(sentence)
                if sub:
                    text_reqest.append(sub)
                index_correct += 1
            else:
                text_reqest.append(sentence+'.')
        print('after', index_correct, sentence_index, sentences_count)
        if sentence_index + index_correct >= sentences_count-1:
            break
    print(text_reqest)
    return text_reqest

def sentence_prepare(sentence: str):
    if sentence not in ['', '\n', ' ']:
        return sentence
    else:
        return []
