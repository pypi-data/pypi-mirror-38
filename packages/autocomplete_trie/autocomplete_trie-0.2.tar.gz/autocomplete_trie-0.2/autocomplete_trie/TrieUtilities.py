# utilities for the trie
import heapq
import re


def read_file(filename, contains_header=True):
    """
    :param filename: The name of a text file. The file should have two columns
    separated by whitespace. The first column is the weight and the second column is the word. The first
    line indicates the number of terms in the file; type = string
    :param contains_header: Does the input file contain a header row?
    :return: a list of (weight , word) values; type = (int, string) - list
    :argument: 'Data/baby-names-short.txt'; read_file('Data/baby-names-short.txt')
    """
    file = open(filename, "r")
    if contains_header:
        next(file)
    regex = re.compile("^\s*(-?\d+)\s+(.*)$")
    out = []
    for line in file:
        match = regex.search(line)
        if match is not None:
            out.extend([(int(match.group(1)), match.group(2))])
    file.close()
    return out


class TrieQueue:
    def __init__(self):
        """
        initialize an empty queue
        """
        self.queue = []

    def push(self, vec):
        """
        :param vec: a tuple to be pushed onto the queue. The type can be either (int, string) (for words) or
        (int, Node) (for nodes).
        """
        heapq.heappush(self.queue, TrieQueueElement(vec))

    def pop(self):
        """
        :return: the greatest element in the queue; type = (int, string) or (int, Node)
        """
        element = heapq.heappop(self.queue)
        return element.number, element.item

    def greatest_element_is_word(self):
        """
        :return: is the greatest element in the queue a word (as opposed to a node)?; type = boolean
        """
        element = self.queue[0]
        return element.item.__class__ == str

    def is_empty(self):
        """
        :return: is the queue empty? type = boolean
        """
        return len(self.queue) == 0


class TrieQueueElement:
    def __init__(self, vector):
        self.number, self.item = vector

    def __lt__(self, other):
        if self.number != other.number:
            output = self.number > other.number
        else:
            if self.item.__class__ != other.item.__class__:
                output = self.item.__class__ == str
            else:
                if self.item.__class__ == str:
                    output = self.item < other.item
                else:
                    output = True
        return output
