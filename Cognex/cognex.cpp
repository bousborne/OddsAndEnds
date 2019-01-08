#include <bits/stdc++.h>
#include <stdio.h>
#include <string.h>
using namespace std;

void histogram(string str)
{
  int hist[256] = {0};
  for (int i = 0; i < str.length(); i++)
  {
    hist[str[i]]++;
  }

  for (int i = 0; i < 256; i++)
  {
    if (hist[i] != 0)
    {
      printf("The letter %c appears %d times", i, hist[i]);
    }
  }
}

int main()
{
  string str = "hello";
  histogram(str);
  return 0;
}