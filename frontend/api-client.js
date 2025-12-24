// APIクライアント - データベースからデータを取得

class APIClient {
    constructor() {
        // 現在のページのホストとポートを使用
        this.baseURL = `${window.location.protocol}//${window.location.host}/api`;
    }

    // 観光地一覧を取得
    async getTouristSpots() {
        try {
            const response = await fetch(`${this.baseURL}/spots`);
            if (!response.ok) throw new Error('観光地の取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 特定の観光地を取得
    async getTouristSpot(spotId) {
        try {
            const response = await fetch(`${this.baseURL}/spots/${spotId}`);
            if (!response.ok) throw new Error('観光地の取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return null;
        }
    }

    // 観光地を検索
    async searchTouristSpots(keyword) {
        try {
            const response = await fetch(`${this.baseURL}/spots/search?keyword=${encodeURIComponent(keyword)}`);
            if (!response.ok) throw new Error('検索に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // レビューを取得
    async getReviews(spotId) {
        try {
            const response = await fetch(`${this.baseURL}/reviews/${spotId}`);
            if (!response.ok) throw new Error('レビューの取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // レビューを投稿
    async postReview(userId, spotId, reviewContent, rating) {
        try {
            const response = await fetch(`${this.baseURL}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    spot_id: spotId,
                    review_content: reviewContent,
                    rating: rating
                })
            });

            if (!response.ok) throw new Error('レビューの投稿に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return { success: false, error: error.message };
        }
    }

    // ユーザー認証
    async authenticateUser(userId, password) {
        try {
            const response = await fetch(`${this.baseURL}/auth`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    password: password
                })
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('エラー:', error);
            return { success: false, error: error.message };
        }
    }

    // ユーザー登録
    async registerUser(password, name) {
        try {
            const response = await fetch(`${this.baseURL}/users`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password,
                    name: name
                })
            });

            if (!response.ok) throw new Error('ユーザー登録に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return { success: false, error: error.message };
        }
    }

    // レビューを削除
    async deleteReview(reviewId, userId) {
        try {
            const response = await fetch(`${this.baseURL}/reviews/${reviewId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId
                })
            });

            if (!response.ok) throw new Error('レビューの削除に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return { success: false, error: error.message };
        }
    }

    // イベント一覧を取得
    async getEvents() {
        try {
            const response = await fetch(`${this.baseURL}/events`);
            if (!response.ok) throw new Error('イベントの取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 月別でイベントを取得
    async getEventsByMonth(month) {
        try {
            const response = await fetch(`${this.baseURL}/events?month=${month}`);
            if (!response.ok) throw new Error('イベントの取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 地域別でイベントを取得
    async getEventsByArea(area) {
        try {
            const response = await fetch(`${this.baseURL}/events?area=${area}`);
            if (!response.ok) throw new Error('イベントの取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // イベントを検索
    async searchEvents(keyword) {
        try {
            const response = await fetch(`${this.baseURL}/events/search?q=${encodeURIComponent(keyword)}`);
            if (!response.ok) throw new Error('検索に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 統計情報を取得
    async getStatsSummary() {
        try {
            const response = await fetch(`${this.baseURL}/stats/summary`);
            if (!response.ok) throw new Error('統計情報の取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return {
                total_spots: 0,
                total_reviews: 0,
                total_users: 0,
                total_events: 0,
                avg_rating_overall: 0
            };
        }
    }

    // 地域別観光地数を取得
    async getStatsByArea() {
        try {
            const response = await fetch(`${this.baseURL}/stats/spots-by-area`);
            if (!response.ok) throw new Error('地域別統計の取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 月別イベント数を取得
    async getStatsByMonth() {
        try {
            const response = await fetch(`${this.baseURL}/stats/events-by-month`);
            if (!response.ok) throw new Error('月別統計の取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 人気観光地ランキングを取得
    async getTopSpots(limit = 5) {
        try {
            const response = await fetch(`${this.baseURL}/stats/top-spots?limit=${limit}`);
            if (!response.ok) throw new Error('ランキングの取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }

    // 近隣の観光地を取得
    async getNearbySpots(lat, lon) {
        try {
            const response = await fetch(`${this.baseURL}/spots/nearby?lat=${lat}&lon=${lon}`);
            if (!response.ok) throw new Error('近隣観光地の取得に失敗しました');
            return await response.json();
        } catch (error) {
            console.error('エラー:', error);
            return [];
        }
    }
}

/**
 * 距離をフォーマットする（m → km変換）
 * return文が抜けている
 * @param {number} meters - メートル単位の距離
 * @returns {string} フォーマットされた距離文字列
 */
function formatDistance(meters) {
    if (meters >= 1000) {
        // バグ: return文がない
        (meters / 1000).toFixed(1) + 'km';
    } else {
        // バグ: return文がない
        meters + 'm';
    }
}

// グローバル変数として利用可能にする
const apiClient = new APIClient();