#include "OrderBook.h"

template<typename T>
bool OrderBook::isBuy(T x) {
    return x->sSide == "BUY";
}

bool OrderBook::is_empty() const {
    return (buyList.empty() || sellList.empty());
}

void OrderBook::add_buy(std::shared_ptr<Order>& order) {
    add(order, true);
}

void OrderBook::add_sell(std::shared_ptr<Order>& order) {
    add(order, false);
}

void OrderBook::add(std::shared_ptr<Order>& order, bool buy) {
    if (buy) {
        buyList.push_back(order);
    } else {
        sellList.push_back(order);
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
    Trade *trade = new Trade("TRADE", buyerOrder->sInstrument, buyerOrder->orderId, sellerOrder->orderId, quantity, price);
    buyerOrder->quantity -= quantity;
    sellerOrder->quantity -= quantity;
    tradeList.push_back(trade);
    delete trade;
}

std::ostream& operator<<(std::ostream& os, const OrderBook& book) {
    if (book.is_empty()) {
        os << "Order book is empty.";
        return os;
    }
    os << std::endl;
    for (auto s : book.sellList) {
        if (s->quantity != 0) {
            os << s->orderId << " " << s->sSide << " " << s->sInstrument << " " << s->quantity << " " << s->price
               << std::endl;
        }
    }
    for (auto b : book.buyList) {
        if (b->quantity != 0) {
            os << b->orderId << " " << b->sSide << " " << b->sInstrument << " " << b->quantity << " " << b->price
               << std::endl;
        }
    }
    return os;
}