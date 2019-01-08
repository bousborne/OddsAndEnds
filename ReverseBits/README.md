# ReverseBits
Random bits of code and/or applets I have decided to save.

Code is compiled with Linux GCC 'gcc -o rev revtest.c
Code is run with './rev', then enter any value.

Instructions
Write a function to reverse the order of bits in an array of 1..n bytes (for 6 bytes, bit 0 is exchanged with bit 47). 

The function prototype should be:
		void ReverseBits(unsigned char *arr, int len_arr);
arr is the array of bytes being reversed
len_arr is the number of bytes being reversed
Examples
Hex Input String
Byte Values
Reversed Values
Hex Output String
1
1
128
80
15
21
168
A8
400
4, 0
0, 32
0020
200F
32, 15
15, 4
F004
550130
85, 1, 48
12, 128, 170
0C80AA
Details
1. Compile the code as-is
Verify that you can compile and run the code provided. Since you have not yet implemented ReverseBits, the program will print out any hex numbers that you enter at the prompt, e.g.
Enter hexadecimal number to be bit reversed. Example: 3F2C45
01
01 --> 01
15
15 --> 15

2. Edit the code to implement the function
The main() function in revtest.c is already set up to call ReverseBits() and display the results. Note that the call to ReverseBits() is commented out and the actual ReverseBits() method.is missing completely. The test program goes into a loop reading hexadecimal input strings and calling the reverse bits function.

3. Compile and run your program
An example of the correct output is shown here:
Enter hexadecimal number to be bit reversed. Example: 3F2C45
01
01 --> 80
15
15 --> A8
