#include <iostream>
#include <vector>
using namespace std;

void countBits(char variable)
{
  std::cout << sizeof(variable) << endl;
  int count = 0;

  for (int i = 0; i < sizeof(variable) * 8; i++)
  {
    if (((0x01 << i) & variable) != 0)
    {
      count++;
    }
    cout << "Current Count = " << count << endl
         << "i = " << i << endl;
  }
  cout << "Count = " << count << endl;
}

int main(void)
{

  char variable = 'a';

  printf("%c\n", variable);

  countBits(variable);

  cout << variable << endl;

  return 0;
}
