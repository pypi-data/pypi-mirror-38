import re
import heapq
import warnings


class TestQueue:
    """
    This collection of tests will test the functionality of the TrieQueue class.
    """
    def __init__(self, n_elements):
        """
        :param n_elements: number of elements to be stored in queue; type = int
        initialize the queue
        """
        self.queue = []
        self.n_elements = n_elements

    def peek(self):
        """
        return the word with greatest weight
        """
        return self.queue[0][0]

    def replace(self, vector):
        """
        :param vector: a (weight, word) tuple; type = (int, string)
        """
        heapq.heapreplace(self.queue, vector)

    def is_full(self):
        """
        :return: is the queue full? type = boolean
        """
        return len(self.queue) == self.n_elements

    def push(self, vector):
        heapq.heappush(self.queue, vector)

    def to_list(self):
        """
        :return: the queue in list form, sorted from greatest to smallest; type = (int, string) - list
        """
        return [heapq.heappop(self.queue) for _ in range(len(self.queue))][::-1]


def slow_complete(query, words, k):
    """
    :param query: The prefix query; type = string
    :param words: a list of words and associated weights; type = (int, string) - list
    :param k: the number of words to return; type = int
    :return: a list of the k most relevant autocompletions and associated weights; type = (int, string) - list
    :argument: query = "Ti"; words = TrieUtilities.read_file("Data/baby-names.txt"); k = 5; slow_complete(query, words, k)
    Notes: if k words with given prefix cannot be found, then raise ImportError
    """
    regex = re.compile('^' + query + "")
    queue = TestQueue(k)
    for curr_weight, curr_word in words:
        if regex.match(curr_word) is not None:
            if not queue.is_full() or curr_weight > queue.peek():
                queue.replace((curr_weight, curr_word)) if queue.is_full() else queue.push((curr_weight, curr_word))
    # unload the queue into output
    if not queue.is_full():
        warnings.warn("The input list contains fewer than " + str(k) + " words with the prefix " + str(query) + ".")
    return queue.to_list()


class SlowDatabase:
    """
    A class that implements autocomplete using the slow algorithm
    """

    def __init__(self, file_name):
        """
        :param file_name: name of the file that contains the data to load
        """
        self.words = TrieUtilities.read_file(file_name)

    def autocomplete(self, query, k):
        """
        The API of this autocomplete function is the same as that of the Trie autocomplete.
        """
        return slow_complete(query, self.words, k)
