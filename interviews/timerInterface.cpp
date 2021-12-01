#include <iostream>
#include <vector>

using namespace std;


class Timer{
    private:
        // int currentTime;
        unsigned int currDueTimeInTickCount;
        int inVal;

    public:
        Timer(unsigned int dueTimeInTickCount, int val) {
            currDueTimeInTickCount = dueTimeInTickCount;
            inVal = val;
        }
        unsigned int getDueTime() {
            return currDueTimeInTickCount;
        }
        int getVal() {
            return inVal;
        }

};
class TimeCollection {
    public:
        vector<Timer*> timerList;
        Timer* CreateTimer(unsigned int dueTimeInTickCount, int val)       {
            // currentTime = 0;
            Timer *t = new Timer(dueTimeInTickCount, val);
            
            timerList.push_back(t);
            return t;
        }

        void cancelTimer(Timer *timer) {
            std::vector<Timer*>::iterator iter = timerList.begin();
            std::vector<Timer*>::iterator enditer = timerList.end();
            for (; iter != enditer; ++iter) {
                if (*iter == timer) {
                    timerList.erase(iter,iter);
                }
            }

        }

        void OnTimerTick(unsigned int currentTimeInTickCount) {
            std::vector<Timer*>::iterator iter = timerList.begin();
            std::vector<Timer*>::iterator enditer = timerList.end();
            for (; iter != enditer; ++iter) {
                if(currentTimeInTickCount >= (*iter)->getDueTime()) {
                    std::cout << (*iter)->getVal() << std::endl;
                    cancelTimer((*iter));
                }
            }
        }
    
};

int main()
{
    cout << "test" << endl;
    TimeCollection *tCol = new TimeCollection();
    tCol->CreateTimer(5, 1);
    tCol->CreateTimer(10, 2);
    tCol->CreateTimer(20, 3);

    for (int j=0; j<30; j++) {
        tCol->OnTimerTick(j);
    }
    // Timer *t1 = new Timer(5, 1);
    return 0;
}
