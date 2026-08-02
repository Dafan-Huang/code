users = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Carol', 'age': 28},
]

# 按年龄排序——临时写个 lambda 当 key
sorted_users = sorted(users, key=lambda u: u['age'])

for u in sorted_users:
    print(u['name'], u['age'])