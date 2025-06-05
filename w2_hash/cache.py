import sys
import hash_table

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        #------------------------#
        self.size = n
        self.hash = hash_table.HashTable(2 * n)
        # make a queue to record the history
        self.history = [] 
        #------------------------#
        pass

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        #------------------------#
        assert(type(url) == str)
        bucket_index = hash_table.calculate_hash(url) % self.hash.bucket_size
        page = self.hash.buckets[bucket_index]
        # if page is in the cache, no change in hashtable
        while page:
            if page.key == url:
                # put url into the history
                self.history.append(url)
                # access the page
                return contents
            page = page.next
        # page is not in the cache
        ## if there is space, just insert the new url
        if self.hash.item_count < self.size :
            self.history.append(url)
            page_new = hash_table.Item(url, contents, self.hash.buckets[bucket_index])
            self.hash.item_count += 1
            self.hash.buckets[bucket_index] = page_new
            return contents

        # else: if there is no space, delete the oldest url and insert the new url
        ## find the oldest one
        ## get the latest index of pages in hashtable
        hashtable_index_in_reversed_history = []
        reversed_history = list(reversed(self.history))
        # search for all pages in hashtable
        for bucket_index in range(len(self.hash.buckets)):
            if self.hash.buckets[bucket_index]:
                page = self.hash.buckets[bucket_index]
                while page: 
                    # find the page in the reversed_history from scratch
                    i = 0
                    while i >= 0 and i < len(self.history):
                        if reversed_history[i] == page.key:
                            hashtable_index_in_reversed_history.append(i)
                            # quit if the latest(smallest) index is found
                            i = -1 
                        else: i += 1
                    page = page.next
        hashtable_index_in_reversed_history.sort()

        ## delete the oldest one
        self.hash.delete(reversed_history[hashtable_index_in_reversed_history[self.size - 1]]) 

        ## insert the new page
        bucket_index = hash_table.calculate_hash(url) % self.hash.bucket_size
        page_new = hash_table.Item(url, contents, self.hash.buckets[bucket_index])
        self.hash.buckets[bucket_index] = page_new
        self.hash.item_count += 1
        ## update the history
        self.history.append(url)
        return contents
        #------------------------#

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        #------------------------#
        ans_index_in_reversed_history = []
        reversed_history = list(reversed(self.history)) # list() is needed here!!
        ## get the latest index of all pages in hashtable
        for bucket_index in range(len(self.hash.buckets)):
            if self.hash.buckets[bucket_index]:
                page = self.hash.buckets[bucket_index]
                i = 0
                while i >= 0 and i < len(self.history):
                    if reversed_history[i] == page.key:
                        ans_index_in_reversed_history.append(i)
                        ## quit if the smallest index is found
                        i = -1
                    else: i += 1
        # most recently accessed URL has the smallest index
        ans_index_in_reversed_history.sort()
        ans = []
        for index in ans_index_in_reversed_history:
            ans.append(reversed_history[index])
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