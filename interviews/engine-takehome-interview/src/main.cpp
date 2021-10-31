#include "OrderProcessor.h"
#include <iostream>
#include <string>


int main(int argc, char *argv[]) {
    std::cerr << "====== Match Engine =====" << std::endl;
    std::string filename;
    OrderProcessor orderProc;
    if(argc >= 2) {
        filename = argv[1]; // NOLINT
    }
    std::cerr << "Enter 'exit' to quit" << std::endl;
    orderProc.run(filename);
    return 0;
}
