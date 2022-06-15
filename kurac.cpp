#include <cstdio>
#include <vector>
#include <set>

#define X first
#define Y second
#define PB push_back

using namespace std;

typedef long long ll;
typedef pair < int, int > pii;
typedef pair < ll, int > pli;

const int N = 1e5 + 500;

int n, m, k, q, bio[N], od[N];
set < pli > S;
ll dis[N];
vector < int > v[N];
vector < pii > g[N];

void oznaci(int x){
	if(bio[x]) return;
	for(int y : v[x])
		oznaci(y);
}

int main(){
	scanf("%d%d%d", &n, &m, &k);
	for(int i = 2;i <= n;i++)
		dis[i] = (ll)1e18;
	for(int i = 0;i < m;i++){
		int u1, u2, c, a; scanf("%d%d%d%d", &u1, &u2, &c, &a);
		g[u1].PB({u2, c});
		g[u2].PB({u1, c});
		if(a) od[u1] = 1, od[u2] = 1;
	}
	S.insert({0, 1});
	for(;(int)S.size() > 0;){
		int cur = S.begin() -> Y;
		S.erase(S.begin());
		for(pii &tmp : g[cur]){
			if(dis[cur] + tmp.Y < dis[tmp.X]){
				dis[tmp.X] = dis[cur] + tmp.Y;
				S.insert({dis[tmp.X], tmp.X});
			}
		}
	}
	for(int i = 1;i <= n;i++){
		for(pii &tmp : g[i]){
			if(dis[tmp.X] == dis[i] + tmp.Y)
				v[i].PB(tmp.X);
		}
	}
	int bst = 0;
	for(int i = 1;i <= n;i++){
		if(od[i] && dis[i] > dis[bst]) 
			bst = i;
	}
	oznaci(bst);
	for(;k--;){
		int x; scanf("%d", &x);
		printf("%d\n", bio[x]);
	}
	return 0;
}
