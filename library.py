"""
CS1026a 2023
Assignemnt 02
Adam Muzzo
251355839
amuzzo3
Wednesday, October 25, 2023
"""

def printMenu():
    
    print('\n######################')
    print('1: (A)dd a new book.')
    print('2: Bo(r)row books.') 
    print('3: Re(t)urn a book.') 
    print('4: (L)ist all books.') 
    print('5: E(x)it.') 
    print('######################\n')

def start():
    allBooks = [
                ['9780596007126',"The Earth Inside Out","Mike B",2,['Ali']],
                ['9780134494166',"The Human Body","Dave R",1,[]],
                ['9780321125217',"Human on Earth","Jordan P",1,['David','b1','user123']]
           ] 
    rentedISBNs=[]
    finish = False
    #loops until the user chooses exit
    while (finish == False):

        printMenu()
        
        select = input("\nYour selection> ")

        if (select == "1" or select.lower() == "a"):
            allBooks = addBook(allBooks)  
        elif (select == "2" or select.lower() == "r"):
            allBooks, rentedISBNs = borrowBook(allBooks, rentedISBNs)
        elif (select == "3" or select.lower() == "t"):
           rentedISBNs = returnBook(rentedISBNs, allBooks)      
        elif (select == "4" or select.lower() == "l"):
            listBooks(allBooks, rentedISBNs)  
        elif (select == "5" or select.lower() == "x"):
            exit(allBooks, rentedISBNs)
            finish = True     
        else :
            print("Wrong selection! Please selection a valid option.")
       
def addBook(books):

    isValid = False

#checks if book name is valid
    while isValid == False:
        bookName = input("Book name> ")
        #Checks if bookname contains a * or a %
        if "*" in bookName or "%" in bookName:
            print("Invalid book name!")
        else :
            isValid = True
        
    authorName = input("Author name> ")
    
    isValid = False

#Checks if edition is valid
    while isValid == False:
        edition = input("Edition> ")
        #if edition contains characters
        if not edition.isdigit():
            print("Invalid Input, Retry")
        else :
            isValid = True

    isValid = False

    #Loops to check the validity of the entered ISBN
    while isValid == False:
        isbn = input("ISBN> ")

        #Compares ISBN to all ISBNs
        for i in range(len(books)):
            if isbn == books[i][0]:
                print("Duplicate ISBN is found! Cannot add the book.")
                return books
        if not isbn.isdigit() or not len(isbn) == 13:
            print("Invalid ISBN!")
     
        #Checks ISBN using the ISBN logic
        else :
            sum = 0
            for i in range(len(isbn)):
                if i % 2 == 0:
                    sum += int(isbn[i]) * 1
                else:
                    sum += int(isbn[i]) * 3
            if sum % 10 != 0:
                print("Invalid ISBN!")
                return books
            else :
                isValid = True 

    #one new book variable stores
    oneNewBook = [isbn, bookName, authorName, edition,[]]
    books.append(oneNewBook)
    print("A new book is added successfully.")
    
    return books

def borrowBook(books, rentISBNs):
    borrowerName = input("Enter the borrower name> ")
    searchTerm = input("Search Term> ")
        
    #if * (contains)
    if "*" in searchTerm:
        isValid = False
        for i in range(len(books)):
            #if match
            if searchTerm[:-1].lower() in books[i][1].lower() and books[i][0] not in rentISBNs:  
                isValid = True
                books[i][-1].append(borrowerName)
                rentISBNs.append(books[i][0])
                print("-\"" + books[i][1] + "\" is borrowed!")
        #if no match
        if isValid == False:
            print("No books found!")
        return books, rentISBNs

    #if % (starts with)
    elif "%" in searchTerm:
        isValid = False
        for i in range(len(books)):
            #if match
            if  books[i][1].lower().startswith(searchTerm[:-1].lower()) and books[i][0] not in rentISBNs:
                isValid = True
                books[i][-1].append(borrowerName)
                rentISBNs.append(books[i][0])
                print("-\"" + books[i][1] + "\" is borrowed!")
        #if no match
        if isValid == False:
            print("No books found!")
        return books, rentISBNs
           
    #else (exact match)
    else :
        isValid = False
        for i in range(len(books)):
            #if match
            if searchTerm.lower() == books[i][1].lower() and books[i][0] not in rentISBNs:
                isValid = True
                books[i][-1].append(borrowerName)
                rentISBNs.append(books[i][0])
                print("-\"" + books[i][1] + "\" is borrowed!")
        #if no match
        if isValid == False:
                print("No books found!")
        return books, rentISBNs
        
def returnBook(rentISBNs, books):
    currentISBN = input("ISBN> ")
    #loops through rented isbns
    for i in range(len(rentISBNs)):
        #if it exists then delete
        if currentISBN in rentISBNs:
            rentISBNs.remove(currentISBN)
    #loops through all books
    for i in range(len(books)):
        #find and print book that is returned
        if currentISBN == books[i][0]:
            print("\"" + books[i][1] + "\" is returned.")
            return rentISBNs
        
    print("No book is found!")

    return rentISBNs

def listBooks(books, rentISBNs):
    #loop through all books
    for i in range(len(books)):
        print("-"*15)
        if books[i][0] in rentISBNs:
            print("[Unavailable]")
        else :
            print("[Available]")
        
        print(books[i][1], "-", books[i][2])
        print("E:", books[i][3], "ISBN:", books[i][0])
        print("borrowed by:", books[i][4])



    return books, rentISBNs

def exit(books, rentISBNs):
    print()
    print("\n$$$$$$$$ FINAL LIST OF BOOKS $$$$$$$$")
    #go to listBooks to print the final list of books
    listBooks(books, rentISBNs)
    return 

start()
