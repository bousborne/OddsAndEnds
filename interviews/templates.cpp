#include <iostream>

/*
 * Write a class template for a moving-average/boxcar filter that inherits
 * from the following virtual base-class template and takes the following parameters:
 * -> Fundamental Type [of the values being averaged]
 * -> Filter Size
 *
 * Class should implement the following virtual methods:
 *  - The '+=' operator to add values to the filter
 *  - The function call operator '()' to obtain the current average
 *  - A method to clear the filter
 */

constexpr size_t FILTER_SIZE = 10;

/* Base class template */
template <typename T, size_t N>

class Filter {

public:
    Filter() {}
    ~Filter() = default;

    virtual void clear() = 0;
    virtual T operator+=(const T sample) = 0;
    virtual operator T() const = 0;
    T samples[N];
};

/* MovingAverage class template */

template <typename T, size_t N>
class MovingAverage : public Filter<T, N> {
public:  // I was just missing this public identifier!
    T operator+=(const T sample) {
        if (index >= N) {
            index=0;
            isFull = true;
        }
        if (index < N) {
            this->samples[index] = sample;
            index++;
        }
        return T();
    }
   
    operator T() const {
        T avg = 0;
        int divisor = 0;
        if(isFull) {
            divisor = N;
        } else {
            divisor = index;
        }

        for(int i=0; i<N; i++) {
            avg += this->samples[(index + i) % N];
        }
        avg /= divisor; // I changed this from N to divisor and used my "isFull" Bool to determine how many I divide by.
        // So, if there are only 2 or so numbers in, it will only average by 2, not the full 10
        // My understanding was the first set will be (3+2+1+2+3) / 5
        // Second set will be (3+2+1+2+3+10+12+14+12+10) / 10
        // Third set will be (12+14+12+10+12+10+12+14+12+10) / 10 which is third set in first half of array, second set in second half of array
        // If the above is a bad understanding of what it is supposed to do, I just wanted to make sure I wrote out my logic here!
        return avg;
    }
   
    void clear() {
        this->index = 0;
        this->isFull = false;
        for(int i=0; i<N; i++) {
            this->samples[i] = T();
        }
    }
    private:
    int index = 0;
    bool isFull = false;
};


int main() {
    MovingAverage<double, FILTER_SIZE> mavg;

    /* set 1 */
    mavg += 3.0;
    mavg += 2.0;
    mavg += 1.0;
    mavg += 2.0;
    mavg += 3.0;
    std::cout << "avg: " << std::to_string(mavg) << std::endl;

    /* set 2 */
    mavg += 10.0;
    mavg += 12.0;
    mavg += 14.0;
    mavg += 12.0;
    mavg += 10.0;

    std::cout << "avg: " << std::to_string(mavg) << std::endl;
    
    /* set 3 */
    mavg += 12.0;
    mavg += 14.0;
    mavg += 12.0;
    mavg += 10.0;
    mavg += 12.0;

    std::cout << "avg: " << std::to_string(mavg) << std::endl;
    
    mavg.clear();
    std::cout << "avg: " << std::to_string(mavg) << std::endl;
  
    return 0;
}
