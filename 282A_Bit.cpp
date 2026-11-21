#include <iostream>
#include <string>
using namespace std;
 
int main()
{
    int n;
    cin >> n;
    int X=0;
    while (n > 0)
    {
        string c;
        cin >> c;
        if (c == "++X" || c == "X++")
            X = X + 1;
        else if (c == "--X" || c == "X--")
            X = X - 1;
        n = n - 1;
    }
    cout << X;
    return 0;
}