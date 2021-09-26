#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define BITSIZE 32

int testBit(int* arr, int k){
    return ((arr[k/BITSIZE] & (1 << (k%BITSIZE) )) !=0);
}

void setBit(int* arr, int k){
    arr[k/BITSIZE] |= 1 << (k%BITSIZE);
}

void clearBit(int* arr, int k){
    arr[k/BITSIZE] &= ~(1 << (k%BITSIZE));
}

void printPages(int* arr, int ROWS, size_t numBits) {
    for (int i=0; i<ROWS; i++) {
        printf("%d\n", arr[i]);
    }
    for (int i=0; i<ROWS; i++) {
	for (int j=0; j<BITSIZE; j++) {
            printf("%d", testBit(arr, (i*BITSIZE)+j));
	}
        printf("\n");
    }
}

int pageAllocator(int* arr, int ROWS, size_t numBits) {
    int location=0;
    int count=0;
    
    for (int i=0; i<ROWS; i++) {
        for (int j=0; j<BITSIZE; j++) {
            if ((arr[i] & (1 << j%BITSIZE)) == 0) {
                location = (i*BITSIZE) + j;
		
		count++;
		printf("location(%d), count(%d)\n", location, count);
		if (count == 3) {
                   location = location - 3 + 1;
		   return location;
		}
	    } else {
                count = 0;
	    }
	}
    } 
   
    if (count < 3) location = -1;

    return location + 1;
}

int main() {
    int numBits = 64;
    int ROWS = 4;
    
    int* arr = (int*)malloc(ROWS * sizeof(int));
    for (int i=0; i <ROWS; i++) {
        arr[i] = 0;
    }

    for (int i=0; i<ROWS; i++) {
        for (int j=0; j<BITSIZE; j++) {
            setBit(arr, (i*BITSIZE)+j);
	}
    }
    clearBit(arr, 0);
    clearBit(arr, 32);
    clearBit(arr, 24);
    clearBit(arr, 25);
    clearBit(arr, 26);
    clearBit(arr, 31);
    
    clearBit(arr, 33);
    printPages(arr, ROWS, numBits);
    int pageBegin = pageAllocator(arr, ROWS, numBits);


    for (int i = 0; i < ROWS; i++)
    {
        //free(arr[i]);
    }
    free(arr);

    printf("Allowable page begins on bit %d\n", pageBegin);
    
}
