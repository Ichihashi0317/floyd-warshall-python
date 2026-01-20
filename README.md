# FloydWarshall (Python)

All-pairs shortest paths (Floyd–Warshall) with an optional incremental relaxation API, designed for competitive programming.

競プロ用途のワーシャル・フロイド実装です。
`add_edge()` で辺を設定した後、`solve()` で全点対最短距離を計算します。
`solve()` 後に辺の追加を行う場合、必要に応じて `solve()` より軽い計算量で距離行列を更新できます。

## 特徴

頂点数を `n` とする

- 全点対最短距離 (APSP)
- 重み付き有向グラフ
- 負辺に対応
- 負閉路検出
- 辺の追加に伴う距離行列の更新を `O(n^2)` で実行可能

### 注意点

- 本実装は緩和（距離を短縮するような辺追加 / 重み減少）のみを反映します。重み増加や辺削除はサポートしません。

## メソッド / プロパティ

### 距離行列の整合 / 非整合状態の定義

- 整合: 現在のグラフに対する全点対最短距離が内部の距離行列に反映されている状態
- 非整合: 辺追加後で、距離行列の再計算が必要な状態

### メソッド / プロパティ 一覧

| メソッド / プロパティ | 機能 | 計算量 | 使用条件 | 状態変化 |
| - | - | - | - | - |
| `__init__(...)` | 初期化 | `O(n^2)` | - | 距離行列を**整合化** |
| `add_edge(...,`<br>`update_dists=False)` | 辺の追加 | `O(1)` | - | 距離行列を**非整合化** |
| `add_edge(...,`<br>`update_dists=True)` | 辺の追加<br>距離行列更新 | `O(n^2)` | 距離行列が**整合** | (距離行列は**整合**維持) |
| `solve()` | 距離行列更新<br>距離行列取得 | `O(n^3)` | - | 距離行列を**整合化** |
| `has_negative_cycle()` | 負閉路検出 | `O(n)` | 距離行列が**整合** | - |
| `dist` | 距離行列取得<br>(プロパティ) | `O(1)` | 距離行列が**整合** | - |

- 空間計算量: `O(n^2)`（距離行列）
- `dist` の参照、および `add_edge(..., update_dists=True)` / `has_negative_cycle()` の呼び出しは、内部の距離行列が整合している状態（`solve()` 後、または辺が存在しない初期状態）でのみ可能です。`add_edge(..., update_dists=False)` により緩和された後は距離行列の整合性が崩れるため、次に `solve()` を呼ぶまでこれらの操作はできません。

## 使い方

### 基本（`add_edge()` → `solve()`）

```python
fw = FloydWarshall(n, inf=10**18)
fw.add_edge(0, 1, 5)  # add an edge 0 -> 1 with weight 5
fw.add_edge(1, 2, -2)  # add an edge 1 -> 2 with weight -2

dist = fw.solve()
print(dist[0][2])  # shortest distance 0 -> 2
```

- `inf` のデフォルト値は `float("inf")` であり、未指定でも問題ありません。有限値を指定する場合は、最大の最短距離より十分大きい値を指定してください。
- `solve()` は、距離行列の更新が不要な場合（整合している場合）は処理をスキップします。

### `solve()` 後の辺追加と距離更新

一度 `solve()` されている、あるいは辺が存在しない初期状態（距離行列が整合している状態）であれば、辺の追加に対して `O(n^2)` で距離行列を更新できます。
緩和が起きない場合（最短距離が短くならない場合）は処理をスキップします。

```python
fw = FloydWarshall(n, inf=10**18)
# ... add edges ...
fw.solve()

# Add a shorter edge and update all-pairs distances
fw.add_edge(u, v, w, update_dists=True)
print(fw.dist[u][v])  # shortest distance u -> v
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

## 動作環境

### 利用者、開発者

- 標準ライブラリのみ
- 動作確認: Python 3.13.5
- 想定: Python 3.10+（型注釈の仕様上）

### 開発者

- pytest

## 検証

- 主機能の検証

  - 検証方法: AtCoder ABC375F
  - 問題: <https://atcoder.jp/contests/abc375/tasks/abc375_f>
  - 解説: <https://atcoder.jp/contests/abc375/editorial/11134>
  - 提出コード: [example.py](example/example.py)

- 他機能の検証（例外条件、負閉路検出）

  - 検証方法: pytest
  - 検証コード: [test_floyd_warshall.py](test/test_floyd_warshall.py)

## ライセンス

CC0-1.0
