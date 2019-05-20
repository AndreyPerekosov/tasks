# with open("input.txt",  encoding="utf-8") as f:
#     for line in f:
#         print(line.strip())

all_users  = [1, 5, 7, 8, 2, 100, 34]        
for index in range(1, len(all_users)):
    min_ = index
    while min_ > 0 and all_users[min_-1] < all_users[min_]:
        all_users[min_ - 1], all_users[min_] = all_users[min_], all_users[min_ - 1]
        min_ -= 1
print(all_users)         