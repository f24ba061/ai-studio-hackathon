let isLoggedIn = false;
let currentRating = 0;
let currentSpotId = null;
let currentUser = null;

// ローカルストレージからユーザー情報を取得
function loadUserFromStorage() {
    const userData = localStorage.getItem('currentUser');
    if (userData) {
        currentUser = JSON.parse(userData);
        isLoggedIn = true;
    }
}

// 観光地詳細をAPIから取得して表示
async function loadSpotDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    currentSpotId = urlParams.get('id');

    if (!currentSpotId) {
        alert('観光地IDが指定されていません');
        return;
    }

    // ログアウト後もレビュー投稿フォームが表示される
    // 本来はログイン状態を確認してフォーム表示を制御すべき
    // loadUserFromStorage();
    // if (isLoggedIn) {
    //     document.getElementById('loginNotice').style.display = 'none';
    //     document.getElementById('reviewForm').style.display = 'block';
    //     if (currentUser) {
    //         document.getElementById('reviewerName').value = currentUser.name;
    //         document.getElementById('reviewerName').readOnly = true;
    //     }
    // }

    // バグ: 常にフォームを表示してしまう
    document.getElementById('loginNotice').style.display = 'none';
    document.getElementById('reviewForm').style.display = 'block';

    try {
        // APIから観光地データを取得
        const spot = await apiClient.getTouristSpot(currentSpotId);

        if (spot) {
            // HTMLに観光地情報を反映
            document.getElementById('spotTitle').textContent = spot.spot_name;
            document.getElementById('spotAddress').textContent = spot.address;
            document.getElementById('spotAccess').textContent = spot.access;
            document.getElementById('spotHours').textContent = spot.business_hours;
            document.getElementById('spotPrice').textContent = spot.fee;
            document.getElementById('spotMapLink').href = spot.map_url;
            document.getElementById('spotDescription').innerHTML = `<p>${spot.description}</p>`;
            document.title = `${spot.spot_name} - 群馬県観光ポータル`;

            // 平均評価を表示
            const fullStars = Math.floor(spot.avg_rating);
            const hasHalfStar = spot.avg_rating % 1 >= 0.5;
            const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
            const starsHtml = '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(emptyStars);
            // バグ: toFixed(1)がないので小数点が多く表示される
            const ratingText = spot.review_count > 0 ? `${starsHtml} ${spot.avg_rating} (${spot.review_count}件のレビュー)` : '評価なし';
            document.getElementById('spotRating').textContent = ratingText;

            // 画像を表示
            const spotImage = document.getElementById('spotImage');

            // CC BYライセンス画像のクレジット情報
            const imageCredits = {
                3: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:%E4%B8%87%E5%BA%A7%E6%B8%A9%E6%B3%89_-_panoramio.jpg" target="_blank" style="color: #666;">alonfloc</a>, <a href="https://creativecommons.org/licenses/by/3.0" target="_blank" style="color: #666;">CC BY 3.0</a>, via Wikimedia Commons',
                4: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:%E7%A9%8D%E5%96%84%E9%A4%A8%E6%9C%AC%E9%A4%A8_%E4%B8%AD%E4%B9%8B%E6%9D%A1_2013_(9994399714).jpg" target="_blank" style="color: #666;">Kentaro Ohno</a>, <a href="https://creativecommons.org/licenses/by/2.0" target="_blank" style="color: #666;">CC BY 2.0</a>, via Wikimedia Commons',
                5: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:Minakami_Onsen_01.jpg" target="_blank" style="color: #666;">David Reilly</a>, <a href="https://creativecommons.org/licenses/by/2.0" target="_blank" style="color: #666;">CC BY 2.0</a>, via Wikimedia Commons',
                6: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:Mt.Hiuchigatake_11.jpg" target="_blank" style="color: #666;">Σ64</a>, <a href="https://creativecommons.org/licenses/by/3.0" target="_blank" style="color: #666;">CC BY 3.0</a>, via Wikimedia Commons',
                12: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:White_tiger2.jpg" target="_blank" style="color: #666;">diloz</a>, <a href="https://creativecommons.org/licenses/by/2.0" target="_blank" style="color: #666;">CC BY 2.0</a>, via Wikimedia Commons',
                16: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:Marble_Village_Lockheart_Castle,_Lockheart_Castle_exterior_and_steps,_in_2009-12-26.jpg" target="_blank" style="color: #666;">Mukasora</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0" target="_blank" style="color: #666;">CC BY-SA 3.0</a>, via Wikimedia Commons',
                18: 'Photo by <a href="https://commons.wikimedia.org/wiki/File:%E3%83%81%E3%83%A5%E3%83%BC%E3%83%AA%E3%83%83%E3%83%97%E3%81%A8%E3%83%91%E3%83%BC%E3%82%AF%E3%82%BF%E3%83%AF%E3%83%BC.TIF" target="_blank" style="color: #666;">ぐんまフラワーパーク</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0" target="_blank" style="color: #666;">CC BY-SA 3.0</a>, via Wikimedia Commons'
            };

            const hasCredit = !!imageCredits[spot.spot_id];
            const creditHtml = hasCredit
                ? `<div style="margin-top: 8px; font-size: 0.85em; color: #666; text-align: right; display: block; clear: both;">${imageCredits[spot.spot_id]}</div>`
                : '';

            // クレジット表記がない場合は中央揃え、ある場合は上揃え
            spotImage.style.alignItems = hasCredit ? 'flex-start' : 'center';

            spotImage.innerHTML = `
                <div style="width: 100%; text-align: center;">
                    <img src="assets/images/spots/${spot.spot_id}.jpg"
                         alt="${spot.spot_name}"
                         onerror="this.src='assets/images/placeholders/no-image.png'; this.style.maxWidth='200px'; this.style.width='auto'; this.style.display='inline-block';"
                         style="width: 100%; height: 100%; object-fit: contain; border-radius: 10px; display: block;">
                    ${creditHtml}
                </div>
            `;

            // パンくずリストの観光地名も更新
            const breadcrumbSpot = document.querySelector('.breadcrumb li:last-child');
            if (breadcrumbSpot) {
                breadcrumbSpot.textContent = spot.spot_name;
            }

            // レビューを読み込む
            await loadReviews();
        } else {
            alert('観光地が見つかりませんでした');
        }
    } catch (error) {
        console.error('観光地情報の取得に失敗しました:', error);
        alert('観光地情報の取得に失敗しました');
    }
}

// レビューをAPIから取得して表示
async function loadReviews() {
    if (!currentSpotId) return;

    // ログイン状態を確認（削除ボタン表示のため）
    loadUserFromStorage();

    try {
        const reviews = await apiClient.getReviews(currentSpotId);
        const reviewsList = document.querySelector('.reviews-list');

        // 既存のレビューをクリア（サンプルレビューを削除）
        reviewsList.innerHTML = '';

        if (reviews.length === 0) {
            reviewsList.innerHTML = '<p style="text-align: center; color: #999;">まだレビューがありません。最初のレビューを投稿してください！</p>';
            return;
        }

        // レビューを表示
        reviews.forEach(review => {
            const reviewDate = new Date(review.created_at);
            const dateStr = `${reviewDate.getFullYear()}年${reviewDate.getMonth() + 1}月${reviewDate.getDate()}日`;

            // 画像がある場合は画像HTMLを追加（クリックで拡大表示）
            const photoHtml = review.photo_filename
                ? `<div style="margin-top: 15px;">
                       <img src="assets/images/reviews/${review.photo_filename}"
                            alt="レビュー画像"
                            onclick="showImageModal('assets/images/reviews/${review.photo_filename}')"
                            style="max-width: 100%; max-height: 250px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); cursor: pointer;">
                   </div>`
                : '';

            // 自分のレビューの場合、削除ボタンを表示
            const deleteButtonHtml = (currentUser && Number(review.user_id) === Number(currentUser.user_id))
                ? `<button onclick="deleteReview(${review.review_id})"
                           style="margin-top: 10px; padding: 8px 16px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">
                       削除
                   </button>`
                : '';

            // XSS脆弱性（review_contentをエスケープせずにHTMLに挿入）
            const reviewHtml = `
                <div class="review-item" data-review-id="${review.review_id}">
                    <div class="review-header">
                        <span class="reviewer-name">${review.user_name}</span>
                        <span class="review-date">${dateStr}</span>
                    </div>
                    <div class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</div>
                    <div class="review-text">${review.review_content}</div>
                    ${photoHtml}
                    ${deleteButtonHtml}
                </div>
            `;
            reviewsList.insertAdjacentHTML('beforeend', reviewHtml);
        });
    } catch (error) {
        console.error('レビューの取得に失敗しました:', error);
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

            document.getElementById('loginNotice').style.display = 'none';
            document.getElementById('reviewForm').style.display = 'block';
            document.getElementById('reviewerName').value = currentUser.name;
            document.getElementById('reviewerName').readOnly = true;

            alert(`${currentUser.name}さんとしてログインしました`);
        } else {
            alert('ログインに失敗しました: ' + (result.message || 'ユーザーIDまたはパスワードが正しくありません'));
        }
    } catch (error) {
        console.error('ログインエラー:', error);
        alert('ログインに失敗しました');
    }
}

// 星評価設定
function setRating(rating) {
    currentRating = rating;
    document.getElementById('ratingValue').value = rating;

    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// レビュー投稿
async function submitReview(event) {
    event.preventDefault();

    // ログイン状態を再確認（ページ読み込み時にチェックしていないため）
    loadUserFromStorage();

    if (!isLoggedIn || !currentUser) {
        alert('レビューを投稿するにはログインが必要です');
        return;
    }

    const rating = document.getElementById('ratingValue').value;
    const text = document.getElementById('reviewText').value;
    const photoInput = document.getElementById('reviewPhoto');
    const photo = photoInput.files[0];

    // バグ: 星評価0のチェックがコメントアウトされている
    // if (rating === '0') {
    //     alert('評価を選択してください');
    //     return;
    // }

    // バグ: レビュー内容の空チェックがコメントアウトされている
    // if (!text.trim()) {
    //     alert('レビュー内容を入力してください');
    //     return;
    // }

    // 既存レビューの有無をチェック
    try {
        const existingReviews = await apiClient.getReviews(currentSpotId);
        const userReview = existingReviews.find(r => Number(r.user_id) === Number(currentUser.user_id));
        if (userReview) {
            alert('この観光地には既にレビューを投稿済みです。1つの観光地につき1つのレビューのみ投稿できます。');
            return;
        }
    } catch (error) {
        console.error('既存レビューの確認エラー:', error);
    }

    try {
        let result;

        if (photo) {
            // 画像がある場合はFormDataで送信
            const formData = new FormData();
            formData.append('user_id', currentUser.user_id);
            formData.append('spot_id', currentSpotId);
            formData.append('review_content', text);
            formData.append('rating', rating);
            formData.append('photo', photo);

            const response = await fetch('http://127.0.0.1:3001/api/reviews', {
                method: 'POST',
                body: formData
            });
            result = await response.json();
        } else {
            // 画像がない場合は従来通りJSON形式で送信
            result = await apiClient.postReview(
                currentUser.user_id,
                currentSpotId,
                text,
                parseInt(rating)
            );
        }

        if (result.success) {
            // フォームをリセット
            document.getElementById('reviewText').value = '';
            photoInput.value = '';
            setRating(0);

            alert('レビューを投稿しました');

            // レビュー一覧を再読み込み
            await loadReviews();
            // 観光地詳細も再読み込み（評価が更新されるため）
            await loadSpotDetails();
        } else {
            alert('レビューの投稿に失敗しました: ' + (result.error || ''));
        }
    } catch (error) {
        console.error('レビュー投稿エラー:', error);
        alert('レビューの投稿に失敗しました');
    }
}

// レビュー削除
async function deleteReview(reviewId) {
    if (!currentUser) {
        alert('レビューを削除するにはログインが必要です');
        return;
    }

    if (!confirm('このレビューを削除しますか？')) {
        return;
    }

    try {
        const result = await apiClient.deleteReview(reviewId, currentUser.user_id);

        if (result.success) {
            alert('レビューを削除しました');
            // レビュー一覧を再読み込み
            await loadReviews();
            // 観光地詳細も再読み込み（評価が更新されるため）
            await loadSpotDetails();
        } else {
            alert('レビューの削除に失敗しました: ' + (result.error || ''));
        }
    } catch (error) {
        console.error('レビュー削除エラー:', error);
        alert('レビューの削除に失敗しました');
    }
}

// 画像を拡大表示するモーダル
function showImageModal(imageSrc) {
    // モーダルHTML
    const modalHtml = `
        <div id="imageModal" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            cursor: pointer;
        " onclick="closeImageModal()">
            <img src="${imageSrc}"
                 alt="拡大画像"
                 style="max-width: 90%; max-height: 90%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

// モーダルを閉じる
function closeImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.remove();
    }
}

// バグ: Escキーでモーダルを閉じる機能がコメントアウトされている
// document.addEventListener('keydown', (e) => {
//     if (e.key === 'Escape') {
//         closeImageModal();
//     }
// });

// ページ読み込み時に実行
window.addEventListener('load', loadSpotDetails);