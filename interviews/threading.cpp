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

class ThreadIncreaser {
public:
    vector<std::thread> threadVector;
    void* incVal(int threadIVal) {
        std::thread::id this_id = std::this_thread::get_id();
        while (true) {
            auto current = globalInt.load();
            if (current >= MAX_VAL) {
                return NULL;
            }
            if((current % 2) == (threadIVal % 2)) {
                cout << "Increasing " << current <<  " from thread: " << this_id << "\n";
                auto next = current + 1;
                globalInt.compare_exchange_strong(current, next);
            }
        }
        return NULL;
    }

    void createThreads(int numThreads) {
        cout << "incVal" << endl;
        for(int i=0; i<numThreads; i++) {
            thread th = std::thread([&](){incVal(i);});
            threadVector.push_back(move(th));
            cout << "Thread created\n";
        }

        for(auto& t: threadVector) {
            t.join();
        }
    }
};

int main() {
    int numThreads = 2;
    ThreadIncreaser threadInc;
    threadInc.createThreads(numThreads);

    cout << "Returned from threads" << endl;
    return 0;
}
