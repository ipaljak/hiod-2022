#include <bits/stdc++.h>

using namespace std;

const int MAXN = 1e6 + 10;

int n;
char s[MAXN], t[MAXN];

int main(void) {
  scanf("%s", s);

  n = strlen(s);
  vector<char> v[2];

  for (int i = 0; i < n; ++i)
    v[i % 2].push_back(s[i]);

  for (int i = 0; i < 2; ++i) {
    sort(v[i].begin(), v[i].end());
    for (int j = 0; j < (int)v[i].size(); ++j)
      t[2 * j + i] = v[i][j];
  }

  sort(s, s + n);
  if (strcmp(s, t) == 0)
    printf("da\n");
  else
    printf("ne\n");

  return 0;
}
