#include <bits/stdc++.h>

using namespace std;

const int MAXN = 1e5 + 10;

vector<int> v[MAXN];

int n;
int dp[2][MAXN], par[MAXN];

inline void init() {
  memset(dp, 0, sizeof dp);
  memset(par, 0, sizeof par);
}

void dfs(bool first, int node, int dad) {
  par[node] = dad;
  dp[first][node] = 1;
  bool fst = true;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    dfs(!first, nxt, node);
    if (fst) {
      dp[first][node] = 1 + dp[!first][nxt];
      fst = false;
      continue;
    }
    if (first)
      dp[first][node] = min(dp[first][node], 1 + dp[!first][nxt]);
    else
      dp[first][node] = max(dp[first][node], 1 + dp[!first][nxt]);
  }
}

int solve() {
  init();
  int root = rand() % n;

  dfs(false, root, -1);
  dfs(true, root, -1);

  int ret = 0;
  for (int i = 0; i < n; ++i) {
    int curr = n + 1;
    for (int j : v[i]) {
      if (j == par[i]) continue;
      curr = min(curr, 1 + dp[false][j]);
    }
    if (curr != n + 1)
      ret = max(ret, curr);
  }

  return ret;
}

int main(void) {
  srand(time(NULL));
  scanf("%d", &n);
  for (int i = 0; i < n - 1; ++i) {
    int a, b;
    scanf("%d%d", &a, &b); --a; --b;
    v[a].push_back(b);
    v[b].push_back(a);
  }

  int sol = 0;
  for (int i = 0; i < 300; ++i)
    sol = max(sol, solve());

  printf("%d\n", sol);

  return 0;
}
