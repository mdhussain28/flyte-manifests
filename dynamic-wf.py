from typing import List, Tuple
from flytekit import task, workflow, dynamic

@task
def split(numbers: List[int]) -> Tuple[List[int], List[int]]:
    length = len(numbers)
    return (
        numbers[0 : int(length / 2)],
        numbers[int(length / 2) :],
    )

@task
def merge(sorted_list1: List[int], sorted_list2: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(sorted_list1) and j < len(sorted_list2):
        if sorted_list1[i] < sorted_list2[j]:
            result.append(sorted_list1[i])
            i += 1
        else:
            result.append(sorted_list2[j])
            j += 1
    result.extend(sorted_list1[i:])
    result.extend(sorted_list2[j:])
    return result

@task
def sort_locally(numbers: List[int]) -> List[int]:
    return sorted(numbers)

@dynamic
def merge_sort_remotely(numbers: List[int], threshold: int) -> List[int]:
    split1, split2 = split(numbers=numbers)
    sorted1 = merge_sort(numbers=split1, threshold=threshold)
    sorted2 = merge_sort(numbers=split2, threshold=threshold)
    return merge(sorted_list1=sorted1, sorted_list2=sorted2)

@dynamic
def merge_sort(numbers: List[int], threshold: int = 5) -> List[int]:
    if len(numbers) <= threshold:
        return sort_locally(numbers=numbers)
    else:
        return merge_sort_remotely(numbers=numbers, threshold=threshold)

@workflow
def merge_sort_wf(numbers: List[int], threshold: int = 5) -> List[int]:
    return merge_sort(numbers=numbers, threshold=threshold)
