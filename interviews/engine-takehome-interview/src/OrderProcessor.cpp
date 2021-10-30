#include "OrderProcessor.h"

template<typename T>
bool OrderProcessor::isNumber(T x) {
    std::string s;
    std::regex e("^-?\\d+");
    std::stringstream ss;
    ss << x;
    ss >> s;
    return std::regex_match(s, e);
}

template<typename T>
bool OrderProcessor::isBuy(T x) {
    return x->sSide == "BUY";
}

void OrderProcessor::processOrder(Order *order) {
    int matchQty = order->quantity;
    orderBook->match(order);
    if (matchQty > 0) {
        if(isBuy(order)) {
            orderBook->add_buy(order);
        } else {
            orderBook->add_sell(order);
        }
    }
}

int OrderProcessor::run(const std::string &filename) {
    std::string line;
    inFile.open(filename);
    while ( ((!filename.empty()) ? getline(inFile, line) : getline(std::cin, line)) && line != "exit") {
        char split_char = ' ';
        std::istringstream split(line);
        std::vector <std::string> tokens;

        time_t order_time = time(nullptr);
        if (!line.empty()) {
            for (std::string each; std::getline(split, each, split_char); tokens.push_back(each)); //NOLINT
        }

        if (tokens.size() != 5) {
            std::cout << "Input: '" << line << "' is not valid: Not correct number of values.\n";
//            continue;
        } else {
            if (!isNumber(tokens[3])) {
                std::cout << "Input: '" << line << "' is not valid. Quantity is not a number.\n";
//                continue;
            }

            if (!isNumber(tokens[4])) {
                std::cout << "Input: '" << line << "' is not valid. Price is not a number.\n";
//                continue;
            }
        }
        Order *order = new Order(tokens[0], tokens[1], tokens[2], stoi(tokens[3]), stoi(tokens[4]), order_time);
        processOrder(order);
        delete order;
    }
    std::cout << *orderBook << std::endl;
    return 0;
}

