/* ============================================================
   APEC 2026 动态追踪看板 - 前端交互
   ============================================================ */

(function () {
  'use strict';

  const DATA_URL = 'data/articles.json';
  let allArticles = [];
  let activeFilters = {
    categories: new Set(['数据跨境', 'AI治理', '互联互通', '地缘政治', '2026中国年', '其他APEC动态']),
    sourceTypes: new Set(['官方公报', '权威媒体']),
    timeRange: '7',
    search: '',
  };

  // ---- 初始化 ----
  async function init() {
    try {
      const resp = await fetch(DATA_URL);
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      const data = await resp.json();
      allArticles = data.articles || [];
      document.getElementById('updateTime').textContent =
        '最后更新：' + (data.last_updated || '未知');
    } catch (e) {
      console.error('加载数据失败:', e);
      allArticles = [];
      document.getElementById('updateTime').textContent = '数据加载失败，请稍后刷新';
    }
    bindFilters();
    render();
  }

  // ---- 绑定筛选器事件 ----
  function bindFilters() {
    // 议题分类
    document.querySelectorAll('[data-filter="category"]').forEach(cb => {
      cb.addEventListener('change', () => {
        updateCategoryFilter();
        render();
      });
    });

    // 来源类型
    document.querySelectorAll('[data-filter="sourceType"]').forEach(cb => {
      cb.addEventListener('change', () => {
        updateSourceTypeFilter();
        render();
      });
    });

    // 时间范围
    document.getElementById('timeFilter').addEventListener('change', function () {
      activeFilters.timeRange = this.value;
      render();
    });

    // 搜索框
    document.getElementById('searchBox').addEventListener('input', function () {
      activeFilters.search = this.value.trim().toLowerCase();
      render();
    });

    // 重置
    document.getElementById('resetFilters').addEventListener('click', () => {
      document.querySelectorAll('[data-filter="category"]').forEach(cb => { cb.checked = true; });
      document.querySelectorAll('[data-filter="sourceType"]').forEach(cb => { cb.checked = true; });
      document.getElementById('timeFilter').value = '7';
      document.getElementById('searchBox').value = '';
      activeFilters.categories = new Set(['数据跨境', 'AI治理', '互联互通', '地缘政治', '2026中国年', '其他APEC动态']);
      activeFilters.sourceTypes = new Set(['官方公报', '权威媒体']);
      activeFilters.timeRange = '7';
      activeFilters.search = '';
      render();
    });
  }

  function updateCategoryFilter() {
    activeFilters.categories = new Set();
    document.querySelectorAll('[data-filter="category"]:checked').forEach(cb => {
      activeFilters.categories.add(cb.value);
    });
  }

  function updateSourceTypeFilter() {
    activeFilters.sourceTypes = new Set();
    document.querySelectorAll('[data-filter="sourceType"]:checked').forEach(cb => {
      activeFilters.sourceTypes.add(cb.value);
    });
  }

  // ---- 过滤逻辑 ----
  function getFilteredArticles() {
    if (!allArticles.length) return [];

    const now = new Date();
    let filtered = allArticles;

    // 时间范围过滤
    if (activeFilters.timeRange !== 'all') {
      const days = parseInt(activeFilters.timeRange, 10);
      const cutoff = new Date(now);
      cutoff.setDate(cutoff.getDate() - days);
      const cutoffStr = cutoff.toISOString().slice(0, 10);
      filtered = filtered.filter(a => a.date >= cutoffStr);
    }

    // 议题分类过滤
    filtered = filtered.filter(a => {
      const cats = a.categories || ['其他APEC动态'];
      return cats.some(c => activeFilters.categories.has(c));
    });

    // 来源类型过滤
    filtered = filtered.filter(a => activeFilters.sourceTypes.has(a.source_type || '权威媒体'));

    // 搜索过滤
    if (activeFilters.search) {
      const s = activeFilters.search;
      filtered = filtered.filter(a =>
        (a.title || '').toLowerCase().includes(s) ||
        (a.source || '').toLowerCase().includes(s) ||
        (a.summary || '').toLowerCase().includes(s)
      );
    }

    return filtered;
  }

  // ---- 渲染 ----
  function render() {
    const content = document.getElementById('content');
    const filtered = getFilteredArticles();
    document.getElementById('articleCount').textContent =
      filtered.length > 0 ? '收录 ' + filtered.length + ' 篇' : '';

    if (!filtered.length) {
      content.innerHTML = `
        <div class="no-results">
          <div class="icon">📭</div>
          <p>没有匹配的动态</p>
          <p style="font-size:0.8rem;margin-top:4px;">试试调整筛选条件或扩大时间范围</p>
        </div>`;
      return;
    }

    // 按日期分组
    const grouped = {};
    filtered.forEach(a => {
      const d = a.date || '未知日期';
      if (!grouped[d]) grouped[d] = [];
      grouped[d].push(a);
    });

    // 排序：最新日期在前
    const sortedDates = Object.keys(grouped).sort((a, b) => b.localeCompare(a));

    let html = '';
    sortedDates.forEach(date => {
      const articles = grouped[date];
      html += `<div class="day-group">
        <div class="day-label">
          ${date}
          <span class="count">${articles.length} 篇</span>
        </div>`;

      articles.forEach(a => {
        const srcClass = a.source_type === '官方公报' ? 'source-official' : 'source-media';
        const badgeClass = a.source_type === '官方公报' ? 'badge-official' : 'badge-media';
        html += `<div class="article-card ${srcClass}">
          <div class="title">
            <a href="${escapeHtml(a.url)}" target="_blank" rel="noopener">${escapeHtml(a.title)}</a>
          </div>
          <div class="meta">
            <span class="source-name">${escapeHtml(a.source || '')}</span>
            <span class="source-badge ${badgeClass}">${escapeHtml(a.source_type || '')}</span>
          </div>`;

        if (a.summary) {
          html += `<div class="summary">${escapeHtml(a.summary)}</div>`;
        }

        if (a.categories && a.categories.length) {
          html += '<div class="tags">';
          a.categories.forEach(cat => {
            const cls = 'tag-' + cat;
            html += `<span class="tag ${cls}">${escapeHtml(cat)}</span>`;
          });
          html += '</div>';
        }

        html += '</div>';
      });

      html += '</div>';
    });

    content.innerHTML = html;
  }

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ---- 启动 ----
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
