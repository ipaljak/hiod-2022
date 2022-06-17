#include <cstdio>
#include <vector>
#include <algorithm>

#define X first
#define Y second
#define PB push_back

using namespace std;

typedef long long ll;
typedef pair < int, int > pii;
typedef vector < int > vi;

const int MOD1 = 1e9 + 7;
const int MOD2 = 998244353;
const int BS1 = 1000003;
const int BS2 = 1000303;

inline int add(int A, int B, int mod){
	if(A + B >= mod)
		return A + B - mod;
	return A + B;
}

inline int mul(int A, int B, int mod){
	return (ll)A * B % mod;
}

int n, k;

vi komp(vi A, vi B){
	vi C; C.resize(k);
	for(int i = 0;i < k;i++)
		C[i] = B[A[i]];
	return C;
}

int hsh(vi &v, int bs, int mod){
	int ret = 0;
	for(int &x : v)
		ret = add(mul(ret, bs, mod), x, mod);
	return ret;
}

vector < pii > v;

int main(){
	scanf("%d%d", &n, &k);
	vi cur;
	for(int j = 0;j < k;j++) cur.PB(j);
	v.PB({hsh(cur, BS1, MOD1), hsh(cur, BS2, MOD2)});
	for(int i = 0;i < n;i++){
		vi sad;
		for(int j = 0;j < k;j++){
			int x; scanf("%d", &x); x--;
			sad.PB(x);
		}
		cur = komp(cur, sad);
		v.PB({hsh(cur, BS1, MOD1), hsh(cur, BS2, MOD2)});
	}	
	sort(v.begin(), v.end());
	ll sol = 0;
	for(int i = 0;i < (int)v.size();){
		int j = i;
		while(j < (int)v.size() && v[i] == v[j])
			j++;
		sol += (ll)(j - i) * (j - i - 1) / 2LL;
		i = j;
	}
	printf("%lld\n", sol);
	return 0;
}
