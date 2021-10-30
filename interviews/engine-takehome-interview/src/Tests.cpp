#define CATCH_CONFIG_MAIN
#include "catch2.hpp"
#include "OrderBook.h"
#include "OrderProcessor.h"

TEST_CASE("Testing Order","[Order]"){
    REQUIRE(1 == 1);

    SECTION("Test Order Creation") {
        // 12345 BUY BTCUSD 5 10000
        time_t order_time = time(NULL);
        Order* order = new Order("12345", "BUY", "BTCUSD", 5, 10000, order_time);
        REQUIRE(order->orderId == "12345");
        REQUIRE(order->sSide == "BUY");
        REQUIRE(order->sInstrument == "BTCUSD");
        REQUIRE(order->quantity == 5);
        REQUIRE(order->price == 10000);
        REQUIRE(order->orderTime == order_time);
        SUCCEED();
    }
}

TEST_CASE("Testing OrderBook","[OrderBook]"){
    REQUIRE(1 == 1);

    SECTION("Test OrderBook.add_buy") {
        time_t order_time = time(NULL);
        Order* order = new Order("12345", "BUY", "BTCUSD", 5, 10000, order_time);
        OrderBook* orderBook = new OrderBook();
        orderBook->add_buy(order);
        SUCCEED();
    }

    SECTION("Test OrderBook << operator") {
        time_t order_time = time(NULL);
        Order* order1 = new Order("12345", "BUY", "BTCUSD", 5, 10000, order_time);
        Order* order2 = new Order("zod42", "SELL", "BTCUSD", 2, 10001, order_time++);
        Order* order3 = new Order("13471", "BUY", "BTCUSD", 6, 9971, order_time++);
        Order* order4 = new Order("11431", "BUY", "ETHUSD", 9, 175, order_time++);
        Order* order5 = new Order("abe14", "SELL", "BTCUSD", 7, 9800, order_time++);
        Order* order6 = new Order("plu401", "SELL", "ETHUSD", 5, 170, order_time++);
        Order* order7 = new Order("45691", "BUY", "ETHUSD", 3, 180, order_time++);


        OrderBook* orderBook = new OrderBook();
        orderBook->add_buy(order1);
        orderBook->add_sell(order2);
        orderBook->add_buy(order3);
        orderBook->add_buy(order4);
        orderBook->add_sell(order5);
        orderBook->add_sell(order6);
        orderBook->add_buy(order7);
        REQUIRE(!(orderBook->buyList.empty()));
        REQUIRE(!(orderBook->sellList.empty()));
        std::cout << *orderBook << std::endl;
        SUCCEED();
    }

    SECTION("Test OrderBook Matching") {
        time_t order_time = time(NULL);
        Order* order1 = new Order("12345", "BUY", "BTCUSD", 5, 10000, order_time);
        Order* order2 = new Order("abe14", "SELL", "BTCUSD", 7, 9800, order_time++);
        OrderProcessor* orderProc = new OrderProcessor();
        orderProc->processOrder(order1);
        std::ostringstream oss;
        std::streambuf* p_cout_streambuf = std::cout.rdbuf();
        std::cout.rdbuf(oss.rdbuf());
        orderProc->processOrder(order2);
        std::cout.rdbuf(p_cout_streambuf);
        REQUIRE(oss);
        REQUIRE(oss.str() == "TRADE BTCUSD abe14 12345 5 10000\n");
        std::cout << oss.str();
    }
}
