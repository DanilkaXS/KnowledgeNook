# fruits = {
#     "apple": 42,
#     "banana": 30,
#     "mandarine": 50,
#     "dga": 50,
#     "asdg": 34,
#     "ergr": 2,
#     ",yu": 234,
#     "maegyu,ndarine": 547,
#     "puo/": 123,
#
# }
#
# filtered_dict = {fruit: cl for fruit, cl in fruits.items() if cl < 100}
#
# print(filtered_dict)
# for key, value in fruits.items():
#     if key == "apple":
#         fruits[key] *= 3
#     print(key, value)

# print(fruits["apple"])

# students = [
#     {"name": "Danil", "age": 20, "grades": {"Math": [12, 1, 1, 2, 3, 4], "Chemistry": [3, 5, 6, 3, 2, 3, 7]}},
#     {"name": "ST2", "age": 17, "grades": {"Math": [12, 2, 13, 2, 7, 6], "Chemistry": [3, 5, 6, 3, 2, 3, 7]}},
#     {"name": "ST3", "age": 32, "grades": {"Math": [12, 3, 12, 5, 3, 4], "Chemistry": [3, 5, 6, 3, 2, 3, 7]}},
#     {"name": "ST5", "age": 43, "grades": {"Math": [12, 4, 11, 8, 8, 5], "Chemistry": [3, 5, 6, 3, 2, 3, 7]}},
# ]
#
# ########################################## TASK 1 ###############################################
# print(f"{'#'*20} Students {'#'*20}")
# for i in students:
#     print(f"Name:\t{i['name']}")
#     print(f"Age:\t{i['age']}")
#     print(f"grades:")
#     for k, v in i["grades"].items():
#         print(f"\t{k}: {' '.join([str(value) for value in v])}")
#     print("\n")
# ########################################## TASK 2 ###############################################
# print(f"{'#'*20} Students {'#'*20}")
# for i in students:
#     print(f"Name:\t{i['name']}")
#     print(f"Age:\t{i['age']}")
#     print(f"grades:")
#     for k, v in i["grades"].items():
#         print(f"\t{k} AVG: {sum(v)/len(v)}")
#     print("\n")

# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
# user_number = int(input("Enter your number: "))
#
# if user_number in numbers:
#     print("Number correct")
# else:
#     print("Incorrect number")

# user = {
#     "name": "Danil",
#     "surname": "nnnn",
#     "age": 0
# }
#
# if "age" in user:
#     print(user["name"], user["age"])
# else:
#     print(user["name"])

# password = input("Enter your password 😀: ")
#
# if len(password) < 6:
#     print("Less")
# else:
#     print("Strong")

# post_ukr = ["Kiev", "Odesa", "Irpin", "Fastiv"]
# post_np = ["Kiev", "Odesa", "Irpin", "Fastiv", "Boyarka", "Gatne"]
# letter_limit = 3
#
# user_city = input("Enter your city 🙄 🚚: ")
# if len(user_city) < letter_limit:
#     print("Enter full city name!😪")
# else:
#     is_post_ukr = user_city in post_ukr
#     is_post_np = user_city in post_np
#
# if is_post_np or is_post_ukr:
#     if is_post_np:
#         print("Nova post delivery available! 😁")
#     if is_post_ukr:
#         print("Ukrpost delivery available! 😁")
# else:
#     print("Delivery is not available 😭")

# numbers = [3, 45, 6, 3, 2, 6, 8, 3, 7, 943, 34567]
#
# numbers = sorted(numbers)
# numbers = reversed(numbers)
#
# for n in numbers:
#     print(n)











