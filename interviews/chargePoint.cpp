#include <iostream>
#include <map>
#include <unordered_map>
#include <bitset>
#include <cstddef>
#include <cstdlib>
#include <iostream>

// *****************************************************************************************
//   Meeting with Matthew
// *****************************************************************************************
// Write a C++ class that has a common dictionary (string, string) between instances
// has a global getter/setter
// can returm the number of other instances
class Common
{
  private:
    static std::unordered_map<std::string, int> m_map;
    std::string key;

  public:

    Common(std::string inKey, int value) {
        key = inKey;
        m_map[key] = value;
        std::cout << key;
    }
    ~Common() {
        m_map.erase(key);
    }
    void setValue(int value) {
        m_map[key] = value;
    }
    
    int getValue() {
        return m_map[key];
    }
    
    int numInstances() {
        return m_map.size();
    }
};

    std::unordered_map<std::string, int> Common::m_map;

// *****************************************************************************************
//   Meeting with Revathi
// *****************************************************************************************
int checkBit(int input, int position, int value) {
  
  if (value == 0) {
    input &= ~(0x1 << position);
  } else {
    input |= 0x1 << position;
  }
  return input;
  
}

// *****************************************************************************************
//   Meeting with David
// *****************************************************************************************
#include <unistd.h>
#include <cstdio>
#include <cassert>
#include <iostream>
#include <string>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

using namespace std;


class file {

public:

    /*
     * Default constructor
     */
    file()
    {
      /* TODO */
      fd_ = -1;
    }

    /*
     * File path constructor.
     * Creates the file, if it does not already exist.
     */
    file(const string &path)
    {
      /* TODO */
        fd_ = open(path.c_str(), O_RDWR | O_CREAT);
    }

    /*
     * Assignment operator
     */
    file &operator=(const file &other)
    {
        /* TODO */
        fd_ = other.fd_;
        std::cout << "copy assigned" << std::endl;
        return *this;
    }

    /*
     * Move assignment operator
     */
    file &operator=(file &&other)
    {
        /* TODO */
        fd_ = std::move(other.fd_);
        std::cout << "move assigned" << std::endl;
        return *this;
    }

    /*
     * Return true if the file is open.
     */
    bool valid() const
    {
        /* TODO */
        struct stat statbuf;    
        if (fstat(fd_,&statbuf)) {
            return false;
        } else {
            return true;
        }
    }
    
    /*
     * Replace the contents of the file with the specified string.
     *
     * Returns the number of characters written.
     * Throws an exception if an error is encountered.
     */
    size_t write(const string &out)
    {
        /* TODO */
        lseek(fd_, 0, SEEK_SET);
        size_t size = (size_t)out.size();
        std::string temp_str = out;
        ssize_t bytes_written = ::write(fd_, out.c_str(), size);
        if (bytes_written <= 0) {
            throw std::invalid_argument( "Write failed" );
        }
        return bytes_written;
    }

    /*
     * Read from the beginning of the file into a string.
     * If len != `npos`, limit read to `len` bytes.
     * Otherwise, read the entire contents of the file into
     * the string.
     *
     * Returns the number of characters read.
     * Throws an exception if an error is encountered.
     */
    size_t read(string &out, size_t len = string::npos)
    {
        /* TODO */
        lseek(fd_, 0, SEEK_END);
        int size = lseek(fd_, 0, SEEK_CUR);
        if (size > len) {
            size = len;
        } 
        lseek(fd_, 0, SEEK_SET);
        char buf[size];
        ssize_t bytes_read = ::read(fd_, buf, size);
        if (bytes_read <= 0) {
            throw std::invalid_argument( "Read failed" );
        } else if ( len == 0 ) {
            //  eof...
            out = buf;
        } else {
            std::string data(buf, size);
            out = data;
        }
        return bytes_read;
    }

private:

    /* Unix file descriptor */
    int fd_;
};



// *****************************************************************************************
//   Meeting with Michael
// *****************************************************************************************
struct Node {
    int value;
    Node *next;
};

// Add a new item to the list
void addValue(Node **list, int value)
{
    struct Node *newNode;
    newNode = (Node *)malloc(sizeof(struct Node));
    newNode->value = value;
    newNode->next = NULL;
    
    while(*list != NULL) {
        list = &(*list)->next;
    }
    (*list) = newNode;
}

// Remove ALL items from the list that match value
void removeValue(Node **list, int value)
{
    Node *del;
    while(*list && (*list)->value != value) {
        list = &(*list)->next;
    }
    
    if (*list) {
        del = *list;
        *list = del->next;
        del->next = NULL;
        free(del);
    }
    
}

// Print the list out
void printList(Node *list)
{
    // struct Node *temp = *list;
    while(list != NULL) {
        std::cout << list->value << " ";
        list = list->next;
    
    }
    std::cout << std::endl;
}

int main() {
    
    // *****************************************************************************************
    //   Meeting with Matthew
    // *****************************************************************************************
    std::cout << "First, I am running the code developed in my meeting with Matthew:" << std::endl << std::endl;
    Common *class1 = new Common("class1", 1);
    std::cout << "Created class1 with value = " << class1->getValue() << ". There are now " << class1->numInstances() << " instantiations." << std::endl;
    Common *class2 = new Common("class2", 2);
    std::cout << "Created class2 with value = " << class2->getValue() << ". There are now " << class2->numInstances() << " instantiations." << std::endl;
    Common *class3 = new Common("class3", 3);
    std::cout << "Created class3 with value = " << class3->getValue() << ". There are now " << class3->numInstances() << " instantiations." << std::endl;
  
    delete class2;
    std::cout << "Deleted class2. There are now " << class3->numInstances() << " instantiations." << std::endl;


    // *****************************************************************************************
    //   Meeting with Revathi
    // *****************************************************************************************
    std::cout << std::endl << "Now, I am running the code developed in my meeting with Revathi:" << std::endl << std::endl;
    
    int val = 127;
    int val1 = checkBit(val, 2, 0);
    std::bitset<8> val1_bin(val1);
    std::cout << "Setting 2nd bit of 0x01111111 to 0: " << val1_bin << std::endl;
    
    val = 213;
    int val2 = checkBit(val, 5, 1);
    std::bitset<8> val2_bin(val2);
    std::cout << "Setting 5th bit of 0x11010101 to 1: " << val2_bin << std::endl;
    
    val = 155;
    int val3 = checkBit(val, 5, 1);
    std::bitset<8> val3_bin(val3);
    std::cout << "Setting 6th bit of 0x10011011 to 1: " << val3_bin << std::endl;
    
    
    // *****************************************************************************************
    //   Meeting with David
    // *****************************************************************************************
    std::cout << std::endl << "Now, I am running the code developed in my meeting with David:" << std::endl << std::endl;
    cout << "Starting test\n";

    const string output = "The brown fox jumped over the lazy dog";

    /* Default constructed */
    file file1;
    assert(!file1.valid());
    std::cout << "Passed invalid file path default constructor test!" << std::endl;

    /* Path constructed */
    file file2("/tmp/my_file");
    assert(file2.valid());
    std::cout << "Passed valid file path construction test!" << std::endl;

    /* Test write + read */
    try {
        file2.write(output);
        {
            string input;
            try {
                file2.read(input);
            }
            catch( const std::invalid_argument& e ) {
                std::cout << "Error: " << e.what() << std::endl;
            }            
            assert(input == output);
            std::cout << "Passed write + read test!" << std::endl;
        }
    }
    catch( const std::invalid_argument& e ) {
        std::cout << "Error: " << e.what() << std::endl;
    }
    /* Test assignment */
    file1 = file2;
    {
        assert(file1.valid());
        assert(file2.valid());
        std::cout << "Passed file assignment test!" << std::endl;


        string input;
        try {
            file1.read(input);
        }
        catch( const std::invalid_argument& e ) {
            std::cout << "Error: " << e.what() << std::endl;
        }
        assert(input == output);
        std::cout << "Passed file assignment input == output test!" << std::endl;

    }

    /* Test read length */
    {
        file file2("/tmp/my_file");

        string input;
        try {
            file2.read(input, 4);
        }
        catch( const std::invalid_argument& e ) {
            std::cout << "Error: " << e.what() << std::endl;
        }
        assert(input == "The ");
        std::cout << "Passed short file read test!" << std::endl;

    }

    std::cout << "Passed all file tests!" << std::endl;

    
    // *****************************************************************************************
    //   Meeting with Michael
    // *****************************************************************************************
    std::cout << std::endl << "Now, I am running the code developed in my meeting with Michael:" << std::endl << std::endl;
	Node *list = NULL;
	
	addValue(&list, 1);
	addValue(&list, 2);
	addValue(&list, 3);
	addValue(&list, 4);
	printList(list);
	
	removeValue(&list, 1);
	printList(list);
	
	removeValue(&list, 10);
	printList(list);
	
	addValue(&list, 4);
	removeValue(&list, 4);
	printList(list);
	
	addValue(&list, 5);
	addValue(&list, 2);
	addValue(&list, 1);
	addValue(&list, 6);
	printList(list);
	
	removeValue(&list, 1);
	removeValue(&list, 2);
	removeValue(&list, 3);
	removeValue(&list, 4);
	removeValue(&list, 5);
	removeValue(&list, 6);
	printList(list);
    return 0;
}
