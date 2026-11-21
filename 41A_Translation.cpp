#include <iostream>
#include <cstring>
using namespace std;
 
int main()
{
    char s[101];
    char t[101];
    cin >> s >> t;
    int n = strlen(s);
    int i = 0;
    while (i < n / 2)
    {
        char temp = s[i];
        s[i] = s[n - 1 - i];
        s[n - 1 - i] = temp;
        i = i + 1;
    }
 
    if (strcmp(s, t) == 0)
        cout << "YES";
    else
        cout << "NO";
 
    return 0;
}