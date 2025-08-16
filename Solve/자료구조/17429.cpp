#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;
const ull MOD = 1ULL << 32;
const int MAXN = 500000;
const int SEGN = 3000000;

struct SegmentTree {
    ull tree[SEGN];
    ull lazy_mult[SEGN];
    ull lazy_add[SEGN];

    SegmentTree() {
        memset(tree, 0, sizeof(tree));
        fill(lazy_mult, lazy_mult + SEGN, 1ULL);
        fill(lazy_add, lazy_add + SEGN, 0ULL);
    }

    void push_down(int node, int start, int end) {
        if (lazy_mult[node] == 1 && lazy_add[node] == 0) return;
        tree[node] = (tree[node] * lazy_mult[node] + (ull)(end - start + 1) * lazy_add[node]) % MOD;
        if (start != end) {
            lazy_mult[node * 2] = (lazy_mult[node * 2] * lazy_mult[node]) % MOD;
            lazy_add[node * 2] = (lazy_add[node * 2] * lazy_mult[node] + lazy_add[node]) % MOD;
            lazy_mult[node * 2 + 1] = (lazy_mult[node * 2 + 1] * lazy_mult[node]) % MOD;
            lazy_add[node * 2 + 1] = (lazy_add[node * 2 + 1] * lazy_mult[node] + lazy_add[node]) % MOD;
        }
        lazy_mult[node] = 1;
        lazy_add[node] = 0;
    }

    void range_update(int node, int start, int end, int left, int right, ull mult, ull add_val) {
        push_down(node, start, end);
        if (right < start || end < left) return;
        if (left <= start && end <= right) {
            tree[node] = (tree[node] * mult + (ull)(end - start + 1) * add_val) % MOD;
            if (start != end) {
                lazy_mult[node * 2] = (lazy_mult[node * 2] * mult) % MOD;
                lazy_add[node * 2] = (lazy_add[node * 2] * mult + add_val) % MOD;
                lazy_mult[node * 2 + 1] = (lazy_mult[node * 2 + 1] * mult) % MOD;
                lazy_add[node * 2 + 1] = (lazy_add[node * 2 + 1] * mult + add_val) % MOD;
            }
            return;
        }
        int mid = (start + end) >> 1;
        range_update(node * 2, start, mid, left, right, mult, add_val);
        range_update(node * 2 + 1, mid + 1, end, left, right, mult, add_val);
        tree[node] = (tree[node * 2] + tree[node * 2 + 1]) % MOD;
    }

    ull range_query(int node, int start, int end, int left, int right) {
        push_down(node, start, end);
        if (right < start || end < left) return 0;
        if (left <= start && end <= right) return tree[node];
        int mid = (start + end) >> 1;
        ull t1 = range_query(node * 2, start, mid, left, right);
        ull t2 = range_query(node * 2 + 1, mid + 1, end, left, right);
        return (t1 + t2) % MOD;
    }
};

vector<int> raw_adj[MAXN + 1];
vector<int> adj_list[MAXN + 1];
bool visited[MAXN + 1];
int subtree_size[MAXN + 1];
int node_depth[MAXN + 1];
int parent[MAXN + 1];
int enter_time[MAXN + 1];
int exit_time[MAXN + 1];
int chain_head[MAXN + 1];
int timer_val;

void dfs_build_adj(int v) {
    visited[v] = true;
    for (int neighbor : raw_adj[v]) {
        if (visited[neighbor]) continue;
        adj_list[v].push_back(neighbor);
        dfs_build_adj(neighbor);
    }
}

void dfs_size_depth(int v) {
    subtree_size[v] = 1;
    for (size_t i = 0; i < adj_list[v].size(); ++i) {
        int child = adj_list[v][i];
        node_depth[child] = node_depth[v] + 1;
        parent[child] = v;
        dfs_size_depth(child);
        subtree_size[v] += subtree_size[child];
        if (i > 0 && subtree_size[child] > subtree_size[adj_list[v][0]]) {
            swap(adj_list[v][i], adj_list[v][0]);
        }
    }
}

void dfs_hld(int v) {
    ++timer_val;
    enter_time[v] = timer_val;
    for (int child : adj_list[v]) {
        if (child == adj_list[v][0]) {
            chain_head[child] = chain_head[v];
        } else {
            chain_head[child] = child;
        }
        dfs_hld(child);
    }
    exit_time[v] = timer_val;
}

void subtree_update(int x, ull mult, ull add_val, SegmentTree& seg_tree, int tree_size) {
    seg_tree.range_update(1, 1, tree_size, enter_time[x], exit_time[x], mult, add_val);
}

void path_update(int a, int b, ull mult, ull add_val, SegmentTree& seg_tree, int tree_size) {
    while (chain_head[a] != chain_head[b]) {
        if (node_depth[chain_head[a]] < node_depth[chain_head[b]]) swap(a, b);
        int st = chain_head[a];
        seg_tree.range_update(1, 1, tree_size, enter_time[st], enter_time[a], mult, add_val);
        a = parent[st];
    }
    if (node_depth[a] > node_depth[b]) swap(a, b);
    seg_tree.range_update(1, 1, tree_size, enter_time[a], enter_time[b], mult, add_val);
}

ull subtree_query(int x, SegmentTree& seg_tree, int tree_size) {
    return seg_tree.range_query(1, 1, tree_size, enter_time[x], exit_time[x]);
}

ull path_query(int a, int b, SegmentTree& seg_tree, int tree_size) {
    ull ret = 0;
    while (chain_head[a] != chain_head[b]) {
        if (node_depth[chain_head[a]] < node_depth[chain_head[b]]) swap(a, b);
        int st = chain_head[a];
        ret = (ret + seg_tree.range_query(1, 1, tree_size, enter_time[st], enter_time[a])) % MOD;
        a = parent[st];
    }
    if (node_depth[a] > node_depth[b]) swap(a, b);
    ret = (ret + seg_tree.range_query(1, 1, tree_size, enter_time[a], enter_time[b])) % MOD;
    return ret;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, Q;
    cin >> N >> Q;

    for (int i = 0; i < N - 1; ++i) {
        int s, e;
        cin >> s >> e;
        raw_adj[s].push_back(e);
        raw_adj[e].push_back(s);
    }

    dfs_build_adj(1);

    dfs_size_depth(1);

    chain_head[1] = 1;
    timer_val = 0;
    dfs_hld(1);

    SegmentTree seg_tree;

    vector<ull> answers;
    for (int qi = 0; qi < Q; ++qi) {
        int k;
        cin >> k;
        if (k == 1) {
            int X;
            ull V;
            cin >> X >> V;
            subtree_update(X, 1, V, seg_tree, N);
        } else if (k == 2) {
            int X, Y;
            ull V;
            cin >> X >> Y >> V;
            path_update(X, Y, 1, V, seg_tree, N);
        } else if (k == 3) {
            int X;
            ull V;
            cin >> X >> V;
            subtree_update(X, V, 0, seg_tree, N);
        } else if (k == 4) {
            int X, Y;
            ull V;
            cin >> X >> Y >> V;
            path_update(X, Y, V, 0, seg_tree, N);
        } else if (k == 5) {
            int X;
            cin >> X;
            answers.push_back(subtree_query(X, seg_tree, N));
        } else if (k == 6) {
            int X, Y;
            cin >> X >> Y;
            answers.push_back(path_query(X, Y, seg_tree, N));
        }
    }

    for (auto ans : answers) {
        cout << ans << '\n';
    }
    return 0;
}