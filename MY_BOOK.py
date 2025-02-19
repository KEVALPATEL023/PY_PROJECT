class Book:
    book_counter = 101  

    def __init__(self, title, author):
        self.book_id = Book.book_counter
        Book.book_counter += 1
        self.title = title
        self.author = author
        self.available = True

    # def __str__(self):
    #     status = "Available" if self.available else "Not Available"
    #     return f"\033[32m\n\t \">> ID: {self.book_id}, Book: {self.title}, Author: {self.author}, Status: {status} <<\" \033[0m"

class Member:
    def __init__(self, name):
        self.name = name.title()
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book)
            print(f"\033[32m\n\t \">> {self.name} borrowed '{book.title}'. <<\"\033[0m")
        else:
            print("\033[31m\033[3m\n\t=> Book is not available.\033[0m")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.available = True
            self.borrowed_books.remove(book)
            print(f"\033[32m\n\t >> {self.name} returned '{book.title}'. <<\033[0m")
        else:
            print("\033[31m\033[3m\n\t=> Invalid return request.\033[0m")

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append(Book(title.title(), author.title()))

    def display_books(self):
        if not self.books:
            print("\033[31m\033[3m\n\t=> No books available in the library.\033[0m")
            return
        self.display_book_details(self.books)
    
    def display_book_details(self,books):
        print("\n" + "=" * 90)
        print("{:^90}".format(" \033[1m\033[34mLIBRARY BOOK DETAILS \033[0m"))
        print("=" * 90)
        print("\033[33m{:<10} {:<25} {:<20} {:<15} {:<15}\033[0m".format("Book ID", "Title", "Author", "Total Copies", "Available"))
        print("-" * 90)
        for book in books:
            print("{:<10} {:<25} {:<20} {:<15} {:<15}".format(book.book_id, book.title, book.author, 1, "Yes" if book.available else "No"))
        print("-" * 90)

    def search_book(self,keyword):
        found_books = [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        if not found_books:
            print("\033[31m\033[3m\n\t=> No matching books found.\033[0m")
        else:
            self.display_book_details(found_books)

    def filter_books(self, author=None, available_only=False):
        filtered_books = self.books
        if author:
            filtered_books = [book for book in filtered_books if book.author.lower() == author.lower()]
        if available_only:
            filtered_books = [book for book in filtered_books if book.available]
        
        if not filtered_books:
            print("\033[31m\033[3m\n\t=> No books match the filter criteria.\033[0m")
        else:
            self.display_book_details(filtered_books)


library = Library()
member = None

while True:
    print("\033[0m\n=========================================")
    print("|       \033[1m\033[34mLibrary Management System \033[0m      |")
    print("=========================================")
    print("| 1. Add Book                           |")
    print("| 2. Display Books                      |")
    print("| 3. Search Book                        |")
    print("| 4. Borrow Book                        |")
    print("| 5. Return Book                        |")
    print("| 6. Filter Books                       |")
    print("| 7. Exit                               |")
    print("=========================================")
    choice = input("\033[4mEnter your choice: \033[0m")

    
    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        library.add_book(title, author)
        print("\033[32m\033[3m\n\t=> Book added successfully.\033[0m")
    elif choice == "2":
        library.display_books()
    elif choice == "3":
        keyword = input("Enter keyword to search: ")
        library.search_book(keyword)
    elif choice == "4":
        member_name = input("Enter your name: ")  # Always ask for the user's name
        member = Member(member_name)

        book_id = int(input("Enter book ID to Borrow: "))
        for book in library.books:
            if book.book_id == book_id:
                member.borrow_book(book)
                break
        else:
            print("\033[31m\033[3m\n\t=> Book ID not found.\033[0m")


    elif choice == "5":
        if not member or not member.borrowed_books:
            print("\033[31m\033[3m\n\t=> No borrowed books found. Borrow a book first.\033[0m")
        else:
            book_id = int(input("Enter book ID to return: "))
            for book in member.borrowed_books:
                if book.book_id == book_id:
                    member.return_book(book)
                    break
            else:  # This else now belongs to the for-loop
                print("\033[31m\033[3m\n\t=> Book not found in borrowed list.\033[0m")

    elif choice == "6":
        author = input("Enter author name (leave blank for all): ")
        available_only = input("Show only available books? (yes/no): ").strip().lower() == "yes"
        library.filter_books(author if author else None, available_only)

    elif choice == "7":
        print("\033[1;30m\033[3m\n\t=> Exiting the Library Management System.\033[0m")
        break

    else:
        print("\033[31m\033[3m\n\t=> Invalid choice. Please try again.\033[0m")