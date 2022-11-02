dicts = [
    {"key1": "value1"},
    {"key1": "value1"},
    {"key1": "value1"},
    {"key1": "value1"},
    {"k1": "v1", "k2": "v2", "k3": "v3"},
    {},
    {},
    {"key2": "value2"},
    {},
]

dicts_set = {tuple(item.items()) for item in dicts}
dicts_unique = [dict(item) for item in dicts_set]
print(dicts_unique)
