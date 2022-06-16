#include <bits/stdc++.h>

using namespace std;

const int MAXN = 1e5 + 10;

vector<int> endpoints, v[MAXN];

bool sol[MAXN];

int n, m, k;
int par[MAXN], lvl[MAXN];

void dfs(int node, int dad, int l) {
  par[node] = dad;
  lvl[node] = l;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    dfs(nxt, node, l + 1);
  }
}

void solve(int node, int dad) {
  sol[node] = true;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    solve(nxt, node);
  }
}

int main(void) {
  scanf("%d%d%d", &n, &m, &k);
  for (int i = 0; i < m; ++i) {
    int a, b, d, x;
    scanf("%d%d%d%d", &a, &b, &d, &x); --a; --b;
    v[a].push_back(b);
    v[b].push_back(a);
    if (x == 1) {
      endpoints.emplace_back(a);
      endpoints.emplace_back(b);
    }
  }

  dfs(0, -1, 0);
  int pivot =
      *max_element(endpoints.begin(), endpoints.end(),
                   [](const int &a, const int &b) { return lvl[a] < lvl[b]; });


  solve(pivot, par[pivot]);

  for (int i = 0; i < k; ++i) {
    int q;
    scanf("%d", &q); --q;
    printf("%d\n", sol[q]);
  }

  return 0;
}
