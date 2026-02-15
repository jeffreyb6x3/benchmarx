test = {"d": 4, "e": 5, "f": 6}
commands = ["a=1", "b=2", "c=3"]

commands = dict(command.split("=") for command in commands)
test.update(commands)
print(test)
