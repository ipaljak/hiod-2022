#include <bits/stdc++.h>

using namespace std;

const int MAXN = 1e5 + 10;

vector<int> v[MAXN];

map<pair<int, int>, int> eid;

int n;
int dp[2][2 * MAXN], par[MAXN];

void solve_down(bool first, int node, int dad) {
  par[node] = dad;
  int edge_id = eid[{dad, node}];
  dp[first][edge_id] = 1;
  bool fst = true;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    solve_down(!first, nxt, node);
    int nxt_eid = eid[{node, nxt}];
    if (fst) {
      dp[first][edge_id] = 1 + dp[!first][nxt_eid];
      fst = false;
      continue;
    }
    if (first)
      dp[first][edge_id] = min(dp[first][edge_id], 1 + dp[!first][nxt_eid]);
    else
      dp[first][edge_id] = max(dp[first][edge_id], 1 + dp[!first][nxt_eid]);
  }
}

void solve_up(bool first, int node, int dad) {
  vector<int> pref, suff;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    pref.emplace_back(1 + dp[!first][eid[{node, nxt}]]);
  }

  suff = pref;
  int deg = (int)pref.size();
  for (int i = 1; i < (int)pref.size(); ++i) {
    if (first) {
      pref[i] = min(pref[i - 1], pref[i]);
      suff[deg - i - 1] = min(suff[deg - i - 1], suff[deg - i]);
    } else {
      pref[i] = max(pref[i - 1], pref[i]);
      suff[deg - i - 1] = max(suff[deg - i - 1], suff[deg - i]);
    }
  }

  int i = 0;
  for (int nxt : v[node]) {
    if (nxt == dad) continue;
    int edge_id = eid[{nxt, node}];
    dp[first][edge_id] = 1 + dp[!first][eid[{node, dad}]];
    if (first) {
      if (i > 0) dp[first][edge_id] = min(dp[first][edge_id], pref[i - 1]);
      if (i < deg - 1) dp[first][edge_id] = min(dp[first][edge_id], suff[i + 1]);
    } else {
      if (i > 0) dp[first][edge_id] = max(dp[first][edge_id], pref[i - 1]);
      if (i < deg - 1) dp[first][edge_id] = max(dp[first][edge_id], suff[i + 1]);
    }
    solve_up(!first, nxt, node);
    ++i;
  }
}

int main(void) {
  scanf("%d", &n);
  int e = 0;
  for (int i = 0; i < n - 1; ++i) {
    int a, b;
    scanf("%d%d", &a, &b); --a; --b;
    v[a].push_back(b);
    v[b].push_back(a);
    eid[{a, b}] = e++;
    eid[{b, a}] = e++;
  }
  eid[{-1, 0}] = e++;
  eid[{0, -1}] = e++;

  solve_down(true, 0, -1);
  solve_down(false, 0, -1);

  solve_up(true, 0, -1);
  solve_up(false, 0, -1);

  int sol = 0;
  for (int i = 0; i < n; ++i) {
    int curr = n;
    for (int j : v[i])
      curr = min(curr, 1 + dp[false][eid[{i, j}]]);
    sol = max(sol, curr);
  }

  printf("%d\n", sol);
  return 0;
}
