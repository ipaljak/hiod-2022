#include <cstdio>
#include <cstring>
#include <ctime>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <unistd.h>

#define PB push_back
#define X first
#define Y second

using namespace std;

typedef vector < int > vi;
typedef pair < int , int > pii;

int n, k;

int pretvori(char* s){
	int l = strlen(s);
	int ret = 0;
	for(int i = 0;i < l;i++)
		ret = 10 * ret + s[i] - '0';
	return ret;
}

int main(int argc, char** argv){
	n = pretvori(argv[1]);
	k = pretvori(argv[2]);
	srand(time(NULL) * getpid());
	n -= rand() % 20;
	if(k > 2 && rand() % 2 == 0) k--;
	printf("%d %d\n", n, k);
	vector < pii > mogu;
	for(int b = 0;b < 10;b++)
		mogu.PB({rand() % k, rand() % k});
	vector < int > v;
	for(int j = 0;j < k;j++) v.push_back(j + 1);
	
	for(int i = 0;i < n;i++){
		for(pii tmp : mogu)
			if(rand() % 2) swap(v[tmp.X], v[tmp.Y]);
		for(int j = 0;j < k;j++){
			printf("%d", v[j]);
			printf(j == k - 1 ? "\n" : " ");
		}
	}
	return 0;
}
