import json

FILE_NAME = "list_data.json"


def loadList():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


def saveList(listIn):
    with open(FILE_NAME, "w") as file:
        json.dump(listIn, file)


def addItems(listIn):
    print("\nEnter items to add (type 'done' to stop):")
    while True:
        item = input("Add item: ")
        if item.lower() == "done":
            break
        listIn.append(item)
    print("Items added!")


def removeItems(listIn):
    if len(listIn) == 0:
        print("\nList is empty!")
        return

    printList(listIn)
    try:
        choice = int(input("Enter item number to remove: "))
        if 1 <= choice <= len(listIn):
            removed = listIn.pop(choice - 1)
            print(f"Removed: {removed}")
        else:
            print("Invalid number!")
    except:
        print("Invalid input!")


def editItems(listIn):
    if len(listIn) == 0:
        print("\nList is empty!")
        return

    printList(listIn)
    try:
        choice = int(input("Enter item number to edit: "))
        if 1 <= choice <= len(listIn):
            newValue = input("Enter new value: ")
            listIn[choice - 1] = newValue
            print("Item updated!")
        else:
            print("Invalid number!")
    except:
        print("Invalid input!")


def moveItems(listIn):
    if len(listIn) < 2:
        print("\nNot enough items to move!")
        return

    printList(listIn)
    try:
        oldPos = int(input("Move item FROM position: "))
        newPos = int(input("Move item TO position: "))

        if 1 <= oldPos <= len(listIn) and 1 <= newPos <= len(listIn):
            item = listIn.pop(oldPos - 1)
            listIn.insert(newPos - 1, item)
            print("Item moved!")
        else:
            print("Invalid positions!")
    except:
        print("Invalid input!")


def printList(listIn):
    if len(listIn) > 0:
        print("\n~~~ LIST ~~~")
        for idx in range(len(listIn)):
            print(f"{idx+1}. {listIn[idx]}")
        print("")
    else:
        print("\nThe list is empty!")


def main():
    appOn = True

    managedList = loadList()   

    print("Welcome to the List Manager!")
    while appOn:
        print("")
        print(" ~~~ Choose an Option Below ~~~")
        print("1. View List")
        print("2. Add Items to List")
        print("3. Remove Items from List")
        print("4. Edit Items on List")
        print("5. Move Items on List")
        print("6. Exit")

        toDo = input(" --> ")

        if toDo == "1":
            printList(managedList)
        elif toDo == "2":
            addItems(managedList)
        elif toDo == "3":
            removeItems(managedList)
        elif toDo == "4":
            editItems(managedList)
        elif toDo == "5":
            moveItems(managedList)
        elif toDo == "6":
            appOn = False
        else:
            print("Invalid option - try again!")

    saveList(managedList)


main()