import random

computer = random.choice([-1, 0, 1])
youstr = input("Enter the your choice:")
youdict = {"s": -1, "w": 0, "g": 1}
revdict = {1: "Gun", 0: "Water", -1: "Snake"}

you = youdict[youstr]

if computer == you:
    print("Its a draw")

else:
    if computer == 1 and you == -1:
        print("you lose the match")

    elif computer == -1 and you == 1:
        print("you win the match")

    elif computer == -1 and you == 0:
        print("you win the match")

    elif computer == 0 and you == -1:
        print("you lose the match")

    elif computer == 0 and you == 1:
        print("you win the match")

    elif computer == 1 and you == 0:
        print("you lose the match")

    else:
        print("Somethings went to Wrong")
