#include <fstream>
#include <iostream>
#include <experimental/filesystem>
using namespace std;
namespace fs = std::experimental::filesystem;

int main()
{
  std::string filename1 = "file1.txt";
  std::string filename1 = "file2.txt";

  ofstream file1;
  ofstream file2;
  fs::create_directories("sandbox/a/b");
  file1 = ofstream("sandbox/file1.txt");
  file2 = ofstream("sandbox/file2.txt");
  file1.open("sandbox/file2.txt");
  // if (file1.is_open())
  // {
  //   cout << "open\n";
  // }
  // else
  // {
  //   cout << "aint open\n";
  // }
  for (auto &p : fs::directory_iterator("sandbox"))
    std::cout << p.path() << '\n';
  // fs::remove_all("sandbox");
}