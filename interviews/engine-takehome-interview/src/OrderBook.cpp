#include "OrderBook.h"

template<typename T>
bool OrderBook::isBuy(T x) {
    return x->sSide == "BUY";
}

bool OrderBook::isEmpty() const {
    return (buyList.empty() || sellList.empty());
}

bool OrderBook::sellSortCompare(const std::shared_ptr<Order>& order1, const std::shared_ptr<Order>& order2) {
    if(order1->price != order2->price) {
        return (order1->price < order2->price);
    }
    return (order1->orderTime < order2->orderTime);
}

bool OrderBook::buySortCompare(const std::shared_ptr<Order>& order1, const std::shared_ptr<Order>& order2) {
    if(order1->price != order2->price) {
        return (order1->price > order2->price);
    }
    return (order1->orderTime < order2->orderTime);
}

bool OrderBook::timeSortCompare(const std::shared_ptr<Order>& order1, const std::shared_ptr<Order>& order2) {
    return (order1->orderTime < order2->orderTime);
}

void OrderBook::addBuy(std::shared_ptr<Order>& order) {
    add(order, true);
}

void OrderBook::addSell(std::shared_ptr<Order>& order) {
    add(order, false);
}

void OrderBook::add(std::shared_ptr<Order>& order, bool buy) {
    if (buy) {
        buyList.push_back(order);
        std::sort( buyList.begin(), buyList.end(), buySortCompare );
    } else {
        sellList.push_back(order);
        std::sort( sellList.begin(), sellList.end(), sellSortCompare );
    }
}

void OrderBook::match( std::shared_ptr<Order>& order) {
    if(isBuy(order)) {
        std::vector<std::shared_ptr<Order>>::iterator it;
        for(it = sellList.begin(); it != sellList.end(); it++) {
            if ((order->sInstrument == (*it)->sInstrument) && (order->price >= (*it)->price) && ((*it)->quantity != 0)) {
                makeTrade(order, (*it), order->price, MIN(order->quantity, (*it)->quantity));
                (*it)->quantity -= MIN(order->quantity, (*it)->quantity);
            }
        }
    }
    if(!isBuy(order)) {
        std::vector<std::shared_ptr<Order>>::iterator it;
        for(it = buyList.begin(); it != buyList.end(); it++) {
            if ((order->sInstrument == (*it)->sInstrument) && (order->price <= (*it)->price) && ((*it)->quantity != 0)) {
                makeTrade((*it), order, (*it)->price, MIN(order->quantity, (*it)->quantity));
                (*it)->quantity -= MIN(order->quantity, (*it)->quantity);
            }
        }
    }
}

void OrderBook::makeTrade( std::shared_ptr<Order>& buyerOrder, std::shared_ptr<Order>& sellerOrder, int price, int quantity) {
    std::cout << "TRADE " << buyerOrder->sInstrument << " " << sellerOrder->orderId << " " << buyerOrder->orderId << " " << quantity << " " << price << std::endl;
    std::shared_ptr <Trade> trade(new Trade("TRADE", buyerOrder->sInstrument, buyerOrder->orderId, sellerOrder->orderId, quantity, price));
    buyerOrder->quantity -= quantity;
    sellerOrder->quantity -= quantity;
    tradeList.push_back(trade);
}

void OrderBook::printRemaining() {
    // These sorts are unnecessary for matching, but rather to just make the end result match the sort of the example
    std::sort( sellList.begin(), sellList.end(), timeSortCompare );
    std::sort( buyList.begin(), buyList.end(), timeSortCompare );

    std::cout << std::endl;
    if (isEmpty()) {
        std::cout << "Order book is empty.";
    }
    for (const auto &s : sellList) {
        if (s->quantity != 0) {
            std::cout << s->orderId << " " << s->sSide << " " << s->sInstrument << " " << s->quantity << " " << s->price
               << std::endl;
        }
    }
    for (const auto &b : buyList) {
        if (b->quantity != 0) {
            std::cout << b->orderId << " " << b->sSide << " " << b->sInstrument << " " << b->quantity << " " << b->price
               << std::endl;
        }
    }
}

std::ostream& operator<<(std::ostream& os, const OrderBook& book) {
    if (book.isEmpty()) {
        os << "Order book is empty.";
        return os;
    }
    os << std::endl;
    for (const auto &s : book.sellList) {
        if (s->quantity != 0) {
            os << s->orderId << " " << s->sSide << " " << s->sInstrument << " " << s->quantity << " " << s->price
               << std::endl;
        }
    }
    for (const auto &b : book.buyList) {
        if (b->quantity != 0) {
            os << b->orderId << " " << b->sSide << " " << b->sInstrument << " " << b->quantity << " " << b->price
               << std::endl;
        }
    }
    return os;
}