import autocomplete_trie
import warnings
import collections


class Node:

    def __init__(self):
        """
        Initialize an empty node.
        """

        self.is_word = False
        self.word_weight = None

        self.has_children = False
        self.children_dict = {}
        self.max_descendant_weight = None


class Trie:

    # public methods
    def __init__(self, file_name):
        """
        Construct a database with data from a file.
        :param file_name: the name of a text file containing the data to load into the database. If None,
         construct an empty database; type = string
        """
        if file_name is None:
            self.root = Node()
        else:
            self._build_trie(file_name)

    def autocomplete(self, prefix, k):
        """
        Return suggested search results for a query, rank-ordered by decreasing weight.
        :param prefix: the query; type = string
        :param k: number of results to return; type = int
        :return: the k descendants of node with greatest weight; type = (int, string) - list
        """
        start_node = _node_search(prefix, self.root)
        return _k_greatest_descendants(start_node, k, prefix)

    def add_term(self, weight, word):
        """
        A a term to the database.
        :param weight: weight of term to add; type = int
        :param word: the term to add; type = string
        :return: None
        """
        _insert_node((weight, word), self.root)

    def update_weight(self, word, weight_function):
        """
        Update the weight of a term in the database.
        :param weight_function: a function that takes as an argument the current weight, and returns a new weight;
        type = int -> int
        :param word: the term in the database whose weight will be updated using the weight function; type = string
        :return: None
        """
        ancestor_list = _search_ancestors(word, self.root)
        _update_weight_helper(ancestor_list, weight_function)

    def delete_term(self, word):
        """
        Delete a term from the database.
        :param word: the term to delete from the database; type = string
        :return: None
        """
        ancestor_list = _search_ancestors(word, self.root)
        _delete_term_helper(word, ancestor_list)

    def prune_trie(self, threshold):
        """
        Delete all terms with weights below a threshold.
        :param threshold: a number such that all terms with weights less than that number are deleted from the database;
        type = string
        :return: None
        """
        ancestor_list = collections.deque()
        _prune_tree_helper(threshold, self.root, ancestor_list, None)

    def rescale_weights(self, weight_function):
        """
        Apply a function to all weights stored in the database.
        :param weight_function: the function to apply to the weights in the database; type = int -> int
        :return: None
        """
        _rescale_weights_helper(weight_function, self.root)

    def insert_or_update(self, word, weight=0):
        """
        Insert a term into the database, or, if already present, increment its weight by 1.
        :param word: The term to insert or increment the weight of; type = string
        :param weight: (optional) The default weight to assign to the term if it is not already present in the database;
        type = int
        :return: None
        """
        node_already_preset, ancestor_list, former_weight = _insert_node((weight, word), self.root, True)
        if not node_already_preset:
            pass  # nothing to do; we just made a normal insertion
        else:
            #  we need to fix the weights
            new_weight = former_weight + 1
            added_node = ancestor_list.pop()
            old_weight = added_node.word_weight
            added_node.word_weight = new_weight
            _update_weight_ascend(ancestor_list, new_weight, old_weight)

    # private methods
    def _build_trie(self, file_name):
        """
        :param file_name: the name of a file containing the word-weight data to load into the database; type = string
        Notes: This method takes the name of a file containing data to load into the database. It then loads this data,
        saving the word and weight data in a the trie.
        """
        self.root = Node()  # instantiate a root node
        vectors = autocomplete_trie.read_file(file_name)  # read in the data via read_file function
        for vector in vectors:
            _insert_node(vector, self.root)  # add each word-weight tuple one by one via _insert_node method


# global functions


def _node_search(query, root):
    """
    :param query: a prefix to search for in the tree; type = string
    :param root: a node whence to search
    :return: a reference to the node containing the specified prefix; type = Node
    """
    curr_node = root
    for i in range(1, len(query) + 1):
        prefix = query[0:i]
        if prefix in curr_node.children_dict:
            curr_node = curr_node.children_dict[prefix]
        else:
            raise (LookupError("The query " + query + " is not in the database."))
    return curr_node


def _insert_node(vector, root, use_in_insert_or_update=False):
    """
    :param vector: a weight, word tuple; type = (int, string)
    :param root: the root node from which to start the descent
    """
    if use_in_insert_or_update:
        ancestor_list = collections.deque([root])
        node_already_preset = True
    weight, word = vector
    curr_node = root
    for i in range(1, len(word) + 1):
        prefix = word[0:i]
        # does the current node have children, and is the prefix we are searching for among the children?
        if curr_node.has_children and prefix in curr_node.children_dict:
            next_node = curr_node.children_dict[prefix]
            curr_node.max_descendant_weight = max(curr_node.max_descendant_weight, weight)
        else:
            if use_in_insert_or_update:
                node_already_preset = False
            next_node = Node()
            curr_node.children_dict[prefix] = next_node
            curr_node.has_children = True
            if curr_node.max_descendant_weight is None:
                curr_node.max_descendant_weight = weight
            else:
                curr_node.max_descendant_weight = max(curr_node.max_descendant_weight, weight)
        curr_node = next_node
        if use_in_insert_or_update:
            ancestor_list.append(curr_node)
    # Finally, now that the loop is done, we know "next_node" is a word
    next_node.is_word = True
    if use_in_insert_or_update:
        former_weight = next_node.word_weight
    next_node.word_weight = weight
    if use_in_insert_or_update:
        return node_already_preset, ancestor_list, former_weight


def _k_greatest_descendants(node, k, prefix):
    """
    :param node: a node in the trie; type = Node
    :param k: number of words to search for; type = int
    "param prefix: the prefix represented by node
    :return: the k descendants of node with greatest weight; type = (int, string) - list
    """
    best_words = []  # initialize best words vector
    queue = autocomplete_trie.TrieQueue()  # initialize queue
    if node.is_word:  # add word inside current node (if there is one)
        queue.push((node.word_weight, prefix))
    return _k_greatest_descendants_helper(node, k, best_words, queue, prefix)  # recursive call


def _k_greatest_descendants_helper(node, k, best_words, queue, prefix):
    """
    :param node: node from which to start the method; type = Node
    :param k: number of words to search for; type = int
    :param best_words: a list of the words with greatest weight; type = (int, string) - list
    :param queue: the weights / maximum weights of descendants of traversed nodes; type = TrieQueue
    :return: the k descendants of node with greatest weight; type = (int, string) - list
    """
    # first, iterate through children of node, and add each to queue
    if node.has_children:
        for entry in node.children_dict:
            child = node.children_dict[entry]
            if child.is_word:
                queue.push((child.word_weight, entry))
            if child.has_children:
                queue.push((child.max_descendant_weight, child))
    # second, unload queue as much as possible
    while len(best_words) < k and not queue.is_empty() and queue.greatest_element_is_word():
        best_words.extend([queue.pop()])
    # Third, what to do next. Three conditions could have stopped the while loop.
    if len(best_words) == k:
        return best_words  # we found the best words; return list
    elif queue.is_empty():
        warnings.warn("The database contains fewer than " + str(k) + " words with the prefix " + prefix + ".")
        return best_words
    elif not queue.greatest_element_is_word():
        dummy, next_node = queue.pop()
        return _k_greatest_descendants_helper(next_node, k, best_words, queue, prefix)  # recursive call


def _search_ancestors(query, root):
    """
    :param query: word to search for
    :param root: starting node
    :return: a list containing all the ancestors of the node, including the node itself; type = deque
    """
    ancestor_list = collections.deque()
    # initialize a linked list ancestor_list containing the root
    ancestor_list.append(root)
    # in a manner similar to _node_search, iterate through the tree until we get to the node containing the query.
    curr_node = root
    for i in range(1, len(query) + 1):
        prefix = query[0:i]
        if prefix in curr_node.children_dict:
            curr_node = curr_node.children_dict[prefix]
            ancestor_list.append(curr_node)
        else:
            raise (LookupError("The query " + query + " is not in the database."))
    # return (node, ancestor_list)
    return ancestor_list


def _update_weight_ascend(ancestor_list_short, new_weight, previous_weight):
    """
    :param ancestor_list_short: a list of ancestors. The last node in this list is the PARENT of the node n whose
    weight we just modified.
    :param new_weight: The weight we just assigned to n (can be None, which signifies deletion of n)
    :param previous_weight: The previous weight of n = max(word weight, max descendant weight)
    :return:
    """
    # stopping case
    if len(ancestor_list_short) == 0:
        pass
    else:
        # still some nodes for which we need to update weight
        parent = ancestor_list_short.pop()
        child_is_greatest_desc = parent.max_descendant_weight == previous_weight
        previous_parent_max_desc_weight = parent.max_descendant_weight
        if child_is_greatest_desc:
            # updated child was the greatest descendant
            if new_weight is not None and new_weight >= previous_weight:  # weight increased or stayed the same
                parent.max_descendant_weight = new_weight
            else:  # weight decreased -- exhaustive search necessary
                if len(parent.children_dict.values()) >= 1:
                    temp = next(iter(parent.children_dict.values()))
                    max_weight = temp.word_weight if temp.is_word else temp.max_descendant_weight
                    for node in parent.children_dict.values():
                        max_weight = max(max_weight, node.word_weight) if node.is_word else max_weight
                        max_weight = max(max_weight, node.max_descendant_weight) if node.has_children else max_weight
                    parent.max_descendant_weight = max_weight
                else:
                    parent.max_descendant_weight = None
                    parent.has_children = False
        else:  # updated child was not the greatest descendant
            if new_weight is not None and new_weight >= previous_weight:  # weight increased or stayed the same
                parent.max_descendant_weight = max(parent.max_descendant_weight, new_weight)
            else:  # weight decreased
                return  # our work here is over
        new_parent_max_desc_weight = parent.max_descendant_weight
        _update_weight_ascend(ancestor_list_short, new_parent_max_desc_weight, previous_parent_max_desc_weight)


def _update_weight_helper(ancestor_list, weight_function):
    """
    :param ancestor_list: a linked list containing the ancestors of node, starting from node itself and ending at root;
    type = linked list
    :param weight_function: weight_function: a function that takes as an argument the current weight, and returns a new weight;
        type = int -> int
    :return: None
    """
    node = ancestor_list.pop()
    previous_weight = node.word_weight
    node.word_weight = weight_function(previous_weight)
    new_weight = node.word_weight
    _update_weight_ascend(ancestor_list, new_weight, previous_weight)


def _delete_term_helper(word, ancestor_list):
    """
    :param node: Node to delete
    :param ancestor_list: a linked list containing the ancestors of node, starting from node itself and ending at root;
    :return: None
    """
    if len(ancestor_list) == 1:  # root only
        return
    # grab the node we seek to delete, as well as its parent
    node_to_delete = ancestor_list.pop()
    # This function (like most of the others) is a glorified case analysis. First, we take cases on whether the node
    # to delete has children
    prev_word_weight = node_to_delete.word_weight
    if node_to_delete.has_children:
        node_to_delete.is_word = False
        node_to_delete.word_weight = None
        _update_weight_ascend(ancestor_list, None, prev_word_weight)
    else:
        # Now, we assume that the node to delete has no children. We recurse up the ancestor list until we find a node
        # that should be kept (is a word or has children that are words).
        parent = ancestor_list[len(ancestor_list) - 1]
        while (len(ancestor_list) >= 2) and not (parent.is_word or len(parent.children_dict) >= 2):
            ancestor_list.pop()
            parent = ancestor_list[len(ancestor_list) - 1]
            word = word[0:len(word) - 1]
        del parent.children_dict[word]
        _update_weight_ascend(ancestor_list, None, prev_word_weight)


def _prune_tree_helper(threshold, base_node, ancestor_list, node_entry):
    """
    :param threshold: the number below which we delete all terms
    :param ancestor_list: a list of ancestors of the node, starting from node.parent and ending at root. (Note: by
    "root," we do not necessarily mean the root of the entire trie. Subsets of tries can themselves be tries, and so
    we generally we use root in a relative way in recursive function calls.)
    :return:
    """
    # first, a simple optimization that will help speed up execution
    if base_node.has_children:
        if base_node.max_descendant_weight <= threshold:
            # destroy all children
            base_node.has_children = False
            base_node.children_dict = {}
            base_node.max_descendant_weight = None
    # treat words and non-words as separate cases
    if base_node.is_word:
        if base_node.word_weight <= threshold:
            # delete the node
            ancestor_list.append(base_node)
            _delete_term_helper(node_entry, ancestor_list)
        if base_node.has_children:
            # recursive call
            c_keys = list(base_node.children_dict.keys())
            for child_entry in c_keys:
                _prune_tree_helper(threshold, base_node.children_dict[child_entry],
                                   collections.deque([base_node]), child_entry)
    else:  # base_node is a non-word
        if base_node.has_children:
            # recursive call
            c_keys = list(base_node.children_dict.keys())
            for child_entry in c_keys:
                _prune_tree_helper(threshold, base_node.children_dict[child_entry],
                                   collections.deque([base_node]), child_entry)
        else:
            # delete the node
            ancestor_list.append(base_node)
            _delete_term_helper(node_entry, ancestor_list)


def _rescale_weights_helper(weight_function, node):
    # Does node have children?
    if node.has_children:
        c_keys = list(node.children_dict.keys())
        # recursively call function on every child
        for child_entry in c_keys:
            _rescale_weights_helper(weight_function, node.children_dict[child_entry])
        #  update max_descendant weight by exhaustive search, which corresponds to:
        _update_weight_ascend(collections.deque([node]), None, node.max_descendant_weight)
    # update weight, regardless of whether childless or not
    if node.is_word:
        node.word_weight = weight_function(node.word_weight)
