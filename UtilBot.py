from urllib import request
from xml.dom import minidom
from bs4 import BeautifulSoup, Tag

__author__ = 'wardellchandler'


# To keep from crowding up the handlers.py handle method, try to out source to here.
class UtilBot:
    @staticmethod
    def check(string):
        return string.replace("&#39", "'")

    @staticmethod
    # TODO This needs a better name... Is actually the define function.
    def define(word, num=1):
        if num < 1:
            num = 1
        try:
            url = "http://wordnetweb.princeton.edu/perl/webwn?s=" + word + "&sub=Search+WordNet&o2=&o0=&o8=1&o1=1&o7=&o5=&o9=&o6=&o3=&o4=&h=0000000000"
        except Exception as e:
            print(e)
            return 'Couldn\'t download definition.'
        soup = BeautifulSoup(request.urlopen(url))
        if soup.ul is not None:
            definitions = [x.text for x in list(soup.ul) if isinstance(x, Tag) and x.text != '\n' and x.text != '']
            if len(definitions) >= num:
                return (definitions[num - 1] + '[' + str(num) + ' of ' + str(len(definitions)) + ']')[3:].capitalize()
        return "Couldn\'t download definition."

    @staticmethod
    def levenshtein_distance(first, second):
        """Find the Levenshtein distance between two strings."""
        chopped = False
        if len(first) > len(second):
            first = first[:len(second)]
            first, second = second, first
            chopped = True
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [[0] * second_length for x in range(first_length)]
        for i in range(first_length):
            distance_matrix[i][0] = i
        for j in range(second_length):
            distance_matrix[0][j] = j
        for i in range(1, first_length):
            for j in range(1, second_length):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion, deletion, substitution)
        return distance_matrix[first_length - 1][second_length - 1], chopped

    @staticmethod
    def find_next_non_blank(list, start=0):
        for x in range(start + 1, len(list)):
            if isinstance(list[x], tuple):
                tocheck = list[x][0]
            else:
                tocheck = list[x]
            tocheck = tocheck.replace(' ', '')
            if tocheck != '':
                return x



