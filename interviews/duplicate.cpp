Given an unsorted array of N integers, sampled from [1,N-1], find a duplicate and return the value.

Constraints:
O(1) additional memory.
Better than O(n^2) time.
Input is immutable.


[1, 3, 6, 6, 6, 5, 4] N = 7, range = 1,6

Buckets: [1 -> 3] : 1, 3,
[4->6]: 6, 6, 6, 5, 4

A second d&c
[4->5]:5, 4
[6->6]: 6, 6, 6


Int duplicate(int *arr, N) {
    If (
}
Int duplicateAux(int *arr, N) {
    
    Int size = N/2;
    Int left_arr;
    Int right_arr;
    Int left_low = 0;
    Int mid = N/2;
    Int right_high = N-1;
    
    While (N > 1) {
    for( int j=0; j < N; j++) {
        If (arr[j] >= left_low && arr[j] < mid) {
            Left_arr += 1;
        }
        If (arr[j] >= mid && arr[j] < right_high) {
            right_arr += 1;
        }
        
    }
    If (left_arr > (mid - left_low)) {
        //found dup
        If (N == 1 && (left_low == mid)) {
            Return left_low;
        } else {
            N -= 1;
            Right_high = mid;
            Mid = (right_high - left_low) / 2;
        }

    }
If (right_arr > (right_high - mid)) {
        //found dup
        If (N == 1 && (right_high == mid)) {
            Return right_high;
        } else {
            N -= 1;
            Left_low = mid;
            
            Mid = (right_high - left_low) / 2;
        }

    }
}
If (N == 1) {
Return mid;
}
    
}

