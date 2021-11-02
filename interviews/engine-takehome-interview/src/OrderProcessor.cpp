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

void OrderProcessor::processOrder(std::shared_ptr<Order>& order) {
    int matchQty = order->quantity;
    orderBook->match(order);
    if (matchQty > 0) {
        if(isBuy(order)) {
            orderBook->addBuy(order);
        } else {
            orderBook->addSell(order);
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

        if(line == "exit") {
            break;
        }
        auto order_time = duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
        if (!line.empty()) {
            for (std::string each; std::getline(split, each, split_char); tokens.push_back(each)); //NOLINT
        }
        bool validOrder = true;
        if (tokens.size() != TOKEN_SIZE) {
            std::cout << "Input: '" << line << "' is not valid: Not correct number of values.\n";
            validOrder = false;
        } else {
            if (!isNumber(tokens[3])) {
                std::cout << "Input: '" << line << "' is not valid. Quantity is not a number.\n";
                validOrder = false;
            }

            if (!isNumber(tokens[4])) {
                std::cout << "Input: '" << line << "' is not valid. Price is not a number.\n";
                validOrder = false;
            }
        }
        if (validOrder) {
            std::shared_ptr <Order> order(
                    new Order(tokens[0], tokens[1], tokens[2], stoi(tokens[3]), stoi(tokens[4]), order_time));
            processOrder(order);
        }
    }
    orderBook->printRemaining();
    return 0;
}

