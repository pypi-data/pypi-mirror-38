
def searchIn(text,search):
    try:
        text.index(search)
        return True
    except ValueError:
        return False

def motivate():
    print("You're doing great, keep it up!")
def sayHello():
    print("Hello!")
def wow():
    print("Wow!")
def cleverOrSilly():
    a = input("What are you doing? ")
    a = a.lower()

    if (searchIn(a, "python") or searchIn(a, "raspberry pi") or searchIn(a,"coding") or searchIn(a,"electronics") or searchIn(a,"arduino") or searchIn(a,"computer") or searchIn(a,"computing")):
        print("You're clever.")
    else:
        print("You're silly.")
def say(thingToSay):
    print(thingToSay)
