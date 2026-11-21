#include <iostream>
#include <cstring>
using namespace std;
 
int main()
{
	char s[101];
	cin >> s;
	int upper=0,lower=0,i = 0;
	while (i < strlen(s))
	{
		if (s[i] >= 'A' && s[i] <= 'Z')
			upper = upper + 1;
		else if (s[i] >= 'a' && s[i] <= 'z')
			lower = lower + 1;
		i = i + 1;
	}
	int j = 0;
	if (upper > lower)
	{
		while (j < strlen(s))
		{
			if (s[j] >= 'a' && s[j] <= 'z')
				s[j] = s[j] - 32;
			j = j + 1;
		}
	}
	else
	{
		while (j < strlen(s))
		{
			if (s[j] >= 'A' && s[j] <= 'Z')
				s[j] = s[j] + 32;
			j = j + 1;
		}
	}
	cout << s;
	return 0;
}