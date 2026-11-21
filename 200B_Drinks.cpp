#include <iostream>
#include <iomanip>
using namespace std;
 
int main()
{
    int n;
    cin >> n;
    double sum = 0;
    for (int i = 0; i < n; i = i + 1)
    {
        double p;
        cin >> p;
        sum = sum + p;
    }
    double average = sum / n;
    cout <<setprecision(14)<< average;
 
    return 0;
}