# 代码地图

> 最后更新：2026-10-27

## 总体结构

```text
browser-css-practice/
├─ index.html           # 语义结构和内联 SVG
├─ styles.css           # 设计令牌、精准调整和响应式规则
├─ script.js            # 移动菜单
├─ test-ui.py           # Playwright 验收
├─ screenshots/         # 桌面截图
├─ docs/                # 项目备忘和代码地图
└─ README.md            # 元素评论记录与运行说明
```

## 逐文件核心内容

### `styles.css`

- 用途：定义整套页面和四个目标元素的局部修改。
- 关键选择器：`.btn-primary`、`.search__input:focus`、`.card:hover`、`.care__item`。
- 数据流：CSS 变量 → 组件样式 → 浏览器计算样式。
- 注意：所有颜色由设计令牌控制，主按钮和护理边框共享珊瑚红。

### `index.html`

- 用途：提供页面语义结构、导航、商品卡片和全部内联 SVG。
- 注意：没有外部字体、图片或 CDN。

### `script.js`

- 用途：切换窄屏导航，并同步 `aria-expanded`。
- 注意：点击导航项后自动收起菜单。

### `test-ui.py`

- 用途：检查四项计算样式、响应式菜单、外部请求和页面异常。
- 输出：全部断言通过时退出码为 0，并更新桌面截图。
