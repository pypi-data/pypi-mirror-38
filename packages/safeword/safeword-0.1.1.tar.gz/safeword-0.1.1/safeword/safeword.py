import uuid
import random
import re
import os
import csv


class SafeWord:
    """WIP Return mutable characters as requested
    """

    def __init__(self, return_type='uuid', append=None, direction='FORWARD',
                 length=12, machine_safe=False):
        # set defaults
        self.return_type = return_type
        self.direction = direction
        self.append = append
        self.length = length
        self.machine_safe = machine_safe

        _ROOT = os.path.abspath(os.path.dirname(__file__))

        self.word_list_complete = []
        self.word_list_adjectives = []
        self.word_list_nouns = []
        self.word_list_verbs = []

        # open file and load word lists
        with open(_ROOT + '/resources/wordlist.csv') as words:
            reader = csv.reader(words)

            # read file row by row
            rowNr = 0
            for row in reader:
                # Skip the header row.
                if rowNr >= 1:
                    self.word_list_complete.append(row[0])
                if row[1] == 'adjective':
                    self.word_list_adjectives.append(row[0])
                if row[1] == 'noun':
                    self.word_list_nouns.append(row[0])
                if row[1] == 'verb':
                    self.word_list_verbs.append(row[0])
                # Increase the row number
                rowNr = rowNr + 1

    def get_random_string(self,
                          allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                                        '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'):
        """
        Return a securely generated random string.
        The default length of 12 with the a-z, A-Z, 0-9 character set returns
        a 71-bit value. log_2((26+26+10)^12) =~ 71 bits

        This is derived from https://github.com/django/django/blob/master/django/utils/crypto.py
        and https://github.com/django/django/blob/master/django/utils/text.py
        """
        # Assume system  PRNG  for seed , else fail.
        # todo: fail safely if no random.SystemRandom()

        # Apply filters here as well (machine safe, exclude chars, int only ,
        #  etc... )
        if self.machine_safe:
            allowed_chars = re.sub(r'(?u)[^-\w.]', '', allowed_chars)
        return ''.join(random.choice(allowed_chars) for i in range(self.length))

    def __str_gen(self):
        # __ makes it feel private, though it is accessible
        # via foo._Foo__method()
        if self.return_type == 'uuid':
            return str(uuid.uuid4())
        elif self.return_type == 'random_string':
            return self.get_random_string()
        else:
            return str('SOMETHING ELSE')

    # def str_manipulate(self):
    #     pass

    def generate(self):
        word_hash = self.__str_gen()
        if self.direction is not 'FORWARD':
            word_hash = word_hash[::-1]
        if self.append is not None:
            word_hash = word_hash + self.append
        return word_hash

    def get_word(self, word_type=''):
        random_salt = random.SystemRandom()
        if not word_type:
            word = random_salt.choice(self.word_list_complete)
        if word_type == 'adjective':
            word = random_salt.choice(self.word_list_adjectives)
        if word_type == 'noun':
            word = random_salt.choice(self.word_list_nouns)
        if word_type == 'verb':
            word = random_salt.choice(self.word_list_verbs)
        return word

