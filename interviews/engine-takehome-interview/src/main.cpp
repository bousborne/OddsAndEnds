#include <iostream>
#include <stdio.h>

int main() {
    std::cerr << "====== Match Engine =====" << std::endl;
    std::cerr << "Enter 'exit' to quit" << std::endl;
    std::string line;
    std::string orderId;
    std::string sSide;
    std::string sInstrument;
    int quantity, price;

    std::string delimiter = " ";

    size_t pos = 0;
    std::string token;
    while (getline(std::cin, line) && line != "exit") {
        std::cout << "Received: '" << line << "'" << std::endl;

    }
    return 0;
}
