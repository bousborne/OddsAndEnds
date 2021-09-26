#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define BITSIZE 64

int testBit(uint64_t* arr, int k){
    return ((arr[k/BITSIZE] & (1 << (k%BITSIZE) )) !=0);
}

void setBit(uint64_t* arr, int k){
    arr[k/BITSIZE] |= 1 << (k%BITSIZE);
}

void clearBit(uint64_t* arr, int k){
    arr[k/BITSIZE] &= ~(1 << (k%BITSIZE));
}

void printPages(uint64_t* arr, int ROWS, size_t numBits) {
    for (int i=0; i<ROWS; i++) {
        printf("%ld\n", arr[i]);
    }
    for (int i=0; i<ROWS; i++) {
	for (int j=0; j<BITSIZE; j++) {
            printf("%d", testBit(arr, (i*BITSIZE)+j));
	}
        printf("\n");
    }
}

//void setBit(int** arr[], int k){
//    arr[k/BITSIZE] |= 1 << (k%BITSIZE);
//}

//int testBit(uint64_t* arr, int k){
//    return ((arr[k/BITSIZE] & (1 << (k%BITSIZE) )) !=0);
//}

int pageAllocator(uint64_t* arr, int ROWS, size_t numBits) {
    int location=0;
    int count=0;
    
    for (int i=0; i<ROWS; i++) {
        for (int j=0; j<BITSIZE; j++) {
            if ((arr[i] & (1 << j%BITSIZE)) == 0) {
                location = (i/BITSIZE) + j;
		count++;
		if (count == 3) {
                   location = location - 3;
		   return location;
		}
	    } else {
                count = 0;
	    }
	}
    } 
   
    if (count < 3) location = -1;

    return location;
}

int main() {
    int numBits = 64;
    int ROWS = 4;
    //uint64_t arr[4] = {1111111101001110011111111111111111111111010011100111111111111111,
    //	          1111111101001110011111111111111111111111010011100111111111111111,
    //		  1111111101001110011111111111111100011111000111111111111111111111,
    //		  1111111101001110011111111111111111111111010011100111111111111111};

    //uint64_t arr[ROWS];

    
    uint64_t* arr = (uint64_t*)malloc(ROWS * sizeof(uint64_t));
    //for (int i=0; i<ROWS; i++) {
    //    arr[i] = (uint64_t*)malloc(sizeof(uint64_t *));
    //}
    for (int i=0; i <ROWS; i++) {
        arr[i] = 0;
        //arr[i] = 1;
    }
    //for (int i=0; i<ROWS; i++) {
    //    setBit(arr, j*i);
    //}
    //PageAllocator* pageAlloc = new PageAllocator();
    //pageAlloc.pageAllocator(arr, numBits);

    //for (int i=0; i<sizeof(arr); i++) {
    //    for (int j=0; j<BITSIZE; j++) {
    //        setBit(arr, j*i);
    //	}
    //}

    for (int i=0; i<ROWS; i++) {
        for (int j=0; j<BITSIZE; j++) {
            setBit(arr, (i*BITSIZE)+j);
	}
    }
    clearBit(arr, 129);
    clearBit(arr, 130);
    clearBit(arr, 131);
    printPages(arr, ROWS, numBits);
    int pageBegin = pageAllocator(arr, ROWS, numBits);

    //printf("Array:\n");
    //for (uint64_t i = 0; i < ROWS; i++)
    //{
    //   for (uint64_t j = 0; j < BITSIZE; j++)
    //    {
    //        uint64_t val = arr[i];
    //        if (val < 10)
    //        {
    //           printf(" ");
    //        }
    //        printf(" %ld", arr[i]);
    //    }
    //    printf("\n");
    //}

    for (uint64_t i = 0; i < ROWS; i++)
    {
        //free(arr[i]);
    }
    free(arr);

    printf("Allowable page begins on bit %d\n", pageBegin);
    
}
