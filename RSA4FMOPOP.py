#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/10 11:30
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA4FMOPOP.py
# @Statement : The ripple-spreading algorithm for the fuzzy multi-objective path optimization problem
# @Reference : Ma, YM., Hu, XB. & Zhou, H. A deterministic and nature-inspired algorithm for the fuzzy multi-objective path optimization problem. Complex Intell. Syst. (2022). https://doi.org/10.1007/s40747-022-00825-3
import copy
import fuzzy_distance as dis


def find_neighbor(network):
    """
    find the neighbor of each node
    :param network:
    :return: [[the neighbors of node1], [the neighbors of node 2], ...]
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor, n_crisp):
    """
    find the ripple-spreading speed
    :param network:
    :param neighbor:
    :param n_crisp:
    :return: v: speed, s_network: the ripple-spreading network
    """
    min_value = [10e6 for i in range(n_crisp)]
    max_value = [0 for i in range(n_crisp)]
    s_network = copy.deepcopy(network)
    for i in range(len(network)):
        for j in neighbor[i]:
            temp_obj = network[i][j][0]
            for k in range(n_crisp):
                min_value[k] = min(min_value[k], temp_obj[k])
                max_value[k] = max(max_value[k], temp_obj[k])
    max_min = [max_value[i] / min_value[i] for i in range(n_crisp)]
    best_index = max_min.index(min(max_min))
    for i in range(len(network)):
        for j in neighbor[i]:
            s_network[i][j] = network[i][j][0][best_index]
    return min_value[best_index], s_network


def pareto_dominated(obj1, obj2, n_fuzzy, f):
    """
    judge whether obj1 is Pareto dominated by obj2
    :param obj1:
    :param obj2:
    :param n_fuzzy:
    :param f:
    :return:
    """
    sum_less = 0
    for i in range(n_fuzzy):
        if obj1[i] < obj2[i]:
            return False
        elif obj1[i] > obj2[i]:
            sum_less += 1
    for i in range(n_fuzzy, len(obj1)):
        temp_obj1 = obj1[i]
        temp_obj2 = obj2[i]
        mn = [min(temp_obj1[n], temp_obj2[n]) for n in range(f)]
        if f == 3:
            dis1 = dis.dis3(mn, temp_obj1)
            dis2 = dis.dis3(mn, temp_obj2)
        else:
            dis1 = dis.dis4(mn, temp_obj1)
            dis2 = dis.dis4(mn, temp_obj2)
        if dis1 < dis2:
            return False
        elif dis1 > dis2:
            sum_less += 1
    if sum_less != 0:
        return True
    return False


def pareto_non_domination(incoming_ripples, n_fuzzy, f):
    """

    :param incoming_ripples:
    :param n_fuzzy:
    :param f:
    :return:
    """
    non_domination_ripples = []
    for i in range(len(incoming_ripples)):
        flag = True
        obj1 = incoming_ripples[i]['objective']
        for j in range(len(incoming_ripples)):
            if i != j:
                if pareto_dominated(obj1, incoming_ripples[j]['objective'], n_fuzzy, f):
                    flag = False
                    break
        if flag:
            non_domination_ripples.append(incoming_ripples[i])
    return non_domination_ripples


def find_POR(incoming_ripples, omega, objective_set, n_fuzzy, f):
    """
    find new PORs
    :param incoming_ripples:
    :param omega:
    :param objective_set:
    :param n_fuzzy:
    :param f:
    :return:
    """
    new_POR = []
    non_domination_ripples = pareto_non_domination(incoming_ripples, n_fuzzy, f)
    if not omega:
        return non_domination_ripples
    else:
        objectives = [objective_set[ripple] for ripple in omega]
        num_ripples = len(non_domination_ripples)
        for i in range(num_ripples):
            flag = True
            obj1 = non_domination_ripples[i]['objective']
            for j in range(len(objectives)):
                if pareto_dominated(obj1, objectives[j], n_fuzzy, f):
                    flag = False
                    break
            if flag:
                new_POR.append(non_domination_ripples[i])
    return new_POR


def main(network, source):
    """
    the main function
    :param network: {node1: {node2: [c1, c2, ... (crisp weights)], [f1, f2, ... (fuzzy weights)], ...}, ...}
    :param source: the source node
    :return:
    """
    # Step 1. Initialization
    neighbor = find_neighbor(network)
    temp_node = neighbor[source][0]  # a neighbor of the source node
    n_crisp = len(network[source][temp_node][0])  # the number of crisp weights
    n_fuzzy = len(network[source][temp_node][1])  # the number of fuzzy weights
    n_obj = n_crisp + n_fuzzy  # the number of objectives
    f = len(network[source][temp_node][1][0])  # f = 3: triangular, f = 4: trapezoidal
    nn = len(neighbor)  # node number
    v, s_network = find_speed(network, neighbor, n_crisp)
    epicenter_set = []  # epicenter set
    active_set = []  # the set containing all active ripples
    path_set = []  # path set
    objective_set = []  # objective value set
    radius_set = []  # radius set
    nr = 0  # the number of ripples - 1
    t = 0  # time
    omega = {}  # the ever generated ripple at each node
    for node in range(nn):
        omega[node] = []

    # Step 2. Initialize the first ripple
    epicenter_set.append(source)
    radius_set.append(0)
    active_set.append(nr)
    omega[source].append(nr)
    path_set.append([source])
    temp_list = []
    for i in range(n_obj):
        if i < n_crisp:
            temp_list.append(0)
        else:
            temp_list.append([0 for n in range(f)])
    objective_set.append(temp_list)
    nr += 1

    # Step 3. The main loop
    while active_set:

        # Step 3.1. Time updates
        t += 1
        incoming_ripples = {}
        remove_ripples = []
        for ripple in active_set:
            flag_inactive = True

            # Step 3.2. Active ripples spread out
            radius_set[ripple] += v

            # Step 3.3. New incoming ripples
            epicenter = epicenter_set[ripple]
            radius = radius_set[ripple]
            path = path_set[ripple]
            obj = objective_set[ripple]
            for node in neighbor[epicenter]:
                temp_length = s_network[epicenter][node]
                if node not in path and temp_length <= radius < temp_length + v:
                    temp_path = copy.deepcopy(path)
                    temp_path.append(node)
                    temp_obj = copy.deepcopy(obj)
                    temp_crisp = network[epicenter][node][0]
                    temp_fuzzy = network[epicenter][node][1]
                    for i in range(n_obj):
                        if i < n_crisp:
                            temp_obj[i] += temp_crisp[i]
                        else:
                            temp_obj[i] = [temp_fuzzy[i - n_crisp][k] + temp_obj[i][k] for k in range(f)]
                    if node in incoming_ripples.keys():
                        incoming_ripples[node].append({
                            'path': temp_path,
                            'objective': temp_obj,
                            'radius': radius - s_network[epicenter][node],
                        })
                    else:
                        incoming_ripples[node] = [{
                            'path': temp_path,
                            'objective': temp_obj,
                            'radius': radius - s_network[epicenter][node],
                        }]

                # Step 3.4. Active -> inactive
                if radius < temp_length:
                    flag_inactive = False
            if flag_inactive:
                remove_ripples.append(ripple)
        for ripple in remove_ripples:
            active_set.remove(ripple)

        # Step 3.5. Generate new ripple
        for node in incoming_ripples.keys():
            new_ripples = find_POR(incoming_ripples[node], omega[node], objective_set, n_fuzzy, f)
            for ripple in new_ripples:
                path_set.append(ripple['path'])
                objective_set.append(ripple['objective'])
                radius_set.append(ripple['radius'])
                active_set.append(nr)
                epicenter_set.append(node)
                omega[node].append(nr)
                nr += 1

    # Step 4. Sort the results
    result = {}
    for i in range(nn):
        result[i] = []
        for ripple in omega[i]:
            result[i].append({
                'path': path_set[ripple],
                'objective': objective_set[ripple],
            })
    return result


if __name__ == '__main__':
    test_network = {0: {1: [[8, 1], [[4, 7, 15], [12, 19, 20]]], 2: [[4, 5], [[8, 12, 17], [6, 14, 15]]],
                        4: [[9, 7], [[14, 15, 19], [2, 19, 20]]]},
                    1: {3: [[2, 2], [[8, 14, 16], [2, 19, 20]]], 4: [[6, 8], [[2, 5, 13], [2, 10, 12]]]},
                    2: {4: [[5, 8], [[13, 18, 19], [5, 9, 13]]], 5: [[8, 1], [[7, 8, 13], [2, 10, 11]]]},
                    3: {4: [[6, 2], [[14, 17, 20], [7, 11, 20]]], 6: [[4, 5], [[4, 6, 17], [2, 12, 16]]]},
                    4: {6: [[6, 9], [[4, 7, 11], [7, 10, 20]]], 7: [[4, 3], [[2, 11, 12], [17, 19, 20]]],
                        9: [[9, 7], [[2, 5, 16], [6, 10, 20]]]},
                    5: {4: [[9, 4], [[2, 3, 17], [2, 11, 20]]], 7: [[4, 3], [[8, 15, 20], [5, 11, 19]]]},
                    6: {8: [[6, 8], [[8, 9, 17], [5, 6, 11]]], 9: [[4, 7], [[3, 12, 15], [6, 12, 17]]]},
                    7: {9: [[9, 2], [[5, 15, 19], [11, 14, 19]]], 10: [[1, 6], [[9, 10, 14], [7, 9, 12]]]},
                    8: {9: [[3, 8], [[2, 11, 18], [5, 12, 19]]], 11: [[7, 1], [[6, 11, 20], [4, 9, 19]]]},
                    9: {11: [[9, 6], [[10, 18, 19], [2, 3, 7]]]},
                    10: {9: [[5, 3], [[4, 8, 16], [9, 13, 19]]], 11: [[9, 2], [[4, 7, 19], [5, 13, 16]]]},
                    11: {}}

    source = 0
    result_RSA = main(test_network, source)
    print(result_RSA[11])
