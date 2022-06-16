#include <bits/stdc++.h>

using namespace std;

typedef long long llint;

const int MAXN = 1e5 + 10;
const int MAXK = 110;

vector<int> endpoints;
vector<pair<int, int>> v[MAXN];

int n, m, k;
int q[MAXK];

vector<llint> dijkstra(int s) {
  priority_queue<pair<llint, int>, vector<pair<llint, int>>,
                 greater<pair<llint, int>>> pq;
  vector<llint> dist(n, -1LL), bst(n, 1e18);
  pq.push({0LL, s});

  while (!pq.empty()) {
    while (!pq.empty() && dist[pq.top().second] != -1) pq.pop();
    if (pq.empty()) break;
    llint curr_d = pq.top().first;
    int node = pq.top().second;
    dist[node] = curr_d;
    pq.pop();
    for (auto &p : v[node]) {
      llint nxt_d = (llint) p.second;
      int nxt = p.first;
      if (dist[nxt] != -1 || bst[nxt] < curr_d + nxt_d) continue;
      bst[nxt] = curr_d + nxt_d;
      pq.push({curr_d + nxt_d, nxt});
    }
  }

  return dist;
}

int main(void) {
  scanf("%d%d%d", &n, &m, &k);
  for (int i = 0; i < m; ++i) {
    int a, b, d, x;
    scanf("%d%d%d%d", &a, &b, &d, &x); --a; --b;
    v[a].emplace_back(b, d);
    v[b].emplace_back(a, d);
    if (x == 1) {
      endpoints.push_back(a);
      endpoints.push_back(b);
    }
  }

  auto ds = dijkstra(0);
  for (int i = 0; i < k; ++i) {
    scanf("%d", &q[i]); --q[i];
    auto dt = dijkstra(q[i]);
    bool ok = true;
    for (int mid : endpoints)
      ok &= ds[mid] + dt[mid] == ds[q[i]];
    printf("%d\n", ok);
  }

  return 0;
}
