#include <iostream>
#include <cstring>
using namespace std;
 
int main()
{
	char a[101];
	cin >> a;
	int count = 0;
	for(int i=0;i<strlen(a);i=i+1)
	{
		bool distinct = true;
		for (int j = 0; j < i; j = j + 1)
		{
			if (a[i] == a[j])
			{
				distinct = false;
			}
		}
		if (distinct)
			count = count + 1;
	}
	if (count % 2 == 0)
		cout << "CHAT WITH HER!";
	else
		cout << "IGNORE HIM!";
		
	return 0;
}