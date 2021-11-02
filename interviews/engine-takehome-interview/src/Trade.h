#ifndef ENGINE_TAKEHOME_INTERVIEW_TRADE_H
#define ENGINE_TAKEHOME_INTERVIEW_TRADE_H

typedef struct Trade {
    std::string sSide;
    std::string sInstrument;
    std::string orderId;
    std::string contraOrderId;
    int quantity;
    int price;

    Trade(std::string in_sSide, std::string in_sInstrument,
          std::string in_orderId, std::string in_contraOrderId, int in_quantity,
          int in_price)
        : sSide(in_sSide), sInstrument(in_sInstrument), orderId(in_orderId),
          contraOrderId(in_contraOrderId), quantity(in_quantity),
          price(in_price) {
    }
} Trade;

#endif // ENGINE_TAKEHOME_INTERVIEW_TRADE_H
