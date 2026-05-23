/* ============================================================
   APEC 2026 动态追踪看板 - 前端交互
   ============================================================ */

(function () {
  'use strict';

  var DATA_URL = '../data/articles.json';
  var allArticles = [];
  var activeFilters = {
    categories: new Set(['数据跨境与隐私保护', 'AI治理', '互联互通', '数字经济', '地缘政治', '供应链安全', '网络犯罪', '2026中国年', '其他APEC动态']),
    sourceTypes: new Set(['官方公报', '权威媒体']),
    timeRange: '7',
    month: '',
    search: '',
  };

  // ---- 初始化 ----
  function init() {
    if (window.__APEC_DATA__) {
      loadData(window.__APEC_DATA__);
    } else {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', DATA_URL, true);
      xhr.onload = function () {
        if (xhr.status === 200) {
          try { loadData(JSON.parse(xhr.responseText)); } catch (e) { showError(); }
        } else { showError(); }
      };
      xhr.onerror = showError;
      xhr.send();
    }
  }

  function loadData(data) {
    allArticles = data.articles || [];
    document.getElementById('updateTime').textContent = '最后更新：' + (data.last_updated || '未知');
    updateStats(data);
    populateMonths();
    bindFilters();
    applyFilters();
  }

  function showError() {
    allArticles = [];
    document.getElementById('updateTime').textContent = '数据加载失败，请刷新重试';
    document.getElementById('content').innerHTML = '<div class="no-results"><p>数据加载失败</p></div>';
  }

  function updateStats(data) {
    document.getElementById('statTotal').textContent = data.total_articles || allArticles.length;
    document.getElementById('statMonth').textContent = data.monthly_count || 0;
    document.getElementById('statToday').textContent = data.today_count || 0;
  }

  function populateMonths() {
    var months = {};
    allArticles.forEach(function (a) {
      var m = (a.date || '').substring(0, 7);
      if (m) months[m] = (months[m] || 0) + 1;
    });
    var sorted = Object.keys(months).sort().reverse();
    var sel = document.getElementById('monthFilter');
    while (sel.options.length > 1) sel.remove(1);
    sorted.forEach(function (m) {
      var opt = document.createElement('option');
      opt.value = m;
      opt.textContent = m + ' (' + months[m] + '篇)';
      sel.appendChild(opt);
    });
  }

  // ---- 筛选器事件 ----
  function bindFilters() {
    var cats = document.querySelectorAll('[data-filter="category"]');
    for (var i = 0; i < cats.length; i++) {
      cats[i].onchange = function () { updateCategoryFilter(); applyFilters(); };
    }

    var srcs = document.querySelectorAll('[data-filter="sourceType"]');
    for (var j = 0; j < srcs.length; j++) {
      srcs[j].onchange = function () { updateSourceTypeFilter(); applyFilters(); };
    }

    document.getElementById('timeFilter').onchange = function () {
      activeFilters.timeRange = this.value;
      if (this.value !== 'all') {
        document.getElementById('monthFilter').value = '';
        activeFilters.month = '';
      }
      applyFilters();
    };

    document.getElementById('monthFilter').onchange = function () {
      activeFilters.month = this.value;
      if (this.value) {
        document.getElementById('timeFilter').value = 'all';
        activeFilters.timeRange = 'all';
      }
      applyFilters();
    };

    document.getElementById('searchBox').oninput = function () {
      activeFilters.search = this.value.trim().toLowerCase();
      applyFilters();
    };

    document.getElementById('resetFilters').onclick = function () {
      var allCats = document.querySelectorAll('[data-filter="category"]');
      for (var k = 0; k < allCats.length; k++) { allCats[k].checked = true; }
      var allSrcs = document.querySelectorAll('[data-filter="sourceType"]');
      for (var l = 0; l < allSrcs.length; l++) { allSrcs[l].checked = true; }
      document.getElementById('timeFilter').value = '7';
      document.getElementById('monthFilter').value = '';
      document.getElementById('searchBox').value = '';
      activeFilters.categories = new Set(['数据跨境与隐私保护', 'AI治理', '互联互通', '数字经济', '地缘政治', '供应链安全', '网络犯罪', '2026中国年', '其他APEC动态']);
      activeFilters.sourceTypes = new Set(['官方公报', '权威媒体']);
      activeFilters.timeRange = '7';
      activeFilters.month = '';
      activeFilters.search = '';
      applyFilters();
    };

    // 刷新按钮
    document.getElementById('btnRefresh').onclick = function () {
      applyFilters();
    };
  }

  function updateCategoryFilter() {
    activeFilters.categories = new Set();
    var checked = document.querySelectorAll('[data-filter="category"]:checked');
    for (var i = 0; i < checked.length; i++) {
      activeFilters.categories.add(checked[i].value);
    }
  }

  function updateSourceTypeFilter() {
    activeFilters.sourceTypes = new Set();
    var checked = document.querySelectorAll('[data-filter="sourceType"]:checked');
    for (var i = 0; i < checked.length; i++) {
      activeFilters.sourceTypes.add(checked[i].value);
    }
  }

  // ---- 过滤 + 渲染 ----
  function applyFilters() {
    var filtered = getFilteredArticles();
    document.getElementById('articleCount').textContent =
      filtered.length > 0 ? '显示 ' + filtered.length + ' 篇' : '无匹配结果';
    renderArticles(filtered);
  }

  function getFilteredArticles() {
    if (!allArticles.length) return [];

    var now = new Date();
    var filtered = allArticles.slice();

    // 月份筛选
    if (activeFilters.month) {
      filtered = filtered.filter(function (a) {
        return (a.date || '').substring(0, 7) === activeFilters.month;
      });
    } else if (activeFilters.timeRange !== 'all') {
      var days = parseInt(activeFilters.timeRange, 10);
      var cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
      var cutoffStr = formatDate(cutoff);
      filtered = filtered.filter(function (a) { return (a.date || '') >= cutoffStr; });
    }

    // 议题分类
    filtered = filtered.filter(function (a) {
      var cats = a.categories || ['其他APEC动态'];
      return cats.some(function (c) { return activeFilters.categories.has(c); });
    });

    // 来源类型
    filtered = filtered.filter(function (a) {
      return activeFilters.sourceTypes.has(a.source_type || '权威媒体');
    });

    // 搜索
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

  function formatDate(d) {
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1);
    var day = String(d.getDate());
    if (m.length === 1) m = '0' + m;
    if (day.length === 1) day = '0' + day;
    return y + '-' + m + '-' + day;
  }

  function renderArticles(filtered) {
    var content = document.getElementById('content');

    if (!filtered.length) {
      content.innerHTML =
        '<div class="no-results">' +
        '<div class="icon" style="font-size:2.5rem">📭</div>' +
        '<p>没有匹配的动态</p>' +
        '<p style="font-size:0.8rem;margin-top:4px;">试试调整筛选条件或点刷新按钮</p>' +
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

    var sortedDates = Object.keys(grouped).sort(function (a, b) { return b.localeCompare(a); });

    var html = '';
    sortedDates.forEach(function (date) {
      var articles = grouped[date];
      html += '<div class="day-group">' +
        '<div class="day-label">' + date +
        '<span class="count">' + articles.length + ' 篇</span></div>';

      articles.forEach(function (a) {
        var srcClass = a.source_type === '官方公报' ? 'source-official' : 'source-media';
        var badgeClass = a.source_type === '官方公报' ? 'badge-official' : 'badge-media';
        var badgeText = a.source_type || '权威媒体';

        html += '<div class="article-card ' + srcClass + '">' +
          '<div class="title"><a href="' + esc(a.url) + '" target="_blank" rel="noopener">' + esc(a.title) + '</a></div>' +
          '<div class="meta">' +
          '<span class="source-name">' + esc(a.source || '') + '</span>' +
          '<span class="source-badge ' + badgeClass + '">' + esc(badgeText) + '</span>' +
          '</div>';

        if (a.summary) {
          html += '<div class="summary">' + esc(a.summary) + '</div>';
        }

        if (a.categories && a.categories.length) {
          html += '<div class="tags">';
          a.categories.forEach(function (cat) {
            html += '<span class="tag tag-' + cat + '">' + esc(cat) + '</span>';
          });
          html += '</div>';
        }

        html += '</div>';
      });

      html += '</div>';
    });

    content.innerHTML = html;
  }

  function esc(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // ---- 启动 ----
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
