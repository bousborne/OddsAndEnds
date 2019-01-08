#include <iostream>
using namespace std;
int test1(void);
int test2(void);
int test3(void);

int main(void)
{
    int arr[] = {10, 20};
    int *p = arr;
    ++*p;
    printf("arr[0] = %d, arr[1] = %d, *p = %d\n", arr[0], arr[1], *p);

    int i[] = {1, 2, 3};
    int j[] = {4, 5, 6};

    // *i++ = *j++;

    test1();
    test2();
    test3();
    return 0;
}

int test1(void)
{
    int arr[] = {10, 20};
    int *p = arr;
    ++*p;
    printf("arr[0] = %d, arr[1] = %d, *p = %d\n", arr[0], arr[1], *p);
    return 0;
}

int test2(void)
{
    int arr[] = {10, 20};
    int *p = arr;
    *p++;
    printf("arr[0] = %d, arr[1] = %d, *p = %d\n", arr[0], arr[1], *p);
    return 0;
}

int test3(void)
{
    int arr[] = {10, 20};
    int *p = arr;
    *++p;
    printf("arr[0] = %d, arr[1] = %d, *p = %d\n", arr[0], arr[1], *p);
    return 0;
}