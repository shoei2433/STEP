import sys
import collections
import time

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def get_id_from_title(self, title):
        return [id for id in self.titles.keys() if self.titles[id] == title]

    def find_shortest_path(self, start, goal):
        # start_idを見つける
        if len(self.get_id_from_title(start)) == 1:
            for id in self.get_id_from_title(start):
                start_id = id
        else: 
            # 複数idが存在する
            print("Error")
        # goal_idを見つける
        if len(self.get_id_from_title(goal)) == 1:
            for id in self.get_id_from_title(goal):
                goal_id = id
        else: 
            # 複数idが存在する
            print("Error")
        # 探索する予定のノード
        found_list = collections.deque(self.links[start_id])
        # 探索済みのノード: {探索中のノード : 1個前のノード} の辞書
        visited_dict = {} 
        ## 見つけたらすぐにvisited_listに入れる -> found_listに同じpageが二回入ることがない
        for page in found_list:
            visited_dict[page] = start_id
        # BFS
        shortest_path = collections.deque([])
        while found_list:
            page = found_list.popleft()
            for page_next in self.links[page]:
                if page_next not in visited_dict.keys():
                    found_list.append(page_next)
                    visited_dict[page_next] = page
                # goalが見つかった
                if page_next == goal_id:
                    while page_next != start_id:
                        shortest_path.appendleft(self.titles[page_next])
                        page_next = visited_dict[page_next] 
                    shortest_path.appendleft(start)
                    print("The shortest path is:")
                    for page_title in shortest_path:
                        print(page_title)
                    return 0
                        

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        # 初期化
        page_score = {}
        for id in self.titles.keys():
            page_score[id] = 1
        # 変化分を記録
        page_score_diff = 1 * len(self.titles.keys())
        
        start_time = time.time() 

        while page_score_diff > 0.01:
            # 変化量が十分小さくなるまで繰り返す

            # method1: わかりやすい方法 time = 132.6
            # 自分の点数を隣接ノードに割り当てる
            ## 新しい点数dictの初期化
            page_score_new = {}
            for id in self.titles.keys():
                page_score_new[id] = 0.15 
            score_isolation = 0
            ## 割り当て
            for id in self.titles.keys():
                next_pages = self.links[id]
                if len(next_pages) > 0:
                    # 行き先が少なくとも1つあるとき
                    score = 0.85 * page_score[id] / len(next_pages)
                    for page in next_pages:
                        page_score_new[page] += score
                else: 
                    # 行き先がないとき
                    score_isolation += 0.85 * page_score[id] / len(self.titles.keys()) 
            for id in self.titles.keys():
                page_score_new[id] += score

            # # method2: 最後に規格化をする場合 time = 138.2
            # ## 自分の点数を隣接ノードに割り当てる
            # ## 新しい点数dictの初期化
            # page_score_new = {}
            # for id in self.titles.keys():
            #     page_score_new[id] = 0
            # ## 割り当て
            # for id in self.titles.keys():
            #     next_pages = self.links[id]
            #     if len(next_pages) > 0:
            #         # 行き先が少なくとも1つあるとき
            #         for page in next_pages:
            #             score = 0.85 * page_score[id] / len(next_pages)
            #             page_score_new[page] += score
            # ## 規格化
            # sum = 0
            # for id in self.titles.keys():
            #     sum +=  page_score_new[id]
            # score_for_all_nodes = 1 - sum / len(self.titles.keys())
            # for id in self.titles.keys():
            #     page_score_new[id] = page_score_new[id] + score_for_all_nodes
            
            # 変化量の計算
            page_score_diff = 0
            for id in self.titles.keys():
                page_score_diff += (page_score_new[id]  - page_score[id])**2
            print(page_score_diff)

            ## 点数の更新
            page_score = page_score_new

        end_time = time.time()  

        # PageRankでsortしたものを返す
        sorted_page_score = sorted(page_score.items(), key=lambda x: x[1], reverse=True)
        print("The most popular pages are:")
        for i in range(10):
            id = sorted_page_score[i][0]
            score = sorted_page_score[i][1]
            print(self.titles[id], score) 
        
        print(end_time - start_time)

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        # start_idを見つける
        if len(self.get_id_from_title(start)) == 1:
            for id in self.get_id_from_title(start):
                start_id = id
        else: 
            # 1対1対応できていない
            print("Error")
        # goal_idを見つける
        if len(self.get_id_from_title(goal)) == 1:
            for id in self.get_id_from_title(goal):
                goal_id = id
        else: 
            # 1対1対応できていない
            print("Error")
        
        # 探索する予定のノード
        found_list = collections.deque(self.links[start_id])
        found_dict = {}
        for page in self.links[start_id]:
            found_dict[page] = start_id
        # 探索済みのノード
        visited_list = collections.deque([])

        # DFS
        longest_path = collections.deque([])
        n = 0
        while found_list and n < 1000:
            page = found_list.pop()
            visited_list.append(page)
            for page_next in self.links[page]:
                if page_next not in visited_list and page_next != goal_id:
                    found_list.appendleft(page)
                    found_dict[page_next] = page
                # goalが見つかった
                if page_next == goal_id:
                    longest_path_new = collections.deque([])
                    print(n)
                    while page_next != start_id:
                        longest_path_new.appendleft(self.titles[page_next])
                        page_next = found_dict[page_next] 
                    longest_path_new.appendleft(start)
                    if len(longest_path_new) > len(longest_path):
                        n += 1
                        longest_path = longest_path_new
            
        print("The longest path is:")
        print(len(longest_path))
        for page_title in longest_path:
            print(page_title)
        return 0

        
    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # # Example
    # wikipedia.find_longest_titles()
    # # Example
    # wikipedia.find_most_linked_pages()
    # # Homework #1
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # # wikipedia.find_shortest_path("A", "C")
    # # Homework #2
    # wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
