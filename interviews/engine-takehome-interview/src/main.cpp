#include "OrderProcessor.h"
#include <iostream>
#include <string>


int main(int argc, char *argv[]) {
    std::cerr << "====== Match Engine =====" << std::endl;
    std::string filename;
    OrderProcessor orderProc;
    std::cout << "argc = " << argc << std::endl;
//    auto args = std::span(argv, size_t(argc));
    if(argc > 0) {
        filename = argv[1]; // NOLINT
    }
    std::cerr << "Enter 'exit' to quit" << std::endl;
    orderProc.run(filename);
    orderProc.clean();
    return 0;
}
