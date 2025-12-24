/**
 * 統計ページのJavaScript
 */

/**
 * ページ読み込み時に実行
 */
document.addEventListener('DOMContentLoaded', async () => {
    await loadStats();
});

/**
 * 統計データを読み込む
 */
async function loadStats() {
    try {
        // 並列で全データ取得
        const [summary, topSpots, areaData, monthData] = await Promise.all([
            apiClient.getStatsSummary(),
            apiClient.getTopSpots(5),
            apiClient.getStatsByArea(),
            apiClient.getStatsByMonth()
        ]);

        displaySummary(summary);
        displayTopSpots(topSpots);
        displaySpotsByArea(areaData);
        displayEventsByMonth(monthData);
    } catch (error) {
        console.error('統計データの読み込みエラー:', error);
        showError('統計データの読み込みに失敗しました');
    }
}

/**
 * 基本統計を表示
 */
function displaySummary(summary) {
    document.getElementById('totalSpots').textContent = summary.total_spots || 0;
    document.getElementById('totalReviews').textContent = summary.total_reviews || 0;
    document.getElementById('totalUsers').textContent = summary.total_users || 0;
    document.getElementById('totalEvents').textContent = summary.total_events || 0;
    document.getElementById('avgRating').textContent = summary.avg_rating_overall
        ? `⭐ ${summary.avg_rating_overall}`
        : '-';
}

/**
 * 人気観光地ランキングを表示
 */
function displayTopSpots(spots) {
    const listElement = document.getElementById('topSpotsList');

    if (!spots || spots.length === 0) {
        listElement.innerHTML = '<div class="loading">データがありません</div>';
        return;
    }

    listElement.innerHTML = '';

    spots.forEach((spot, index) => {
        const rank = index + 1; // バグ: +1 していない
        const medal = getMedal(rank);

        const item = document.createElement('li');
        item.className = 'ranking-item';

        item.innerHTML = `
            ${medal ? `<span class="ranking-medal">${medal}</span>` : ''}
            <span class="ranking-number">${rank}位</span>
            <div class="ranking-info">
                <div class="ranking-name">${escapeHtml(spot.spot_name)}</div>
                <div class="ranking-rating">⭐ ${spot.avg_rating} (${spot.review_count}件)</div>
            </div>
        `;

        listElement.appendChild(item);
    });
}

/**
 * 順位に応じたメダルを返す
 */
function getMedal(rank) {
    switch(rank) {
        case 1: return '🥇';
        case 2: return '🥈';
        case 3: return '🥉';
        default: return '';
    }
}

/**
 * 地域別観光地数を表示
 */
function displaySpotsByArea(areas) {
    const chartElement = document.getElementById('areaChart');

    if (!areas || areas.length === 0) {
        chartElement.innerHTML = '<div class="loading">データがありません</div>';
        return;
    }

    chartElement.innerHTML = '';
    const maxValue = Math.max(...areas.map(a => a.count));

    areas.forEach(area => {
        const barItem = createBarChartItem(area.area_name, area.count, maxValue);
        chartElement.appendChild(barItem);
    });
}

/**
 * 月別イベント数を表示
 */
function displayEventsByMonth(months) {
    const chartElement = document.getElementById('monthChart');

    if (!months || months.length === 0) {
        chartElement.innerHTML = '<div class="loading">データがありません</div>';
        return;
    }

    chartElement.innerHTML = '';
    const maxValue = Math.max(...months.map(m => m.count));

    // カウントが0より大きい月のみ表示し、カウント順にソート
    const filteredMonths = months.filter(m => m.count > 0);
    filteredMonths.sort((a, b) => b.count - a.count);

    filteredMonths.forEach(month => {
        const barItem = createBarChartItem(month.month_name, month.count, maxValue);
        chartElement.appendChild(barItem);
    });
}

/**
 * 棒グラフアイテムを作成
 */
function createBarChartItem(label, value, maxValue) {
    const barItem = document.createElement('div');
    barItem.className = 'bar-chart-item';

    const widthPercent = value * 30; // バグ: 最大値を使っていない（1件でも30%になる）

    barItem.innerHTML = `
        <span class="bar-chart-label">${escapeHtml(label)}</span>
        <div class="bar-chart-bar-container">
            <div class="bar-chart-bar" style="width: ${widthPercent}%"></div>
        </div>
        <span class="bar-chart-value">${value}</span>
    `;

    return barItem;
}

/**
 * エラーメッセージを表示
 */
function showError(message) {
    const container = document.getElementById('statsContainer');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    container.insertBefore(errorDiv, container.firstChild);
}

/**
 * HTMLエスケープ（XSS対策）
 */
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.toString().replace(/[&<>"']/g, m => map[m]);
}
