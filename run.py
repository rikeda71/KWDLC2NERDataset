from typing import List, Tuple
import tarfile
import logging
import re
import argparse


logging.basicConfig(level=logging.INFO)


def label_indexes_to_morphs(formatted_data: List[str]) \
        -> Tuple[List[str], List[str]]:
    """
    make label indexes of morphs and morphs list
    :param formatted_data: result of `regexp_and_formatting`
    :return ([morph, ...], [B-*** or I-*** or None, ...])
    """

    logging.info('search NE label indexes')
    morphs: list = []
    labels: list = [None] * len(formatted_data)
    for i, text in enumerate(formatted_data):
        if re.search(r'([A-Z]+)-(.+)', text):
            label, word = text.split('-')
            tmp = []
            cnt = i
            while cnt > 0:
                cnt -= 1
                if formatted_data[cnt].split(' ')[0] in word:
                    tmp.append(cnt)
                else:
                    break
            cnt = i
            while cnt < len(formatted_data):
                cnt += 1
                if formatted_data[cnt].split(' ')[0] in word:
                    tmp.append(cnt)
                else:
                    break
            tmp.sort()
            for i, b in enumerate(tmp):
                labels[b] = 'B-{}'.format(label[:3]) if i == 0\
                    else 'I-{}'.format(label[:3])
            morphs.append(None)
        else:
            morphs.append(text)

    return morphs, labels


def regexp_and_formatting(sentences: List[str]) -> List[str]:
    """
    regexp and format data
    :param sentences: result of `load_sentences`
    :return formatted data
            [`morph` or `NElabel and NE` or `EOS`, ...]
    """

    data = []
    regexp0 = re.compile(r'^#')  # check comment outs
    regexp1 = re.compile(  # check whethe morpheme
        r'^([^ ]+)\s[^ ]+\s[^ ]+\s[^ ]+\s[^ ]+\s[^ ]+\s[^ ]+$')
    regexp2 = re.compile(  # check NElabel and NE
        r'.*ne type=\"([A-Z]+)\" target=\"(.+)\".*')
    regexp3 = re.compile(r'\".+[0-9]')  # check other information in NElabel

    logging.info('exec regexp')
    for sentence in sentences:
        for line in sentence.split('\n'):
            if regexp0.search(line):
                pass
            elif regexp1.search(line):
                data.append(line)
            elif regexp2.search(line):
                label_and_ne = re.sub(regexp2, r'\1-\2', line)
                data.append(re.sub(regexp3, '', label_and_ne))
        data.append('EOS')
    return data


def load_sentences(dataset_path: str) -> List[str]:
    """
    load sentences from KWDLC tar file
    :param dataset_path: KWDLC tar file path
    :return senteces in KWDLC tar file
            [[morph or information of morph, ...], ...]
    """

    sentences: list = []
    logging.info('loading text files...')
    with tarfile.open(dataset_path, 'r') as tf:
        for ti in tf:
            fname = tf.getmember(ti.name)
            f = tf.extractfile(fname)
            if ti.isfile() and '.KNP' in ti.name:
                sentences += f.read().decode('utf-8').split('EOS')[:-1]
    return sentences


def main(dataset_path: str, file_path: str):
    """
    call when exec this script
    :param dataset_path: KWDLC tar file path
    :param file_path: generated dataset path
    """

    sentences = load_sentences(dataset_path)
    data = regexp_and_formatting(sentences)
    morphs, labels = label_indexes_to_morphs(data)
    content = ''
    logging.info('making dataset')
    for i, d in enumerate(morphs):
        if d == 'EOS':
            content += '\n'
        elif d is not None:
            if labels[i] is None:
                content += d + '\t' + 'O'
            else:
                content += d + '\t' + labels[i]
            content += '\n'
    with open(file_path, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--dataset', default='KWDLC-1.0.tar.bz2',
                   help='KWDLC tar file path. default ./KWDLC-1.0.tar.bz2')
    p.add_argument('-f', '--file', default='dataset.txt',
                   help='generated dataset path. default ./dataset.txt')
    args = p.parse_args()

    main(args.dataset, args.file)
