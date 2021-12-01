#include <iostream>

void printSpaces(int indentCount) {
    for(int j=0; j<indentCount; j++) {
        std::cout << " ";
    }
}
void printJson(std::string str) {
    int indentCount=0;

    for(int j=0; j<str.size(); j++) {
        if(str[j] == '{' || str[j] == '[') {
            std::cout << str[j];
            std::cout << std::endl;
            indentCount = indentCount +2;
            printSpaces(indentCount);
        } else if (str[j] == '}' || str[j] == ']' ) {
            indentCount = indentCount - 2;
            std::cout << std::endl;
            printSpaces(indentCount);
            std::cout << str[j];
        } else if (str[j] == ',') {
            std::cout << str[j];
            std::cout << std::endl;
            printSpaces(indentCount);
        } 
        else if(str[j] == ' ') {
        }
        else {
            std::cout << str[j];
        }
    }
}

int main() {
    // you can write to stdout for debugging purposes, e.g.
    std::cout << "This is a debug message" << std::endl;
    std::string str = R"({"Name": "A", "Age": 3, "Address":{"State":"B", "City":"C"}, "Cars":["D", "E"]})";
    printJson(str);
    return 0;
}
