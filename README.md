### The Ripple-Spreading Algorithm for the Fuzzy Multi-Objective Path Optimization Problem

##### Reference: Ma Y M, Hu X B, Zhou H. A deterministic and nature-inspired algorithm for the fuzzy multi-objective path optimization problem[J]. Complex & Intelligent Systems, 2022, accepted.

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node1: {node2: [c1, c2, ... (crisp weights)], [f1, f2, ... (fuzzy weights)], ...}, ...} |
| s_network     | The network described by a crisp weight on which we conduct the ripple relay race |
| source        | The source node                                              |
| destination   | The destination node                                         |
| nn            | The number of nodes                                          |
| n_cirsp       | The number of crisp weights                                  |
| n_fuzzy       | The number of fuzzy weights                                  |
| f             | f = 3: triangular fuzzy number, f = 4: trapezoidal fuzzy number |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the i-th ripple is epicenter_set[i] |
| path_set      | List, the path of the i-th ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the i-th ripple is radius_set[i]         |
| active_set    | List, active_set contains all active ripples                 |
| objective_set | List, the objective value of the traveling path of the i-th ripple is objective_set[i] |
| Omega         | Dictionary, Omega[n] = i denotes that ripple i is generated at node n |

#### Example

|  Arc  | Crisp 1 | Crisp 2 |   Fuzzy 1    |   Fuzzy 2    |
| :---: | :-----: | :-----: | :----------: | :----------: |
|  0-1  |    8    |    1    |  (4, 7, 15)  | (12, 19, 20) |
|  0-2  |    4    |    5    | (8, 12, 17)  | (6, 14, 15)  |
|  0-4  |    9    |    7    | (14, 15, 19) | (2, 19, 20)  |
|  1-3  |    2    |    2    | (8, 14, 16)  | (2, 19, 20)  |
|  1-4  |    6    |    8    |  (2, 5, 13)  | (2, 10, 12)  |
|  2-4  |    5    |    8    | (13, 18, 19) |  (5, 9, 13)  |
|  2-5  |    8    |    1    |  (7, 8, 13)  | (2, 10, 11)  |
|  3-4  |    6    |    2    | (14, 17, 20) | (7, 11, 20)  |
|  3-6  |    4    |    5    |  (4, 6, 17)  | (2, 12, 16)  |
|  4-6  |    6    |    9    |  (4, 7, 11)  | (7, 10, 20)  |
|  4-7  |    4    |    3    | (2, 11, 12)  | (17, 19, 20) |
|  4-9  |    9    |    7    |  (2, 5, 16)  | (6, 10, 20)  |
|  5-4  |    9    |    4    |  (2, 3, 17)  | (2, 11, 20)  |
|  5-7  |    4    |    3    | (8, 15, 20)  | (5, 11, 19)  |
|  6-8  |    6    |    8    |  (8, 9, 17)  |  (5, 6, 11)  |
|  6-9  |    4    |    7    | (3, 12, 15)  | (6, 12, 17)  |
|  7-9  |    9    |    2    | (5, 15, 19)  | (11, 14, 19) |
| 7-10  |    1    |    6    | (9, 10, 14)  |  (7, 9, 12)  |
|  8-9  |    3    |    8    | (2, 11, 18)  | (5, 12, 19)  |
| 8-11  |    7    |    1    | (6, 11, 20)  |  (4, 9, 19)  |
| 9-11  |    9    |    6    | (10, 18, 19) |  (2, 3, 7)   |
| 10-9  |    5    |    3    |  (4, 8, 16)  | (9, 13, 19)  |
| 10-11 |    9    |    2    |  (4, 7, 19)  | (5, 13, 16)  |



```python
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
    print(result_RSA[11])  # all Pareto-optimal paths from the source node to node 11
```

##### Output:

```python
[
    {'path': [0, 4, 7, 10, 11], 'objective': [23, 18, [29, 43, 64], [31, 60, 68]]}, 
    {'path': [0, 2, 5, 7, 10, 11], 'objective': [26, 17, [36, 52, 83], [25, 57, 73]]}, 
    {'path': [0, 4, 9, 11], 'objective': [27, 20, [26, 38, 54], [10, 32, 47]]}, 
    {'path': [0, 1, 3, 6, 8, 11], 'objective': [27, 17, [30, 47, 85], [25, 65, 86]]}, 
    {'path': [0, 1, 3, 4, 7, 10, 11], 'objective': [30, 16, [41, 66, 96], [50, 90, 108]]}, 
    {'path': [0, 4, 7, 9, 11], 'objective': [31, 18, [31, 59, 69], [32, 55, 66]]}, 
    {'path': [0, 2, 5, 7, 9, 11], 'objective': [34, 17, [38, 68, 88], [26, 52, 71]]}, 
    {'path': [0, 1, 3, 4, 7, 9, 11], 'objective': [38, 16, [43, 82, 101], [51, 85, 106]]}
]
```

