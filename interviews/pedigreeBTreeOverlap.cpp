#include <iostream>
using namespace std;

// To execute C++, please define "int main()"
int main() {
  auto words = { "Hello, ", "World!", "\n" };
  for (const string& word : words) {
    cout << word;
  }
  return 0;
}


/* 
Your previous Python 3 content is preserved below:

 
# # Question
# #
# # Two of my neighbors recently adopted their own dog from the same dog rescue
# # organization. These dogs each came with an extensive pedigree.
# #  
# # Write a routine to determine if the two dogs have a common ancestor.
# #
# #
# # For Example:
# #
# #       A            dog            Z
# #   +---^---+                      / \
# #   B       C      parents        Y   G
# #  / \     / \                   / \
# # D   E   F   G  grandparents   B   W
# #                              / \
# #                             D   E
# #                            
# # In the above example, B, D, E, or G would all be valid answers
# 
#    
# #For each dog, the pedigree contains:
# 
# #    Its sire, if known
# #    Its dam, if known
# #    A list of its offspring, if there are any
# 
# #Inbreeding is common so a dog's sire may also be it's dam's
# #grand-sire (however, there are no loops)
# 
# #A dog's pedigree is finite in size

 */
struct DogNode {
  string pedigree;
  string sire;
  string dam;
  DogNode *left;
  DogNode *right;
  DogNode(string xIn) : pedigree(xIn), left(NULL), right(NULL);
};

class Pedigree {
 public:
  bool findCommonParent(DogNode* root1, DogNode* root2) {
    unordered_map<string> map;
    queue<DogNode*> q;
    queue<DogNode*> q2;
    
    
    //check for NULL on both!!!
    q.push(root1);
    q2.push(root2);
    while(!q.empty()) {
      
      DogNode* temp = q.front();
      map.insert(temp);
      
      while(!q2.empty()) {
        DogNode* temp2 = q2.front();
        
        
        if (map.find(temp2)) {
         return true; 
        }
        
        if(root2->left != NULL) {
         q2.push(root2->left); 
        }
        if (root2->right != NULL) {
         q2.push(root2->right); 
        }
        
        q2.pop();
        
      }
      
      if(root1->left != NULL) {
       q.push(root1->left);
      }
      if (root1->right != NULL) {
       q.push(root1->right);
      }
      
      q.pop();
      
      
    }
    // if (root1 == NULL || root2 == NULL)
      // return 
    
    // TreeNode 
    return false;
  }
  
}
