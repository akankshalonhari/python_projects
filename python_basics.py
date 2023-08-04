
class Fruit:

    def __init__(self, name, flavor, worms):       #constructor in python
        self.name = name
        self.flavor = flavor
        self.worms = Worms(worms)	#composite class
    
    def __str__(self):
        return "This is a fruit with name {} and flavor {} and {}".format(self.name, self.flavor, self.worms)

class Worms:
    def __init__(self, worms):
        self.worms = worms
    
    def __str__(self):
        return "Worms present {} ".format(self.worms)

class Apple(Fruit):	#inherited class
    def cut(self):
        return "This is how you cut {} if you have {}".format(self.name, self.worms)

class Pear(Fruit):
    pass


def say_hello():
    print('Hello, World')


def factorial(num):
    if num == 1:
        return 1
    else:
        return (num * factorial(num-1))    # recursive call


def main():
    for i in range(2):
        print(i)
        say_hello()  # function call

    num = 3
    print("Factorial of ", num , " is " , factorial(num))

    for i in [30, 5, 64]:
        print(i)

    dicttemp = {"txt": 10, "js": 20, "html": 15}
    for key, value in dicttemp.items():  # .items() return (key,value) tuple
        print(key, value)

    for key in dicttemp:       # only dictiornary name returns keys
        print(key)

    for key in dicttemp.keys():       # .keys() returns keys
        print(key)

    for value in dicttemp.values():       # .values() returns values
        print(value)

    # set in python
    set1 = set(["Welcome", "to", "Half moon bay"])
    print(set1) 

    set2 = set([1, 2, 3])
    print(set2)

    apple1 = Apple('granny smith', 'sweet',{"worm1", "worm2"})
    print(apple1)
    print(apple1.cut())   

if __name__ == '__main__':
    main()
