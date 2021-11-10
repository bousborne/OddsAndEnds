#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <cstdint>
#include <iostream>

//{SeqNo=1, MEID=0, Price=10, Quantity=100}
//{SeqNo=1, MEID=1, Price=10, Quantity=100}
//{SeqNo=2, MEID=0, Price=200, Quantity=200}
//{SeqNo=3, MEID=0, Price=30, Quantity=300}
//{SeqNo=2, MEID=1, Price=200, Quantity=200}
//{SeqNo=3, MEID=1, Price=30, Quantity=300}

class Message {
public:
    uint64_t seqNo;
    uint8_t MEID;
    uint32_t price;
    uint32_t quantity;

public:
    std::vector<Message> mes;

    Message(uint64_t in_seqNo, uint8_t in_MEID, uint32_t in_price, uint32_t in_quantity) {
        seqNo = in_seqNo;
        MEID = in_MEID;
        price = in_price;
        quantity = in_quantity;
    }

    void PrintMessage() {
        std::cout << seqNo << " " << MEID << " " << price << " " << quantity << std::endl;
    }
};

void printNonDuplicate(std::vector<Message> mes) {
    int greatestSeqId=0;
    for (auto m : mes) {
        if (m.seqNo > greatestSeqId) {
            //not duplicate
            m.PrintMessage();
            greatestSeqId = m.seqNo;
        }
    }
}

int main(int argc, char *argv[]) {

    Message m1(1, 0, 10, 100);
    Message m2(1, 1, 10, 100);
    Message m3(2, 0, 200, 200);
    Message m4(3, 0, 30, 300);
    Message m5(2, 1, 200, 200);
    Message m6(3, 1, 30, 300);

    std::vector<Message> mes;
    mes.push_back(m1);
    mes.push_back(m2);
    mes.push_back(m3);
    mes.push_back(m4);
    mes.push_back(m5);
    mes.push_back(m6);

    printNonDuplicate(mes);

    return 0;
}