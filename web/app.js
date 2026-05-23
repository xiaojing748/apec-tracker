/* ============================================================
   APEC 2026 动态追踪看板 - 前端交互
   支持：实时筛选、历史归档、关键词搜索
   ============================================================ */

(function () {
  'use strict';

  const DATA_URL = 'data/articles.json';
  let allArticles = [];
  let activeFilters = {
    categories: new Set(['数据跨境', 'AI治理', '互联互通', '地缘政治', '2026中国年', '其他APEC动态']),
    sourceTypes: new Set(['官方公报', '权威媒体']),
    timeRange: '7',
    month: '',
    search: '',
  };

  // ---- 初始化 ----
  async function init() {
    var data = null;
    if (window.__APEC_DATA__) {
      data = window.__APEC_DATA__;
    } else {
      try {
        var resp = await fetch(DATA_URL);
        if (resp.ok) data = await resp.json();
      } catch (e) {
        console.error('加载数据失败:', e);
      }
    }
    if (data) {
      allArticles = data.articles || [];
      document.getElementById('updateTime').textContent =
        '最后更新：' + (data.last_updated || '未知');
      // 更新统计
      updateStats(data);
      // 填充月份选择器
      populateMonths();
    } else {
      allArticles = [];
      document.getElementById('updateTime').textContent = '数据加载失败，请稍后刷新';
    }
    bindFilters();
    render();
  }

  function updateStats(data) {
    var total = data.total_articles || allArticles.length;
    var todayCount = data.today_count || 0;
    var monthlyCount = data.monthly_count || 0;
    document.getElementById('statTotal').textContent = total;
    document.getElementById('statMonth').textContent = monthlyCount;
    document.getElementById('statToday').textContent = todayCount;
  }

  function populateMonths() {
    var months = {};
    allArticles.forEach(function (a) {
      var m = (a.date || '').substring(0, 7);
      if (m) months[m] = (months[m] || 0) + 1;
    });
    var sorted = Object.keys(months).sort().reverse();
    var sel = document.getElementById('monthFilter');
    // 保留第一个默认选项，清空后面的
    while (sel.options.length > 1) sel.remove(1);
    sorted.forEach(function (m) {
      var opt = document.createElement('option');
      opt.value = m;
      opt.textContent = m + ' (' + months[m] + '篇)';
      sel.appendChild(opt);
    });
  }

  // ---- 绑定筛选器事件 ----
  function bindFilters() {
    document.querySelectorAll('[data-filter="category"]').forEach(function (cb) {
      cb.addEventListener('change', function () {
        updateCategoryFilter();
        render();
      });
    });

    document.querySelectorAll('[data-filter="sourceType"]').forEach(function (cb) {
      cb.addEventListener('change', function () {
        updateSourceTypeFilter();
        render();
      });
    });

    document.getElementById('timeFilter').addEventListener('change', function () {
      activeFilters.timeRange = this.value;
      // 选择了具体天数后，清除月份筛选
      if (this.value !== 'all') {
        document.getElementById('monthFilter').value = '';
        activeFilters.month = '';
      }
      render();
    });

    document.getElementById('monthFilter').addEventListener('change', function () {
      activeFilters.month = this.value;
      // 选择了具体月份后，清除天数筛选
      if (this.value) {
        document.getElementById('timeFilter').value = 'all';
        activeFilters.timeRange = 'all';
      }
      render();
    });

    document.getElementById('searchBox').addEventListener('input', function () {
      activeFilters.search = this.value.trim().toLowerCase();
      render();
    });

    document.getElementById('resetFilters').addEventListener('click', function () {
      document.querySelectorAll('[data-filter="category"]').forEach(function (cb) { cb.checked = true; });
      document.querySelectorAll('[data-filter="sourceType"]').forEach(function (cb) { cb.checked = true; });
      document.getElementById('timeFilter').value = '7';
      document.getElementById('monthFilter').value = '';
      document.getElementById('searchBox').value = '';
      activeFilters.categories = new Set(['数据跨境', 'AI治理', '互联互通', '地缘政治', '2026中国年', '其他APEC动态']);
      activeFilters.sourceTypes = new Set(['官方公报', '权威媒体']);
      activeFilters.timeRange = '7';
      activeFilters.month = '';
      activeFilters.search = '';
      render();
    });
  }

  function updateCategoryFilter() {
    activeFilters.categories = new Set();
    document.querySelectorAll('[data-filter="category"]:checked').forEach(function (cb) {
      activeFilters.categories.add(cb.value);
    });
  }

  function updateSourceTypeFilter() {
    activeFilters.sourceTypes = new Set();
    document.querySelectorAll('[data-filter="sourceType"]:checked').forEach(function (cb) {
      activeFilters.sourceTypes.add(cb.value);
    });
  }

  // ---- 过滤逻辑 ----
  function getFilteredArticles() {
    if (!allArticles.length) return [];

    var now = new Date();
    var filtered = allArticles;

    // 月份筛选（精确到月）
    if (activeFilters.month) {
      filtered = filtered.filter(function (a) {
        return (a.date || '').substring(0, 7) === activeFilters.month;
      });
    } else {
      // 时间范围筛选（相对天数）
      if (activeFilters.timeRange !== 'all') {
        var days = parseInt(activeFilters.timeRange, 10);
        var cutoff = new Date(now);
        cutoff.setDate(cutoff.getDate() - days);
        var cutoffStr = cutoff.toISOString().slice(0, 10);
        filtered = filtered.filter(function (a) { return a.date >= cutoffStr; });
      }
    }

    // 议题分类过滤
    filtered = filtered.filter(function (a) {
      var cats = a.categories || ['其他APEC动态'];
      return cats.some(function (c) { return activeFilters.categories.has(c); });
    });

    // 来源类型过滤
    filtered = filtered.filter(function (a) {
      return activeFilters.sourceTypes.has(a.source_type || '权威媒体');
    });

    // 搜索过滤
    if (activeFilters.search) {
      var s = activeFilters.search;
      filtered = filtered.filter(function (a) {
        return (a.title || '').toLowerCase().indexOf(s) !== -1 ||
          (a.source || '').toLowerCase().indexOf(s) !== -1 ||
          (a.summary || '').toLowerCase().indexOf(s) !== -1;
      });
    }

    return filtered;
  }

  // ---- 渲染 ----
  function render() {
    var content = document.getElementById('content');
    var filtered = getFilteredArticles();
    document.getElementById('articleCount').textContent =
      filtered.length > 0 ? '显示 ' + filtered.length + ' 篇' : '';

    if (!filtered.length) {
      content.innerHTML =
        '<div class="no-results">' +
        '<div class="icon">&#x1F4ED;</div>' +
        '<p>没有匹配的动态</p>' +
        '<p style="font-size:0.8rem;margin-top:4px;">试试调整筛选条件或扩大时间范围</p>' +
        '</div>';
      return;
    }

    // 按日期分组
    var grouped = {};
    filtered.forEach(function (a) {
      var d = a.date || '未知日期';
      if (!grouped[d]) grouped[d] = [];
      grouped[d].push(a);
    });

    // 排序：最新日期在前
    var sortedDates = Object.keys(grouped).sort(function (a, b) { return b.localeCompare(a); });

    var html = '';
    sortedDates.forEach(function (date) {
      var articles = grouped[date];
      html += '<div class="day-group">' +
        '<div class="day-label">' +
        date +
        '<span class="count">' + articles.length + ' 篇</span>' +
        '</div>';

      articles.forEach(function (a) {
        var srcClass = a.source_type === '官方公报' ? 'source-official' : 'source-media';
        var badgeClass = a.source_type === '官方公报' ? 'badge-official' : 'badge-media';
        html += '<div class="article-card ' + srcClass + '">' +
          '<div class="title">' +
          '<a href="' + escapeHtml(a.url) + '" target="_blank" rel="noopener">' + escapeHtml(a.title) + '</a>' +
          '</div>' +
          '<div class="meta">' +
          '<span class="source-name">' + escapeHtml(a.source || '') + '</span>' +
          '<span class="source-badge ' + badgeClass + '">' + escapeHtml(a.source_type || '') + '</span>' +
          '</div>';

        if (a.summary) {
          html += '<div class="summary">' + escapeHtml(a.summary) + '</div>';
        }

        if (a.categories && a.categories.length) {
          html += '<div class="tags">';
          a.categories.forEach(function (cat) {
            html += '<span class="tag tag-' + cat + '">' + escapeHtml(cat) + '</span>';
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
    var div = document.createElement('div');
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
