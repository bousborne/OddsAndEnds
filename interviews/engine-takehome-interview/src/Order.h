#ifndef ENGINE_TAKEHOME_INTERVIEW_ORDER_H
#define ENGINE_TAKEHOME_INTERVIEW_ORDER_H

#include <string>

typedef struct Order {
    std::string orderId;
    std::string sSide;
    std::string sInstrument;
    int quantity;
    int price;
    time_t orderTime;

    Order(std::string in_orderId, std::string in_sSide,
          std::string in_sInstrument, int in_quantity, int in_price,
          time_t in_orderTime)
        : orderId(in_orderId), sSide(in_sSide), sInstrument(in_sInstrument),
          quantity(in_quantity), price(in_price), orderTime(in_orderTime) {
    }
} Order;

#endif // ENGINE_TAKEHOME_INTERVIEW_ORDER_H
