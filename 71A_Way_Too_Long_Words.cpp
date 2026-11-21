#include <iostream>
#include <cstring>
using namespace std;
 
int main()
{
    int n;
    cin >> n;
    char word[101];
 
    for (int i = 0; i < n; i = i + 1)
    {
        cin >> word;
 
        if (strlen(word) <= 10)
            cout << word << endl;
        else
            cout << word[0] << strlen(word) - 2 << word[strlen(word) - 1] << endl;
    }
 
    return 0;
}