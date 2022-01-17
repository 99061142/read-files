from time import sleep

with open("README.md") as file:
    for line in file:
        print(line)
        sleep(1)