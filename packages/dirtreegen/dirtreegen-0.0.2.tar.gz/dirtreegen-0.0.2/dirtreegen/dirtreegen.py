# -*- coding: utf-8 -*-
# @Time         : 2018/11/26 下午5:52
# @Author       : luoyeqi
# @Email        : luoyeqi@duoshoubang.cn
# @FileName     : dirtreegen.py
# @Description  :

from anytree import Node, RenderTree
import os

def nodeLink(parent, children):
    """Associate a child node in the list with a parent node

    :param parent: Parent root
    :param lists: A list of child node
    :return: None
    """
    for child in children:
        Node(child, parent=parent)


def nodeMap(IGNORE=None):
    """Combine all nodes

    :return: Combined root directory
    """
    root = Node('.')
    nodes = {}
    for roots, dirs, files in os.walk('.'):
        temp = roots.split('/')
        if IGNORE:
            isRoot = [i for i in IGNORE if i in temp]
            files = [f for f in files if f not in IGNORE]
        else:
            isRoot = False
        if not isRoot:
            if len(temp) == 1:
                nodeLink(root, files)
                nodes.setdefault(temp[-1], root)
            else:
                for i in range(1, len(temp)):
                    prename = temp[i-1]
                    nowname = temp[i]
                    if nowname not in nodes:
                        new = Node(temp[1], nodes[prename])
                        nodeLink(new, files)
                        nodes.setdefault(temp[i], new)
    return root

def treegen(IGNORE=None):
    """print directory tree

    :return: None
    """
    root = nodeMap(IGNORE)
    for pre, fill, node in RenderTree(root):
        print('%s%s' % (pre, node.name))


