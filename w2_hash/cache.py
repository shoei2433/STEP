import sys
import hash_table

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

# An item object that represents one key - value pair in the hash table.
class Item_for_doubly_linked_list:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, url = "", contents = "", prev = None, next = None):
        assert type(url) == str
        self.url = url
        self.contents = contents
        self.prev = prev
        self.next = next

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        #------------------------#
        self.size = n
        self.hash = hash_table.HashTable(2 * n) # key: url, value: Item_for_doubly_linked_list()
        self.history_oldest = Item_for_doubly_linked_list()
        self.history_newest = Item_for_doubly_linked_list()
        #------------------------#
        pass

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        #------------------------#
        assert(type(url) == str)
        access_item = self.hash.get(url)[0]
        if access_item is not None:
            # page is in the cache -> no change in hashtable
            # update the history 
            ## delete the old item
            if access_item.prev.prev is None:
                # access_item is the oldest one in the history
                access_item.next.prev = self.history_oldest
                self.history_oldest.next = access_item.next
            elif access_item.next.next is None:
                # access_item is the newest one in the history
                access_item.prev.next = self.history_newest
                self.history_newest.prev = access_item.prev
            else:
                # access_item is at the middle in the history
                access_item.prev.next = access_item.next
                access_item.next.prev = access_item.prev
            ## put the item at the newest
            access_item.prev = self.history_newest.prev
            self.history_newest.prev.next = access_item
            self.history_newest.prev = access_item
            access_item.next = self.history_newest
        elif self.hash.item_count < self.size:
            # page is not in the cache, but there is enough space to put new page
            ## update the history
            new_item = Item_for_doubly_linked_list(url, contents, self.history_newest.prev, self.history_newest)
            if self.history_newest.prev is not None:
                # history is not empty
                self.history_newest.prev.next = new_item
                self.history_newest.prev = new_item
            else:
                # history is empty
                new_item.prev = self.history_oldest
                self.history_newest.prev = new_item
                self.history_oldest.next = new_item
            ## put the item into the hash
            self.hash.put(url, new_item)
        else: 
            # page is not in the cache, and there no space to put new page
            ## update the history
            ## delete the oldest one from the hashtable
            self.hash.delete(self.history_oldest.next.url)
            ## delete the oldest one from the history
            self.history_oldest.next.next.prev = self.history_oldest
            self.history_oldest.next = self.history_oldest.next.next
            ## put the item at the newest
            new_item = Item_for_doubly_linked_list(url, contents, self.history_newest.prev, self.history_newest)
            self.history_newest.prev.next = new_item
            self.history_newest.prev = new_item
            ## put the item into the hash
            self.hash.put(url, new_item)
        return contents
        #------------------------#

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        #------------------------#
        ans = []
        if self.history_newest.prev is None: 
            # history is not empty
            return ans
        # history is not empty
        item_in_history = self.history_newest.prev
        while item_in_history.prev is not None:
            ans.append(item_in_history.url)
            item_in_history = item_in_history.prev
        return ans
        #------------------------#
        

def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()