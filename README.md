# FloydWarshall (Python)

All-pairs shortest paths (Floyd–Warshall) with an optional incremental relaxation API, designed for competitive programming.

競プロ用途の Floyd–Warshall 実装です。
`add_edge()` で辺を設定した後、`solve()` で全点対最短距離を計算します。
`solve()` 後に辺の追加を行う場合、必要に応じて `solve()` より軽い計算量で距離行列を更新できます。

## 特徴

- 全点対最短距離 (APSP)
- 重み付き有向グラフ
- 負辺に対応
- `has_negative_cycle()` で負閉路検出
- `add_edge(..., update_dists=True)` による距離行列の更新

## 注意点

- 本実装は緩和（距離を短縮するような辺追加 / 重み減少）のみを反映します。重み増加や辺削除はサポートしません。
- `dist` の参照、および `add_edge(..., update_dists=True)` / `has_negative_cycle()` の呼び出しは、距離行列が有効な状態（`solve()` 後、または辺が存在しない初期状態）でのみ可能です。
  `add_edge(..., update_dists=False)` を呼んだ後は距離行列が有効な状態でないため、再び `solve()` を呼ぶまでこれらの操作はできません。

## 計算量

ここで `n` は頂点数（引数 `num_v`）です。

- Memory: `O(n^2)`（距離行列）
- `solve()`: `O(n^3)` time
- `add_edge(..., update_dists=True)`: `O(n^2)` time
- `add_edge(..., update_dists=False)`: `O(1)` time

## 使い方

### 基本（辺追加 → solve）

```python
fw = FloydWarshall(n, inf=10**18)
fw.add_edge(0, 1, 5)
fw.add_edge(1, 2, -2)

dist = fw.solve()
print(dist[0][2])  # shortest distance 0 -> 2
```

infのデフォルト値は`float("inf")`であり、未指定でも問題ありません。
有限値を指定する場合は、最大の最短距離より十分大きい値を指定してください。

### solve 後の辺追加と距離更新

一度 `solve()` していれば、辺の追加に対して `O(n^2)` で距離行列を更新できます。
ただし、緩和が起きない場合（最短距離が短くならない場合）は処理をスキップします。

```python
fw = FloydWarshall(n, inf=10**18)
# ... add edges ...
fw.solve()

# Add a shorter edge and update all-pairs distances
fw.add_edge(u, v, w, update_dists=True)
```

### 負閉路の検出

```python
fw = FloydWarshall(3, inf=10**18)
fw.add_edge(0, 1, 1)
fw.add_edge(1, 2, 1)
fw.add_edge(2, 0, -3)  # forms a negative cycle

fw.solve()
if fw.has_negative_cycle():
    print("negative cycle detected")
else:
    print(fw.dist[0][2])
```

`has_negative_cycle()` が True の場合、最短距離は一般に定義できません。
その場合 `dist` を最短距離として解釈しないでください。

## 検証

AtCoder のテストケースで検証しました。

- <https://atcoder.jp/contests/abc375/tasks/abc375_f>
- <https://atcoder.jp/contests/abc375/editorial/11134>

## ライセンス

TBD（後で決定）
