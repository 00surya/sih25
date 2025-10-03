console.log('📊 Dashboard JS loaded');

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

let trendChart, barChart, relevanceChart;
let dashboardResults = {};
const SENTIMENT_COLORS = { Positive: "#4CAF50", Neutral: "#FFC107", Negative: "#F44336" };
let preloaderElem, preloaderNumberElem, loadingInterval;
let groupSelect;

document.addEventListener('DOMContentLoaded', () => {
  preloaderElem = document.getElementById('preloader');
  preloaderNumberElem = document.getElementById('preloader-number');
  groupSelect = document.getElementById('groupSelect');

  const parts = window.location.pathname.split('/');
  const draftIdIndex = parts.indexOf('draft') + 1;
  const draftId = draftIdIndex > 0 ? parts[draftIdIndex] : null;
  if (draftId) loadDashboard(draftId);
  else showNotification("Invalid URL", "Draft ID missing.", "warning", 4000);

  // Sidebar chart tab clicks
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active class
      document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
  
      const tab = btn.dataset.tab;
      const currentGroup = groupSelect.value || Object.keys(dashboardResults)[0];
  
      // Hide all chart sections first
      document.querySelectorAll('.chart-section').forEach(s => s.classList.remove('active'));
  
      if (tab === 'all') {
        document.getElementById('all').classList.add('active');
        renderAllCharts(currentGroup);
      } else {
        const section = document.getElementById(tab);
        if (section) section.classList.add('active');
        renderDashboardGroup(currentGroup);
      }
    });
  });


  // Sidebar collapse toggle (place inside your DOMContentLoaded handler)
const sidebar = document.querySelector('.sidebar');
const dashboardLayout = document.querySelector('.dashboard-layout');
const toggleBtn = document.getElementById('sidebarToggle');

if (toggleBtn && sidebar && dashboardLayout) {
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    // update aria attribute for accessibility
    const collapsed = sidebar.classList.contains('collapsed');
    toggleBtn.setAttribute('aria-expanded', collapsed ? 'true' : 'false');
  });
} else {
  // helpful debug if something's not present
  console.warn('Sidebar toggle elements missing', { toggleBtn, sidebar, dashboardLayout });
}

  


  
});

function startPreloader() {
  if (!preloaderNumberElem) return;
  let count = 0;
  loadingInterval = setInterval(() => {
    count += Math.floor(Math.random() * 15) + 1;
    preloaderNumberElem.textContent = count.toString().padStart(6, '0');
  }, 50);
}

function stopPreloader() {
  clearInterval(loadingInterval);
  if (preloaderElem) preloaderElem.style.display = 'none';
}



/* ---------- MAIN DASHBOARD LOADING ---------- */
async function loadDashboard(draftId) {
  if (preloaderElem) preloaderElem.style.display = 'flex';
  startPreloader();

  const csrfToken = getCookie('csrf_access_token');
  try {
    const res = await fetch(window.location.href, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': csrfToken },
      body: JSON.stringify({ draft_id: draftId })
    });

    stopPreloader();
    const data = await res.json();
    if (data.error) return;

    dashboardResults = data.results || {};
    const groups = Object.keys(dashboardResults);
    if (!groups.length) {
      showNotification("No Data", "No groups found in the dashboard.", "warning", 5000);
      return;
    }

    const defaultGroup = groups.includes("All Data") ? "All Data" : groups[0];

    // Populate group filter dropdown
    groupSelect.innerHTML = groups.map(g => `<option value="${g}">${g}</option>`).join('');
    groupSelect.value = defaultGroup;
    groupSelect.addEventListener('change', () => {
      renderDashboardGroup(groupSelect.value);
    });

    renderDashboardGroup(defaultGroup);
    showNotification("Dashboard Ready", `Loaded data for "${defaultGroup}"`, "success", 3000);
  } catch (err) {
    stopPreloader();
    console.error('🚨 Fetch Error:', err);
    showNotification("Dashboard Load Failed", "Something went wrong.", "error", 5000);
  }
}

/* ---------- RENDER FUNCTIONS ---------- */
function renderDashboardGroup(groupName) {
  const groupData = dashboardResults[groupName];
  if (!groupData) return;

  const totalComments = groupData.total_comments || 0;
  const avgSentiment = groupData.avg_sentiment !== undefined 
      ? groupData.avg_sentiment.toFixed(2) 
      : "N/A";

  // --- Sentiment Bar ---
  const barCanvas = document.getElementById("sentimentBar");
  if (barCanvas) {
    const barCtx = barCanvas.getContext("2d");
    if (barChart) barChart.destroy();

    // Clear old metrics if exist
    const metricsDiv = document.getElementById("sentimentMetrics");
    if (metricsDiv) {
      metricsDiv.innerHTML = `Total: ${totalComments} comments | Avg Sentiment: ${avgSentiment}`;
    }

    barChart = new Chart(barCtx, {
      type: "bar",
      data: {
        labels: Object.keys(groupData.sentiment_counts),
        datasets: [{
          data: Object.values(groupData.sentiment_counts),
          backgroundColor: Object.keys(groupData.sentiment_counts).map(s => SENTIMENT_COLORS[s] || "#999"),
          borderRadius: 8
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  }

  // --- Trend ---
  const trendLabels = groupData.trend?.labels.map(label =>
    new Date(label).toLocaleString(undefined, { month:"short", day:"numeric", hour:"2-digit", minute:"2-digit", hour12:false })
  ) || [];
  const visibleSentiments = new Set(["Positive","Neutral","Negative"]);
  createTrendChart(trendLabels, groupData.trend?.datasets || {}, visibleSentiments);

  // --- Word Cloud ---
  renderWordCloud(Object.entries(groupData.wordcloud || {}));

  // --- Clusters ---
  renderClusters(groupData.clustering?.clusters || []);

  // --- Fact vs Emotion ---
  renderFactEmotionChart(groupData.fact_emotion);

  // --- Relevance ---
  if (groupData.relevance) renderRelevanceGraph(groupData.relevance);
}

/* ---------- TREND CHART ---------- */
function createTrendChart(labels, datasets, visibleSentiments, canvasId="sentimentTrend") {
  const filteredDatasets = Object.keys(datasets)
    .filter(sentiment => visibleSentiments.has(sentiment))
    .map(sentiment => ({
      label: sentiment,
      data: datasets[sentiment],
      fill: false,
      tension: 0.3,
      pointRadius: 5,
      pointHoverRadius: 7,
      borderWidth: 2,
      borderColor: SENTIMENT_COLORS[sentiment] || "#000"
    }));

  const ctx = document.getElementById(canvasId)?.getContext("2d");
  if (!ctx) return;

  if (trendChart) trendChart.destroy();

  trendChart = new Chart(ctx, {
    type: "line",
    data: { labels, datasets: filteredDatasets },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { color: "#444" } },
        tooltip: { callbacks: { title: c => c[0].label, label: c => `${c.dataset.label}: ${c.parsed.y}` } }
      },
      scales: {
        x: { ticks: { color: "#555" }, title: { display:true, text:"Date & Time", color:"#666" } },
        y: { beginAtZero:true, ticks: { stepSize:1, color:"#555" }, title:{ display:true, text:"Mentions", color:"#666" } }
      }
    }
  });
}

/* ---------- WORD CLOUD ---------- */
function renderWordCloud(wordList, canvasId = "wordCloudCanvas") {
  const canvas = document.getElementById(canvasId);
  if (!canvas || !wordList?.length) return;

  const maxWords = 120;
  const limitedList = wordList.slice(0, maxWords);

  // Create tooltip if not exists
  let tooltip = document.getElementById('wcTooltip');
  if (!tooltip) {
    tooltip = document.createElement('div');
    tooltip.id = 'wcTooltip';
    tooltip.style.position = 'absolute';
    tooltip.style.background = 'rgba(0,0,0,0.8)';
    tooltip.style.color = '#fff';
    tooltip.style.padding = '4px 8px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '0.85rem';
    tooltip.style.pointerEvents = 'none';
    tooltip.style.display = 'none';
    tooltip.style.zIndex = '9999';
    document.body.appendChild(tooltip);
  }

  WordCloud(canvas, {
    list: limitedList,
    gridSize: Math.floor(16 + canvas.width / 250),
    weightFactor: w => 12 + w * 1.5,
    fontFamily: 'Inter, sans-serif',
    color: function(word, weight) {
      // Color based on frequency (or random bright colors)
      const colors = ['#ef4444','#f97316','#facc15','#4ade80','#22d3ee','#3b82f6','#9333ea'];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    backgroundColor: '#ffffff',
    rotateRatio: 0,
    shrinkToFit: true,
    origin: [canvas.width / 2, canvas.height / 2],
    drawOutOfBound: false,

    hover: function(item, dimension, event) {
      if (item) {
        tooltip.innerHTML = `<strong>${item[0]}</strong>: ${item[1]} occurrences`;
        tooltip.style.left = event.pageX + 10 + 'px';
        tooltip.style.top = event.pageY + 10 + 'px';
        tooltip.style.display = 'block';
      } else {
        tooltip.style.display = 'none';
      }
    }
  });

  // Hide tooltip on mouse leave
  canvas.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
}


/* ---------- CLUSTERS ---------- */
function renderClusters(clusters, listId = "clusterList") {
  const clusterList = document.getElementById(listId);
  clusterList.innerHTML = '';

  if (!clusters?.length) {
    clusterList.innerHTML = '<p>No topic clusters available.</p>';
    return;
  }

  clusters.forEach(cluster => {
    const li = document.createElement('li');
    li.style.marginBottom = '1rem';
    li.style.cursor = 'pointer';

    const clusterTitle = document.createElement('div');
    clusterTitle.className = 'cluster-title';
    clusterTitle.textContent = `Cluster ${cluster.cluster_id + 1}: Top Terms`;

    const clusterDetails = document.createElement('div');
    clusterDetails.className = 'cluster-details';
    clusterDetails.textContent = `Keywords: ${cluster.top_terms.join(', ')} | Mentions: ${cluster.size}`;

    const sampleCommentsDiv = document.createElement('div');
    sampleCommentsDiv.className = 'sample-comments';
    sampleCommentsDiv.innerHTML = cluster.sample_comments?.length
      ? cluster.sample_comments.map(c => `<p style="margin:0.3rem 0;">${c}</p>`).join('')
      : '<p>No sample comments available.</p>';

    // Toggle only this cluster's comments
    li.addEventListener('click', () => {
      sampleCommentsDiv.classList.toggle('show');
    });

    li.appendChild(clusterTitle);
    li.appendChild(clusterDetails);
    li.appendChild(sampleCommentsDiv);
    clusterList.appendChild(li);
  });
}


/* ---------- FACT vs EMOTION ---------- */
function renderFactEmotionChart(factEmotionData, canvasId = "factEmotionChart") {
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx || !factEmotionData) return;
  if (window.factEmotionChartInstance) window.factEmotionChartInstance.destroy();

  window.factEmotionChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: factEmotionData.labels,
      datasets: [{
        data: factEmotionData.counts,
        backgroundColor: ['#1d4ed8', '#f43f5e'], // Blue & Red
        borderColor: '#fff',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { color: "#333" } },
        tooltip: { callbacks: { label: c => `${c.label}: ${c.parsed} (${((c.parsed / c.dataset.data.reduce((a,b)=>a+b))*100).toFixed(1)}%)` } }
      }
    }
  });
}


/* ---------- RELEVANCE ---------- */
function renderRelevanceGraph(relevanceData, canvasId = "relevanceGraph") {
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx || !relevanceData) return;
  if (relevanceChart) relevanceChart.destroy();

  relevanceChart = new Chart(ctx,{
    type:'bar',
    data:{ labels:relevanceData.labels, datasets:[{ label:'Number of Comments', data:relevanceData.counts, backgroundColor:['#4CAF50','#FFC107','#F44336'], borderRadius:6 }] },
    options:{ responsive:true, plugins:{ legend:{ display:false } } }
  });
}



function renderAllCharts(groupName) {
  const groupData = dashboardResults[groupName];
  if (!groupData) return;

  const metricsRow = document.getElementById("metricsRow");
  const grid = document.getElementById("allChartsGrid");

  // Reset content
  metricsRow.innerHTML = "";
  grid.innerHTML = "";

  // Compute metrics
  const totalComments = groupData.total_comments || 0;
  const avgSentiment = groupData.avg_sentiment !== undefined 
    ? groupData.avg_sentiment.toFixed(2) 
    : "N/A";
  const mostCommonSentiment = Object.entries(groupData.sentiment_counts || {})
    .sort((a,b) => b[1]-a[1])[0]?.[0] || "N/A";

  // Populate metrics row
  metricsRow.innerHTML = `
    <div class="metric-box">
      <h4>Total Comments</h4>
      <p>${totalComments}</p>
    </div>
    <div class="metric-box">
      <h4>Avg Sentiment</h4>
      <p>${avgSentiment}</p>
    </div>
    <div class="metric-box">
      <h4>Most Common Sentiment</h4>
      <p>${mostCommonSentiment}</p>
    </div>
  `;

  // Build charts grid
  grid.innerHTML = `
    <div class="chart-box"><h3>Sentiment Distribution</h3><canvas id="all_sentimentBar"></canvas></div>
    <div class="chart-box"><h3>Trend Over Time</h3><canvas id="all_sentimentTrend"></canvas></div>
    <div class="chart-box"><h3>Word Cloud</h3><canvas id="all_wordCloudCanvas" width="500" height="400"></canvas></div>
    <div class="chart-box"><h3>Topic Clusters</h3><ul id="all_clusterList"></ul></div>
    <div class="chart-box"><h3>Fact vs Emotion</h3><canvas id="all_factEmotionChart"></canvas></div>
    <div class="chart-box"><h3>Relevance</h3><canvas id="all_relevanceGraph"></canvas></div>
  `;

  // Render charts (reuse existing functions)
  createTrendChart(
    groupData.trend?.labels.map(label =>
      new Date(label).toLocaleString(undefined, {
        month:"short", day:"numeric", hour:"2-digit", minute:"2-digit", hour12:false
      })
    ) || [],
    groupData.trend?.datasets || {},
    new Set(["Positive","Neutral","Negative"]),
    "all_sentimentTrend"
  );
  renderWordCloud(Object.entries(groupData.wordcloud || {}), "all_wordCloudCanvas");
  renderClusters(groupData.clustering?.clusters || [], "all_clusterList");
  renderFactEmotionChart(groupData.fact_emotion, "all_factEmotionChart");
  renderRelevanceGraph(groupData.relevance, "all_relevanceGraph");

  // Sentiment Bar Chart
  const barCtx = document.getElementById("all_sentimentBar").getContext("2d");
  new Chart(barCtx, {
    type: "bar",
    data: {
      labels: Object.keys(groupData.sentiment_counts),
      datasets: [{
        data: Object.values(groupData.sentiment_counts),
        backgroundColor: Object.keys(groupData.sentiment_counts).map(s => SENTIMENT_COLORS[s] || "#999"),
        borderRadius: 8
      }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
  });
}



/* ---------- NOTIFICATION PLACEHOLDER ---------- */
function showNotification(title,msg,type='info',duration=3000){ console.log(title,msg,type); }
