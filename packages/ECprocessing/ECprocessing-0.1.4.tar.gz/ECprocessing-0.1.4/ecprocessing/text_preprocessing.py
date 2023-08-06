'''Functions to help with preprocessing of text'''
# Ideas for more functions ---- remove_punctuation, replace_number_with_text, remove duplicate letters, convert LaTeX to the word LaTeX
from bs4 import BeautifulSoup
import unicodedata
import re
from ecprocessing.contractions import CONTRACTION_MAP
import nltk
from nltk.corpus import wordnet
from nltk.tokenize.toktok import ToktokTokenizer

DEFAULT_STOPWORD_LIST = nltk.corpus.stopwords.words('english')
DEFAULT_STOPWORD_LIST.remove('no')
DEFAULT_STOPWORD_LIST.remove('not')


def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def expand_match(contraction, contraction_mapping):
    '''Takes a match object that has matched with a key (not case sensitive) in the contraction_mapping and returns the equivelent value
        retains the case of the first character'''
    match = contraction.group(0)
    first_char = match[0]
    expanded_contraction = contraction_mapping.get(match)\
                            if contraction_mapping.get(match)\
                            else contraction_mapping.get(match.lower())                       
    expanded_contraction = first_char+expanded_contraction[1:]
    return expanded_contraction


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)

        
    expanded_text = contractions_pattern.sub(lambda x: expand_match(x, contraction_mapping), text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_special_characters(text, remove_digits=False, remove_underscores=True):
    '''If remove_underscores is true, replace underscores with spaces
        Should take raw text'''
    
    # insert spaces between special characters to isolate them    
    special_char_pattern = re.compile(r'([{.(-)!}=/])')
    text = special_char_pattern.sub(" \\1 ", text)

    # Remove anything that isn't a group of alphanumeric/numeric and remove square brackets and carets
    pattern = r'[^a-zA-z0-9\s]|[\[\]\^]' if not remove_digits else r'[^a-zA-z\s]|[\[\]\^]'
    text = re.sub(pattern, '', text)
    
    # Remove backslashes from text
    backslashpattern = '\\\\'
    text = re.sub(backslashpattern, '', text)
    
    # Remove underscores
    if remove_underscores:
        text = re.sub('_', ' ', text)
    
    # Remove excess spaces
    text = re.sub(' +', ' ', text)

    # Remove end space
    if text[-1] == ' ':
        text = text[:-1]
    
    return text


def simple_stemmer(text):
    ps = nltk.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatize_text(text):
    pos_tagged_words = nltk.pos_tag(text.split())
    lmtzr = nltk.WordNetLemmatizer()
    lemm_words = ' '.join([lmtzr.lemmatize(word[0], get_wordnet_pos(word[1])) for word in pos_tagged_words])
    return lemm_words

def remove_stopwords(text, is_lower_case=False, stopword_list=DEFAULT_STOPWORD_LIST):
    '''If is_lower_case is True then will only remove stopwords if they are lower case, stopword list should all be lowercase
        Default stop word list is the standard english default list with no and not removed'''

    if is_lower_case:
        filtered_tokens = [token for token in text.split() if token not in stopword_list]
    else:
        filtered_tokens = [token for token in text.split() if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

def normalize_text(text, *, html_stripping=True, contraction_expansion=True,
                            accented_char_removal=True, text_lower_case=True, 
                            text_stemming='Stem', special_char_removal=True, 
                            stopword_removal=True, stopword_list=DEFAULT_STOPWORD_LIST, remove_digits=True, remove_underscores=True):

    '''Applies selected preprocessing steps, must use key words to specify changes to default'''

    if html_stripping:
        text = strip_html_tags(text)
    
    if contraction_expansion:
        text = expand_contractions(text)
    
    if accented_char_removal:
        text = remove_accented_chars(text)
    
    if text_lower_case:
        text = text.lower()
    
    text = re.sub(r'[\r|\n|\r\n]+', ' ',text)

    if special_char_removal:
        text = remove_special_characters(text, remove_digits=remove_digits, remove_underscores=remove_underscores)

    if stopword_removal:
        text = remove_stopwords(text, is_lower_case=text_lower_case, stopword_list=stopword_list)

    if text_stemming == 'Stem':
        text = simple_stemmer(text)
    elif text_stemming == 'Lem':
        text = lemmatize_text(text)
    elif text_stemming == False:
        pass
    else:
        raise ValueError('Invalid value of text stemming parameter {}'.format(text_stemming))
    
    


    return text 



if __name__ == '__main__':
    
   example_text = 'Is it just me or have you ever been in this phase wherein you became ignorant to the people you once loved, completely disregarding their feelings/lives so you get to have something go your way and feel temporarily at ease. How did things change?'
   parsed = normalize_text(example_text, text_stemming='Lem')
   print(parsed)