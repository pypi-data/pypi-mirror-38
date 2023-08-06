import jieba
from xpinyin import Pinyin
import re
import logging
from pinmix.opendoc_factory import DocFactory

def line_to_pinyin(line):
    jieba.setLogLevel(logging.ERROR)
    segments = jieba.cut(line)
    output = " ".join(segments)
    p = Pinyin()
    pinyined = p.get_pinyin(output, splitter='', show_tone_marks=True)
    return pinyined

def is_chinese(line):
    matches = re.findall(r'[\u4e00-\u9fff]+', line)
    return len(matches) > 0

def gen_line_from_file(filename):
    with open(filename, encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if is_chinese(line):
                yield ('chinese', line)
                yield ('pinyin', line_to_pinyin(line))
            else:
                yield ('other', line)


def process_to_print(filename):
    for tuple in gen_line_from_file(filename):
        print(tuple[1])


def process_file_to_odt(filename, outputdoc):
    doc = DocFactory(outputdoc)
    for tuple in gen_line_from_file(filename):
        text = tuple[1]
        if tuple[0] == 'other':
            doc.add_p1_text(text)
        if tuple[0] == 'chinese':
            doc.add_p3_text(text)
        if tuple[0] == 'pinyin':
            doc.add_p2_text(text)
    doc.save()
