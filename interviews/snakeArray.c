/*
The objective here is to populate an array of a given size in a 'snakelike' pattern up and down like so:

Given an empty array of 3x3, the array should look like this at the end:
    0  7  8
    1  6  9
    2  5  10
    3  4  11
Assumptions:
- The array is not necessarily square
- The number of elements is 'reasonable' (no special scaling needed)

*/

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

void snake_array(uint64_t **arr, const uint64_t rows, const uint64_t cols)
{
    // TODO
  int count=0;
  for (int i=0; i<cols; i++) {
    if (i % 2 == 0){
      for (int j=0; j<rows; j++) {
        // if(j%2==1) arr[i][j] = 
        //fill in 0 to 
        arr[j][i] = count;
        count++;
      }
    } else {
      for (int j = rows-1; j>= 0; j--) {
       //fill in opposite
        arr[j][i] = count;
        count++;
      }
    }
  }
}

int main()
{
    uint64_t ROWS = 3;
    uint64_t COLS = 3;

    uint64_t **arr = (uint64_t**)malloc(sizeof(uint64_t *) * ROWS);
    for (uint64_t i = 0; i < ROWS; i++)
    {
        arr[i] = (uint64_t *)malloc(sizeof(uint64_t) * COLS);
    }

    for (uint64_t i = 0; i < ROWS; i++)
    {
        for (uint64_t j = 0; j < COLS; j++)
        {
            arr[i][j] = 0;
        }
    }

    snake_array(arr, ROWS, COLS);

    printf("Array:\n");
    for (uint64_t i = 0; i < ROWS; i++)
    {
        for (uint64_t j = 0; j < COLS; j++)
        {
            uint64_t val = arr[i][j];
            if (val < 10)
            {
               printf(" ");
            }
            printf(" %ld", arr[i][j]);
        }
        printf("\n");
    }

    for (uint64_t i = 0; i < ROWS; i++)
    {
        free(arr[i]);
    }
    free(arr);


}
