# tsundere-stickers

**本鱼的表情包索引 · 按情绪查图，一条命令取下来**

> 一句话：不是替你收藏图，是给「这张图什么时候该发」建个索引 —— 图留在原站，这里只存链接、情绪和用法。

| | |
| --- | --- |
| 版本 | `0.3.0` |
| 收录 | 14 张，6 种情绪，3 类授权 |
| 依赖 | Python 3.8+，**零第三方库**（只用标准库） |
| 许可 | 代码 MIT；图版权归原作者，见 [版权](#版权这回事) |

> 🔒 **仓库里不存图**。存的是链接 + 标注，等于一本藏书目录，不是藏书本身。

---

## 三十秒上手

不想读文档就这三条：

```bash
git clone https://github.com/NotFatJustRound/tsundere-stickers.git
cd tsundere-stickers
python tools/sticker.py list -e 傲娇
```

看到想要的，取下来：

```bash
python tools/sticker.py get "#10"
# -> 10.png
```

想一次全拿走（只拿作者明确开放的）：

```bash
python tools/sticker.py fetch-all --license open -o images
```

想用眼睛挑，浏览器打开 `docs/gallery.html`（需要起个静态服务，直接双击本地文件读不到 json）：

```bash
python -m http.server 8000
# 然后开 http://localhost:8000/docs/gallery.html
```

---

## 全部命令

| 命令 | 干什么 |
| --- | --- |
| `list` | 列出全部，可按情绪/授权过滤 |
| `search <词>` | 在画面描述、用法、关键词里搜 |
| `get <编号>` | 下载单张，存成 `10.png` 这种 |
| `fetch-all` | 批量下载到 `images/` |
| `check` | 逐个 HEAD 验链接还活着没 |

常用的几个参数：`-e 傲娇`（情绪）、`--license open`（只取开源授权）、`-o 目录`（存哪）、`-v`（搜索时带用法）。

```bash
$ python tools/sticker.py list -e 傲娇
#03  傲娇  [net ] 大字「傲娇!」的二次元角色图，脸绷着但明显心虚
#04  傲娇  [net ] 「一脸傲娇」的人物特写，下巴微抬，眼神往别处飘
...
$ python tools/sticker.py search 赌气 -v
#10  傲娇  [open] 辉夜大小姐「反正会长也不会给我过生日的吧」，低头赌气脸
     用法：期待落空又要面子的时候用，是很标准的傲娇句型。
```

---

## 文件

| 文件 | 干什么的 |
| --- | --- |
| `stickers.json` | 主索引，机器可读，一条一个表情 |
| `categories.md` | 情绪分类和常见场景的对照表（人看的） |
| `SOURCES.md` | 图源、索引地址、直链怎么拼 |
| `tools/sticker.py` | 取图脚本（标准库，不用 pip） |
| `docs/gallery.html` | 网页版图鉴，按情绪/授权/关键词筛 |
| `docs/sync-images.md` | 想开 Actions 自动同步就看这个 |

---

## 字段说明

| 字段 | 说明 |
| --- | --- |
| `no` | 编号，`#01` 这种，发的时候直接报这个 |
| `emotion` | 情绪分类，只从 `emotionList` 里挑，别自己造词 |
| `content` | 一句话说清图里是什么（画面 + 人物 + 动作） |
| `keywords` | 触发词，最多 8 个 |
| `usage` | 什么场合用最自然，顺手写个反面例子 |
| `source` / `page` | 来源站 + 回得去的页面 |
| `url` | 图源直链（只登记不搬图） |
| `license` | `open` 作者明确开放 / `net` 网上公开 / `own` 自带 |

---

## 几条自己的规矩

- 收藏别贪多。三分钟热度偷一堆，最后全是没标注的废图。
- 普通闲聊 3~5 轮一张就够，热闹时密一点，但别刷屏。
- 严肃话题、正式场合、别人情绪低落想认真说话的时候，不塞表情。
- 别老用同一张。连着出现两次就已经很像复读机了。
- 表情不能代替回话 —— 单独一张图挂在那儿，很像敷衍。

---

## 版权这回事

图不是我的原创，也不会拿去商用。这里只存**链接和标注**，真要挪作他用，先确认原站的说法。

| license | 大概什么情况 | 能不能搬 |
| --- | --- | --- |
| `open` | 作者明确说可以拿来用（如 ChineseBQB） | 可以，标注来源 |
| `net` | 网上公开流传、来源不明（如斗图啦） | 只留链接，不打包进仓库 |
| `own` | 我自己有的 | 随便 |

`fetch-all --license open` 就是按这个分界来的：默认不把 `net` 的图复制进仓库。

---

## 更新记录

- `0.1.0` 建库，先把自带的两张塞进来。
- `0.2.0` 从斗图啦补了 #03~#09，加了 `url` / `page` 字段。
- `0.3.0` 接 ChineseBQB 补 #10~#14（傲娇/无语/害羞/惊讶/摆烂），
  加 `tools/sticker.py`、`docs/gallery.html`、`SOURCES.md`；索引里加 `license` 分类。
