#include <bits/stdc++.h>
using namespace std;

class Person
{
public:
  string firstName;
  string lastName;
  int test = 33;

  Person()
  {
    firstName = "Ben";
    lastName = "Ousborne";
  }

  virtual void printTest()
  {
    cout << "Person test value is: " << test << "\n";
  }

  void printName()
  {
    cout << "This persons name is " << firstName << " " << lastName << "\n";
  }
};

class Geek : public Person
{
  // Access specifier
public:
  // Data Members
  string language;
  int test = 21;

  Geek()
  {
    language = "C++";
  }

  void printTest()
  {
    cout << "Geek Test value is: " << test << "\n";
  }

  // Member Functions()
  void printLanguage()
  {
    cout << "This Geeks language is: "
         << language << "\n";
  }
};

int main()
{

  // Declare an object of class geeks
  Person *person1 = new Person;
  Geek geek1;

  person1 = &geek1;

  // accessing data member
  geek1.firstName = "Harry";
  geek1.lastName = "Potter";
  geek1.language = "Witch++";

  // accessing member function
  geek1.printName();
  geek1.printLanguage();
  geek1.printTest();

  cout << "Now testing person:\n";

  person1->printName();
  // person1->printLanguage();
  person1->printTest();

  return 0;
}