import unittest
import ecprocessing.text_preprocessing as txp
import re
import warnings

class Test_TextPreprocessing(unittest.TestCase):
    
    def test_strip_html_tags(self):
        self.assertEqual(txp.strip_html_tags('<html><h2 style="color:red">Some import<br>ant text</h2></html>'), 'Some important text')

    def test_remove_accented_chars(self):
        self.assertEqual(txp.remove_accented_chars('Sómě Áccěntěd těxt ÀÁÂÃÄÇÈÉÊËÌÍÎÏÑÒÓÔÕÖŠÚÛÜÙÝŸŽàáâãäçèéêëìíîïñòóôõöšùúûüýÿž'), 'Some Accented text AAAAACEEEEIIIINOOOOOSUUUUYYZaaaaaceeeeiiiinooooosuuuuyyz')

    def test_expand_match(self):
        self.assertEqual(txp.expand_match(re.match("don't", "don't"), {"don't": "do not"}), "do not")
        self.assertEqual(txp.expand_match(re.match("Don't", "Don't"), {"don't": "do not"}), "Do not")
        self.assertEqual(txp.expand_match(re.match("DoN't", "DoN't"), {"don't": "do not"}), "Do not")

    def test_expand_contractions(self):
        self.assertEqual(txp.expand_contractions("Y'allcan't expand contractions I'd think i'd"), 'You allcannot expand contractions I would think i would')

    def test_remove_special_chars(self):
        self.assertEqual(txp.remove_special_characters('/Well [this was fun! ^What_do {you think? 123#@!', remove_digits=True, remove_underscores=True), 'Well this was fun What do you think')
        self.assertEqual(txp.remove_special_characters('Well this was fun! What_do you think? 123#@!'), 'Well this was fun What do you think 123')
        self.assertEqual(txp.remove_special_characters('Well this was fun! What_do you think? 123#@!', remove_underscores=False), 'Well this was fun What_do you think 123')
        self.assertEqual(txp.remove_special_characters(r'{ \this \might \be \LaTex}'), ' this might be LaTex')
        self.assertEqual(txp.remove_special_characters('I now [remove square] brackets and ^carets'), 'I now remove square brackets and carets')

    def test_simple_stemmer(self):
      self.assertEqual(txp.simple_stemmer('My system keeps crashing his crashed yesterday, ours crashes daily'), 'My system keep crash hi crash yesterday, our crash daili')  

    def test_get_wordnet_pos(self):
        
        with warnings.catch_warnings():     # Hide resource warning messages for unclosed wordnet
            warnings.simplefilter("ignore")
            self.assertEqual([txp.get_wordnet_pos(pos) for pos in ['JJ','JJR', 'JJS']], ['a']*3)                         # Check adjectives
            self.assertEqual([txp.get_wordnet_pos(pos) for pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']], ['v']*6)   # Check verbs
            self.assertEqual([txp.get_wordnet_pos(pos) for pos in ['NN', 'NNPS', 'NNS']], ['n']*3)                       # Check Nouns
            self.assertEqual([txp.get_wordnet_pos(pos) for pos in ['RB', 'RBR', 'RBS', 'RP']], ['r']*4)                  # Check adverbs
        
            pos_taglist =  ['$', '"', '(', ')', ',', '-', '.', ':',
                        'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ',
                        'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNPS', 'NNS',
                        'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS',
                        'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN',
                        'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '`']
            wordnet_pos_set = set(['a', 'v', 'n', 'r'])
            
            for pos in pos_taglist:                                      # Check all possible tags will return a wordnet tag
                self.assertIn(txp.get_wordnet_pos(pos), wordnet_pos_set)

    
    def test_lemmatize_text(self):
        self.assertEqual(txp.lemmatize_text('This is a string that will be lemmatized. I am currently testing it and hope it works as planned'), 'This be a string that will be lemmatized. I be currently test it and hope it work a plan')

    def test_remove_stopwords(self):
        self.assertEqual(txp.remove_stopwords('This is my test.', False, ['my']), 'This is test.')
        self.assertEqual(txp.remove_stopwords('This is My test.', True, ['my']), 'This is My test.')

    def test_normalize_text(self):
        messy_unchanging_string = "This string<br> shouldn't cha__nge at all ev3n with '£lots of messy párts."
        self.assertEqual(txp.normalize_text(messy_unchanging_string, html_stripping=False, contraction_expansion=False, accented_char_removal=False, text_lower_case=False, text_stemming=False, special_char_removal=False, stopword_removal=False, remove_digits=False, remove_underscores=False), messy_unchanging_string)

if __name__ == '__main__':

    unittest.main()
