#include <iostream>
#include <string>
using namespace std;
 
int main()
{
    string s;
    cin >> s;
    int count1 = 0, count2 = 0, count3 = 0;
    for (int i = 0; i < s.length(); i++)
    {
        if (s[i] == '1')
            count1=count1+1;
        else if (s[i] == '2')
            count2= count2 + 1;
        else if (s[i] == '3')
            count3= count3 + 1;
    }
 
    bool first = true;
 
    while (count1 > 0)
    {
        if (!first)
            cout << "+";
        cout << "1";
        first = false;
        count1--;
    }
 
    while (count2 > 0)
    {
        if (!first)
            cout << "+";
        cout << "2";
        first = false;
        count2--;
    }
 
    while (count3 > 0)
    {
        if (!first)
            cout << "+";
        cout << "3";
        first = false;
        count3--;
    }
 
    return 0;
}