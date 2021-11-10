#include <iostream>

// stopwatch
// 

class Stopwatch {
private:
    chrono::time startTime;
    chrono::duration<long int> total_time = 0;
    bool running;
public:
    void start() {
        startClock();
    } //
    void pause() {
        pauseClock();
    }
    void reset() {
        resetClock();
    }
    chrono::duration<long int> getTime() {
        if(running) {
            chrono::duration<long int> return_time = chrono::time:now() - startTime + total_time
            return return_time;
        } else {
            return total_time;
        }
    }
private:
    void startClock() {
        if(!running) {
            startTime = chrono::time::now();
            running = true;
        }
    }

    void pauseClock() {
        if(running) {
            total_time += chrono::time::now() - startTime;
            running = false;
        }
    }

    void resetClock() {
        running = false;
        startTime = 0;
        total_time = 0;
    }


}
int main() {
    // you can write to stdout for debugging purposes, e.g.
    std::cout << "This is a debug message" << std::endl;

    return 0;
}
