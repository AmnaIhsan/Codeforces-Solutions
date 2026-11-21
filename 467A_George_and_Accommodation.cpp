#include <iostream>
using namespace std;
 
int main()
{
    int n,count=0;
    cin >> n;
    for (int i = 0; i < n; i = i + 1)
    {
        int p, q;
        cin >> p>> q;
        if (p+2 <= q)
            count = count + 1;
    }
    cout << count;
    return 0;
}