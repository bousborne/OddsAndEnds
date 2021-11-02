#ifndef ENGINE_TAKEHOME_INTERVIEW_ORDERPROCESSOR_H
#define ENGINE_TAKEHOME_INTERVIEW_ORDERPROCESSOR_H
#include <chrono>
#include <ctime>
#include <fstream>
#include <iostream>
#include <memory>
#include <regex>
#include <sstream>
#include <stdio.h>
#include <string>
#include <sys/time.h>

#include "Order.h"
#include "OrderBook.h"
#include "Trade.h"

#define TOKEN_SIZE 5

using std::chrono::duration_cast;
using std::chrono::milliseconds;
using std::chrono::seconds;
using std::chrono::system_clock;

class OrderProcessor {
private:
    OrderBook *orderBook;

public:
    std::ifstream inFile;
    OrderProcessor() {
        orderBook = new OrderBook();
    };
    virtual ~OrderProcessor() {
        clean();
    }
    template <typename T> bool isNumber(T x);
    template <typename T> bool isBuy(T x);
    void processOrder(std::shared_ptr<Order> &order);
    int run(const std::string &filename);
    void clean() {
        delete orderBook;
    }
};

#endif // ENGINE_TAKEHOME_INTERVIEW_ORDERPROCESSOR_H
