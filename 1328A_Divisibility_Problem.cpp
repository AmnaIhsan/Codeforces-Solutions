#include <iostream>
using namespace std;
 
int main()
{
    int t;
    cin >> t;
    int a, b;
    for (int i = 0; i < t; i = i + 1)
    {
        cin >> a >> b;
        int count = 0;
        if(a % b != 0)
        {
            count = b - (a % b);
        }
        cout << count << endl;
    }
    return 0;
}