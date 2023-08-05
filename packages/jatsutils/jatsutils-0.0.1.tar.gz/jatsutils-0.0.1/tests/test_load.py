
from jatsutils import JatsElementTree as JET
from xml.etree.ElementTree import dump
import os


def test_load_from_file(static_dir):

    test_manuscript = os.path.join(static_dir, 'manuscript.xml')

    jet = JET(from_file=test_manuscript)

    title = jet.root.find('front/article-meta/title-group/article-title').text

    assert 'Object vision to hand action in macaque parietal, premotor, and motor cortices' == title


def test_load_from_string(static_dir):

    test_manuscript = os.path.join(static_dir, 'manuscript.xml')

    data = ''
    with open(test_manuscript, 'r') as data_file:
        data = data_file.read().encode()

    jet = JET(from_string=data)

    title = jet.root.find('front/article-meta/title-group/article-title').text

    assert 'Object vision to hand action in macaque parietal, premotor, and motor cortices' == title
