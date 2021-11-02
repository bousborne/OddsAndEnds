#ifndef ENGINE_TAKEHOME_INTERVIEW_ORDERBOOK_H
#define ENGINE_TAKEHOME_INTERVIEW_ORDERBOOK_H

#include "Order.h"
#include "Trade.h"
#include <algorithm>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

class OrderBook {
    std::string orderId;
    std::string sSide;
    std::string sInstrument;
    int quantity, price;

public:
    std::vector<std::shared_ptr<Order>> buyList;
    std::vector<std::shared_ptr<Order>> sellList;
    std::vector<std::shared_ptr<Trade>> tradeList;

    OrderBook(){};
    template <typename T> bool isBuy(T x);
    void add(std::shared_ptr<Order> &order, bool buy);
    bool isEmpty() const;
    static bool sellSortCompare(const std::shared_ptr<Order> &order1,
                                const std::shared_ptr<Order> &order2);
    static bool buySortCompare(const std::shared_ptr<Order> &order1,
                               const std::shared_ptr<Order> &order2);
    static bool timeSortCompare(const std::shared_ptr<Order> &order1,
                                const std::shared_ptr<Order> &order2);
    void addBuy(std::shared_ptr<Order> &order);
    void addSell(std::shared_ptr<Order> &order);
    void match(std::shared_ptr<Order> &order);
    void makeTrade(std::shared_ptr<Order> &buyerOrder,
                   std::shared_ptr<Order> &sellerOrder, int price,
                   int quantity);
    void printRemaining();

    // This friend function is used for testing
    friend std::ostream &operator<<(std::ostream &os,
                                    const OrderBook &orderBook);
};

#endif // ENGINE_TAKEHOME_INTERVIEW_ORDERPBOOK_H
