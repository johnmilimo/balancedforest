skipped = 0

class Node(object):
    """docstring for Node"""
    def __init__(self, value, indentifier):
        super(Node, self).__init__()
        self.value = value
        self.identifier = indentifier
        self.next = None


class Graph(object):
    """docstring for Graph"""
    def __init__(self, values, edges):
        super(Graph, self).__init__()
        self.node_values = values
        self.vertices = len(values)
        self.edges = edges
        self.graph = [None] * self.vertices
        # self.edges.sort()
        self.grand_sum = sum(self.node_values)

    def build_adjacency_list(self):
        for edge in self.edges:
            fro = edge[0] - 1
            to = edge[1]- 1

            # Adding the node to the source node
            node = Node(self.node_values[to], to)
            node.next = self.graph[fro]
            self.graph[fro] = node

            # Adding the source node to the destination as 
            # it is the undirected graph 
            node = Node(self.node_values[fro], fro)
            node.next = self.graph[to]
            self.graph[to] = node

 
    def print_graph(self):
        for i in range(self.vertices):
            node = self.graph[i]
            print("Vertex:", i)
            while(node!=None):
                print(node.value, node.identifier)
                node = node.next
            print("<<"*20)

    def get_tree_nodes(self, start_node, nodes, edge, total):

        if(start_node==None):
            return nodes

        while(start_node!=None):
            if(start_node.identifier==edge[0] or start_node.identifier==edge[2] or (start_node.identifier in nodes)):
                print("skipping ", start_node.identifier)
            else:
                print("adding ", start_node.identifier)
                nodes.append(start_node.identifier)
                total[0] += start_node.value
                next_n = self.graph[start_node.identifier]
                self.get_tree_nodes(next_n, nodes, edge, total)
            start_node = start_node.next
        return nodes


    def split_and_compute_tree_sum(self, t1_nodes = [], t2_nodes = [], edge=[], ton = False):
        t1_total = 0
        t2_total = 0
        total = [0]
        
        start_node = self.graph[edge[1]]
        if(start_node.next != None):
            t2_nodes = self.get_tree_nodes(start_node, t2_nodes, edge, total)

        if(len(t2_nodes)==0 and edge[1]!=edge[2]):
            t2_nodes.append(edge[1])
            total[0] += self.node_values[edge[1]]

        t2_total = total[0]
        if(not ton and t2_total < self.grand_sum/2):
            for i in range(self.vertices):
                if(i not in t2_nodes):
                    t1_nodes.append(i)

        t1_total = self.grand_sum - t2_total

        print("t2_nodes", t2_nodes)
        print("t2_total", t2_total)

        return t1_total, t2_total


    def check(self, tree1_total, tree2_total, tree3_total):
        print("###"*10)
        print("FINAL tree1_total: ", tree1_total)
        print("FINAL tree2_total: ", tree2_total)
        print("FINAL tree3_total: ", tree3_total)
        print("###"*10)

        if (tree1_total == tree2_total) or (tree1_total == tree3_total) or (tree2_total == tree3_total):
            mx = max(tree1_total, tree2_total, tree3_total)
            if([tree1_total, tree2_total, tree3_total].count(mx) >= 2):
                ret =  mx - min(tree1_total, tree2_total, tree3_total)
                return ret, True
        return -1, False

    def split_tree_into_two(self):
        ret = -1
        found = False
        global skipped

        for entry in range(self.vertices):
            tree1_nodes = []
            tree2_nodes = []
            tree3_nodes = []
            temp_nodes = []

            n = self.graph[entry]
            while(n!=None):
                edge = [entry, n.identifier, -1]
                if(n.identifier <= entry):
                    n = n.next
                    skipped += 1
                    continue
                print("##MAIN##. SPLIT POINT EDGE: ", edge)
                tree1_nodes = []
                tree2_nodes = []
                tree1_total, tree2_total = self.split_and_compute_tree_sum(tree1_nodes, tree2_nodes, edge)
                print("ORIGINALS: ", tree1_total, tree2_total)
                if(min(tree1_total, tree2_total) < (tree1_total+tree2_total)/3):
                    n = n.next
                    continue

                if(tree1_total > tree2_total):
                    ret, found = self.find_third_tree(tree1_total, tree2_total,tree1_nodes, 1, edge[1])
                elif(tree2_total > tree1_total):
                    ret, found = self.find_third_tree(tree1_total, tree2_total,tree2_nodes, 2, edge[0])
                elif (tree1_total == tree2_total):
                    ret = tree1_total
                    found = True
                else:
                    found = True
                if(found):
                    break
                n = n.next
            if(found):
                break
        return ret


    def find_third_tree(self, tree1_total, tree2_total, nodes, t = 1, m=0):

        ret , found = -1, False
        global skipped
        consumed = []

        for i in range(len(nodes)):
            skip_n = nodes[i]
            consumed.append(skip_n)
            n = self.graph[skip_n]
            while(n!=None):
                if(n.identifier in consumed):
                    n = n.next
                    skipped += 1
                    continue
                edge = [skip_n, n.identifier, m]
                print("2. SPLIT POINT EDGE: ", edge)
                print("tree1_total",tree1_total)
                tree3_nodes = []
                temp_nodes = []
                _,tree3_total = self.split_and_compute_tree_sum(temp_nodes, tree3_nodes, edge, True)
                if(t==1):
                    ret , found = self.check(tree1_total - tree3_total, tree2_total, tree3_total)
                elif(t==2):
                    ret , found = self.check(tree1_total, tree2_total - tree3_total, tree3_total)
                if(found):
                    break
                n = n.next
            if(found):
                break

        return ret, found


def balancedForest(values, edges):
    mygraph = Graph(values, edges)
    mygraph.build_adjacency_list()
    mygraph.print_graph()
    return mygraph.split_tree_into_two()

import unittest

class BalancedForestTest(unittest.TestCase):
    def test1(self):
        expected = 10
        c = [1, 1, 1, 18, 10, 11, 5, 6]
        edges = [[1, 2], [1, 4], [2, 3], [1, 8], [8, 7], [7, 6], [5, 7]]
        self.assertEqual(balancedForest(c, edges), expected)

    def test2(self):
        expected = 13
        c = [12, 7, 11, 17, 20, 10]
        edges = [[1, 2], [2, 3], [4, 5], [6, 5], [1, 4]]

        self.assertEqual(balancedForest(c, edges), expected)

    def test3(self):
        expected = 19
        c = [15, 12, 8, 14, 13]
        edges = [[4,5],[1,2],[1,3],[1,4]]
        self.assertEqual(balancedForest(c, edges), expected)

    def test4(self):
        expected = 2
        c = [1,2,2,1,1]
        edges = [[1,2],[1,3],[3,5],[1,4]]
        self.assertEqual(balancedForest(c, edges), expected)

    def test5(self):
        expected = -1
        c = [1,3,5]
        edges = [[1,3],[1,2]]
        self.assertEqual(balancedForest(c, edges), expected)

    def test6(self):
        expected = -1
        c = [7, 7, 4, 1, 1, 1]
        edges = [(1, 2), (3, 1), (2, 4), (2, 5), (2, 6)]
        self.assertEqual(balancedForest(c, edges), expected)

    def test7(self):
        expected = 0
        c = [1, 3, 4, 4]
        edges = [(1, 2), (1, 3), (1, 4)]
        self.assertEqual(balancedForest(c, edges), expected)

    def test8(self):
        expected = 297
        c = [100, 99, 98, 100, 99, 98]
        edges = [[1, 2], [2, 3], [4, 5], [6, 5], [1, 4]]
        self.assertEqual(balancedForest(c, edges), expected)

    def test9(self):
        expected = 4
        c = [12, 10, 8, 12, 14, 12]
        edges = [[1, 2], [1, 3], [1, 4], [2, 5], [4, 6]]
        self.assertEqual(balancedForest(c, edges), expected)

        print("SKIPPED", skipped)


if __name__ == '__main__':
    unittest.main()