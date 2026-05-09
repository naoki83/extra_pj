# PRODUCT_V1

> Phase 1 商品 scope の固定書。`COMPOUND_SYSTEM_ARCHITECTURE.md` の Phase 1 を満たすための唯一の商品。
> Day 30 まで scope 変更禁止 (typo 修正除く)。

---

## 1. Product Name

**LLM Observability Minimal Kit**

短縮形: `llm-obs-kit`
バージョン: v0.1.0 (Phase 1 ローンチ版)

---

## 2. Target Customer

### Primary
- **Indie / solo dev** が LLM API (Claude / OpenAI / Google) を本番投入している
- 自分の API 呼び出しを「測りたいが Datadog/Helicone を導入する程ではない」層
- Python が読める / cron が分かる
- 月の API 支払い ¥5,000〜¥50,000 規模

### Secondary
- 小規模チームの LLM tech lead (社内 PoC で provider 比較したい)
- LLM provider 選定中の technical decision maker

### NOT target
- non-technical buyer
- enterprise (SLA / SOC2 等の要件層)
- 「すぐ動くダッシュボード」が欲しい層
- LLM 初学者

---

## 3. Core Promise

> **10分で動く、自分の手元で。30日分のサンプル data 付き。全部再現可能。**

具体的には:
- `git clone` → `pip install` → `python observability.py` で1行が DB に入るまで **10分以内**
- 30日 cross-provider sample data (CSV) が即座に手に入る
- すべての数値は同梱の reproducer script で再現可能
- SaaS 不要、依存サービスなし、自分の VPS / PC で完結

---

## 4. Included Files

```
llm-obs-kit-v0.1.0.zip
├── code/
│   ├── observability.py              # core runner (~250 LOC)
│   ├── config.py
│   ├── schema.sql
│   ├── prompts/
│   │   └── v1.jsonl                  # 5 prompts (summarize, codegen, tool_use, long_ctx, arithmetic)
│   ├── requirements.txt              # httpx, python-dotenv のみ
│   └── .env.example
├── data/
│   ├── sample_30d_anthropic.csv      # 30日蓄積の実データ
│   ├── daily_aggregates.csv          # 日次集計版
│   └── README_data.md                # 列定義
├── docs/
│   ├── SETUP.md                      # 10分セットアップ手順 (Mac/Linux/Windows)
│   ├── INTERPRETATION.md             # 数値の読み方
│   └── EXTENDING.md                  # provider/prompt 追加howto (stub レベルで OpenAI/Google 例を含む)
├── examples/
│   ├── simple_anomaly_check.py       # ~50 LOC, 異常検出例
│   └── cost_estimation.py            # ~50 LOC, cost 計算例
├── LICENSE                            # MIT
└── README.md                          # 5分で全体像
```

**total LOC**: 概算 400〜500行 (data除く)
**zip サイズ**: <2 MB 想定

---

## 5. NOT Included

明示的に含まないものを宣言する。「これは入っていますか?」の問い合わせを構造的に減らすため。

```
✗ Real-time dashboard (UI なし)
✗ Alerting / notification system
✗ SaaS / hosted version
✗ Multi-provider 本格運用 (sample data は Anthropic のみ、OpenAI/Google は code stub のみ)
✗ Web 管理画面
✗ Database migration tool
✗ Authentication / multi-user
✗ Cloud deployment scripts (AWS/GCP/Azure)
✗ Custom integrations
✗ 1:1 support / consulting hours
✗ Cooking SLA / uptime guarantees
✗ Slack / Discord channel access
✗ Video tutorial
✗ Lifetime updates beyond 12 months
```

これらが必要な人は target ではない。

---

## 6. Price

| Tier | 価格 | 条件 |
|---|---|---|
| Early bird | **$32** | 最初の20件、launch から14日以内 |
| Standard | **$40** | 上記終了後 |

- 通貨: USD
- 支払い: Gumroad (Stripe / PayPal 経由)
- 課税: Gumroad VAT/sales tax 自動処理
- 返金: 30日 no-questions (購入後30日以内なら理由不問で全額返金)
- bundle / discount: **Phase 1 では作らない** (Phase 3 で検討)
- 教育/research メール優待: **Phase 1 では作らない**

価格変更ルール:
- Early bird → Standard の自動切替以外、**Day 30 まで価格変更禁止**
- Day 30 review で sales 0 なら価格を疑う前に scope を疑う

---

## 7. Completion Definition

商品が「ship 可能」と判断する3条件 (全 Yes 必須):

1. **`SETUP.md` の手順を Mac / Linux / Windows でクリーン環境から実行し、10分以内に DB へ1行入ることを確認した**
2. **`data/sample_30d_anthropic.csv` が ≥ 700 rows (30日 hourly = 720 rows) 含む**
3. **README の `## reproducing` セクションに記載された command 群が、新規 venv で edit なしで通る**

これら3つを満たせば商品 scope は完成。**「もう少し magnify したら売れる」感覚を排除する**ためのチェックポイント。

---

## 8. 30-day Launch Criteria

`COMPOUND_SYSTEM_ARCHITECTURE.md` の Phase 1 milestone と整合:

| Day | Milestone | Hard or Soft |
|---|---|---|
| Day 7 | GitHub repo public, README live, LICENSE 有, `PRODUCT_V1.md` 引用済 | **Hard** |
| Day 14 | Gumroad LP draft 完成 (画像1枚 + 5 bullet + price) + Substack 第0号公開 | **Hard** |
| Day 21 | 商品 final QA 通過 (Section 7 の 3条件 Yes), 価格確定 | **Hard** |
| Day 26 | Gumroad live (URL 取得), 第1 manual launch X post 配信 | **Hard** |
| Day 30 | 第1 sale 達成 OR `PHASE_1_RETRO.md` 執筆 | **Soft** (sale は確率事象、retro は確実) |

Hard milestone 1つでも未達なら Phase 1 失敗 → scope 縮小して再 attempt。**戦略変更ではない**。

---

## 9. Support Policy

明文化することで、support 工数の青天井化を防ぐ:

```
Email / Gumroad message:
  - best effort response
  - 平均応答 3〜7 日想定
  - SLA なし、平日昼間営業時間なし
  - 月 5h 以内を上限とする (operator self-binding)

Refund:
  - 購入後 30 日以内、理由不問
  - Gumroad の自動 refund flow を使用
  - 拒否しない、議論しない

Updates:
  - 購入後 12ヶ月、minor / patch update を無償提供
  - major version (v1.0.0) は別商品扱い (購入者は割引適用検討)
  - update 通知は Gumroad の "post update" 機能のみ

Custom modifications:
  - 提供しない (Phase 3 まで)
  - 「○○を追加してほしい」は GitHub issue として記録、対応保証なし

1:1 sessions / consulting:
  - 含まれない
  - 別商品も Phase 1 では作らない

Bug reports:
  - GitHub Issues で受付 (商品購入者専用ではない)
  - 重大 bug は patch release で対応
  - SLA なし
```

---

## 10. Anti-scope-creep Rules

商品が「ship したのに膨らむ」現象を防ぐ:

### 機能追加に対するルール
- 「OpenAI / Google を本格 sample data にも入れて」 → **Phase 2 商品 (別商品)** で対応
- 「real-time dashboard 欲しい」 → **永久に作らない**、別人が作るべき
- 「alerting 機能」 → **Phase 4 の別商品候補** (今は議論しない)
- 「Slack 通知」 → 上に同じ
- 「web UI」 → 永久に作らない
- 「Docker 化」 → community が PR を出せば mergeを検討、こちらから作らない
- 「他言語 (TS/Rust) port」 → community 任せ、こちらから作らない

### 価格・販売に対するルール
- bundle 作成 → Phase 3 まで禁止
- subscription 化 → Phase 5 まで議論しない
- enterprise tier → Phase 4 まで議論しない
- 値下げ → 30日 sales 0 でも値下げ禁止 (scope を疑う)
- 値上げ → Phase 2 完了後に検討

### "次の商品" に対するルール
- v0.2.0 / v1.0.0 等の next version 議論は **Day 30 review 以降のみ**
- 第2商品 (例: Cost Reconciliation Kit) の構想は **Phase 3 まで凍結**
- 派生商品 / 教材 / course 化は **Phase 3 まで凍結**

### community / brand に対するルール
- Discord 作らない
- Telegram 作らない
- 公式 Twitter (商品専用) 作らない (既存 X account で告知)
- ロゴ / brand identity 作らない (text logo で十分)
- 専用 domain 取らない (Gumroad URL + GitHub URL で十分)

### 衝動が来た時の処理
- "あれも入れたい" / "もっと polish したい" / "もう一週間あれば..." が来たら:
  1. `IDEAS_PARKING.md` に1行書く
  2. このファイルを再読する
  3. 進行中の Hard milestone に戻る
- 例外なし

---

## Reference

- `COMPOUND_SYSTEM_ARCHITECTURE.md` - 上位思想、本書を拘束する
- `llm-observability/` - 商品の core asset (Phase 0 で作成済)
- `IDEAS_PARKING.md` - scope 外アイデアの置き場
- `PHASE_1_RETRO.md` - Day 30 review (Day 30 に作成)

---

## 改訂履歴
- v1.0 (Day 0): 初版固定
