#include <cstdio>
#include <cstring>
#include <ctime>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <unistd.h>

using namespace std;

typedef vector < int > vi;

const int N = 1e5 + 500;

int n;
char s[N];

int pretvori(char* s){
	int l = strlen(s);
	int ret = 0;
	for(int i = 0;i < l;i++)
		ret = 10 * ret + s[i] - '0';
	return ret;
}

int main(int argc, char** argv){
	int n = pretvori(argv[1]);
	srand(time(NULL) * getpid());
	n -=  rand() % 6;
	for(int i = 0;i < n;i++)
		s[i] = 'a' + rand() % 3;
	sort(s, s + n);
	int gr = (rand() % 3 == 0 ? 0 : rand() % 30 + 5);
	for(int i = 0;i < gr;i++)
		swap(s[rand() % n], s[rand() % n]);
	printf("%s\n", s);
	return 0;
}
