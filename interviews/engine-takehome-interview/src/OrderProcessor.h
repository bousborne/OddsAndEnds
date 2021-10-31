#ifndef ENGINE_TAKEHOME_INTERVIEW_ORDERPROCESSOR_H
#define ENGINE_TAKEHOME_INTERVIEW_ORDERPROCESSOR_H
#include <iostream>
#include <sstream>
#include <string>
#include <regex>
#include <stdio.h>
#include <fstream>
#include <memory>

#include "OrderBook.h"
#include "Order.h"
#include "Trade.h"

class OrderProcessor
{
private:
    OrderBook* orderBook;

public:
    std::ifstream inFile;
    OrderProcessor()
    {
        orderBook = new OrderBook();
    };
//    ~OrderProcessor()
//    {
//        delete orderBook;
//    };
    virtual ~OrderProcessor() {clean();}
    template<typename T> bool isNumber(T x);
    template<typename T> bool isBuy(T x);
    void processOrder( std::shared_ptr<Order>& order );
    int run(const std::string &filename);
    void clean() { delete orderBook; }

};

#endif //ENGINE_TAKEHOME_INTERVIEW_ORDERPROCESSOR_H
