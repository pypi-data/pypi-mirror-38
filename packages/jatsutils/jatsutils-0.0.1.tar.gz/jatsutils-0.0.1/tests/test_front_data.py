
def test_article_categories(element_tree):
    categories = element_tree.get_article_categories()
    # assert 'en' in categories.keys()
    # assert categories['en'][0]['content-type'] == "display-channel"
    # assert categories['en'][0]['content'] == "Research Article"
    # assert categories['en'][1]['content-type'] == "heading"
    # assert categories['en'][1]['content'] == "Computational and Systems Biology"
    # assert categories['en'][2]['content-type'] == "heading"
    # assert categories['en'][2]['content'] == "Epidemiology and Global Health"
    #
    # assert 'es' in categories.keys()
    # assert categories['es'][0]['content-type'] == "display-channel"
    # assert categories['es'][0]['content'] == "Artículo de investigación"
    # assert categories['es'][1]['content-type'] == "heading"
    # assert categories['es'][1]['content'] == "Biología computacional y de sistemas"
    # assert categories['es'][2]['content-type'] == "heading"
    # assert categories['es'][2]['content'] == "Epidemiología y salud global"

    assert categories['article-categories']['subj-group'][0]['@xml:lang'] == "en"
    assert categories['article-categories']['subj-group'][0]['subject'][0]['@content-type'] == "display-channel"
    assert categories['article-categories']['subj-group'][0]['subject'][0]['#text'] == "Research Article"
    assert categories['article-categories']['subj-group'][0]['subject'][1]['@content-type'] == "heading"
    assert categories['article-categories']['subj-group'][0]['subject'][1]['#text'] == "Computational and Systems Biology"
    assert categories['article-categories']['subj-group'][0]['subject'][2]['@content-type'] == "heading"
    assert categories['article-categories']['subj-group'][0]['subject'][2]['#text'] == "Epidemiology and Global Health"

    assert categories['article-categories']['subj-group'][1]['@xml:lang'] == "es"
    assert categories['article-categories']['subj-group'][1]['subject'][0]['@content-type'] == "display-channel"
    assert categories['article-categories']['subj-group'][1]['subject'][0]['#text'] == "Artículo de investigación"
    assert categories['article-categories']['subj-group'][1]['subject'][1]['@content-type'] == "heading"
    assert categories['article-categories']['subj-group'][1]['subject'][1]['#text'] == "Biología computacional y de sistemas"
    assert categories['article-categories']['subj-group'][1]['subject'][2]['@content-type'] == "heading"
    assert categories['article-categories']['subj-group'][1]['subject'][2]['#text'] == "Epidemiología y salud global"


def test_title(element_tree):
    assert element_tree.get_title() == 'Object vision to hand action in macaque parietal, premotor, and motor cortices'


def test_trans_titles(element_tree):
    trans_titles = element_tree.get_trans_titles()
    assert 'es' in trans_titles.keys()
    assert trans_titles['es']['id'] == 'trans-title-1'
    assert trans_titles['es']['title'] == 'Objeto de visión a acción manual en cortezas parietales, premotoras y motoras de macaco'


def test_article_authors(element_tree):
    article_authors = element_tree.get_article_authors()
    assert article_authors[0]['contrib']['@contrib-type'] == "person"
    assert article_authors[0]['contrib']['@equal-contrib'] == "yes"
    assert article_authors[0]['contrib']['@corresp'] == "no"
    assert article_authors[0]['contrib']['@deceased'] == "no"
    assert article_authors[0]['contrib']['name']['surname'] == 'Schaffelhofer'
    assert article_authors[0]['contrib']['name']['given-names'] == 'Stefan'
    assert article_authors[0]['contrib']['xref'][0]['@ref-type'] == 'aff'
    assert article_authors[0]['contrib']['xref'][0]['@rid'] == 'aff1'
    assert article_authors[0]['contrib']['xref'][1]['@ref-type'] == 'aff'
    assert article_authors[0]['contrib']['xref'][1]['@rid'] == 'aff2'

    assert article_authors[1]['contrib']['@contrib-type'] == "person"
    assert article_authors[1]['contrib']['@equal-contrib'] == "no"
    assert article_authors[1]['contrib']['@corresp'] == "no"
    assert article_authors[1]['contrib']['@deceased'] == "no"
    assert article_authors[1]['contrib']['name']['surname'] == 'Scherberger'
    assert article_authors[1]['contrib']['name']['given-names'] == 'Hansjörg'
    assert article_authors[1]['contrib']['xref'][0]['@ref-type'] == 'aff'
    assert article_authors[1]['contrib']['xref'][0]['@rid'] == 'aff1'
    assert article_authors[1]['contrib']['xref'][1]['@ref-type'] == 'aff'
    assert article_authors[1]['contrib']['xref'][1]['@rid'] == 'aff3'

    assert article_authors[2]['contrib']['@contrib-type'] == "person"
    assert article_authors[2]['contrib']['@equal-contrib'] == "no"
    assert article_authors[2]['contrib']['@corresp'] == "no"
    assert article_authors[2]['contrib']['@deceased'] == "no"
    assert article_authors[2]['contrib']['name']['surname'] == 'Kelly'
    assert article_authors[2]['contrib']['name']['given-names'] == 'Laura A.'
    assert article_authors[2]['contrib']['xref']['@ref-type'] == 'aff'
    assert article_authors[2]['contrib']['xref']['@rid'] == 'aff2'

    assert article_authors[3]['contrib']['@contrib-type'] == "person"
    assert article_authors[3]['contrib']['@equal-contrib'] == "no"
    assert article_authors[3]['contrib']['@corresp'] == "no"
    assert article_authors[3]['contrib']['@deceased'] == "no"
    assert article_authors[3]['contrib']['name']['surname'] == 'Randall'
    assert article_authors[3]['contrib']['name']['given-names'] == 'Daniel Lee'
    assert article_authors[3]['contrib']['name']['suffix'] == 'Jr.'
    assert article_authors[3]['contrib']['string-name']['@content-type'] == 'alias'
    assert article_authors[3]['contrib']['string-name']['#text'] == 'Dan Randall'
    assert article_authors[3]['contrib']['xref']['@ref-type'] == 'aff'
    assert article_authors[3]['contrib']['xref']['@rid'] == 'aff3'


def test_article_editors(element_tree):
    article_authors = element_tree.get_article_editors()
    assert article_authors[0]['contrib']['@contrib-type'] == "person"
    assert article_authors[0]['contrib']['@equal-contrib'] == "no"
    assert article_authors[0]['contrib']['@corresp'] == "no"
    assert article_authors[0]['contrib']['@deceased'] == "no"
    assert article_authors[0]['contrib']['name']['surname'] == 'Kastner'
    assert article_authors[0]['contrib']['name']['given-names'] == 'Sabine'
    assert article_authors[0]['contrib']['xref']['@ref-type'] == 'aff'
    assert article_authors[0]['contrib']['xref']['@rid'] == 'aff1'


def test_article_affiliations(element_tree):
    article_affiliations = element_tree.get_article_affiliations()
    assert article_affiliations[0]['aff']['@id'] == "aff1"
    assert article_affiliations[0]['aff']['institution'][0]['@content-type'] == "orgname"
    assert article_affiliations[0]['aff']['institution'][0]['#text'] == "German Primate Center GmbH"
    assert article_affiliations[0]['aff']['institution'][1]['@content-type'] == "orgdiv1"
    assert article_affiliations[0]['aff']['institution'][1]['#text'] == "Neurobiology Laboratory"
    assert article_affiliations[0]['aff']['city'] == "Göttingen"
    assert article_affiliations[0]['aff']['country'] == "Germany"

    assert article_affiliations[1]['aff']['@id'] == "aff2"
    assert article_affiliations[1]['aff']['institution'][0]['@content-type'] == "orgname"
    assert article_affiliations[1]['aff']['institution'][0]['#text'] == "The Rockefeller University"
    assert article_affiliations[1]['aff']['institution'][1]['@content-type'] == "orgdiv1"
    assert article_affiliations[1]['aff']['institution'][1]['#text'] == "Laboratory of Neural Systems"
    assert article_affiliations[1]['aff']['city'] == "New York"
    assert article_affiliations[1]['aff']['country'] == "United States"

    assert article_affiliations[2]['aff']['@id'] == "aff3"
    assert article_affiliations[2]['aff']['institution'][0]['@content-type'] == "orgname"
    assert article_affiliations[2]['aff']['institution'][0]['#text'] == "University of Göttingen"
    assert article_affiliations[2]['aff']['institution'][1]['@content-type'] == "orgdiv1"
    assert article_affiliations[2]['aff']['institution'][1]['#text'] == "Department of Biology"
    assert article_affiliations[2]['aff']['city'] == "Göttingen"
    assert article_affiliations[2]['aff']['country'] == "Germany"

    assert article_affiliations[3]['aff']['@id'] == "aff4"
    assert article_affiliations[3]['aff']['institution'][0]['@content-type'] == "orgname"
    assert article_affiliations[3]['aff']['institution'][0]['#text'] == "Princeton University"
    assert article_affiliations[3]['aff']['city'] == "Princeton"
    assert article_affiliations[3]['aff']['country'] == "United States"


def assert_date(date_dict, date_type, date):
    assert date_dict['@date-type'] == date_type
    assert date_dict['@iso-8601-date'] == date
    assert date_dict['day'] == date.split('-')[2]
    assert date_dict['month'] == date.split('-')[1]
    assert date_dict['year'] == date.split('-')[0]


def test_article_publication_date(element_tree):
    article_pub_date = element_tree.get_article_publication_date()
    assert_date(article_pub_date['pub-date'], "pub", "1999-01-29")


def test_volume(element_tree):
    assert element_tree.get_volume() == '318'


def test_issue(element_tree):
    assert element_tree.get_issue() == '7187'


def test_fpage(element_tree):
    assert element_tree.get_fpage() == '837'


def test_lpage(element_tree):
    assert element_tree.get_lpage() == '841'


def test_page_range(element_tree):
    assert element_tree.get_page_range() == '837-841'


def test_article_history(element_tree):
    article_history = element_tree.get_article_history()
    assert_date(article_history['history']['date'][0], "accepted", "1998-06-06")
    assert_date(article_history['history']['date'][1], "received", "1998-01-05")
    assert_date(article_history['history']['date'][2], "rev-recd", "1998-05-24")
    assert_date(article_history['history']['date'][3], "rev-request", "1998-03-14")


def test_article_permissions(element_tree):
    article_permissions = element_tree.get_article_permissions()
    assert article_permissions['permissions']['copyright-statement'] == '© 2018 Substance Consortium'
    assert article_permissions['permissions']['copyright-year'] == '2018'
    assert article_permissions['permissions']['copyright-holder'] == 'Substance Consortium'
    assert article_permissions['permissions']['license']['ali:license_ref'] == 'http://creativecommons.org/licenses/by/4.0/'


def test_article_abstract(element_tree):
    article_abstract = element_tree.get_article_abstract()
    assert article_abstract['abstract']['p']['@id'] == 'p-1'


def test_article_trans_abstracts(element_tree):
    article_trans_abstracts = element_tree.get_article_trans_abstracts()
    assert article_trans_abstracts[0]['trans-abstract']['@id'] == 'trans-abstract-1'
    assert article_trans_abstracts[0]['trans-abstract']['@xml:lang'] == 'es'
    assert article_trans_abstracts[0]['trans-abstract']['p']['@id'] == 'p-1-1'


def test_article_keywords(element_tree):
    article_keywords = element_tree.get_article_keywords()
    assert article_keywords[0]['kwd-group']['@xml:lang'] == 'en'
    assert article_keywords[0]['kwd-group']['kwd'][0]['@content-type'] == 'author-keyword'
    assert article_keywords[0]['kwd-group']['kwd'][0]['#text'] == 'optogenetics'
    assert article_keywords[0]['kwd-group']['kwd'][1]['@content-type'] == 'author-keyword'
    assert article_keywords[0]['kwd-group']['kwd'][1]['#text'] == 'two-photon'
    assert article_keywords[0]['kwd-group']['kwd'][2]['@content-type'] == 'author-keyword'
    assert article_keywords[0]['kwd-group']['kwd'][2]['#text'] == 'calcium imaging'
    assert article_keywords[0]['kwd-group']['kwd'][3]['@content-type'] == 'research-organism'
    assert article_keywords[0]['kwd-group']['kwd'][3]['#text'] == 'Mouse'

    assert article_keywords[1]['kwd-group']['@xml:lang'] == 'es'
    assert article_keywords[1]['kwd-group']['kwd'][0]['@content-type'] == 'author-keyword'
    assert article_keywords[1]['kwd-group']['kwd'][0]['#text'] == 'nada'
    assert article_keywords[1]['kwd-group']['kwd'][1]['@content-type'] == 'author-keyword'
    assert article_keywords[1]['kwd-group']['kwd'][1]['#text'] == 'si'


def test_article_funding_group(element_tree):
    article_funding_group = element_tree.get_article_funding_group()
    assert article_funding_group['funding-group']['award-group']['@id'] == 'fund1'
    assert article_funding_group['funding-group']['award-group']['funding-source']['institution-wrap']['institution-id']['@institution-id-type'] == 'FundRef'
    assert article_funding_group['funding-group']['award-group']['funding-source']['institution-wrap']['institution-id']['#text'] == 'https://dx.doi.org/10.13039/100000011'
    assert article_funding_group['funding-group']['award-group']['funding-source']['institution-wrap']['institution'] == 'Howard Hughes Medical Institute'
    assert article_funding_group['funding-group']['award-group']['award-id'] == 'F32 GM089018'
