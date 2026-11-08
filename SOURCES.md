# 图片来源

本库只登记**链接和标注**，不搬图。图都是别人做的，我只是编目。

## 目前在用的

| 来源 | 地址 | 说明 |
| --- | --- | --- |
| 斗图啦 | https://www.doutula.com | 站内搜「傲娇」抓的，#03~#09 出自这里。图是网友上传的，来源杂，别商用。 |
| ChineseBQB | https://github.com/zhaoolee/ChineseBQB | **真正开源的那个**：115 个分类、5887 张表情，图片和标注都开放，作者明确说可以用作数据源。 |

## ChineseBQB 怎么用（省得下次再翻一遍）

它自带两个机器可读的索引，比爬页面靠谱：

- 分类目录：https://zhaoolee.com/ChineseBQB/catalog/index.json
- 完整图片索引：https://zhaoolee.com/ChineseBQB/catalog/search.json

索引里的 `src` / `thumb` 是相对路径，前面拼 `https://zhaoolee.com/ChineseBQB/` 就成直链。
每条还带 `categoryTitle`、宽高、是否动图、字节数，筛「动图 + 小于 500KB」特别方便。

离线也行：每个分类都有一个 zip 直链，比如 `辉夜大小姐` 那个是
https://github.com/zhaoolee/ChineseBQB/releases/download/bqb-downloads/bqb-071-6b7c75c25ebe81eb.zip

### 里面跟本库对得上的分类

- `071 辉夜大小姐` —— 傲娇教科书，有「傲娇生气」「暴怒」「诶」这种现成情绪标签
- `022 苏大强` —— 摆烂 / 无语 / 作妖
- `110 人工智能` —— 拿来吐槽 AI 正合适
- `023 表情符号`、`001 滑稽大佬` —— 通用接梗

## 挑图的原则

1. 优先用 ChineseBQB 这种作者明确说开放的，出问题时底气足；
2. 网图站的图只登记链接，不当成自己的东西；
3. 表情包里的人物形象该是谁的就是谁的，注明出处，别装原创；
4. 有人问我图哪来的，答得出来。

## 待办

- [ ] 从 ChineseBQB 挑一批补进主索引（委屈/无语/摆烂/告别 优先）
- [ ] 给每个条目都补上 `license` 字段，写清楚是「开源仓库」还是「网图」
