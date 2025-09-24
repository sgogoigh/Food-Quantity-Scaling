from runner import scale_recipe, load_from_file

data = load_from_file("paneer_recipes.json")

while True:
    try:
        choice = int(input("Enter 1 for Palak Paneer,\n 2 for Matar Paneer,\n 3 for Shahi Paneer or\n 4 for Paneer Masala: "))
        if choice not in [1, 2, 3, 4]:
            raise EOFError("jhfjfh")
        break
    except Exception as e:
        print("Wrong input!")

while True:
    try:
        people_number = int(input("Enter no. of people you want to serve: "))
        if people_number <= 0:
            raise EOFError("hgfhfg")
        break
    except Exception as e:
        print("Need positive int input!")

# Scale palak paneer from sizes 1&3 to serve 6 people
lists = {
    1 : "palak_paneer",
    2 : "matar_paneer",
    3 : "shahi_paneer",
    4 : "paneer_masala"
}
choice = lists[choice]

from scaling_policy import select_optimal_sizes
size1, size2 = select_optimal_sizes(people_number)

scaled_ingredients = scale_recipe(data, choice, size1, size2, people_number)

print(f"The Scaled Ingredients you need for {choice} are : ")
print(scaled_ingredients)
