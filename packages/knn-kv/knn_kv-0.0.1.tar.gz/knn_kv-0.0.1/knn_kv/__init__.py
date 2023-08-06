from typing import Tuple, Dict, List, Callable
import math

#
# distance function
#


def euclidean(
    v1: List[float],
    v2: List[float]
) -> float:
    '''euclidean distance'''
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
    return math.sqrt(d)

#
# helper functions
#


def inverseweight(
    dist: float,
    num: float = 1.0,
    const: float = 0.1
) -> float:
    # inverse weight
    return num/(dist+const)


def subtractweight(
    dist: float,
    const: float = 1.0
) -> float:
    # subtract weight
    if dist > const:
        return 0
    else:
        return const-dist


def gaussian(
    dist: float,
    sigma: float = 10.0
) -> float:
    # gaussian function
    return math.e**(-dist**2/(2*sigma**2))


def getdistances(
    data: List[dict],
    vec1: List[float]
) -> List[Tuple]:
    distancelist: List[Tuple] = []
    for i in range(len(data)):
        vec2 = data[i]['features']
        distancelist.append((euclidean(vec1, vec2), i))
    distancelist.sort()
    return distancelist


#
# k-nearest neighbors algorithms
#


def knnestimate(
    data: List[dict],
    vec1: List[float],
    k: int = 3
) -> float:
    '''standart implementation of knn'''
    # get distances list
    dlist = getdistances(data, vec1)
    avg = 0.0
    # calculate average value by k-samples
    for i in range(k):
        idx = dlist[i][1]
        avg += data[idx]['result']
    avg = avg/k
    return avg


def weightedknn(
    data: List[dict],
    vec1: List[float],
    k: int = 5,
    weightf: Callable[[float], float]=gaussian
) -> float:
    '''weighted implementation of knn'''
    # get distances
    dlist: List[Tuple] = getdistances(data, vec1)
    avg: float = 0.0
    totalweight: float = 0.0

    # calculate weighted average value
    for i in range(k):
        dist = dlist[i][0]
        idx = dlist[i][1]
        weight: float = weightf(dist)
        avg += weight*data[idx]['result']
        totalweight += weight
    if totalweight == 0:
        return 0.0
    avg = avg/totalweight
    return avg
