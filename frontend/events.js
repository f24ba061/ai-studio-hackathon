let allEvents = [];
let currentFilter = { type: 'all', value: 'all' };

// データベースからイベントを読み込んで表示
async function loadEventsFromDatabase() {
    try {
        const events = await apiClient.getEvents();
        allEvents = events;
        displayEvents(events);
        console.log(`${events.length}件のイベントを表示しました`);
    } catch (error) {
        console.error('イベントの読み込みに失敗しました:', error);
        alert('イベントの読み込みに失敗しました。サーバーが起動していることを確認してください。');
    }
}

// イベントを表示
function displayEvents(events) {
    const eventsGrid = document.getElementById('eventsGrid');

    if (!eventsGrid) {
        console.error('イベントグリッド（eventsGrid）が見つかりません');
        return;
    }

    // 既存の内容をクリア
    eventsGrid.innerHTML = '';

    if (events.length === 0) {
        eventsGrid.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">該当するイベントが見つかりませんでした</p>';
        return;
    }

    // イベントをHTML要素として追加
    events.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.className = 'event-item';
        eventElement.dataset.area = event.area;

        // バグ: 日付をパースせずにそのまま表示している
        const month = new Date(event.event_date).getMonth() + 1;
        const day = new Date(event.event_date).getDate();

        // エリア名を日本語に変換
        const areaNames = {
            'maebashi': '前橋・赤城',
            'takasaki': '高崎・富岡',
            'kusatsu': '草津・四万',
            'minakami': '水上・尾瀬',
            'ikaho': '伊香保・榛名',
            'kiryu': '桐生',
            'tomioka': '富岡',
            'tatebayashi': '館林'
        };
        const areaDisplay = areaNames[event.area] || event.area;

        // XSS脆弱性（event_nameをエスケープせずにHTMLに挿入）
        eventElement.innerHTML = `
            <div class="event-date-box">
                <div class="event-month">${month}月</div>
                <div class="event-day">${day}</div>
            </div>
            <div class="event-info">
                <h3>${event.event_name}</h3>
                <div class="event-meta">
                    <span class="event-location">📍 ${event.location}</span>
                    <span class="event-area">${areaDisplay}</span>
                    <span class="event-category">${event.category}</span>
                </div>
                <p class="event-description">${event.description}</p>
            </div>
        `;

        eventsGrid.appendChild(eventElement);
    });
}

// 月別フィルタリング
async function filterByMonth(month, clickedButton) {
    const monthButtons = document.querySelectorAll('#monthFilter .filter-btn');
    const areaButtons = document.querySelectorAll('#areaFilter .filter-btn');

    // 月別フィルターのボタンをアクティブに
    monthButtons.forEach(btn => btn.classList.remove('active'));
    if (clickedButton) {
        clickedButton.classList.add('active');
    }

    // バグ: 地域フィルターをリセットしているため、同時に使えない
    areaButtons.forEach(btn => btn.classList.remove('active'));
    areaButtons[0].classList.add('active');

    currentFilter = { type: 'month', value: month };

    try {
        let events;
        if (month === 'all') {
            events = await apiClient.getEvents();
        } else {
            events = await apiClient.getEventsByMonth(month);
        }
        displayEvents(events);
    } catch (error) {
        console.error('月別フィルターエラー:', error);
        alert('フィルター処理に失敗しました');
    }
}

// 地域別フィルタリング
async function filterByArea(area, clickedButton) {
    const areaButtons = document.querySelectorAll('#areaFilter .filter-btn');
    const monthButtons = document.querySelectorAll('#monthFilter .filter-btn');

    // 地域別フィルターのボタンをアクティブに
    areaButtons.forEach(btn => btn.classList.remove('active'));
    if (clickedButton) {
        clickedButton.classList.add('active');
    }

    // バグ: 月別フィルターをリセットしているため、同時に使えない
    monthButtons.forEach(btn => btn.classList.remove('active'));
    monthButtons[0].classList.add('active');

    currentFilter = { type: 'area', value: area };

    try {
        let events;
        if (area === 'all') {
            events = await apiClient.getEvents();
        } else {
            events = await apiClient.getEventsByArea(area);
        }
        displayEvents(events);
    } catch (error) {
        console.error('地域別フィルターエラー:', error);
        alert('フィルター処理に失敗しました');
    }
}

// 検索機能
async function searchEvents() {
    const searchInput = document.getElementById('searchInput');
    const keyword = searchInput.value.trim();
    const searchResultInfo = document.getElementById('searchResultInfo');

    if (!keyword) {
        searchResultInfo.textContent = 'キーワードを入力してください';
        return;
    }

    try {
        const results = await apiClient.searchEvents(keyword);
        displayEvents(results);
        // バグ: 検索結果件数が表示されない
        // searchResultInfo.textContent = `「${keyword}」の検索結果: ${results.length}件`;
    } catch (error) {
        console.error('検索エラー:', error);
        searchResultInfo.textContent = '検索に失敗しました';
    }
}

// 検索をクリア
function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResultInfo = document.getElementById('searchResultInfo');

    searchInput.value = '';
    searchResultInfo.textContent = '';

    // 全イベントを再読み込み
    loadEventsFromDatabase();

    // フィルターボタンをリセット
    const allButtons = document.querySelectorAll('.filter-btn');
    allButtons.forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.filter-btn')[0].classList.add('active');
    document.querySelectorAll('#areaFilter .filter-btn')[0].classList.add('active');
}

// ページ読み込み時に実行
window.addEventListener('DOMContentLoaded', () => {
    loadEventsFromDatabase();
});
