# Coursework
# 1. Introduction
# a. What is your application?
My application is a library management program which keeps tracks of books and whether they are available or not. The following information can be saved: the books name, the author and the publication date. If a book is no longer available, you can either change it's status or remove it from the list entirely.
# b. How to run the program? 
You can either run the program from a compiler of your choosing, or by executing it from a commandline.
# c. How to use the program?
After launching the code, a window pops up. In that window you choose the text file which contains all the book data. After that, you are greeted with a new window, which has two buttons. If you press the "Display existing books" button, you can see all the saved books and delete them from the list or change their availability status. The other button is for entering  new books. Upon pressing that button, a window pops up where you are asked to fill out some basic information about the book, such as the name of the book, the author's name and the publication date.
# 2. Body/Analysis
# a. Explain how the program covers (implements) functional requirements
Polymorphism allows methods to do different things based on the object it is acting upon, even though they share the same name. In my code, this is exemplified by the execute method in the FileOperation class and its subclasses. The `execute` method is polymorphic because it behaves differently depending on whether the instance is of type ReadFileOperation or WriteFileOperation.
```
class FileOperation:
    def execute(self, file_path):
        pass

class ReadFileOperation(FileOperation):
    def execute(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found."

class WriteFileOperation(FileOperation):
    def execute(self, file_path, data):
        try:
            with open(file_path, 'a') as file:
                file.write(data + '\n')
            return "Data successfully written to file."
        except Exception as e:
            return f"Error writing to file: {e}"

```

Abstraction involves hiding the complex implementation details and showing only the necessary features of an object. In my code, the FileOperation class provides a base class that abstracts the concept of a file operation without exposing the implementation details. Users of this class do not need to know how execute is implemented; they just need to know that subclasses will provide the actual implementation.
```
class FileOperation:
    def execute(self, file_path):
        pass

```

Inheritance allows a class to inherit attributes and methods from another class. In my code, ReadFileOperation and WriteFileOperation inherit from FileOperation. ReadFileOperation and WriteFileOperation inherit the execute method definition from FileOperation and provide their own specific implementations.


```
class FileOperation:
    def execute(self, file_path):
        pass

class ReadFileOperation(FileOperation):
    def execute(self, file_path):
        ...

class WriteFileOperation(FileOperation):
    def execute(self, file_path, data):
```

Encapsulation is the mechanism of restricting access to some of an object's components and can be achieved using private variables and methods. In my code, encapsulation is demonstrated by the use of private variables to control window state in the FileApp class. The variables __main_window_open, __display_window_open, and __write_window_open are prefixed with double underscores, making them private to the class. This prevents external modification and ensures that the window state is managed only through the class's methods. 

```
class FileApp:
    def __init__(self, root):
        self.root = root
        self.__main_window_open = False
        self.__display_window_open = False
        self.__write_window_open = False
        ...

    def open_main_window(self, file_path):
        if self.__main_window_open:
            return
```

The Factory Method pattern is used in my code to create instances of FileOperation subclasses. This pattern defines an interface for creating an object but lets subclasses alter the type of objects that will be created. It encapsulates the creation of ReadFileOperation and WriteFileOperation objects, adhering to the Single Responsibility Principle. The FileApp class does not need to know the details of these subclasses. Adding new file operations (like DeleteFileOperation or UpdateFileOperation) is straightforward. You only need to extend the FileOperation class and modify the factory method to support the new operation. It decouples the client code (FileApp class) from the concrete classes (ReadFileOperation and WriteFileOperation). This makes the system more modular and easier to maintain. It avoids unnecessary complexity that would come with more heavyweight patterns like Abstract Factory or Builder.
Here is how it is implemented in my code:
```
class FileOperationFactory:
    @staticmethod
    def create_operation(operation_type):
        if operation_type == "read":
            return ReadFileOperation()
        elif operation_type == "write":
            return WriteFileOperation()
        else:
            raise ValueError("Invalid operation type")
```

In my code, reading from and writing to a file is handled through the ReadFileOperation and WriteFileOperation classes. These classes inherit from the FileOperation base class and implement the execute method differently to perform their respective file operations.


# 3. Results and Summary

    Polymorphism: Achieved through the execute method in FileOperation and its subclasses, allowing different behaviors based on the subclass.
    Abstraction: Provided by the FileOperation base class, which defines a generic interface for file operations.
    Inheritance: Used by ReadFileOperation and WriteFileOperation to inherit from FileOperation.
    Encapsulation: Demonstrated by private variables in the FileApp class to manage window state securely.

    
# c. How it would be possible to extend your application?
It would be possible to integrate the function of writing and displaying books into one, which would provide a better and smoother experience. It would also be possible to create an account system, where every user of the library would have their account and could manage their books
