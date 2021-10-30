#ifndef ENGINE_TAKEHOME_INTERVIEW_ORDERBOOK_H
#define ENGINE_TAKEHOME_INTERVIEW_ORDERBOOK_H

#include <iostream>
#include <string>
#include <vector>
#include "Order.h"
#include "Trade.h"

#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))

class OrderBook {
    std::string orderId;
    std::string sSide;
    std::string sInstrument;
    int quantity, price;

public:
    std::vector<Order*> buyList;
    std::vector<Order*> sellList;
    std::vector<Trade*> tradeList;

    OrderBook() {};
    template<typename T> bool isBuy(T x);
    void add(Order* order, bool buy);
    bool is_empty() const;
    void add_buy(Order* order);
    void add_sell(Order* order);
    void match(Order* order);
    void makeTrade( Order* buyerOrder, Order* sellerOrder, int price, int quantity);

    friend std::ostream& operator<<(std::ostream& os, const OrderBook& orderBook);
};

#endif //ENGINE_TAKEHOME_INTERVIEW_ORDERPBOOK_H
