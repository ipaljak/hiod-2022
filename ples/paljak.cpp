#include <bits/stdc++.h>

typedef long long llint;

using namespace std;


int n, k;

vector<int> M, A;
map<pair<int, int>, int> cnt;

inline void init() {
  srand(time(NULL)); // za koga je, dobro je
  M = { 1000000007, 1018199999 };
  A = { k + 1 + (rand() % (M[0] - k)),  k + 1 + (rand() % (M[1] - k)) };
}

inline int add(int a, int b, int m) {
  if (a + b < 0) return a + b + m;
  if (a + b >= m) return a + b - m;
  return a + b;
}

inline int mul(int a, int b, int m) {
  return (llint) a * b % m;
}

inline vector<int> compose(const vector<int> &a, const vector<int> &b) {
  vector<int> ret(k);
  for (int i = 0; i < k; ++i)
    ret[b[i]] = a[i];
  return ret;
}

pair<int, int> hsh(const vector<int> &v) {

  int h[2];
  for (int i = 0; i < 2; ++i) {
    int a = A[i], m = M[i];
    h[i] = 0;
    for (int x : v) {
      h[i] = add(h[i], mul(x, a, m), m);
      a = mul(a, A[i], m);
    }
  }

  return {h[0], h[1]};
}

int main(void) {
  scanf("%d%d", &n, &k);

  init();

  vector<int> id(k);
  iota(id.begin(), id.end(), 0);

  vector<int> pref = id;
  llint sol = 0;

  cnt[hsh(pref)]++;
  for (int i = 0; i < n; ++i) {
    vector<int> xi(k);
    for (int j = 0; j < k; ++j) {
      scanf("%d", &xi[j]);
      --xi[j];
    }
    pref = compose(pref, xi);
    auto h = hsh(pref);
    sol += (llint) cnt[h];
    cnt[h]++;
  }

  printf("%lld\n", sol);
  return 0;
}
