import os
from datetime import datetime

# ============================== LIBRARY CLASS ==============================

class Library:
    def __init__(self):
        """Initializes the library system."""
        self.members = []
        self.books = []
        self.transaction_history = []
        self.load_data()

    def load_data(self):
        """Loads data from files into the library system with error handling."""
        if os.path.exists("members.txt"):
            with open("members.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) < 3:  # Ensure all required fields are present
                        print(f"Skipping malformed line in members.txt: {line.strip()}")
                        continue
                    
                    name, member_id, borrowed_books = parts
                    borrowed_books = [int(bid) for bid in borrowed_books.split(";")] if borrowed_books else []
                    self.members.append(LibraryUser(self, name, int(member_id), borrowed_books, is_loading=True))

    def save_data(self):
        """Saves data to files."""
        with open("members.txt", "w") as f:
            for member in self.members:
                borrowed_books = ";".join(str(book_id) for book_id in member.borrowed_books)
                f.write(f"{member.name},{member.member_id},{borrowed_books}\n")

        with open("books.txt", "w") as f:
            for book in self.books:
                f.write(f"{book['book_id']},{book['title']},{book['author']},{book['total_books']},{book['available_books']}\n")

        with open("transactions.txt", "w") as f:
            for transaction in self.transaction_history:
                f.write(f"{transaction}\n")

    def display_book_details(self):
        """Displays details of all books in a formatted table."""
        print("\n" + "*" * 50)
        print(f"{'Book ID':<8} | {'Title':<20} | {'Author':<15} | {'Total':<5} | {'Available':<8}")
        print("-" * 50)

        if not self.books:
            print("No books available.")
        else:
            for book in self.books:
                print(f"{book['book_id']:<8} | {book['title']:<20} | {book['author']:<15} | {book['total_books']:<5} | {book['available_books']:<8}")
        print("*" * 50)

    def display_transaction_history(self):
        """Displays the borrowing and returning history in table format."""
        print("\n" + "*" * 60)
        print(f"{'Member Name':<15} | {'Action':<10} | {'Book Title':<25} | {'Time':<10}")
        print("-" * 60)

        if not self.transaction_history:
            print("No transactions yet.")
        else:
            for transaction in self.transaction_history:
                print(transaction)
        print("*" * 60)

    def display_members(self):
        """Displays all registered members in a formatted table."""
        print("\n" + "*" * 60)
        print(f"{'Member ID':<10} | {'Name':<20} | {'Borrowed Books':<25}")
        print("-" * 60)

        if not self.members:
            print("No members found.")
        else:
            for member in self.members:
                borrowed_books = ", ".join(str(bid) for bid in member.borrowed_books) if member.borrowed_books else "None"
                print(f"{member.member_id:<10} | {member.name:<20} | {borrowed_books:<25}")

        print("*" * 60)

# ============================== LIBRARY USER CLASS ==============================

class LibraryUser:
    def __init__(self, library, name, member_id=None, borrowed_books=None, is_loading=False):
        """Initializes a library user (member)."""
        self.library = library
        self.name = name
        self.member_id = member_id if member_id else len(self.library.members) + 1
        self.borrowed_books = borrowed_books if borrowed_books else []

        if not is_loading:  # Prevent duplicate members when loading from file
            self.library.members.append(self)
            print(f"Member '{self.name}' registered successfully! Your Member ID is {self.member_id}.")

    def borrow_book(self):
        """Allows a member to borrow a book if available."""
        book_id = int(input("Enter the Book ID to borrow: "))
        for book in self.library.books:
            if book['book_id'] == book_id:
                if book['available_books'] > 0:
                    book['available_books'] -= 1
                    self.borrowed_books.append(book_id)
                    transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"'{book['title']}' borrowed successfully by {self.name}.")
                    self.library.transaction_history.append(f"{self.name} (ID: {self.member_id}) borrowed '{book['title']}' at {transaction_time}")
                    self.library.save_data()
                else:
                    print(f"'{book['title']}' is currently unavailable.")
                return
        print("Book not found.")

    def return_book(self):
        """Allows a member to return a borrowed book."""
        book_id = int(input("Enter the Book ID to return: "))
        for book in self.library.books:
            if book['book_id'] == book_id:
                if book_id in self.borrowed_books:
                    book['available_books'] += 1
                    self.borrowed_books.remove(book_id)
                    transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Thank you {self.name} for returning '{book['title']}'.")
                    self.library.transaction_history.append(f"{self.name} (ID: {self.member_id}) returned '{book['title']}' at {transaction_time}")
                    self.library.save_data()
                else:
                    print("You have not borrowed this book.")
                return
        print("Book not found.")

# ============================== LIBRARY ADMIN CLASS ==============================

class LibraryAdmin:
    def __init__(self, library):
        """Initializes a library admin."""
        self.library = library

    def add_book(self):
        """Allows admin to add a new book."""
        book_id = max([book['book_id'] for book in self.library.books], default=0) + 1
        title = input("Enter the book title: ").strip()
        author = input("Enter the author name: ").strip()
        total_books = int(input("Enter the total number of copies: "))
        new_book = {'book_id': book_id, 'title': title, 'author': author, 'total_books': total_books, 'available_books': total_books}
        self.library.books.append(new_book)
        print(f"Book '{title}' added successfully.")
        self.library.save_data()

# ============================== MAIN PROGRAM LOOP ==============================

library = Library()
admin = LibraryAdmin(library)

while True:
    print("\n" + "*" * 50)
    print(f"{'LIBRARY MANAGEMENT SYSTEM':^50}")
    print("*" * 50)
    print(f"{'Option':<5} | {'Functionality':<40}")
    print("-" * 50)
    print(f"{'1':<5} | Register as Member")
    print(f"{'2':<5} | Display Members")
    print(f"{'3':<5} | Display Book Details")
    print(f"{'4':<5} | Borrow Book")
    print(f"{'5':<5} | Return Book")
    print(f"{'6':<5} | Display Transaction History")
    print(f"{'7':<5} | Add New Book (Admin)")
    print(f"{'8':<5} | Exit")
    print("*" * 50)

    choice = input("Enter your choice (1-8): ")

    if choice == '1':
        name = input("Enter your name: ").strip()
        LibraryUser(library, name)
    elif choice == '2':
        library.display_members()
    elif choice == '3':
        library.display_book_details()
    elif choice == '4':
        member_id = int(input("Enter your Member ID: "))
        member = next((m for m in library.members if m.member_id == member_id), None)
        if member: 
            member.borrow_book()
        else:
            print("Invalid Member ID!")
    elif choice == '5':
        member_id = int(input("Enter your Member ID: "))
        member = next((m for m in library.members if m.member_id == member_id), None)
        if member: 
            member.return_book()
        else:
            print("Invalid Member ID!")
    elif choice == '6':
        library.display_transaction_history()
    elif choice == '7':
        admin.add_book()
    elif choice == '8':
        print("\nThank you for using the Library Management System. Goodbye!")
        print("*" * 50)
        break
    else:
        print("Invalid choice! Please enter a number between 1 and 8.")
