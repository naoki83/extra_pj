# COMPOUND_SYSTEM_ARCHITECTURE

> 自己拘束文書。長期 vision を一度固定し、現在 scope を strict に守るための contract。  
> 戦略を再議論したくなったら、まずここを読み直す。

---

## 0. メタルール

- このドキュメントは **追記**だけ可、削除・重大変更は **30日経過後** にのみ許可
- 30日に1回の review 以外で内容を見直さない
- 「もっと良いアイデア」は思いついたら `IDEAS_PARKING.md` に書き、本書には反映しない
- このルールが破られた瞬間、本プロジェクトは戦略議論プロジェクトに変質する

---

## 1. Project Philosophy

### Why compound model
- 単発収益は build → cashflow → 次の build の **空白期間**で operator が止まる
- compound 構造なら、operator が休んでも既存 asset が稼働し、再着手の心理障壁が下がる
- 個人事業の長期 sustainability は、線形 income より複利 asset の蓄積で決まる

### Why automation-first
- operator は毎日継続が苦手（観測された性格特性）
- 「daily に何かが進んでいる」感覚は engineering で作れる（cron, auto-post, sales notification）
- maintain 期に手が空くことが、build 期 burst 投入の前提条件
- automation は手段、目的は operator の意思決定容量を保護すること

### Why low-touch
- 24/7 SLA を要する事業は1人運用で必ず崩壊する
- customer support が増える事業は、収益が増えるほど自由が減る
- 「収益増 = 自由減」の事業は本プロジェクトの目的に反する

### Why distribution is core
- 商品の質と販売量は線形相関しない
- 同等の商品でも distribution 構造の差で収益は10〜100倍違う
- 1人運用で持続可能な distribution = automation + compound channel
- distribution channel そのものが asset 化する

---

## 2. Long-term Vision (24〜36か月後)

### 目標形：Autonomous Distribution Machine

```
1〜3 core 領域に対して:

  Products (5〜20本) ─┐
                     │
  OSS (1〜3 repo)   ─┼─→ [Auto-distribution Layer] ─→ Channels (X, Substack, GitHub)
                     │           │
  Newsletter        ─┘           ↓
                          AI repost / repackage /
                          translate / cross-post

Operator touch: 週 2〜4h
Revenue floor: 月 ¥300k〜1.5M
Revenue upper realistic: 月 ¥3M〜10M
```

### 達成形の特徴
- 商品 launch は月 1〜2、burst 型
- distribution は完全自動、operator 不在でも動く
- 既存 channel が新商品の販売チャネルとして自動稼働
- AI が draft を書き、operator は edit + ship のみ
- 各 asset の lifetime > 3年

### この vision に含めない（明確な不採用）
- SaaS 型 subscription business
- 24/7 alert / monitoring service
- Discord/Telegram コミュニティ運営
- Daily content publication
- B2B 営業依存事業
- Heavy infra (K8s, multi-region, 等)
- Real-time anything

---

## 3. Phase Architecture

### Phase 0: Foundation ✅ (完了済み)
- llm-observability 87LOC + cron 稼働
- 45+ rows accumulated
- GitHub repo 存在 (private)

### Phase 1: First Product Live (現在, Day 1〜30)
**唯一の目標**: Gumroad に商品1本が live し、第1 sale を取る

- llm-observability を polish して商品化
- GitHub public 化
- Gumroad live
- Substack 第0号
- 1 manual launch X post

### Phase 2: Distribution Layer (Day 31〜60)
- X auto-rotation 実装
- post inventory 30本
- GitHub Sponsors / Polar 設定
- Substack 第1号 monthly digest

### Phase 3: Product Portfolio (Month 3〜6)
- 商品 2〜3本目 launch
- 既存商品の minor update
- audience build 継続

### Phase 4: Audience Asset (Month 6〜12)
- Substack subscriber 200〜500 到達
- 商品 4〜6 本累積
- recurring revenue が visible

### Phase 5: Semi-autonomous Compound (Month 12〜24)
- maintain 期週 2〜4h で年商 ¥3〜10M
- 商品 ship cadence 月1〜2 安定
- 全 channel が自動稼働

**重要**: Phase n+1 への移行条件は **Phase n の完了**であり、時間ではない。Day 31 でも Phase 1 が未完了なら Phase 2 に入らない。

---

## 4. Current Scope (Phase 1, Strict)

### IN SCOPE (今やること)
1. `llm-observability` 商品化のための code polish (cross-provider stub、prompt v1 拡張)
2. GitHub repo public 化、README/LICENSE/SETUP整備
3. Gumroad 商品 page 作成、価格 $40 ($32 early bird)
4. Substack 開設、第0号「what this is」公開
5. 商品 launch 用 manual X post (1〜3本)
6. PRODUCT_V1.md (商品 scope 確定書) を別途 commit

### OUT OF SCOPE (Phase 1 では絶対やらない)
- X auto-rotation 実装 (Phase 2)
- GitHub Sponsors 設定 (Phase 2)
- multi-provider 本格運用 (Phase 2 以降)
- Substack 月次 digest 自動化 (Phase 3)
- 第2商品の構想 (Phase 3)
- anomaly detection (Phase 4 以降)
- dashboard / analytics UI (Phase 5 以降、または永久に作らない)
- AI agent / multi-agent (永久に作らない)
- Discord / Telegram community (永久に作らない)

### Phase 1 完了の操作的定義
全項目 Yes で Phase 2 へ移行可:
- [ ] Gumroad に商品が live (URL がある)
- [ ] GitHub repo が public、README に SETUP 手順記載
- [ ] Substack 第0号が公開済み
- [ ] manual launch X post 配信済み
- [ ] 第1 sale 達成 (sale 数は問わない、1件以上)
- [ ] operator が燃え尽きていない

---

## 5. Anti-patterns (禁止行動)

過去のセッションで観測された pattern。発生した瞬間に self-correct する。

### 戦略系
- **Strategy hopping**: 30日内に方針を再評価する
- **同一質問の貼り直し**: 同じ prompt を ChatGPT/Claude に再送する
- **「もっと良い構造」探索**: shipped product がゼロのうちに新方向を検討する
- **比較表の生成欲**: 既に比較済みの選択肢を再度 table 化する

### 実装系
- **Just one more provider**: Anthropic で十分な段階で OpenAI/Google を本格追加する
- **Pre-mature abstraction**: provider abstraction layer 等を Phase 1 で作る
- **Infra creep**: TimescaleDB / Redis / Queue を Phase 1〜2 で導入する
- **Dashboard addiction**: Grafana / Streamlit / 自前 UI を作る
- **Test framework化**: pytest 構成を磨く時間を本筋より優先する

### 配信系
- **Daily SNS grind**: X に毎日手動投稿する義務感を発生させる
- **Reply farming**: 他人の投稿に追従して engagement を稼ごうとする
- **Hashtag spam**: hashtag 戦略を設計する
- **Generic AI commentary**: "Claude 4.7 すごい" 系の没個性投稿
- **Hype copy**: 「衝撃」「革命的」「絶対知っておくべき」系語彙

### 計画系
- **Endless planning**: 設計文書を週単位で更新する
- **Documentation theater**: README を週次で polish し続ける
- **Roadmap inflation**: Phase 5 までの詳細を Phase 1 で固める
- **Permission-seeking**: ChatGPT/Claude に「これでいいか」を再確認する

---

## 6. Decision Rules

新しい行動を検討する時、以下を順に通す。1つでも No なら採用しない。

### Filter 1: Compound Test
> この行動は、既存 asset の compound 性を高めるか?

- 商品の販売、OSS の visibility、subscriber 増 のどれかを直接強化するなら Yes
- 「将来の何か」のためなら No

### Filter 2: Automation Test
> この行動の output は、一度作れば自動稼働するか?

- 商品、cron、template、reusable code は Yes
- recurring meeting、daily post 義務、24/7 SLA は No

### Filter 3: Touch Test
> この行動の maintain 期 ongoing cost は、週 30分以下か?

- 商品の販売、OSS の release、Substack 月1配信 は Yes
- DM 1:1 対応、daily content、live customer support は No

### Filter 4: Cost Test
> この行動の月間 marginal cost は ¥1,000 以下か?

- subscription 内に収まる、または free tier 利用 は Yes
- 新たな paid SaaS、専用 infra、API 課金増 は No

### Filter 5: Reversibility Test
> この行動は、2週間 paused できるか? (operator 不在で破綻しないか)

- product on Gumroad、OSS on GitHub、scheduled post は Yes
- live alerting、real-time dashboard、active community は No

### Filter 6: Pivot Test
> この行動は、現在の Phase の完了に直接寄与するか?

- Phase 1 なら "shipped" に直結するか
- 次 Phase の準備、新領域探索、過去 review は No (現 Phase 完了後)

### Filter 7: Identity Test
> この行動は、long-term vision の "Autonomous Distribution Machine" の一部か?

- products / OSS / channels / automation のどれかに帰属するなら Yes
- consulting、daily grind、SaaS 化準備 は No

---

## 7. Success Metrics

### Phase 1 metrics (Day 30 評価)
- shipped product count (target: 1)
- GitHub repo: public + README完備 (target: yes)
- Gumroad: live + 1 sale 以上 (target: yes / 1+)
- Substack: 第0号公開 (target: yes)
- maintenance hours (Day 8〜30 average): target ≤ 8h/週
- AI marginal cost: target ≤ ¥1,000/月 (Phase 1 中)
- operator burnout score: target = 0 (continue 可能か yes/no)

### Phase 2+ metrics (Day 31以降に追加)
- auto-distribution uptime (cron 失敗率 < 5%)
- post inventory size
- weekly hands-off hours

### Phase 3+ metrics
- product portfolio size
- recurring revenue floor (¥/月 のうち過去商品由来分)
- audience quality (Substack open rate, X engagement rate)

### 追わない指標 (vanity)
- X follower count
- X impression / like
- Substack click rate
- 累積投稿数

---

## 8. 30-day Hard Rules (Day 1〜30)

### 絶対やらないこと
- 戦略再検討。本書の見直しを含む
- ChatGPT/Claude に「もっと良い方向はないか」を聞く
- 商品を別案 (TOP5の2〜5) に変更する
- Phase 2〜5 の詳細設計
- multi-provider observation の本格運用
- dashboard / analytics UI の構築
- daily X 投稿スケジュール作成
- Substack の paid tier 設計
- 新領域の調査 (例: Chrome extension、YouTube、podcast)
- AI agent / multi-agent / mood engine の議論
- 「あと少しで完璧になる」感覚での ship 延期

### 絶対やること
- Day 7 までに GitHub public、PRODUCT_V1.md commit
- Day 14 までに Gumroad LP draft + Substack 第0号
- Day 21 までに 商品 final QA、価格確定
- Day 28 までに 商品 launch
- Day 30 に Phase 1 metrics review

### Phase 1 失敗時の対応
- Day 30 時点で Phase 1 完了基準を満たさない場合:
  - 失敗の原因を1行で書く (`PHASE_1_RETRO.md`)
  - **戦略変更ではなく、scope 縮小**で再 attempt
  - 例: 商品 polish が間に合わない → minimum kit ($25) に縮小して再 ship
  - 戦略を変えるのは Phase 1 を3回連続失敗してから

---

## 9. Self-binding Commitments

operator として以下を書面コミット:

1. 本書を Day 30 まで再編集しない (typo 修正除く)
2. 戦略再議論は Day 30 review 以降のみ許可
3. Day 7、14、21、28 の milestone を git commit で記録する
4. Phase 1 完了前に Phase 2 の作業を開始しない
5. 「ピボットしたい衝動」が来たら、`IDEAS_PARKING.md` に書いて即座に閉じる

---

## 10. Reference

### 関連ファイル
- `PRODUCT_V1.md` - Phase 1 商品 scope (別 commit)
- `IDEAS_PARKING.md` - 衝動的アイデア置き場 (Phase 1 中は読まない)
- `PHASE_1_RETRO.md` - Day 30 review 結果 (Day 30 に作成)
- `llm-observability/` - Phase 1 商品の core asset

### 改訂履歴
- v1.0 (Day 0): 初版固定
