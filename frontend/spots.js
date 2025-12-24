let isLoggedIn = false;
let currentUser = null;

// ローカルストレージからユーザー情報を取得
function loadUserFromStorage() {
    const userData = localStorage.getItem('currentUser');
    if (userData) {
        currentUser = JSON.parse(userData);
        isLoggedIn = true;
        updateLoginButton();
    }
}

// ログインボタンの状態を更新
function updateLoginButton() {
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn) {
        if (isLoggedIn && currentUser) {
            loginBtn.textContent = `${currentUser.name} (ログアウト)`;
            loginBtn.onclick = handleLogout;
        } else {
            loginBtn.textContent = 'ログイン';
            loginBtn.onclick = handleLogin;
        }
    }
}

// ログイン処理
async function handleLogin() {
    const userId = prompt('ユーザーIDを入力してください（例: 4）:');
    const password = prompt('パスワードを入力してください:');

    if (!userId || !password) {
        alert('ユーザーIDとパスワードを入力してください');
        return;
    }

    try {
        const result = await apiClient.authenticateUser(userId, password);

        if (result.success) {
            isLoggedIn = true;
            currentUser = result.user;

            // ローカルストレージに保存
            localStorage.setItem('currentUser', JSON.stringify(currentUser));

            updateLoginButton();
            alert(`${currentUser.name}さんとしてログインしました`);
        } else {
            alert('ログインに失敗しました: ' + (result.message || 'ユーザーIDまたはパスワードが正しくありません'));
        }
    } catch (error) {
        console.error('ログインエラー:', error);
        alert('ログインに失敗しました');
    }
}

// ログアウト処理
function handleLogout() {
    isLoggedIn = false;
    currentUser = null;
    localStorage.removeItem('currentUser');
    updateLoginButton();
    alert('ログアウトしました');
    // spot-detail.htmlにいる場合、レビューフォームを非表示にする処理がない
    // 本来はここでレビューフォームを非表示にすべき
}

// データベースから観光地を読み込んで表示
async function loadSpotsFromDatabase() {
    try {
        const spots = await apiClient.getTouristSpots();
        const spotsGrid = document.getElementById('spotsGrid');

        if (!spotsGrid) {
            console.error('観光地グリッド（spotsGrid）が見つかりません');
            return;
        }

        // 既存の内容をクリア
        spotsGrid.innerHTML = '';

        // 観光地をHTML要素として追加
        spots.forEach(spot => {
            // エリアを判定（HTMLのボタンと一致するように）
            let area = 'other';
            if (spot.address.includes('前橋') || spot.address.includes('赤城')) {
                area = 'maebashi';
            } else if (spot.address.includes('高崎') || spot.address.includes('富岡')) {
                area = 'takasaki';
            } else if (spot.address.includes('草津') || spot.address.includes('四万')) {
                area = 'kusatsu';
            } else if (spot.address.includes('水上') || spot.address.includes('みなかみ') || spot.address.includes('利根郡') || spot.spot_name.includes('尾瀬') || spot.spot_name.includes('谷川')) {
                area = 'minakami';
            } else if (spot.address.includes('伊香保') || spot.address.includes('渋川') || spot.spot_name.includes('榛名')) {
                area = 'ikaho';
            }

            const spotElement = document.createElement('div');
            spotElement.className = 'spot-item';
            spotElement.dataset.area = area;

            // 星評価の表示を作成
            const fullStars = Math.floor(spot.avg_rating);
            const hasHalfStar = spot.avg_rating % 1 >= 0.5;
            const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
            const starsHtml = '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(emptyStars);
            const ratingText = spot.review_count > 0 ? `${starsHtml} ${spot.avg_rating.toFixed(1)} (${spot.review_count}件)` : '評価なし';

            spotElement.innerHTML = `
                <div class="spot-image" style="overflow: hidden;">
                    <img src="assets/images/spots/${spot.spot_id}.jpg"
                         alt="${spot.spot_name}"
                         onerror="this.src='assets/images/placeholders/no-image.png'"
                         style="width: 100%; height: 100%; object-fit: contain;">
                </div>
                <div class="spot-info">
                    <span class="spot-area">${spot.address}</span>
                    <h3><a href="spot-detail.html?id=${spot.spot_id}">${spot.spot_name}</a></h3>
                    <div class="spot-rating" style="color: #ffd700; margin: 5px 0;">${ratingText}</div>
                    <p class="spot-description">${spot.description ? spot.description.substring(0, 100) + '...' : ''}</p>
                </div>
            `;

            // Explicitly set the grid layout to ensure consistency
            spotElement.style.display = 'grid';
            spotElement.style.gridTemplateColumns = '200px 1fr';
            spotElement.style.gap = '20px';

            spotsGrid.appendChild(spotElement);
        });

        // ランキングも生成
        loadRanking(spots);

        console.log(`${spots.length}件の観光地を表示しました`);
    } catch (error) {
        console.error('観光地の読み込みに失敗しました:', error);
        alert('観光地の読み込みに失敗しました。サーバーが起動していることを確認してください。');
    }
}

// ランキングを生成（評価順にソート）
function loadRanking(spots) {
    const rankingList = document.getElementById('rankingList');
    if (!rankingList) return;

    rankingList.innerHTML = '';

    // 評価順にソート（評価高い順 → レビュー数多い順 → ID順）
    const sortedSpots = [...spots].sort((a, b) => {
        if (b.avg_rating !== a.avg_rating) {
            return b.avg_rating - a.avg_rating;
        }
        if (b.review_count !== a.review_count) {
            return b.review_count - a.review_count;
        }
        return a.spot_id - b.spot_id;
    });

    // 上位10件をランキングとして表示
    sortedSpots.slice(0, 10).forEach((spot, index) => {
        const rankItem = document.createElement('li');
        rankItem.className = `ranking-item ${index < 3 ? 'top3' : ''}`;

        // 星評価の表示を作成
        // バグ: 星の計算ロジックが間違っている（Math.ceilを使うと計算がおかしくなる）
        const fullStars = Math.ceil(spot.avg_rating);
        const hasHalfStar = spot.avg_rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars;
        const starsHtml = '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(emptyStars);
        const ratingDisplay = spot.review_count > 0 ? `<div style="color: #ffd700; font-size: 0.9rem;">${starsHtml} ${spot.avg_rating.toFixed(1)}</div>` : '<div style="color: #999; font-size: 0.9rem;">評価なし</div>';

        rankItem.innerHTML = `
            <span class="ranking-number">${index + 1}</span>
            <span class="ranking-name">
                <a href="spot-detail.html?id=${spot.spot_id}">${spot.spot_name}</a>
                ${ratingDisplay}
            </span>
        `;

        rankingList.appendChild(rankItem);
    });
}

// 検索機能
async function searchSpots() {
    const searchInput = document.getElementById('searchInput');
    const keyword = searchInput.value.trim();
    const searchResultInfo = document.getElementById('searchResultInfo');

    if (!keyword) {
        searchResultInfo.textContent = 'キーワードを入力してください';
        return;
    }

    try {
        const results = await apiClient.searchTouristSpots(keyword);
        displaySearchResults(results, keyword);
    } catch (error) {
        console.error('検索エラー:', error);
        searchResultInfo.textContent = '検索に失敗しました';
    }
}

// 検索結果を表示
function displaySearchResults(results, keyword) {
    const spotsGrid = document.getElementById('spotsGrid');
    const searchResultInfo = document.getElementById('searchResultInfo');

    if (!spotsGrid) return;

    // 既存の内容をクリア
    spotsGrid.innerHTML = '';

    // 検索結果情報を表示
    searchResultInfo.textContent = `「${keyword}」の検索結果: ${results.length}件`;

    if (results.length === 0) {
        spotsGrid.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">検索結果が見つかりませんでした</p>';
        return;
    }

    // 検索結果をHTML要素として追加
    results.forEach(spot => {
        // エリアを判定
        let area = 'other';
        if (spot.address.includes('前橋') || spot.address.includes('赤城')) {
            area = 'maebashi';
        } else if (spot.address.includes('高崎') || spot.address.includes('富岡')) {
            area = 'takasaki';
        } else if (spot.address.includes('草津') || spot.address.includes('四万')) {
            area = 'kusatsu';
        } else if (spot.address.includes('水上') || spot.address.includes('みなかみ') || spot.address.includes('利根郡') || spot.spot_name.includes('尾瀬') || spot.spot_name.includes('谷川')) {
            area = 'minakami';
        } else if (spot.address.includes('伊香保') || spot.address.includes('渋川') || spot.spot_name.includes('榛名')) {
            area = 'ikaho';
        }

        const spotElement = document.createElement('div');
        spotElement.className = 'spot-item';
        spotElement.dataset.area = area;

        // 星評価の表示を作成
        const fullStars = Math.floor(spot.avg_rating);
        const hasHalfStar = spot.avg_rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        const starsHtml = '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(emptyStars);
        const ratingText = spot.review_count > 0 ? `${starsHtml} ${spot.avg_rating.toFixed(1)} (${spot.review_count}件)` : '評価なし';

        spotElement.innerHTML = `
            <div class="spot-image" style="overflow: hidden;">
                <img src="assets/images/spots/${spot.spot_id}.jpg"
                     alt="${spot.spot_name}"
                     onerror="this.src='assets/images/placeholders/no-image.png'"
                     style="width: 100%; height: 100%; object-fit: contain;">
            </div>
            <div class="spot-info">
                <span class="spot-area">${spot.address}</span>
                <h3><a href="spot-detail.html?id=${spot.spot_id}">${spot.spot_name}</a></h3>
                <div class="spot-rating" style="color: #ffd700; margin: 5px 0;">${ratingText}</div>
                <p class="spot-description">${spot.description ? spot.description.substring(0, 100) + '...' : ''}</p>
            </div>
        `;

        spotElement.style.display = 'grid';
        spotElement.style.gridTemplateColumns = '200px 1fr';
        spotElement.style.gap = '20px';

        spotsGrid.appendChild(spotElement);
    });
}

// 検索をクリア
function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResultInfo = document.getElementById('searchResultInfo');

    searchInput.value = '';
    searchResultInfo.textContent = '';

    // 全観光地を再読み込み
    loadSpotsFromDatabase();
}

// エリアでフィルタリング
function filterByArea(area, clickedButton) {
    const spotItems = document.querySelectorAll('.spot-item');
    const areaButtons = document.querySelectorAll('.area-btn');

    // バグ: 前のボタンのactiveクラスを削除していない
    // areaButtons.forEach(btn => {
    //     btn.classList.remove('active');
    // });

    if (clickedButton) {
        clickedButton.classList.add('active');
    }

    spotItems.forEach(item => {
        if (area === 'all') {
            item.style.display = 'grid';
            item.style.gridTemplateColumns = '200px 1fr';
            item.style.gap = '20px';
        } else {
            if (item.dataset.area === area) {
                item.style.display = 'grid';
                item.style.gridTemplateColumns = '200px 1fr';
                item.style.gap = '20px';
            } else {
                item.style.display = 'none';
            }
        }
    });

    console.log(`フィルター: ${area} - ${document.querySelectorAll(`.spot-item[data-area="${area}"]`).length}件表示`);
}

// ページ読み込み時に実行
window.addEventListener('DOMContentLoaded', () => {
    loadUserFromStorage();
    loadSpotsFromDatabase();
});