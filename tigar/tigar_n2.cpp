#include <bits/stdc++.h>

using namespace std;

const int MAXN = 5010;

vector<int> v[MAXN];

int n;
int memo[2][MAXN][MAXN];

int solve(bool first, int node, int dad) {
  if (memo[first][node][dad] != -1) return memo[first][node][dad];
  int ret = 1;
  bool fst = true;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    if (fst) {
      ret = 1 + solve(!first, nxt, node);
      fst = false;
      continue;
    }
    if (first)
      ret = min(ret, 1 + solve(!first, nxt, node));
    else
      ret = max(ret, 1 + solve(!first, nxt, node));
  }
  return memo[first][node][dad] = ret;
}

int main(void) {
  scanf("%d", &n);
  for (int i = 0; i < n - 1; ++i) {
    int a, b;
    scanf("%d%d", &a, &b); --a; --b;
    v[a].push_back(b);
    v[b].push_back(a);
  }

  memset(memo, -1, sizeof memo);

  int sol = 0;
  for (int i = 0; i < n; ++i) {
    int curr = n;
    for (int j : v[i])
      curr = min(curr, 1 + solve(false, j, i));
    sol = max(sol, curr);
  }

  printf("%d\n", sol);
  return 0;
}

