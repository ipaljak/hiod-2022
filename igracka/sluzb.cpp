#include <cstdio>
#include <cstring>
#include <algorithm>

using namespace std;

const int N = 1e5 + 500;

char s[N], t[2][N];
int n;

int main(){
	scanf("%s", s);
	n = strlen(s);
	for(int i = 0;i < n;i++)
		t[i & 1][i / 2] = s[i];
	sort(t[0], t[0] + (n + 1) / 2);
	sort(t[1], t[1] + n / 2);
	for(int i = 0;i < n;i++)
		s[i] = t[i & 1][i / 2];
	for(int i = 1;i < n;i++){
		if(s[i] < s[i - 1]){
			printf("ne\n");
			return 0;
		}
	}
	printf("da\n");
	return 0;
}
