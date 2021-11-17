
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

// #include <iostream>
// using namespace std;



// /*

// Write a program that takes a count and creates 2 threads. Each thread increments a global variable.
// Thread 1 increments the global only if the global is odd, while thread 2 increments the global only if it is even.
// The program terminates once the count reaches the value of the input.

// */

// thread tid[2];
// mutex countMutex;
// int globalInt = 0;
  
// class threadInc {
//   public:
  
//   void incVal(void* threadIdIncoming) {
//     countMutex.lock();
//     if (globalInt % 2 == 0) {
//       if(threadIdIncoming == 0 ) {
//         globalInt++;
//       }
//     }
//     if (globalInt % 2 == 1) {
//       if(threadIdIncoming == 1 ) {
//         globalInt++;
//       }
//     }
//     countMutex.unlock()
//   }
  
// }

// int main() {
// 	// cout<<"Hello";
//   int i=0;
//   while (i < 2) {}
//     thread th(&(tid[i]), incVal );
    
//   }
  
//   thread.join()
// 	return 0;
// }
