with open("../month9.txt", "r") as file:
    txt_file = file.readlines()

count = 2708
for line in txt_file:
    if line != "\n":
        output = line
        if line[2:9] == "Week 34":
            exec(f"new_season={line}")
            # print(line[2:9])
            count -= 1
            output = {f"League ID {count}": new_season}
        with open("converted_output.txt", "at") as file:
            print(output, file=file)
