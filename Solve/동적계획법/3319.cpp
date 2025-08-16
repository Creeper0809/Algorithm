#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const int MAXN = 100010;

struct Line {
    ll m, b;
    Line() : m(0), b(0) {}
    Line(ll m_, ll b_) : m(m_), b(b_) {}
};

vector<Line> lines(MAXN);

int ptr = 1;

ll eval(const Line& l, ll x) {
    return (ll)((__int128)l.m * x + l.b);
}

bool q_check(const Line& A, const Line& B, ll x) {
    __int128 left = (__int128)(B.b - A.b);
    __int128 right = (__int128)x * (A.m - B.m);
    return left < right;
}

ll query(ll x) {
    int lo = 0, hi = ptr - 1;
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2;
        Line A = lines[mid - 1];
        Line B = lines[mid];
        if (q_check(A, B, x)) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    return eval(lines[lo], x);
}

bool add_check(const Line& A, const Line& B, const Line& C) {
    __int128 p = (__int128)(A.b - C.b);
    __int128 q = (__int128)(B.m - A.m);
    __int128 r = (__int128)(A.b - B.b);
    __int128 s = (__int128)(C.m - A.m);
    return p * q < r * s;
}

int add_line(Line new_l) {
    int lo = 1, hi = ptr;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        Line A = lines[mid - 1];
        Line B = lines[mid];
        if (add_check(A, B, new_l)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

vector<pair<int, ll>> adj[MAXN];
ll S[MAXN], V[MAXN], f[MAXN], dist[MAXN];

struct RollbackInfo {
    int rb_idx;
    Line rb_line;
    int old_ptr;
};

RollbackInfo add_line_rb(ll new_m, ll new_b) {
    Line cur_line(new_m, new_b);
    int old_ptr = ptr;
    int rb_idx = add_line(cur_line);
    Line rb_line = lines[rb_idx];
    lines[rb_idx] = cur_line;
    ptr = rb_idx + 1;
    return {rb_idx, rb_line, old_ptr};
}

void undo_add(const RollbackInfo& info) {
    lines[info.rb_idx] = info.rb_line;
    ptr = info.old_ptr;
}

void dfs(int u, int par, ll cur_dist) {
    dist[u] = cur_dist;
    RollbackInfo info = {0, Line(), 0};
    if (u != 1) {
        ll min_val = query(V[u]);
        f[u] = S[u] + dist[u] * V[u] + min_val;
        info = add_line_rb(-dist[u], f[u]);
    }
    for (auto& p : adj[u]) {
        int v = p.first;
        ll d = p.second;
        if (v != par) {
            dfs(v, u, cur_dist + d);
        }
    }
    if (u != 1) {
        undo_add(info);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int N;
    cin >> N;
    for (int i = 0; i < N - 1; i++) {
        int u, v, d;
        cin >> u >> v >> d;
        adj[u].emplace_back(v, d);
        adj[v].emplace_back(u, d);
    }
    for (int i = 2; i <= N; i++) {
        cin >> S[i] >> V[i];
    }
    lines[0] = Line(0, 0);
    dfs(1, -1, 0);
    for (int i = 2; i <= N; i++) {
        if (i > 2) cout << " ";
        cout << f[i];
    }
    cout << "\n";
    return 0;
}