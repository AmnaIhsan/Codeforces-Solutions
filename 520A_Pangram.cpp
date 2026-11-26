#include <iostream>
using namespace std;
 
int main()
{ 
	int n;
	cin >> n;
	string s;
	cin >> s;
	for (int i = 0; i < n; i = i + 1)
	{
		if (s[i] >= 'A' && s[i] <= 'Z')
			s[i] = s[i] + 32;
	}
	int count = 0;
    for (char ch = 'a'; ch <= 'z'; ch++)
    {
        for (int i = 0; i < n; i++)
        {
            if (s[i] == ch)
            {
                count++;
                break;
            }
        }
    }
 
    if (count == 26)
        cout << "YES";
    else
        cout << "NO";
 
	return 0;
}