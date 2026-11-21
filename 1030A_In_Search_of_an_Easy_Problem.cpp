#include <iostream>
using namespace std;
 
int main()
{
    int n;
    cin >> n;
    int opinion[100];
    for (int i = 0; i < n; i = i + 1)
    {
        cin >> opinion[i];
    }
    bool hard = false;
    for (int i = 0; i < n; i = i + 1)
    {
        if (opinion[i] == 1)
            hard = true;
    }
    if (hard==true)
        cout << "HARD";
    else
        cout << "EASY";
 
    return 0;
}