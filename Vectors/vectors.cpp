#include <iostream>
#include <vector>
using namespace std;

int main(void)
{
  std::vector<int> v1, v2, v3;
  v1 = {1, 2, 3, 4, 5};
  v2 = {6, 7, 8, 9, 10};
  std::vector<int>::const_iterator i;

  v1.insert(v1.end(), v2.begin(), v2.end());

  for (i = v1.begin(); i != v1.end(); i++)
  {
    std::cout << (*i);
  }

  v1.clear();
  for (i = v1.begin(); i != v1.end(); i++)
  {
    std::cout << (*i);
    std::cout << "clear";
  }
  std::cout << "cleared";

  float fl = 217.342454;

  printf("\n");

  cout << fl;

  return 0;
}
