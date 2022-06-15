#include <cstdio>
#include <set>
#include <vector>

#define X first
#define Y second
#define PB push_back

using namespace std;

typedef pair < int , int > pii;

const int N = 1e5 + 500;

set < pii > S[N][2];
vector < int > v[N];
int n, ans[N], dp[N][2];

inline void recalc(int x){
	if((int)S[x][0].size() == 0)
		dp[x][0] = dp[x][1] = 1;
	else{
		dp[x][0] = S[x][0].rbegin() -> X + 1;
		dp[x][1] = S[x][1].begin() -> X + 1;
	}
}

void f_ob(int x, int lst){
	for(int y : v[x]){
		if(y == lst) continue;
		f_ob(y, x);
		S[x][1].insert({dp[y][0], y});
		S[x][0].insert({dp[y][1], y});
	}
	recalc(x);
}

void f_re(int x, int lst){
	recalc(x);
	ans[x] = dp[x][1];
	for(int y : v[x]){
		if(y == lst) continue;
		int st0 = dp[y][0], st1 = dp[y][1];
		S[x][0].erase({st1, y}); S[x][1].erase({st0, y});
		recalc(x); 
		S[y][0].insert({dp[x][1], x}); S[y][1].insert({dp[x][0], x});
		f_re(y, x);
		S[y][0].erase({dp[x][1], x}); S[y][1].erase({dp[x][0], x});
		S[x][0].insert({st1, y}); S[x][1].insert({st0, y});
		dp[y][0] = st0, dp[y][1] = st1;
	}
}

int main(){
	scanf("%d", &n);
	for(int i = 1;i < n;i++){
		int x, y; scanf("%d%d", &x, &y);
		v[x].PB(y), v[y].PB(x);
	}
	f_ob(1, 1); f_re(1, 1);
	int bst = 0;
	for(int i = 1;i <= n;i++)
		bst = max(bst, ans[i]);
	printf("%d\n", bst);
	return 0;
}
