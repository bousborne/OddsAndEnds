
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>
#include <atomic>

#define MAX_VAL 10

using namespace std;

thread tid[2];
mutex countMutex;
atomic<int> globalInt = 0;

class BuyLine {
public:
    vector<
}