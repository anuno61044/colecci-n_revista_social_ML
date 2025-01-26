import random

def get_random_partition(items, partition_ratio : float) -> list:
    random_partitions = []
    
    items_length = len(items)
    items_indices = {}
    for i, item in enumerate(items):
        items_indices[item] = i
    item_mask = [1 for _ in items]

    for k in _get_subsets_lengths(partition_ratio, items_length):
        subset = random.sample(population=items, counts=item_mask, k=k)
        for item in subset:
            i = items_indices[item]
            item_mask[i] = 0
        random_partitions.append(subset)

    return random_partitions

def _get_subsets_lengths(sample_ratio : float, length : int):
    assert 0 < sample_ratio <= 1, '0 < sample_ratio <= 1'
    assert length > 0, 'length > 0'
    
    base_sample = int(length * sample_ratio)
    for _ in range(int(length / base_sample) - 1):
        yield base_sample
    yield base_sample + length % base_sample