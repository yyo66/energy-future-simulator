import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import requests
import time                   # <--- 新增這行 (解決截圖中的錯誤)
import random                 # <--- 新增這行 (為了碳交易市場的隨機事件)
from datetime import datetime # <--- 新增這行 (為了記錄交易時間)

# ---------------------------------------------------------
# 🚀 終極修復版：使用 CDN 連結下載，保證穩定不 404
# ---------------------------------------------------------
def download_and_set_font():
    # 這裡我們改用 .otf 格式，這是思源黑體的原始格式
    font_name = "NotoSansCJKtc-Regular.otf"
    
    # 1. 檢查並刪除壞掉的檔案 (如果檔案小於 1MB，代表之前下載失敗)
    if os.path.exists(font_name):
        if os.path.getsize(font_name) < 1000000:
            os.remove(font_name)
            print("已刪除損毀的字體檔，準備重新下載...")
    
    # 2. 如果檔案不存在，才下載
    if not os.path.exists(font_name):
        with st.spinner("正在下載中文字體 (約 16MB)，請耐心等候..."):
            # 使用 jsDelivr CDN 連結，比 GitHub Raw 更穩定
            url = "https://cdn.jsdelivr.net/gh/googlefonts/noto-cjk@main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf"
            try:
                response = requests.get(url, timeout=60) # 設定 60 秒超時
                response.raise_for_status()  # 確保連結有效
                with open(font_name, "wb") as f:
                    f.write(response.content)
                st.success("✅ 字體下載成功！已套用思源黑體。")
            except Exception as e:
                st.error(f"❌ 下載失敗，請檢查網路: {e}")
                return

    # 3. 加入字體
    try:
        fm.fontManager.addfont(font_name)
        font_prop = fm.FontProperties(fname=font_name)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False 
    except Exception as e:
        st.warning(f"字體載入有點問題，改用系統預設: {e}")

# 執行設定
download_and_set_font()
# ---------------------------------------------------------

# ... (下面接著寫您的 st.title 等主程式) ...
# 自定義CSS樣式
st.markdown("""
<style>
    /* 全局樣式 */
    .main {
        background: linear-gradient(135deg, #0a1929 0%, #001e3c 100%);
        color: #e0f2fe;
    }
    
    /* 限制內容寬度 */
    .block-container {
        max-width: 1000px;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    
    /* 主標題樣式 - 能源感設計 */
    .energy-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00c6ff, #00e676, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1rem 0;
        padding: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 198, 255, 0.7);
        letter-spacing: 1px;
        position: relative;
    }
    
    .energy-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 25%;
        width: 50%;
        height: 3px;
        background: linear-gradient(to right, transparent, #00e676, transparent);
    }
    
    /* 副標題樣式 */
    .sub-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #00c6ff;
        text-align: center;
        margin: 1.5rem 0 1rem 0;
        text-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
    }
    
    /* 能源感卡片樣式 */
    .energy-card {
        background: rgba(19, 47, 76, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 198, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        color: #e0f2fe;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .energy-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 198, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
        pointer-events: none;
    }
    
    @keyframes shine {
        0% { left: -50%; }
        100% { left: 150%; }
    }
    
    .energy-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 36px rgba(0, 198, 255, 0.4);
        border-color: rgba(0, 198, 255, 0.5);
    }
    
    /* 可點擊卡片樣式 */
    .clickable-card {
        background: rgba(19, 47, 76, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 198, 255, 0.2);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        color: #e0f2fe;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    
    .clickable-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 198, 255, 0.3);
        border-color: rgba(0, 198, 255, 0.4);
        background: rgba(26, 35, 126, 0.7);
    }
    
    /* 能源標籤樣式 */
    .energy-tag {
        display: inline-block;
        background: rgba(0, 198, 255, 0.15);
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid rgba(0, 198, 255, 0.3);
        color: #e0f2fe;
        margin: 4px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .energy-tag:hover {
        background: rgba(0, 198, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 198, 255, 0.3);
    }
    
    /* 指標卡樣式 */
    .metric-card {
        background: rgba(19, 47, 76, 0.7);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 198, 255, 0.2);
        color: #e0f2fe;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 198, 255, 0.3);
        border-color: rgba(0, 198, 255, 0.4);
    }
    
    .metric-card h3 {
        color: #90caf9;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card h2 {
        color: #00e676;
        font-size: 1.8rem;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    /* 導航選項卡樣式 - 能源感設計 */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: transparent;
    justify-content: center;
    border-bottom: 1px solid rgba(0, 198, 255, 0.2);
    margin-bottom: 1.5rem;
    flex-wrap: nowrap;
    overflow-x: auto;
    white-space: nowrap;
}

.stTabs [data-baseweb="tab"] {
    height: 45px;
    white-space: nowrap;
    background-color: rgba(19, 47, 76, 0.5);
    border-radius: 8px 8px 0 0;
    gap: 8px;
    padding: 10px 16px;
    border: 1px solid rgba(0, 198, 255, 0.2);
    color: #90caf9;
    font-weight: 500;
    backdrop-filter: blur(5px);
    margin: 0 2px;
    flex-shrink: 0;
    min-width: auto;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(26, 35, 126, 0.8);
    color: #00e676;
    border-bottom: 3px solid #00e676;
    box-shadow: 0 4px 12px rgba(0, 230, 118, 0.3);
}

/* 響應式調整 */
@media (max-width: 1200px) {
    .stTabs [data-baseweb="tab"] {
        padding: 8px 12px;
        font-size: 0.85rem;
    }
}

@media (max-width: 1000px) {
    .stTabs [data-baseweb="tab"] {
        padding: 6px 10px;
        font-size: 0.8rem;
    }
}
    
    /* 按鈕樣式 */
    .stButton button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 198, 255, 0.4);
        background: linear-gradient(135deg, #00e676 0%, #00c6ff 100%);
    }
    
    /* 文字顏色修正 */
    .stText, .stMarkdown, .stInfo, .stSuccess, .stWarning, .stError {
        color: #e0f2fe !important;
    }
    
    /* 增強對比度 */
    p, li, .stCaption {
        color: #e0f2fe !important;
        font-weight: 400;
    }
    
    strong {
        color: #00e676 !important;
    }
    
    /* 進度條樣式 */
    .stProgress > div > div {
        background: linear-gradient(to right, #00c6ff, #00e676);
        border-radius: 4px;
    }
    
    /* 能源動畫效果 */
    @keyframes pulse-energy {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6;
    }
    
    .pulse-energy {
        animation: pulse-energy 2s infinite ease-in-out;
    }
    
    /* 頁腳樣式 */
    footer {
        color: #90caf9 !important;
        text-align: center;
        padding: 1rem 0;
    }
    
    /* 響應式調整 */
    @media (max-width: 768px) {
        .energy-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
        }
        
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.9rem;
        }
    }
    
    /* 問答頁面專用樣式 */
    .quiz-level-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
        font-size: 0.8rem;
    }
    
    .quiz-beginner {
        background: linear-gradient(135deg, #4CAF50, #8BC34A);
        color: white;
    }
    
    .quiz-intermediate {
        background: linear-gradient(135deg, #2196F3, #03A9F4);
        color: white;
    }
    
    .quiz-advanced {
        background: linear-gradient(135deg, #9C27B0, #E91E63);
        color: white;
    }
    
    .question-card {
        background: rgba(25, 55, 85, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #00e676;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .option-card {
        background: rgba(30, 60, 90, 0.6);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 198, 255, 0.2);
    }
    
    .option-card:hover {
        background: rgba(40, 80, 120, 0.8);
        transform: translateX(5px);
        border-color: rgba(0, 198, 255, 0.5);
    }
    
    .option-card.correct {
        background: rgba(0, 200, 83, 0.3);
        border-color: #00e676;
    }
    
    .option-card.incorrect {
        background: rgba(255, 82, 82, 0.3);
        border-color: #ff5252;
    }
    
    .score-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #00c6ff, #00e676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    .leaderboard-item {
        display: flex;
        justify-content: space-between;
        padding: 0.8rem;
        margin: 0.3rem 0;
        background: rgba(30, 60, 90, 0.5);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 設定頁面
st.set_page_config(
    page_title="🌍 能源未來模擬器", 
    layout="wide", 
    page_icon="🌞",
    initial_sidebar_state="collapsed"
)

# 創建導航選項卡 - 添加氣候變遷頁面
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏠 首頁", "🌏 氣候變遷", "⚡ 發電模擬", "👣 碳足跡計算", 
    "💰 碳交易市場", "❓ 能源問答", "📊 未來預測", "📈 投資概略"
])

# 首頁內容
with tab1:
    # 主標題
    st.markdown('<h1 class="energy-header">🌍 能源未來模擬器</h1>', unsafe_allow_html=True)
    # 歡迎訊息和能源轉型動畫
    st.markdown("""
    <div class="energy-card">
        <h3 style="text-align: center; color: #00e676; margin-bottom: 1rem;">歡迎使用能源未來模擬器！</h3>
        <p style="text-align: center;">這是一個互動平台，讓您探索可再生能源、碳足跡與氣候變遷的關係。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 能源轉型動畫
    with st.expander("🎬 點擊觀看能源轉型模擬", expanded=False):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 25:
                status_text.text("🌱 模擬植樹造林中...")
            elif i < 50:
                status_text.text("☀️ 安裝太陽能板中...")
            elif i < 75:
                status_text.text("💨 建設風力發電中...")
            else:
                status_text.text("⚡ 電網綠色化進行中...")
            time.sleep(0.02)
        
        progress_bar.empty()
        status_text.success("✅ 能源轉型完成！碳排放減少60%！")
    
    # 平台簡介
    st.markdown("""
    <div class="energy-card">
        <h3 style="text-align: center; color: #00e676; margin-bottom: 1.5rem;">探索可再生能源、碳足跡與氣候變遷的互動模擬平台</h3>
        <p style="text-align: center; margin-bottom: 1.5rem;">每個<strong>選項卡</strong>具有各種近代關切能源主題！每個主題有著提供獨特的互動體驗，趕緊到<strong>頁頂體驗吧!</strong></p>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 1rem 0;">
            <div class="energy-tag">🌏 氣候變遷</div>
            <div class="energy-tag">⚡ 發電模擬</div>
            <div class="energy-tag">👣 碳足跡計算</div>
            <div class="energy-tag">💰 碳交易市場</div>
            <div class="energy-tag">❓ 能源問答</div>
            <div class="energy-tag">📊 未來預測</div>
            <div class="energy-tag">📈 投資概略</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

     # 可點擊的功能卡片
    st.markdown('<h3 class="sub-header">介紹功能</h3>', unsafe_allow_html=True)
    
    # 创建功能卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌏 氣候變遷\n\n了解全球氣候危機與影響", key="btn_climate_card", use_container_width=True):
            st.session_state.selected_tab = "氣候變遷"
    
    with col2:
        if st.button("⚡ 發電模擬\n\n調整能源結構，觀察對環境的影響", key="btn_sim_card", use_container_width=True):
            st.session_state.selected_tab = "發電模擬"
    
    with col3:
        if st.button("👣 碳足跡計算\n\n計算個人碳排放，學習減排方法", key="btn_footprint_card", use_container_width=True):
            st.session_state.selected_tab = "碳足跡計算"
    
    with col4:
        if st.button("💰 碳交易市場\n\n模擬碳權交易，了解市場機制", key="btn_market_card", use_container_width=True):
            st.session_state.selected_tab = "碳交易市場"
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("❓ 能源問答\n\n測試能源知識，分難度挑戰", key="btn_quiz_card", use_container_width=True):
            st.session_state.selected_tab = "能源問答"
    
    with col6:
        if st.button("📊 未來預測\n\n探索不同情境下的能源未來", key="btn_forecast_card", use_container_width=True):
            st.session_state.selected_tab = "未來預測"
    
    with col7:
        if st.button("📈 投資概略\n\n分析能源投資趨勢與機會", key="btn_invest_card", use_container_width=True):
            st.session_state.selected_tab = "投資概略"

    # 能源轉型模擬
    st.markdown('<h3 class="sub-header">能源轉型模擬</h3>', unsafe_allow_html=True)
    
    st.info("""
    **什麼是能源轉型？**
            
    能源轉型是指從傳統化石燃料為主的能源系統，轉向可再生能源為主的低碳能源系統的過程。
    這包括增加太陽能、風能、水能等可再生能源的比例，減少對煤炭、石油和天然氣的依賴。
    
    **為什麼碳排放減少60%很重要？**
    
    根據國際能源署(IEA)的研究，要實現《巴黎協定》將全球升溫控制在1.5°C以內的目標，
    全球需要在2050年前將能源相關的碳排放減少60-70%。這個模擬展示了通過能源轉型可以達到的減排效果。
    """)

    # 轉型策略選擇
    strategy = st.selectbox(
        "選擇能源轉型策略",
        ["保守轉型", "積極轉型", "激進轉型"],
        index=1,
        help="選擇不同的轉型策略來模擬不同的減排效果"
    )
    
    # 根據策略設定減排目標
    if strategy == "保守轉型":
        reduction_target = 40
        duration = 40
    elif strategy == "積極轉型":
        reduction_target = 60
        duration = 30
    else:  # 激進轉型
        reduction_target = 80
        duration = 20
    
    # 在首頁的能源轉型模擬部分添加
    st.info(f"**進度指示器**: 當前全球再生能源占比: {35}% | 目標: {50 if strategy == '保守轉型' else 60 if strategy == '積極轉型' else 70}%")

    # 添加進度條
    progress_value = 35 / (50 if strategy == '保守轉型' else 60 if strategy == '積極轉型' else 70)
    st.progress(progress_value)
    
    st.write(f"**目標**: 通過{strategy}策略，在{duration}年內將碳排放減少{reduction_target}%")
    
    # 開始模擬按鈕
    if st.button("🚀 開始模擬能源轉型", use_container_width=True):
        with st.expander("能源轉型模擬進度", expanded=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 20:
                    status_text.text("🌱 發展再生能源技術...")
                elif i < 40:
                    status_text.text("🏗️ 建設綠色基礎設施...")
                elif i < 60:
                    status_text.text("🔌 升級電網系統...")
                elif i < 80:
                    status_text.text("⚡ 逐步淘汰化石燃料...")
                else:
                    status_text.text("🌍 實現能源轉型...")
                time.sleep(0.05)
            
            progress_bar.empty()
            st.success(f"✅ 能源轉型完成！碳排放減少{reduction_target}%！")
            
            # 顯示轉型成果
            st.info(f"""
            **{strategy}策略成果**:
            - ✅ 碳排放減少: {reduction_target}%
            - ✅ 再生能源占比: {70 if strategy == '激進轉型' else 60 if strategy == '積極轉型' else 50}%
            - ✅ 轉型時間: {duration}年
            - ✅ 投資回報: {8 if strategy == '激進轉型' else 6 if strategy == '積極轉型' else 4}% 年化收益
            
            **環境效益**:
            - 🌿 空氣品質改善: {(reduction_target/2)+20}%
            - 💧 水資源節約: {reduction_target-10}%
            - 🏭 化石燃料進口減少: {reduction_target+10}%
            """)

    # 全球能源現況
    st.markdown('<h3 class="sub-header">全球能源現況</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="pulse-energy">🌡️</div>
            <h3>全球升溫</h3>
            <h2>1.2°C</h2>
            <p>比較工業化前上升幅度</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
            st.markdown("""
        <div class="metric-card">
            <div class="pulse-energy">☀️</div>
            <h3>再生能源占比</h3>
            <h2>35%</h2>
            <p>全球發電結構</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="pulse-energy">💰</div>
            <h3>碳價格</h3>
            <h2>$45/吨</h2>
            <p>全球平均</p>
        </div>
        """, unsafe_allow_html=True)

    # 能源轉型資訊
    st.markdown('<h3 class="sub-header">能源轉型進程方向</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="energy-card">
            <h4 style="color: #00e676; margin-bottom: 1rem;">🌍 全球目標</h4>
            <ul style="padding-left: 1.5rem;">
                <li>2030年再生能源占比達50%</li>
                <li>2050年實現全球淨零排放</li>
                <li>全球升溫控制在1.5°C內</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="energy-card">
            <h4 style="color: #00e676; margin-bottom: 1rem;">🚀 技術發展</h4>
            <ul style="padding-left: 1.5rem;">
                <li>太陽能轉換效率提升至25%</li>
                <li>儲能成本下降70%</li>
                <li>綠色氫能商業化應用</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 氣候變遷頁面
    with tab2:
        st.markdown('<h1 class="energy-header">🌏 氣候變遷：全球危機與影響</h1>', unsafe_allow_html=True)
        
        # 為什麼要關注氣候變遷
        st.markdown("""
        <div class="energy-card">
            <h3 style="text-align: center; color: #00e676; margin-bottom: 1rem;">為什麼我們要關注氣候變遷？</h3>
            <p style="text-align: center;">氣候變遷不僅是環境問題，更是影響人類生存、經濟發展和社會穩定的全球性危機。</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 創建氣候變遷影響的指標卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="pulse-energy">🌡️</div>
                <h3>全球升溫</h3>
                <h2>+1.2°C</h2>
                <p>相比工業化前</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="pulse-energy">🌊</div>
                <h3>海平面上升</h3>
                <h2>+20cm</h2>
                <p>1900年以來</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="pulse-energy">🔥</div>
                <h3>極端天氣</h3>
                <h2>+30%</h2>
                <p>過去20年增加</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="pulse-energy">🐾</div>
                <h3>物種滅絕風險</h3>
                <h2>25%</h2>
                <p>物種面臨威脅</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 氣候變遷的各個維度
        st.markdown("---")
        st.subheader("🌍 氣候變遷的多維度影響")
        
        # 溫室效應
        with st.expander("🔥 溫室效應與全球暖化", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("""
                **什麼是溫室效應？**
                
                溫室效應是指地球大氣層中的溫室氣體（如二氧化碳、甲烷等）吸收並重新輻射熱能，
                使地球表面溫度升高的自然現象。沒有溫室效應，地球平均溫度將為-18°C，不適合生命存在。
                
                **人為加劇的溫室效應**
                
                工業革命以來，人類活動大量排放溫室氣體，導致溫室效應過度增強，造成全球暖化。
                
                **主要溫室氣體來源**:
                - 二氧化碳(CO₂): 化石燃料燃燒、森林砍伐
                - 甲烷(CH₄): 畜牧業、垃圾填埋、化石燃料開採
                - 氧化亞氮(N₂O): 農業化肥、工業過程
                - 氟化氣體: 制冷劑、工業製程
                """)
            
            with col2:
                # 溫室氣體貢獻圖
                fig, ax = plt.subplots(figsize=(6, 4))
                gases = ['二氧化碳', '甲烷', '氧化亞氮', '氟化氣體']
                contributions = [76, 16, 6, 2]
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
                ax.pie(contributions, labels=gases, colors=colors, autopct='%1.1f%%', startangle=90)
                ax.set_title('溫室氣體排放貢獻比例')
                st.pyplot(fig)
                plt.close(fig)
        
        # 海平面上升
        with st.expander("🌊 海平面上升", expanded=False):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("""
                **海平面上升的影響**
                
                - **沿海城市淹沒**: 全球數億人居住的沿海地區面臨威脅
                - **島國消失**: 馬爾代夫、圖瓦盧等低窪島國可能完全被淹沒
                - **鹽水入侵**: 淡水資源受到海水入侵污染
                - **極端天氣加劇**: 風暴潮威力增強，沿海災害頻發
                
                **主要原因**:
                - 冰川融化: 格陵蘭和南極冰蓋融化
                - 熱膨脹: 海水因溫度升高而體積膨脹
                - 山地冰川消退: 阿爾卑斯、喜馬拉雅等冰川快速消退
                """)
            
            with col2:
                # 海平面上升預測圖
                years = [2000, 2020, 2040, 2060, 2080, 2100]
                low_scenario = [0, 10, 20, 30, 40, 50]  # 厘米
                high_scenario = [0, 15, 35, 60, 90, 120]  # 厘米
                
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.plot(years, low_scenario, marker='o', label='樂觀情景', linewidth=2)
                ax.plot(years, high_scenario, marker='s', label='悲觀情景', linewidth=2)
                ax.set_xlabel('年份')
                ax.set_ylabel('海平面上升 (厘米)')
                ax.set_title('海平面上升預測 (相比2000年)')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
        
        # 極端天氣與聖嬰現象
        with st.expander("🌪️ 極端天氣與聖嬰現象", expanded=False):
            st.write("""
            **極端天氣事件增加**
            
            氣候變遷導致極端天氣事件頻率和強度增加:
            - **熱浪**: 持續時間更長、溫度更高
            - **暴雨洪水**: 降雨強度增加，洪水頻發
            - **乾旱**: 乾旱區域擴大，持續時間延長
            - **強烈颱風**: 颱風強度增強，路徑更不穩定
            
            **聖嬰現象(El Niño)與反聖嬰現象(La Niña)**
            
            聖嬰現象是太平洋赤道地區海水溫度異常升高的自然氣候模式，
            氣候變遷可能使聖嬰現象更加頻繁和強烈，導致全球氣候異常。
            
            **影響包括**:
            - 亞太地區乾旱與森林大火
            - 美洲西海岸暴雨洪水
            - 全球糧食生產受影響
            - 珊瑚白化事件增加
            """)
            
            # 極端天氣事件統計
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("熱浪事件", "+45%", "過去20年增加")
            with col2:
                st.metric("洪水頻率", "+35%", "過去20年增加")
            with col3:
                st.metric("乾旱強度", "+25%", "過去20年增加")
        
        # 北極與臭氧層破洞
        with st.expander("❄️ 北極融化與臭氧層破洞", expanded=False):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("""
                **北極冰層快速融化**
                
                - **海冰減少**: 北極夏季海冰面積減少40%以上
                - **永久凍土融化**: 釋放大量甲烷，加劇暖化
                - **生態系統破壞**: 北極熊等物種生存受威脅
                - **反饋循環**: 冰層減少降低地球反照率，加速暖化
                
                **臭氧層破洞**
                
                儘管蒙特婁公約成功減少了破壞臭氧層的化學物質，
                但氣候變遷可能影響臭氧層恢復速度:
                - 極地平流層雲變化影響臭氧消耗
                - 大氣環流改變影響臭氧分布
                - 紫外線輻射增加對生態系統的影響
                """)
            
            with col2:
                # 北極海冰面積變化
                years = [1980, 1990, 2000, 2010, 2020]
                ice_extent = [7.5, 7.2, 6.8, 5.9, 4.5]  # 百萬平方公里
                
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(years, ice_extent, color='#87CEEB', alpha=0.7)
                ax.set_xlabel('年份')
                ax.set_ylabel('海冰面積 (百萬平方公里)')
                ax.set_title('北極9月最小海冰面積變化')
                st.pyplot(fig)
                plt.close(fig)
        
        # 生物多樣性與動物棲息地
        with st.expander("🐾 生物多樣性危機", expanded=False):
            st.write("""
            **氣候變遷對生物多樣性的影響**
            
            - **棲息地喪失**: 溫度變化導致物種遷移，棲息地碎片化
            - **物種滅絕加速**: 無法適應快速氣候變化的物種面臨滅絕
            - **生態系統失衡**: 物種間關係改變，食物網受破壞
            - **珊瑚白化**: 海洋酸化與升溫導致珊瑚大規模死亡
            
            **受威脅的物種與生態系統**
            
            - **北極生態系統**: 北極熊、海象、北極狐等
            - **珊瑚礁生態系統**: 全球50%以上珊瑚已白化或死亡
            - **山地物種**: 溫度升高迫使物種向更高海拔遷移
            - **候鳥模式改變**: 遷徙時間和路線發生變化
            """)
            
            # 物種滅絕風險圖
            categories = ['兩棲類', '珊瑚', '哺乳類', '鳥類', '植物']
            risk_percentage = [41, 33, 26, 14, 22]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(categories, risk_percentage, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#F7DC6F'])
            ax.set_xlabel('面臨滅絕風險的比例 (%)')
            ax.set_title('各類物種面臨滅絕風險的比例')
            # 在條形圖上添加數值標籤
            for i, v in enumerate(risk_percentage):
                ax.text(v + 1, i, f'{v}%', va='center')
            st.pyplot(fig)
            plt.close(fig)
        
        # 太空維度觀測
        with st.expander("🛰️ 太空視角下的氣候變遷", expanded=False):
            st.write("""
            **衛星監測氣候變化**
            
            太空科技為我們提供了全球尺度的氣候變化觀測能力:
            
            - **溫度監測**: 衛星紅外線感測器監測全球地表溫度變化
            - **冰層監測**: 測量南北極冰蓋厚度和面積變化
            - **海平面監測**: 雷達高度計精確測量海平面變化
            - **大氣成分**: 監測溫室氣體濃度分布
            - **植被變化**: 追踪森林覆蓋和荒漠化進程
            
            **重要衛星任務**
            
            - **哥白尼計劃**: 歐洲太空總署的氣候監測計劃
            - **Landsat系列**: 美國NASA的地球觀測衛星
            - **GRACE**: 測量地球重力場變化，監測冰蓋融化
            - **OCO-2**: 專門監測大氣二氧化碳濃度
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("""
                **衛星觀測的優勢**:
                - 全球覆蓋，無地理限制
                - 長期連續監測
                - 提供客觀科學數據
                - 早期預警極端事件
                """)
            
            with col2:
                st.success("""
                **數據應用**:
                - 氣候模型驗證與改進
                - 災害預警與應對
                - 政策制定科學依據
                - 公眾教育與意識提升
                """)
        
        # 為什麼要關注氣候變遷 - 深入分析
        st.markdown("---")
        st.subheader("🤔 為什麼我們必須關注氣候變遷？")
        
        reasons = [
            {
                "title": "🌾 糧食安全威脅",
                "content": "極端天氣影響農業生產，全球糧食供應不穩定，價格波動加劇飢餓問題。"
            },
            {
                "title": "💧 水資源危機",
                "content": "冰川消退影響河流流量，乾旱地區擴大，全球數十億人面臨水資源短缺。"
            },
            {
                "title": "🏥 公共衛生風險",
                "content": "熱浪導致死亡增加，病媒傳播疾病範圍擴大，空氣污染加劇呼吸道疾病。"
            },
            {
                "title": "💸 經濟損失",
                "content": "極端天氣造成基礎設施損壞，保險損失增加，生產力下降影響經濟增長。"
            },
            {
                "title": "⚖️ 社會不平等加劇",
                "content": "貧困社區和發展中國家最易受氣候影響，氣候難民問題日益嚴重。"
            },
            {
                "title": "🌿 生態系統崩潰",
                "content": "生物多樣性喪失影響生態服務功能，如授粉、水淨化和氣候調節。"
            }
        ]
        
        # 顯示原因卡片
        cols = st.columns(2)
        for i, reason in enumerate(reasons):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="energy-card">
                    <h4 style="color: #00e676;">{reason['title']}</h4>
                    <p>{reason['content']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 行動呼籲
        st.markdown("---")
        st.markdown("""
        <div class="energy-card" style="text-align: center;">
            <h3 style="color: #00e676;">🌱 我們可以採取行動！</h3>
            <p>雖然氣候變遷是嚴峻挑戰，但通過集體行動，我們仍然可以減緩其影響並適應變化。</p>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 1rem;">
                <div class="energy-tag">減少碳足跡</div>
                <div class="energy-tag">支持再生能源</div>
                <div class="energy-tag">保護森林</div>
                <div class="energy-tag">永續消費</div>
                <div class="energy-tag">氣候教育</div>
                <div class="energy-tag">政策參與</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 發電模擬
    with tab3:
        st.markdown('<h1 class="energy-header">⚡ 發電組合模擬器</h1>', unsafe_allow_html=True)
        
        with st.expander("ℹ️ 為什麼要關注發電結構？", expanded=False):
            st.write("""
            **為何重要：**
            電力部門是全球碳排放的主要來源之一，佔比約25%。不同的發電方式對環境、經濟和社會有截然不同的影響。
            
            **目標：**
            透過調整發電結構，我們可以：
            - 🎯 減少溫室氣體排放，減緩氣候變遷
            - 🎯 改善空氣品質，保障公眾健康
            - 🎯 提高能源自主性，增強國家安全
            - 🎯 創造綠色就業機會，推動經濟轉型
            
            **調整反應：**
            增加再生能源比例會降低碳排放，但可能需要投資電網升級和儲能系統；
            減少化石燃料會改善空氣品質，但可能影響能源穩定性和電價。
            """)
        
        # 初始化狀態
        if 'energy_ratios' not in st.session_state:
            st.session_state.energy_ratios = {
                'coal': 40.0,
                'gas': 20.0, 
                'nuclear': 10.0,
                'hydro': 8.0,
                'solar': 12.0,
                'wind': 10.0
            }
        
        if 'simulate_clicked' not in st.session_state:
            st.session_state.simulate_clicked = False
        
        # 改進的發電比例調整 - 使用表單來防止即時反應
        st.subheader("發電比例調整")
        st.info("💡 調整能源比例，然後點擊「開始模擬」按鈕查看結果，如超出或低於100%會進行自動平衡。")
        
        # 使用表單來防止即時反應
        with st.form("energy_ratio_form"):
            # 創建6個滑桿
            cols = st.columns(3)
            energy_types = ['coal', 'gas', 'nuclear', 'hydro', 'solar', 'wind']
            energy_labels = ['燃煤發電', '燃氣發電', '核能發電', '水力發電', '太陽能發電', '風力發電']
            
            # 使用臨時變量存儲滑桿值
            temp_ratios = st.session_state.energy_ratios.copy()
            
            for i, (energy_type, label) in enumerate(zip(energy_types, energy_labels)):
                with cols[i % 3]:
                    temp_ratios[energy_type] = st.slider(
                        f"{label} (%)", 
                        0.0, 100.0, temp_ratios[energy_type], 0.1,
                        key=f"slider_{energy_type}"
                    )
            
            # 開始模擬按鈕
            submitted = st.form_submit_button("🚀 開始模擬", use_container_width=True)
            
            if submitted:
                st.session_state.simulate_clicked = True
                
                # 計算總和
                total = sum(temp_ratios.values())
                
                # 如果總和不等於100%，則按比例調整
                if abs(total - 100.0) > 0.1:
                    scale = 100.0 / total
                    for energy_type in energy_types:
                        temp_ratios[energy_type] = round(temp_ratios[energy_type] * scale, 1)
                
                # 更新session_state
                st.session_state.energy_ratios = temp_ratios
                st.rerun()
        
        # 重置按鈕
        if st.button("🔄 重置比例", use_container_width=True):
            st.session_state.energy_ratios = {
                'coal': 40.0,
                'gas': 20.0, 
                'nuclear': 10.0,
                'hydro': 8.0,
                'solar': 12.0,
                'wind': 10.0
            }
            st.session_state.simulate_clicked = False
            st.rerun()
        
        # 只有點擊了模擬按鈕才顯示結果
        if st.session_state.simulate_clicked:
            coal = st.session_state.energy_ratios['coal']
            gas = st.session_state.energy_ratios['gas']
            nuclear = st.session_state.energy_ratios['nuclear']
            hydro = st.session_state.energy_ratios['hydro']
            solar = st.session_state.energy_ratios['solar']
            wind = st.session_state.energy_ratios['wind']
            
            # 顯示當前比例
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**燃煤發電:** {coal}%")
                st.write(f"**燃氣發電:** {gas}%")
            with col2:
                st.write(f"**核能發電:** {nuclear}%")
                st.write(f"**水力發電:** {hydro}%")
            with col3:
                st.write(f"**風力發電:** {wind}%")
                st.write(f"**太陽能發電:** {solar}%")
            
            total_percent = sum([coal, gas, nuclear, hydro, solar, wind])
            st.success(f"發電比例總和: {total_percent:.1f}%")
            
            # 更精確的碳排放係數（單位：kgCO₂/kWh）
            emission_factors = {
                'coal': 0.95,    # 燃煤
                'gas': 0.45,     # 燃氣
                'nuclear': 0.05, # 核能
                'hydro': 0.01,   # 水力
                'solar': 0.02,   # 太陽能
                'wind': 0.01     # 風力
            }

            # 計算碳排放
            emissions = sum(st.session_state.energy_ratios[energy_type] * emission_factors[energy_type] for energy_type in energy_types) / 100
            
            annual_emissions = emissions * 8760  # 每年8760小時
            trees_needed = annual_emissions / 0.022  # 每棵樹每年吸收約22kg CO2
            
            # 顯示結果
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("發電結構")
                fig, ax = plt.subplots(figsize=(6, 6))
                sources = ['燃煤', '燃氣', '核能', '水力', '太陽能', '風力']
                sizes = [coal, gas, nuclear, hydro, solar, wind]
                colors = ['#666666', '#FF9999', '#66B2FF', '#0066CC', '#FFCC00', '#99CCFF']
                ax.pie(sizes, labels=sources, colors=colors, autopct='%1.1f%%')
                st.pyplot(fig)
                plt.close(fig)
                    
            with col2:
                st.subheader("環境影響")
                
                # 碳排放強度評估標準
                if emissions < 0.1:
                    emission_status = "✅ 極低碳"
                    emission_color = "green"
                elif emissions < 0.3:
                    emission_status = "✅ 低碳"
                    emission_color = "green"
                elif emissions < 0.6:
                    emission_status = "⚠️ 中等"
                    emission_color = "orange"
                else:
                    emission_status = "❌ 高碳"
                    emission_color = "red"
                    
                st.metric("碳排放強度", f"{emissions:.2f} kgCO₂/kWh", delta=emission_status, delta_color="off")
                st.caption(f"評估標準: <0.1(極低碳), 0.1-0.3(低碳), 0.3-0.6(中等), >0.6(高碳)", unsafe_allow_html=True)
                
                # 年碳排放量評估標準
                if annual_emissions < 100000:
                    annual_status = "✅ 優秀"
                    annual_color = "green"
                elif annual_emissions < 200000:
                    annual_status = "✅ 良好"
                    annual_color = "green"
                elif annual_emissions < 400000:
                    annual_status = "⚠️ 需改善"
                    annual_color = "orange"
                else:
                    annual_status = "❌ 危險"
                    annual_color = "red"
                    
                st.metric("預計年碳排放", f"{annual_emissions:,.0f} 吨", delta=annual_status, delta_color="off")
                st.caption(f"評估標準: <100k(優秀), 100k-200k(良好), 200k-400k(需改善), >400k(危險)", unsafe_allow_html=True)
                
                # 植樹需求評估標準
                if trees_needed < 5000000:
                    tree_status = "✅ 可行"
                    tree_color = "green"
                elif trees_needed < 10000000:
                    tree_status = "⚠️ 挑戰"
                    tree_color = "orange"
                else:
                    tree_status = "❌ 困難"
                    tree_color = "red"
                    
                st.metric("相當於植樹", f"{trees_needed:,.0f} 棵", delta=tree_status, delta_color="off")
                st.caption(f"評估標準: <5M(可行), 5M-10M(挑戰), >10M(困難)", unsafe_allow_html=True)
                
                # 植樹碳吸收量
                carbon_absorption = trees_needed * 0.022
                absorption_diff = carbon_absorption - annual_emissions
                
                if absorption_diff > 10000:
                    absorption_status = f"✅ 吸收 {abs(absorption_diff):,.0f} 吨"
                    absorption_color = "green"
                elif absorption_diff > 0:
                    absorption_status = f"✅ 平衡"
                    absorption_color = "green"
                else:
                    absorption_status = f"❌ 不足 {abs(absorption_diff):,.0f} 吨"
                    absorption_color = "red"
                    
                st.metric("植樹碳吸收量", f"{carbon_absorption:,.0f} 吨/年", delta=absorption_status, delta_color="off")
                st.caption("植樹碳吸收量與年碳排放量的比較", unsafe_allow_html=True)
                
            
            # 發電技術詳細說明
            st.markdown("---")
            st.subheader("🔧 發電技術詳細說明")
            
            tech_option = st.selectbox(
                "選擇發電技術了解更多",
                ["燃煤發電", "燃氣發電", "核能發電", "水力發電", '太陽能發電', "風力發電"],
                index=4
            )
            
            tech_info = {
                "燃煤發電": {
                    "優點": ["技術成熟", "成本相對較低", "供應穩定"],
                    "缺點": ["高碳排放", "空氣污染", "礦業環境影響", "資源有限"],
                    "碳排放": "800-1000 gCO₂/kWh",
                    "備註": "逐漸被淘汰的傳統基載電力"
                },
                "燃氣發電": {
                    "優點": ["啟動快速", "碳排放較煤低", "可配合再生能源調度"],
                    "缺點": ["仍會排放碳", "價格波動大", "依賴進口"],
                    "碳排放": "400-500 gCO₂/kWh", 
                    "備註": "轉型期的過渡性能源"
                },
                "核能發電": {
                    "優點": ["零碳排放", "能源密度高", "供應穩定", "基載電力"],
                    "缺點": ["核廢料處理", "安全疑慮", "建造成本高", "公眾接受度"],
                    "碳排放": "5-15 gCO₂/kWh",
                    "備註": "爭議性但低碳的基載電力選項"
                },
                "水力發電": {
                    "優點": ["可再生", "零碳排放", "調度性佳", "技術成熟"],
                    "缺點": ["生態影響", "地質限制", "淹沒區域", "氣候依賴"],
                    "碳排放": "10-30 gCO₂/kWh",
                    "備註": "重要的再生能源基載"
                },
                "太陽能發電": {
                    "優點": ["完全可再生", "零碳排放", "分散式應用", "成本快速下降"],
                    "缺點": ["間歇性發電", "需要土地", "受天氣影響", "儲能需求"],
                    "碳排放": "20-50 gCO₂/kWh",
                    "備註": "成長最快的再生能源"
                },
                "風力發電": {
                    "優點": ["完全可再生", "零碳排放", "成本競爭力", "技術成熟"],
                    "缺點": ["間歇性發電", "視覺景觀影響", "噪音問題", "鳥類影響"],
                    "碳排放": "10-20 gCO₂/kWh", 
                    "備註": "重要的再生能源來源"
                }
            }
            
            selected = tech_info[tech_option]
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**✅ 優點:**")
                for advantage in selected["優點"]:
                    st.write(f"- {advantage}")
                
                st.write(f"**📊 碳排放強度:** {selected['碳排放']}")
            
            with col2:
                st.write("**❌ 缺點:**")
                for disadvantage in selected["缺點"]:
                    st.write(f"- {disadvantage}")
                
                st.write(f"**💡 備註:** {selected['備註']}")
        else:
            st.info("請調整能源比例，然後點擊「開始模擬」按鈕查看結果")

    # 碳足跡計算
    with tab4:
        st.markdown('<h1 class="energy-header">👣 個人碳足跡計算器</h1>', unsafe_allow_html=True)
        
        with st.expander("ℹ️ 為什麼要計算碳足跡？", expanded=False):
            st.write("""
            **為何重要：**
            個人日常選擇佔全球碳排放的60-70%。了解自己的碳足跡是採取氣候行動的第一步。
            
            **目標：**
            - 🎯 提高對個人行為環境影響的認識
            - 🎯 識別減排機會，制定個人氣候行動計劃
            - 🎯 培養永續生活習慣，帶動社會改變
            
            **調整反應：**
            減少開車、節約用電、選擇植物性飲食等改變，能顯著降低個人碳足跡，
            同時節省開支並改善健康狀況。
            """)
        
        # 添加快速設定按鈕
        st.markdown("---")
        st.subheader("🚀 快速生活模式設定")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏙️ 都市上班族", use_container_width=True):
                st.session_state.car_km = 150
                st.session_state.bus_km = 30
                st.session_state.train_km = 20
                st.session_state.electricity = 350
                st.session_state.gas_usage = 25
                st.session_state.meat_meals = 10
                st.session_state.local_food = "一些"
                st.rerun()
        with col2:
            if st.button("🌿 環保生活家", use_container_width=True):
                st.session_state.car_km = 30
                st.session_state.bus_km = 50
                st.session_state.train_km = 40
                st.session_state.electricity = 200
                st.session_state.gas_usage = 15
                st.session_state.meat_meals = 3
                st.session_state.local_food = "大部分"
                st.rerun()
        with col3:
            if st.button("🎓 學生族群", use_container_width=True):
                st.session_state.car_km = 20
                st.session_state.bus_km = 40
                st.session_state.train_km = 30
                st.session_state.electricity = 150
                st.session_state.gas_usage = 10
                st.session_state.meat_meals = 7
                st.session_state.local_food = "一半"
                st.rerun()
        
        # 初始化session_state
        if 'car_km' not in st.session_state:
            st.session_state.car_km = 100
        if 'bus_km' not in st.session_state:
            st.session_state.bus_km = 50
        if 'train_km' not in st.session_state:
            st.session_state.train_km = 30
        if 'electricity' not in st.session_state:
            st.session_state.electricity = 300
        if 'gas_usage' not in st.session_state:
            st.session_state.gas_usage = 20
        if 'meat_meals' not in st.session_state:
            st.session_state.meat_meals = 7
        if 'local_food' not in st.session_state:
            st.session_state.local_food = "一些"
        
        # 使用expander組織輸入項目
        with st.expander("🚗 交通方式", expanded=True):
            st.caption("碳排放係數: 開車 (0.2 kgCO₂/公里) | 公車 (0.08 kgCO₂/公里) | 火車 (0.05 kgCO₂/公里)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                car_km = st.slider("每週開車里程 (公里)", 0, 500, st.session_state.car_km, key="car_slider")
                st.session_state.car_km = car_km
                car_co2 = car_km * 0.2 * 52
                st.caption(f"年碳排放: {car_co2:.0f} kgCO₂")
                
            with col2:
                bus_km = st.slider("每週公車里程 (公里)", 0, 300, st.session_state.bus_km, key="bus_slider")
                st.session_state.bus_km = bus_km
                bus_co2 = bus_km * 0.08 * 52
                st.caption(f"年碳排放: {bus_co2:.0f} kgCO₂")
                
            with col3:
                train_km = st.slider("每週火車里程 (公里)", 0, 200, st.session_state.train_km, key="train_slider")
                st.session_state.train_km = train_km
                train_co2 = train_km * 0.05 * 52
                st.caption(f"年碳排放: {train_co2:.0f} kgCO₂")
        
        with st.expander("🏠 能源使用", expanded=True):
            st.caption("碳排放係數: 用電 (0.5 kgCO₂/度) | 瓦斯 (2.0 kgCO₂/m³)")
            
            col1, col2 = st.columns(2)
            with col1:
                electricity = st.slider("每月用電量 (度)", 0, 1000, st.session_state.electricity, key="elec_slider")
                st.session_state.electricity = electricity
                elec_co2 = electricity * 0.5 * 12
                st.caption(f"年碳排放: {elec_co2:.0f} kgCO₂")
                
            with col2:
                gas_usage = st.slider("每月瓦斯使用 (m³)", 0, 100, st.session_state.gas_usage, key="gas_slider")
                st.session_state.gas_usage = gas_usage
                gas_co2 = gas_usage * 2.0 * 12
                st.caption(f"年碳排放: {gas_co2:.0f} kgCO₂")
        
        with st.expander("🍽️ 飲食習慣", expanded=True):
            st.caption("碳排放係數: 每餐肉食 (5.0 kgCO₂/餐) | 本地食物可減少運輸碳排放")
            
            meat_meals = st.slider("每週肉食餐數", 0, 21, st.session_state.meat_meals, key="meat_slider")
            st.session_state.meat_meals = meat_meals
            
            # 本地食物比例選擇
            local_food = st.select_slider("本地食物比例", 
                                        options=["很少", "一些", "一半", "大部分", "全部"],
                                        value=st.session_state.local_food,
                                        key="local_slider")
            st.session_state.local_food = local_food
            
            # 本地食物加分 (減少10-50%食物碳足跡)
            local_food_factor = {"很少": 1.0, "一些": 0.9, "一半": 0.8, "大部分": 0.7, "全部": 0.5}[local_food]
            
            # 顯示調整前後的對比
            original_food_co2 = meat_meals * 5.0 * 52
            adjusted_food_co2 = original_food_co2 * local_food_factor
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"🍖 原始年碳排放: {original_food_co2:.0f} kgCO₂")
            with col2:
                st.caption(f"🌱 調整後年碳排放: {adjusted_food_co2:.0f} kgCO₂")
                st.caption(f"📍 因選擇本地食物減少: {original_food_co2 - adjusted_food_co2:.0f} kgCO₂")
        
        # 計算總碳足跡
        transport_co2 = (car_km * 0.2 + bus_km * 0.08 + train_km * 0.05) * 52
        energy_co2 = electricity * 0.5 * 12 + gas_usage * 2.0 * 12
        food_co2 = adjusted_food_co2
        
        total_co2 = transport_co2 + energy_co2 + food_co2
        
        # 與台灣平均比較
        taiwan_avg = 10000  # 台灣人均年碳足跡
        difference = total_co2 - taiwan_avg
        percentage = (difference / taiwan_avg) * 100
        
        st.markdown("---")
        st.subheader("📊 您的碳足跡結果")
        
        # 顯示主要結果
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("交通碳排放", f"{transport_co2:.0f} kgCO₂")
        with col2:
            st.metric("能源碳排放", f"{energy_co2:.0f} kgCO₂")
        with col3:
            st.metric("飲食碳排放", f"{food_co2:.0f} kgCO₂")
        
        st.metric("🏁 總年碳足跡", f"{total_co2:.0f} kgCO₂", 
                f"{percentage:+.1f}% 相比台灣平均")
        
        # 碳足跡水平指示器
        st.markdown("---")
        st.subheader("🌍 您的碳足跡水平")
        
        carbon_level = min(total_co2 / 20000, 1.0)  # 假設20000為參考值
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            if total_co2 < 5000:
                st.success("🌿 環保先鋒 - 您的碳足跡很低！")
                st.progress(0.25)
                st.info("您的生活方式對環境非常友好，請繼續保持！")
            elif total_co2 < 8000:
                st.success("✅ 優良表現 - 低於台灣平均")
                st.progress(0.4)
                st.info("您的碳足跡低於平均水平，表現不錯！")
            elif total_co2 < 10000:
                st.info("📊 接近平均 - 還有進步空間")
                st.progress(0.6)
                st.info("接近台灣平均水平，小改變就能帶來大影響")
            elif total_co2 < 15000:
                st.warning("⚠️ 需要改善 - 高於台灣平均")
                st.progress(0.8)
                st.warning("您的碳足跡偏高，建議參考下面的減排建議")
            else:
                st.error("🔴 嚴重超標 - 急需改善")
                st.progress(1.0)
                st.error("碳足跡嚴重超標，請立即採取減排行動")
        
        # 視覺化碳足跡組成（縮小至75%）
        st.markdown("---")
        st.subheader("📈 碳足跡組成分析")
        
        fig, ax = plt.subplots(figsize=(6, 4.5))  # 縮小至75%
        categories = ['交通', '能源', '飲食']
        values = [transport_co2, energy_co2, food_co2]
        colors = ['#FF9999', '#66B2FF', '#99CC00']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8)
        ax.set_ylabel('碳排放 (kgCO₂)', fontsize=10)
        ax.set_title('碳足跡組成分析', fontsize=12)
        
        # 在柱狀圖上顯示數值
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{value:.0f} kg', ha='center', va='bottom', fontsize=9)
        
        ax.tick_params(axis='both', which='major', labelsize=9)
        st.pyplot(fig)
        plt.close(fig)
        
        # 個性化減排建議
        st.markdown("---")
        st.subheader("💡 個性化減排建議")
        
        suggestions = []
        
        # 交通建議
        if car_km > 100:
            reduce_km = car_km - 80
            reduction = reduce_km * 0.2 * 52
            suggestions.append(f"🚗 **減少開車**: 每週減少{reduce_km}公里開車，可年減{reduction:.0f}kg碳排放")
        elif car_km > 0:
            suggestions.append("🚗 **交通現狀**: 開車里程合理，可考慮偶爾使用大眾運輸")
        
        if bus_km + train_km < 50:
            suggestions.append("🚌 **增加大眾運輸**: 多使用公車/火車，減少碳足跡")
        
        # 能源建議
        if electricity > 350:
            reduce_elec = electricity - 300
            reduction = reduce_elec * 0.5 * 12
            suggestions.append(f"💡 **節約用電**: 每月減少{reduce_elec}度用電，可年減{reduction:.0f}kg碳排放")
        
        if gas_usage > 25:
            reduce_gas = gas_usage - 20
            reduction = reduce_gas * 2.0 * 12
            suggestions.append(f"🔥 **節省瓦斯**: 每月減少{reduce_gas}m³瓦斯，可年減{reduction:.0f}kg碳排放")
        
        # 飲食建議
        if meat_meals > 10:
            reduce_meals = meat_meals - 7
            reduction = reduce_meals * 5.0 * 52
            suggestions.append(f"🥦 **減少肉食**: 每週減少{reduce_meals}餐肉食，可年減{reduction:.0f}kg碳排放")
        
        if local_food in ["很少", "一些"]:
            suggestions.append("📍 **選擇本地食物**: 提高本地食物比例，減少運輸碳排放")
        
        # 顯示建議
        if suggestions:
            st.info("根據您的數據，我們建議：")
            for i, suggestion in enumerate(suggestions[:5], 1):  # 最多顯示5條建議
                st.write(f"{i}. {suggestion}")
            
            # 計算潛在減排量
            potential_reduction = min(total_co2 * 0.3, 3000)  # 最多減少30%或3000kg
            st.success(f"💪 實施這些改變，您每年可減少約{potential_reduction:.0f}kg碳排放！")
        else:
            st.success("🎉 您的生活習慣已經很環保了！繼續保持優良的永續生活方式！")
        
        # 添加重置按鈕
        st.markdown("---")
        if st.button("🔄 重置所有數據", use_container_width=True):
            for key in ['car_km', 'bus_km', 'train_km', 'electricity', 'gas_usage', 'meat_meals', 'local_food']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # 碳交易市場模擬
    with tab5:
        st.markdown('<h1 class="energy-header">💰 碳權交易模擬市場</h1>', unsafe_allow_html=True)
        
        # 概念說明區域
        with st.expander("📚 碳交易基礎概念", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **什麼是碳交易？**
                
                碳交易（Carbon Trading）也稱為排放權交易，是一種基於市場的氣候政策工具。
                政府設定碳排放總量上限，然後將排放配額分配或拍賣給企業。企業可以根據自身需求進行配額交易。
                
                **核心機制**:
                - **總量管制與交易** (Cap-and-Trade)：政府設定排放上限，配額總量有限
                - **碳定價**：為碳排放設定價格，創造減排經濟誘因
                - **市場效率**：讓減排成本最低的企業先減排，實現成本效益最大化
                
                **為什麼重要？**
                - 🌍 最經濟有效的減排方式
                - 💰 創造綠色經濟新機會
                - ⚖️ 公平分配減排責任
                - 🔬 激發技術創新
                """)
            
            with col2:
                # 碳交易流程圖示 - 使用文字描述替代圖片
                st.markdown("""
                **📋 碳交易流程**
                
                1. **總量設定**：政府設定碳排放上限
                2. **配額分配**：分配給企業排放額度
                3. **市場交易**：企業買賣多餘配額
                4. **履約清繳**：年底結算排放量
                5. **懲罰機制**：超排企業受罰
                
                **🎯 交易目的**
                - 降低社會總減排成本
                - 激勵綠色技術創新
                - 實現氣候目標
                """)
        
        # 全球碳市場現狀
        st.markdown("---")
        st.subheader("🌍 全球碳市場現狀")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("全球碳市場規模", "3,000億美元", "+15%", delta_color="normal")
            st.caption("2024年交易總額")
        with col2:
            st.metric("歐盟碳價", "€85/吨", "+€12", delta_color="normal")
            st.caption("EU ETS主力合約")
        with col3:
            st.metric("中國碳價", "¥72/吨", "+¥8", delta_color="normal")
            st.caption("全國碳市場")
        with col4:
            st.metric("覆蓋全球排放", "23%", "+3%", delta_color="normal")
            st.caption("碳市場覆蓋比例")
        
        # 碳價格走勢圖
        st.markdown("---")
        st.subheader("📈 碳價格走勢分析")
        
        # 模擬碳價格數據
        months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        carbon_prices = [45, 47, 49, 52, 55, 58, 62, 65, 68, 72, 75, 78]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(months, carbon_prices, marker='o', linewidth=2, color='#00e676', markersize=6)
        ax.fill_between(months, carbon_prices, alpha=0.3, color='#00e676')
        ax.set_xlabel('月份')
        ax.set_ylabel('碳價格 ($/吨)')
        ax.set_title('2024年碳價格走勢')
        ax.grid(True, alpha=0.3)
        
        # 添加趨勢線
        z = np.polyfit(range(len(months)), carbon_prices, 1)
        p = np.poly1d(z)
        ax.plot(months, p(range(len(months))), "--", color='#00c6ff', alpha=0.7, label='趨勢線')
        ax.legend()
        
        st.pyplot(fig)
        plt.close(fig)
        
        # 交易模擬器
        st.markdown("---")
        st.subheader("🎮 碳交易模擬器")
        
        # 初始化遊戲狀態 - 簡化為只有碳權交易
        if 'carbon_game' not in st.session_state:
            st.session_state.carbon_game = {
                'cash': 100000,  # 初始資金
                'credits': 0,    # 碳權持有量
                'portfolio_value': 100000,
                'transactions': [],
                'current_price': 45.60,
                'total_invested': 0  # 總投資金額
            }
        
        # 市場資訊面板
        st.markdown("#### 📊 當前市場狀況")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("當前碳價", f"${st.session_state.carbon_game['current_price']:.2f}/吨")
        with col2:
            st.metric("可用資金", f"${st.session_state.carbon_game['cash']:,.2f}")
        with col3:
            st.metric("碳權持有", f"{st.session_state.carbon_game['credits']} 吨")
        with col4:
            total_value = st.session_state.carbon_game['cash'] + st.session_state.carbon_game['credits'] * st.session_state.carbon_game['current_price']
            st.metric("總資產", f"${total_value:,.2f}")
        
        # 交易操作面板
        st.markdown("#### 💼 交易操作")
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            trade_amount = st.slider("交易數量 (吨)", 1, 1000, 100)
            max_affordable = int(st.session_state.carbon_game['cash'] / st.session_state.carbon_game['current_price'])
            st.caption(f"最大可買入: {max_affordable} 吨")
        
        with col2:
            if st.button("💰 買入碳權", use_container_width=True):
                cost = trade_amount * st.session_state.carbon_game['current_price']
                if st.session_state.carbon_game['cash'] >= cost:
                    st.session_state.carbon_game['cash'] -= cost
                    st.session_state.carbon_game['credits'] += trade_amount
                    st.session_state.carbon_game['total_invested'] += cost
                    st.session_state.carbon_game['transactions'].append({
                        'type': '買入',
                        'amount': trade_amount,
                        'price': st.session_state.carbon_game['current_price'],
                        'cost': cost,
                        'time': datetime.now().strftime("%H:%M:%S")
                    })
                    st.success(f"✅ 成功買入 {trade_amount} 吨碳權! 花費: ${cost:,.2f}")
                else:
                    st.error("❌ 資金不足!")
        
        with col3:
            if st.button("💸 賣出碳權", use_container_width=True):
                if st.session_state.carbon_game['credits'] >= trade_amount:
                    revenue = trade_amount * st.session_state.carbon_game['current_price']
                    st.session_state.carbon_game['cash'] += revenue
                    st.session_state.carbon_game['credits'] -= trade_amount
                    st.session_state.carbon_game['transactions'].append({
                        'type': '賣出',
                        'amount': trade_amount,
                        'price': st.session_state.carbon_game['current_price'],
                        'revenue': revenue,
                        'time': datetime.now().strftime("%H:%M:%S")
                    })
                    st.success(f"✅ 成功賣出 {trade_amount} 吨碳權! 收入: ${revenue:,.2f}")
                else:
                    st.error("❌ 碳權不足!")
        
        with col4:
            if st.button("🔄 清空持倉", use_container_width=True):
                if st.session_state.carbon_game['credits'] > 0:
                    revenue = st.session_state.carbon_game['credits'] * st.session_state.carbon_game['current_price']
                    st.session_state.carbon_game['cash'] += revenue
                    st.session_state.carbon_game['transactions'].append({
                        'type': '清倉',
                        'amount': st.session_state.carbon_game['credits'],
                        'price': st.session_state.carbon_game['current_price'],
                        'revenue': revenue,
                        'time': datetime.now().strftime("%H:%M:%S")
                    })
                    st.session_state.carbon_game['credits'] = 0
                    st.success(f"✅ 清倉完成! 收入: ${revenue:,.2f}")
                else:
                    st.warning("⚠️ 沒有持倉可清空")
        
        # 市場事件模擬
        st.markdown("---")
        st.subheader("🌪️ 市場事件模擬")
        
        st.info("點擊下方按鈕模擬市場事件對碳價格的影響")
        
        event_col1, event_col2, event_col3, event_col4 = st.columns(4)
        
        with event_col1:
            if st.button("📜 政策利好", use_container_width=True):
                # 氣候政策加強，碳價上漲
                increase = random.uniform(5, 15)
                old_price = st.session_state.carbon_game['current_price']
                st.session_state.carbon_game['current_price'] += increase
                st.success(f"🇺🇳 國際氣候協議達成，碳價從 ${old_price:.2f} 上漲至 ${st.session_state.carbon_game['current_price']:.2f}")
        
        with event_col2:
            if st.button("🌋 經濟波動", use_container_width=True):
                # 經濟因素影響
                change = random.uniform(-10, 10)
                old_price = st.session_state.carbon_game['current_price']
                st.session_state.carbon_game['current_price'] += change
                if change >= 0:
                    st.success(f"📈 經濟復甦，碳價從 ${old_price:.2f} 上漲至 ${st.session_state.carbon_game['current_price']:.2f}")
                else:
                    st.warning(f"📉 經濟放緩，碳價從 ${old_price:.2f} 下跌至 ${st.session_state.carbon_game['current_price']:.2f}")
        
        with event_col3:
            if st.button("⚡ 技術突破", use_container_width=True):
                # 減排技術突破，碳價可能下跌
                change = random.uniform(-8, 5)
                old_price = st.session_state.carbon_game['current_price']
                st.session_state.carbon_game['current_price'] += change
                if change >= 0:
                    st.info(f"🔬 技術成本上升，碳價從 ${old_price:.2f} 上漲至 ${st.session_state.carbon_game['current_price']:.2f}")
                else:
                    st.info(f"💡 減排技術突破，碳價從 ${old_price:.2f} 下跌至 ${st.session_state.carbon_game['current_price']:.2f}")
        
        with event_col4:
            if st.button("🌊 極端天氣", use_container_width=True):
                # 極端天氣事件，碳價波動
                change = random.uniform(-12, 18)
                old_price = st.session_state.carbon_game['current_price']
                st.session_state.carbon_game['current_price'] += change
                if change >= 0:
                    st.warning(f"🌀 極端天氣增加排放，碳價從 ${old_price:.2f} 上漲至 ${st.session_state.carbon_game['current_price']:.2f}")
                else:
                    st.success(f"🌤️ 氣候改善，碳價從 ${old_price:.2f} 下跌至 ${st.session_state.carbon_game['current_price']:.2f}")
        
        # 投資組合分析
        st.markdown("---")
        st.subheader("📊 投資組合分析")
        
        # 計算投資組合價值
        portfolio_value = (st.session_state.carbon_game['cash'] + 
                        st.session_state.carbon_game['credits'] * st.session_state.carbon_game['current_price'])
        profit_loss = portfolio_value - 100000
        profit_loss_percent = (profit_loss / 100000) * 100
        
        # 顯示投資組合指標
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("投資組合價值", f"${portfolio_value:,.2f}", 
                    f"{profit_loss:+.2f}", delta_color="normal" if profit_loss >= 0 else "inverse")
        with col2:
            st.metric("投資回報率", f"{profit_loss_percent:+.1f}%")
        with col3:
            credits_value = st.session_state.carbon_game['credits'] * st.session_state.carbon_game['current_price']
            allocation_cash = (st.session_state.carbon_game['cash'] / portfolio_value * 100) if portfolio_value > 0 else 0
            allocation_credits = 100 - allocation_cash
            st.metric("資產配置", f"現金{allocation_cash:.1f}% / 碳權{allocation_credits:.1f}%")
        with col4:
            if st.session_state.carbon_game['total_invested'] > 0:
                avg_cost = st.session_state.carbon_game['total_invested'] / st.session_state.carbon_game['credits'] if st.session_state.carbon_game['credits'] > 0 else 0
                current_price = st.session_state.carbon_game['current_price']
                price_diff = current_price - avg_cost
                st.metric("平均成本", f"${avg_cost:.2f}/吨", f"{price_diff:+.2f} vs 現價")
        
        # 資產配置圖 - 只有當有持倉時顯示
        if portfolio_value > 0:
            fig, ax = plt.subplots(figsize=(6, 6))
            sizes = [st.session_state.carbon_game['cash'], credits_value]
            labels = ['現金', '碳權資產']
            colors = ['#66B2FF', '#00e676']
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('投資組合配置')
            st.pyplot(fig)
            plt.close(fig)
            
            # 持倉詳情
            st.markdown("#### 📦 持倉詳情")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**碳權數量**: {st.session_state.carbon_game['credits']} 吨")
            with col2:
                st.info(f"**當前價值**: ${credits_value:,.2f}")
            with col3:
                if st.session_state.carbon_game['credits'] > 0:
                    unrealized_pnl = credits_value - st.session_state.carbon_game['total_invested']
                    pnl_color = "green" if unrealized_pnl >= 0 else "red"
                    st.info(f"**未實現損益**: <span style='color:{pnl_color}'>${unrealized_pnl:,.2f}</span>", unsafe_allow_html=True)
        
        # 交易歷史
        if st.session_state.carbon_game['transactions']:
            st.markdown("#### 📝 交易歷史")
            
            # 創建交易歷史表格
            transactions_data = []
            for i, tx in enumerate(reversed(st.session_state.carbon_game['transactions'][-10:])):  # 顯示最近10筆
                if tx['type'] == '買入':
                    amount_str = f"-{tx['amount']} 吨"
                    value_str = f"-${tx['cost']:,.2f}"
                else:
                    amount_str = f"+{tx['amount']} 吨"
                    value_str = f"+${tx.get('revenue', 0):,.2f}"
                
                transactions_data.append({
                    '時間': tx['time'],
                    '類型': tx['type'],
                    '數量': amount_str,
                    '價格': f"${tx['price']:.2f}",
                    '金額': value_str
                })
            
            transactions_df = pd.DataFrame(transactions_data)
            st.dataframe(transactions_df, use_container_width=True, hide_index=True)
        
        # 投資策略建議
        st.markdown("---")
        st.subheader("💡 即時投資建議")
        
        current_price = st.session_state.carbon_game['current_price']
        credits_held = st.session_state.carbon_game['credits']
        cash_available = st.session_state.carbon_game['cash']
        
        advice_col1, advice_col2 = st.columns(2)
        
        with advice_col1:
            if credits_held == 0:
                st.success("**建議**: 考慮買入碳權開始投資")
            elif current_price > 60:
                st.warning("**建議**: 碳價偏高，考慮減持或觀望")
            elif current_price < 40:
                st.success("**建議**: 碳價偏低，可能是買入機會")
            else:
                st.info("**建議**: 市場平穩，持有觀望")
        
        with advice_col2:
            if credits_held > 0:
                avg_cost = st.session_state.carbon_game['total_invested'] / credits_held
                if current_price > avg_cost * 1.2:
                    st.success("**持倉表現**: 盈利良好 👍")
                elif current_price < avg_cost * 0.9:
                    st.warning("**持倉表現**: 暫時虧損 📉")
                else:
                    st.info("**持倉表現**: 盈虧平衡 ⚖️")
        
        # 教育內容：碳交易策略
        st.markdown("---")
        st.subheader("🎯 碳交易策略指南")
        
        strategy_tabs = st.tabs(["基礎知識", "交易策略", "風險管理"])
        
        with strategy_tabs[0]:
            st.markdown("""
            **碳交易基礎知識**
            
            🔍 **什麼是碳權？**
            - 1碳權 = 排放1吨二氧化碳的權利
            - 由政府分配或拍賣給企業
            - 可在市場上自由交易
            
            💰 **碳價影響因素**：
            - 氣候政策嚴格程度
            - 經濟活動水平
            - 清潔技術發展
            - 極端天氣事件
            
            📊 **市場參與者**：
            - 排放企業（買方）
            - 減排企業（賣方）
            - 金融機構（投資者）
            - 政府機構（監管者）
            """)
        
        with strategy_tabs[1]:
            st.markdown("""
            **碳交易策略**
            
            1. **趨勢交易**：
            - 跟隨政策利好上漲趨勢
            - 在經濟復甦期買入持有
            
            2. **均值回歸**：
            - 碳價過高時賣出
            - 碳價過低時買入
            
            3. **事件驅動**：
            - 關注氣候大會結果
            - 跟踪極端天氣影響
            """)
        
        with strategy_tabs[2]:
            st.markdown("""
            **風險管理原則**
            
            ⚠️ **價格波動風險**：
            - 碳價受政策影響大
            - 設置止損點控制損失
            
            ⚠️ **流動性風險**：
            - 新興市場流動性有限
            - 避免過度集中投資
            
            ⚠️ **政策風險**：
            - 關注國際氣候談判
            - 分散投資不同市場
            """)
        
        # 重置按鈕
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 重置模擬遊戲", use_container_width=True):
                st.session_state.carbon_game = {
                    'cash': 100000,
                    'credits': 0,
                    'portfolio_value': 100000,
                    'transactions': [],
                    'current_price': 45.60,
                    'total_invested': 0
                }
                st.success("✅ 模擬遊戲已重置！")
                st.rerun()
        
        # 頁面底部說明
        st.markdown("---")
        st.info("""
        **💡 教學提示**: 
        - 碳交易是複雜的金融工具，實際交易需要專業知識
        - 本模擬器簡化了市場機制，用於教育目的
        - 碳價受多種因素影響：政策變化、經濟狀況、技術發展等
        - 成功的碳交易需要持續學習和風險管理
        """)

    # 能源問答遊戲 - 完全重新設計
    with tab6:
        st.markdown('<h1 class="energy-header">🎓 能源知識挑戰賽</h1>', unsafe_allow_html=True)
        
        # 定義擴充的題庫 - 分為三個難度級別
        questions = {
            "小學士": [
                {
                    "question": "太陽能板在陰天能發電嗎？",
                    "options": ["完全不能", "效率降低但仍可發電", "比晴天更有效率"],
                    "answer": 1,
                    "explanation": "太陽能板在陰天仍可發電，但效率會降低約50-80%，具體取決於雲層厚度。",
                    "category": "可再生能源"
                },
                {
                    "question": "以下哪種能源的碳排放最高？",
                    "options": ["風力發電", "燃煤發電", "核能發電"],
                    "answer": 1,
                    "explanation": "燃煤發電的碳排放最高，每度電約排放800-1000克二氧化碳，遠高於風力(10-20克)和核能(5-15克)。",
                    "category": "碳排放"
                },
                {
                    "question": "什麼是碳足跡？",
                    "options": ["腳印的碳含量", "個人活動產生的碳排放", "碳元素的痕跡"],
                    "answer": 1,
                    "explanation": "碳足跡是指個人、組織或產品在生產、使用和處理過程中直接或間接產生的溫室氣體排放總量。",
                    "category": "基礎概念"
                },
                {
                    "question": "植樹造林有助於應對氣候變遷的主要原因是？",
                    "options": ["樹木提供陰影降溫", "樹木吸收二氧化碳", "樹木釋放氧氣"],
                    "answer": 1,
                    "explanation": "樹木通過光合作用吸收大氣中的二氧化碳，將其轉化為有機物儲存在體內，從而減少大氣中的溫室氣體。",
                    "category": "氣候行動"
                },
                {
                    "question": "哪種交通方式的碳排放最低？",
                    "options": ["開私家車", "騎自行車", "坐飛機"],
                    "answer": 1,
                    "explanation": "騎自行車是零碳排放的交通方式，對環境最友好。",
                    "category": "交通運輸"
                }
            ],
            "小碩士": [
                {
                    "question": "什麼是『能源回報期』(Energy Payback Time)?",
                    "options": ["能源投資回收時間", "電費繳納期限", "能源政策執行期"],
                    "answer": 0,
                    "explanation": "能源回報期是指能源設備(如太陽能板)生產過程中消耗的能源，需要多長時間才能通過發電回收。",
                    "category": "能源技術"
                },
                {
                    "question": "台灣的能源轉型目標「2025非核家園」不包括以下哪項?",
                    "options": ["核能發電歸零", "再生能源達20%", "燃煤發電歸零"],
                    "answer": 2,
                    "explanation": "2025非核家園目標是核能發電歸零、再生能源達20%，但燃煤發電仍會保留一定比例。",
                    "category": "能源政策"
                },
                {
                    "question": "碳交易的主要目的是什麼？",
                    "options": ["賺取利潤", "減少溫室氣體排放", "促進國際貿易"],
                    "answer": 1,
                    "explanation": "碳交易的主要目的是通過市場機制，以最低社會成本減少溫室氣體排放。",
                    "category": "碳市場"
                },
                {
                    "question": "什麼是『綠色溢價』(Green Premium)?",
                    "options": ["環保產品價格更高", "綠色股票溢價", "環保稅收"],
                    "answer": 0,
                    "explanation": "綠色溢價指的是清潔能源技術相比傳統化石燃料技術的額外成本。",
                    "category": "經濟學"
                },
                {
                    "question": "哪種再生能源被認為是最具潛力的基載電力？",
                    "options": ["太陽能", "風能", "地熱能"],
                    "answer": 2,
                    "explanation": "地熱能不受天氣影響，可以提供穩定的基載電力，被認為是極具潛力的再生能源。",
                    "category": "能源技術"
                }
            ],
            "小博士": [
                {
                    "question": "什麼是『綠氫』(Green Hydrogen)?",
                    "options": ["綠色的氫氣", "可再生能源製氫", "天然氣製氫"],
                    "answer": 1,
                    "explanation": "綠氫是指使用可再生能源(如太陽能、風能)通過電解水製取的氫氣，整個過程幾乎不產生碳排放。",
                    "category": "前沿技術"
                },
                {
                    "question": "IPCC報告中提到的『碳預算』(Carbon Budget)概念是指什麼？",
                    "options": ["碳交易預算", "可排放的二氧化碳總量", "碳稅收預算"],
                    "answer": 1,
                    "explanation": "碳預算是指為了將全球升溫控制在特定目標內，人類還可以排放的二氧化碳總量。",
                    "category": "氣候科學"
                },
                {
                    "question": "什麼是『氣候臨界點』(Climate Tipping Points)?",
                    "options": ["氣候談判關鍵時刻", "不可逆的氣候系統變化", "極端天氣事件"],
                    "answer": 1,
                    "explanation": "氣候臨界點是指全球氣候系統中一些關鍵的閾值，一旦跨越就會引發不可逆的、自我強化的變化。",
                    "category": "氣候科學"
                },
                {
                    "question": "『藍碳』(Blue Carbon)指的是什麼？",
                    "options": ["藍色能源", "海洋生態系統碳匯", "低碳技術"],
                    "answer": 1,
                    "explanation": "藍碳是指由海洋和沿海生態系統(如紅樹林、海草床、鹽沼)捕獲和儲存的碳。",
                    "category": "生態系統"
                },
                {
                    "question": "什麼是『碳捕捉與封存』(CCS)技術？",
                    "options": ["碳交易系統", "從大氣中移除二氧化碳並儲存", "碳排放監測"],
                    "answer": 1,
                    "explanation": "碳捕捉與封存技術是指從工業過程或大氣中捕捉二氧化碳，並將其安全地儲存於地質構造中的技術。",
                    "category": "減排技術"
                }
            ]
        }
        
        # 初始化session_state
        if 'quiz_level' not in st.session_state:
            st.session_state.quiz_level = "小學士"
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'quiz_finished' not in st.session_state:
            st.session_state.quiz_finished = False
        if 'selected_answer' not in st.session_state:
            st.session_state.selected_answer = None
        if 'answer_submitted' not in st.session_state:
            st.session_state.answer_submitted = False
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        if 'leaderboard' not in st.session_state:
            st.session_state.leaderboard = []
        
        # 難度選擇和開始界面
        if not st.session_state.quiz_started:
            st.markdown("""
            <div class="energy-card" style="text-align: center;">
                <h3 style="color: #00e676;">🎯 挑戰你的能源知識</h3>
                <p>選擇難度級別，測試你對能源與環境議題的了解程度！</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="energy-card" style="text-align: center; cursor: pointer;" onclick="st.session_state.quiz_level='小學士'">
                    <h4>🎓 小學士</h4>
                    <p>適合初學者<br>基礎能源知識</p>
                    <div class="quiz-level-badge quiz-beginner">5題選擇題</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("選擇小學士", key="beginner_btn", use_container_width=True):
                    st.session_state.quiz_level = "小學士"
                    st.session_state.quiz_started = True
                    st.rerun()
            
            with col2:
                st.markdown("""
                <div class="energy-card" style="text-align: center;">
                    <h4>🎓 小碩士</h4>
                    <p>適合有一定基礎<br>進階能源概念</p>
                    <div class="quiz-level-badge quiz-intermediate">5題選擇題</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("選擇小碩士", key="intermediate_btn", use_container_width=True):
                    st.session_state.quiz_level = "小碩士"
                    st.session_state.quiz_started = True
                    st.rerun()
            
            with col3:
                st.markdown("""
                <div class="energy-card" style="text-align: center;">
                    <h4>🎓 小博士</h4>
                    <p>適合專家級<br>深度能源議題</p>
                    <div class="quiz-level-badge quiz-advanced">5題選擇題</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("選擇小博士", key="advanced_btn", use_container_width=True):
                    st.session_state.quiz_level = "小博士"
                    st.session_state.quiz_started = True
                    st.rerun()
            
            # 顯示排行榜
            if st.session_state.leaderboard:
                st.markdown("---")
                st.subheader("🏆 知識挑戰排行榜")
                
                # 按分數排序
                sorted_leaderboard = sorted(st.session_state.leaderboard, 
                                        key=lambda x: x['score'], reverse=True)
                
                for i, entry in enumerate(sorted_leaderboard[:5]):  # 顯示前5名
                    emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
                    st.markdown(f"""
                    <div class="leaderboard-item">
                        <span>{emoji} {entry['name']}</span>
                        <span>{entry['score']}/5 - {entry['level']}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 問答進行中
        elif st.session_state.quiz_started and not st.session_state.quiz_finished:
            current_level_questions = questions[st.session_state.quiz_level]
            current_q = current_level_questions[st.session_state.current_question]
            
            # 顯示進度
            progress = (st.session_state.current_question) / len(current_level_questions)
            st.progress(progress)
            
            # 顯示當前問題
            st.markdown(f"""
            <div class="question-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="quiz-level-badge quiz-{['beginner', 'intermediate', 'advanced'][['小學士', '小碩士', '小博士'].index(st.session_state.quiz_level)]}">
                        {st.session_state.quiz_level}
                    </span>
                    <span>題目 {st.session_state.current_question + 1}/{len(current_level_questions)}</span>
                </div>
                <h3>{current_q['question']}</h3>
                <p><small>分類: {current_q['category']}</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            # 顯示選項
            if not st.session_state.answer_submitted:
                selected_option = st.radio(
                    "請選擇答案:",
                    current_q['options'],
                    key=f"q_{st.session_state.current_question}"
                )
                st.session_state.selected_answer = current_q['options'].index(selected_option)
                
                if st.button("提交答案", type="primary", use_container_width=True):
                    st.session_state.answer_submitted = True
                    # 檢查答案
                    if st.session_state.selected_answer == current_q['answer']:
                        st.session_state.quiz_score += 1
                        st.balloons()
                    st.rerun()
            else:
                # 顯示答案結果
                for i, option in enumerate(current_q['options']):
                    if i == current_q['answer']:
                        st.markdown(f"""
                        <div class="option-card correct">
                            ✅ {option} <strong>(正確答案)</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    elif i == st.session_state.selected_answer:
                        st.markdown(f"""
                        <div class="option-card incorrect">
                            ❌ {option} <strong>(你的選擇)</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="option-card">
                            ○ {option}
                        </div>
                        """, unsafe_allow_html=True)
                
                # 顯示解釋
                st.info(f"**💡 解釋:** {current_q['explanation']}")
                
                # 下一題或結束按鈕
                if st.session_state.current_question < len(current_level_questions) - 1:
                    if st.button("下一題 →", use_container_width=True):
                        st.session_state.current_question += 1
                        st.session_state.answer_submitted = False
                        st.session_state.selected_answer = None
                        st.rerun()
                else:
                    if st.button("查看成績", type="primary", use_container_width=True):
                        st.session_state.quiz_finished = True
                        st.rerun()
        
        # 測驗結束，顯示成績
        elif st.session_state.quiz_finished:
            st.balloons()
            
            st.markdown(f"""
            <div class="energy-card" style="text-align: center;">
                <div class="score-display">{st.session_state.quiz_score}/5</div>
                <h3>🎉 {st.session_state.quiz_level}挑戰完成！</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 根據得分給出評價
            score_percentage = (st.session_state.quiz_score / 5) * 100
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if score_percentage >= 80:
                    st.success("""
                    ### 🌟 優秀表現！
                    你對能源與環境議題有深入的了解，
                    是真正的環保專家！
                    """)
                elif score_percentage >= 60:
                    st.warning("""
                    ### 👍 良好表現！
                    你對能源知識有一定了解，
                    但還有進步空間。
                    """)
                else:
                    st.error("""
                    ### 💪 繼續努力！
                    能源知識需要持續學習，
                    下次挑戰會更好！
                    """)
            
            # 記錄成績
            st.markdown("---")
            st.subheader("📝 記錄你的成績")
            
            player_name = st.text_input("輸入你的名字:", max_chars=15, placeholder="匿名勇士")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏆 記錄成績", use_container_width=True) and player_name:
                    st.session_state.leaderboard.append({
                        'name': player_name,
                        'score': st.session_state.quiz_score,
                        'level': st.session_state.quiz_level,
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("成績已記錄到排行榜！")
            
            # 返回難度選擇介面的按鈕
            st.markdown("---")
            st.subheader("🔄 返回選單")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🏠 返回難度選擇介面", use_container_width=True, type="primary"):
                    # 重置所有測驗狀態
                    st.session_state.quiz_started = False
                    st.session_state.quiz_finished = False
                    st.session_state.quiz_score = 0
                    st.session_state.current_question = 0
                    st.session_state.answer_submitted = False
                    st.session_state.selected_answer = None
                    st.rerun()
            
            # 顯示答案解析
            st.markdown("---")
            st.subheader("📚 題目解析")
            
            current_level_questions = questions[st.session_state.quiz_level]
            for i, q in enumerate(current_level_questions):
                with st.expander(f"第{i+1}題: {q['question']}", expanded=False):
                    st.write(f"**正確答案:** {q['options'][q['answer']]}")
                    st.write(f"**解釋:** {q['explanation']}")
                    st.write(f"**分類:** {q['category']}")

    # 能源未來預測
    with tab7:
        st.markdown('<h1 class="energy-header">📊 能源未來預測</h1>', unsafe_allow_html=True)
        
        with st.expander("ℹ️ 為什麼要做能源預測？", expanded=False):
            st.write("""
            **為何重要：**
            能源轉型是一個長達數十年的過程，需要前瞻性的規劃和投資決策。預測幫助我們了解不同選擇的長期後果。
            
            **目標：**
            - 🎯 評估不同政策情境的影響
            - 🎯 指引基礎設施投資方向
            - 🎯 設定現實可行的減排目標
            - 🎯 準備應對氣候變遷的衝擊
            
            **預測價值：**
            雖然預測不可能100%準確，但能幫助我們比較不同選擇的相對優劣，
            避免鎖定在高碳的發展路徑上。
            """)
        
        # 預測參數調整區域
        col1, col2 = st.columns([2, 1])
        
        with col1:
            year = st.slider("選擇預測年份", 2025, 2050, 2035)
        
        with col2:
            st.metric("預測時間跨度", f"{year-2025}年", f"{year}年目標")
        
        # 詳細參數調整區域
        with st.expander("🔧 詳細參數調整", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                tech_advancement = st.slider("技術進步速度", 0.5, 2.0, 1.0, 0.1,
                                        help="1.0為正常速度，>1.0表示加速發展")
                policy_strength = st.slider("政策力度", 0.5, 2.0, 1.0, 0.1,
                                        help="氣候政策實施強度")
                
            with col2:
                investment_growth = st.slider("投資增長率%", -5.0, 20.0, 8.0, 0.5,
                                            help="年度綠色投資增長率")
                carbon_price = st.slider("碳價格($/噸)", 20, 200, 60, 5,
                                    help="碳交易價格影響減排動力")
        
        # 主要情境選擇
        scenario = st.selectbox("選擇主要分析情境", 
                            ["現行政策", "巴黎協定目標", "淨零排放", "技術突破", "經濟衰退", "積極轉型"],
                            index=3)
        
        # 計算預測結果的函數
        def calculate_detailed_forecast(year, scenario, tech_factor=1.0, policy_factor=1.0, carbon_price=60):
            """詳細的能源預測計算"""
            years_from_now = year - 2025
            
            # 基礎增長率
            base_renewable_growth = 1.5
            base_emissions_reduction = 2.0
            
            # 情境加成
            scenario_bonus = {
                "現行政策": 0,
                "巴黎協定目標": 10,
                "淨零排放": 20,
                "技術突破": 25,
                "經濟衰退": -5,
                "積極轉型": 15
            }.get(scenario, 0)
            
            # 碳價格影響因子（碳價越高，減排動力越強）
            carbon_factor = 1.0 + (carbon_price - 60) / 200
            
            # 應用調整因子
            adjusted_growth = base_renewable_growth * tech_factor * policy_factor
            adjusted_reduction = base_emissions_reduction * policy_factor * carbon_factor
            
            # 計算結果
            renewable_share = 20 + years_from_now * adjusted_growth + scenario_bonus
            emissions_reduction = years_from_now * adjusted_reduction
            
            # 相關計算
            energy_cost = max(65 - (years_from_now * 0.8 * tech_factor), 20)  # 能源成本下降
            jobs_created = 10000 + years_from_now * 500 * tech_factor  # 就業機會
            
            return {
                "renewable_share": min(renewable_share, 95),
                "emissions_reduction": min(emissions_reduction, 90),
                "energy_cost": energy_cost,
                "jobs_created": jobs_created,
                "carbon_price_impact": carbon_factor
            }
        
        def calculate_investment_returns(year, scenario, investment_growth):
            """計算投資回報"""
            base_roi = 6.0  # 基礎回報率
            growth_bonus = investment_growth * 0.1  # 投資增長帶來的回報提升
            
            scenario_multiplier = {
                "現行政策": 1.0,
                "巴黎協定目標": 1.2,
                "淨零排放": 1.3,
                "技術突破": 1.4,
                "經濟衰退": 0.8,
                "積極轉型": 1.25
            }.get(scenario, 1.0)
            
            roi = (base_roi + growth_bonus) * scenario_multiplier
            risk_adjusted_roi = roi * 0.85  # 風險調整
            payback_years = max(10 - (roi - 6), 4)  # 回報率越高，回收期越短
            
            return {
                "roi": roi,
                "risk_adjusted_roi": risk_adjusted_roi,
                "payback_years": payback_years,
                "roi_premium": roi - 6.2  # 相比傳統能源的溢價
            }
        
        def calculate_environmental_benefits(year, scenario):
            """計算環境效益"""
            years_from_now = year - 2025
            
            # 基礎效益
            base_co2_reduction = 1000000  # 每年減少100萬噸
            base_lives_saved = 5000      # 每年避免5000人死亡
            
            scenario_multiplier = {
                "現行政策": 1.0,
                "巴黎協定目標": 1.5,
                "淨零排放": 2.0,
                "技術突破": 1.8,
                "經濟衰退": 0.7,
                "積極轉型": 1.6
            }.get(scenario, 1.0)
            
            total_co2 = base_co2_reduction * years_from_now * scenario_multiplier
            total_lives = base_lives_saved * years_from_now * scenario_multiplier
            water_saved = total_co2 * 0.5  # 每噸碳減排節約0.5噸水
            health_benefits = total_lives * 0.1  # 每避免1人死亡產生10萬美元健康效益
            
            return {
                "co2_reduction": total_co2,
                "lives_saved": total_lives,
                "water_saved": water_saved,
                "health_benefits": health_benefits
            }
        
        # 顯示主要情境結果
        main_results = calculate_detailed_forecast(year, scenario, tech_advancement, policy_strength, carbon_price)
        
        st.subheader(f"🎯 {scenario}情境預測結果 ({year}年)")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("再生能源占比", f"{main_results['renewable_share']:.1f}%")
        with col2:
            st.metric("碳排放減少", f"{main_results['emissions_reduction']:.1f}%")
        with col3:
            st.metric("能源成本", f"${main_results['energy_cost']:.2f}/MWh")
        with col4:
            st.metric("綠色就業", f"{main_results['jobs_created']:,.0f}個")
        
        # 多情境比較分析
        st.markdown("---")
        st.subheader("📊 多情境比較分析")
        
        # 選擇要比較的情境
        comparison_scenarios = st.multiselect(
            "選擇比較情境（可多選）",
            ["現行政策", "巴黎協定目標", "淨零排放", "技術突破", "經濟衰退", "積極轉型"],
            default=["現行政策", "技術突破", "淨零排放"]
        )
        
        # 確定要顯示的情境列表
        scenarios_to_display = comparison_scenarios if comparison_scenarios else ["現行政策", "技術突破"]
        
        # 显示比较表格
        comparison_data = []
        for scen in scenarios_to_display:
            results = calculate_detailed_forecast(year, scen, tech_advancement, policy_strength, carbon_price)
            comparison_data.append({
                "情境": scen,
                "再生能源占比": f"{results['renewable_share']:.1f}%",
                "碳排減少": f"{results['emissions_reduction']:.1f}%",
                "能源成本": f"${results['energy_cost']:.2f}/MWh",
                "就業機會": f"{results['jobs_created']:,.0f}個"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # 如果没有选择任何情境，显示提示
        if not comparison_scenarios:
            st.info("ℹ️ 目前顯示預設情境比較，您可以上方選擇其他情境組合")
        
        # 情境比較圖表 - 只有选择了多个情境时才显示图表
        if len(scenarios_to_display) > 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            renewable_shares = [calculate_detailed_forecast(year, s, tech_advancement, policy_strength)['renewable_share'] for s in scenarios_to_display]
            
            bars = ax.bar(scenarios_to_display, renewable_shares, color=['#00c6ff', '#00e676', '#ff9800', '#e91e63', '#9c27b0', '#ffeb3b'])
            ax.set_ylabel('再生能源占比 (%)')
            ax.set_title(f'{year}年各情境再生能源占比比較')
            ax.set_ylim(0, 100)
            
            # 在柱子上添加數值
            for bar, value in zip(bars, renewable_shares):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{value:.1f}%', ha='center', va='bottom')
            
            st.pyplot(fig)
            plt.close(fig)
        
        # 敏感性分析
        st.markdown("---")
        st.subheader("⚠️ 敏感性分析")
        
        sensitivity_option = st.selectbox(
            "分析關鍵不確定因素",
            ["無", "技術突破", "政策不確定", "投資波動", "極端天氣", "國際合作"],
            index=0
        )
        
        def show_sensitivity_analysis(year, scenario, factor):
            """顯示敏感性分析"""
            sensitivities = {
                "技術突破": {
                    "樂觀": "太陽能成本再降60%，儲能技術突破，再生能源占比可達80%",
                    "悲觀": "技術進展緩慢，關鍵材料短缺，占比可能僅達40%",
                    "影響": "±20% 再生能源占比，±15% 減排速度",
                    "建議": "加強研發投資，推動技術創新"
                },
                "政策不確定": {
                    "樂觀": "全球氣候合作加強，政策連續穩定，減排加速",
                    "悲觀": "各國政策倒退，補貼取消，進展遲緩", 
                    "影響": "±15% 減排速度，±10% 投資信心",
                    "建議": "建立長期政策框架，確保投資可預測性"
                },
                "投資波動": {
                    "樂觀": "綠色投資持續增長，資金充足，項目快速推進",
                    "悲觀": "經濟下行投資萎縮，資金鏈斷裂，項目停滯",
                    "影響": "±25% 項目完成率，±30% 就業創造",
                    "建議": "多元化資金來源，降低投資風險"
                },
                "極端天氣": {
                    "樂觀": "氣候韌性增強，災害影響有限，恢復快速",
                    "悲觀": "極端事件頻發，設施損毀，重建成本高昂",
                    "影響": "±15% 能源供應穩定性，±20% 保險成本",
                    "建議": "加強基礎設施韌性，建立災害應對機制"
                },
                "國際合作": {
                    "樂觀": "全球協同減排，技術共享，成本大幅下降",
                    "悲觀": "貿易壁壘，技術保護主義，發展受阻",
                    "影響": "±30% 技術擴散速度，±25% 規模效應",
                    "建議": "加強國際合作，推動技術和知識共享"
                }
            }
            
            if factor in sensitivities:
                info = sensitivities[factor]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"✅ **樂觀情境**: {info['樂觀']}")
                    st.metric("影響程度", info['影響'].split(' ')[0], "正向影響")
                    
                with col2:
                    st.error(f"❌ **悲觀情境**: {info['悲觀']}")
                    st.metric("風險等級", "中高" if factor in ["政策不確定", "投資波動"] else "中", "需關注")
                
                st.info(f"💡 **應對建議**: {info['建議']}")
                
                # 顯示具體數值影響
                base_results = calculate_detailed_forecast(year, scenario)
                optimistic_factor = 1.2 if factor == "技術突破" else 1.15
                pessimistic_factor = 0.8 if factor == "技術突破" else 0.85
                
                optimistic_share = min(base_results['renewable_share'] * optimistic_factor, 95)
                pessimistic_share = max(base_results['renewable_share'] * pessimistic_factor, 20)
                
                st.write(f"**具體數值影響**: 再生能源占比可能在 {pessimistic_share:.1f}% 到 {optimistic_share:.1f}% 之間波動")
        
        if sensitivity_option != "無":
            show_sensitivity_analysis(year, scenario, sensitivity_option)
        
        # 投資回報分析
        st.markdown("---")
        st.subheader("💰 投資回報分析")
        
        investment_results = calculate_investment_returns(year, scenario, investment_growth)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("平均投資回報率", f"{investment_results['roi']:.1f}%", 
                    f"較傳統能源高{investment_results['roi_premium']:.1f}%")
        with col2:
            st.metric("風險調整回報", f"{investment_results['risk_adjusted_roi']:.1f}%", 
                    "波動率較低")
        with col3:
            st.metric("投資回收期", f"{investment_results['payback_years']:.1f}年", 
                    "技術進步縮短周期")
        
        # 投資趨勢圖
        investment_years = list(range(2025, min(2051, year+1), 5))
        if year >= 2030:  # 只有當預測年份足夠遠時顯示趨勢
            roi_trend = [calculate_investment_returns(y, scenario, investment_growth)['roi'] for y in investment_years]
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(investment_years, roi_trend, marker='o', linewidth=2, color='#00e676')
            ax.set_xlabel('年份')
            ax.set_ylabel('投資回報率 (%)')
            ax.set_title('投資回報率趨勢預測')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 15)
            
            st.pyplot(fig)
            plt.close(fig)
        
        # 環境效益量化
        st.markdown("---")
        st.subheader("🌿 環境效益量化")
        
        env_benefits = calculate_environmental_benefits(year, scenario)
        
        benefits_col1, benefits_col2, benefits_col3, benefits_col4 = st.columns(4)
        with benefits_col1:
            st.metric("碳排減少", f"{env_benefits['co2_reduction']:,.0f} 噸")
        with benefits_col2:
            st.metric("空氣污染避免死亡", f"{env_benefits['lives_saved']:,.0f} 人")
        with benefits_col3:
            st.metric("水資源節約", f"{env_benefits['water_saved']:,.0f} 百萬噸")
        with benefits_col4:
            st.metric("健康效益", f"${env_benefits['health_benefits']:,.0f} 百萬")
        
        # 環境效益解釋
        with st.expander("💡 環境效益計算說明", expanded=False):
            st.write("""
            **碳排放減少**: 基於能源結構轉型減少的二氧化碳排放量
            **避免死亡人數**: 因改善空氣質量而避免的過早死亡人數
            **水資源節約**: 再生能源相比化石燃料節約的用水量
            **健康效益**: 醫療費用減少和生產力提升的貨幣化價值
            
            *數據來源: WHO空氣質量指南、IEA水-能源關聯報告、世界銀行健康經濟學研究*
            """)
        
        # 政策建議
        st.markdown("---")
        st.subheader("💡 政策建議")
        
        def generate_policy_recommendations(scenario, renewable_share):
            """根據情境生成政策建議"""
            recommendations = []
            
            if renewable_share < 40:
                recommendations.append({
                    "title": "加速再生能源部署",
                    "priority": "高",
                    "timeline": "短期(1-3年)",
                    "measures": "簡化審批流程、提供稅收優惠、建立綠色電網",
                    "impact": "快速提升再生能源占比"
                })
            elif renewable_share < 60:
                recommendations.append({
                    "title": "加強電網現代化",
                    "priority": "中高",
                    "timeline": "中期(3-5年)", 
                    "measures": "投資智能電網、發展儲能技術、提升電網韌性",
                    "impact": "確保高比例再生能源的穩定供應"
                })
            else:
                recommendations.append({
                    "title": "深化系統整合",
                    "priority": "中",
                    "timeline": "長期(5-10年)",
                    "measures": "推動跨部門耦合、發展氫能經濟、建立區域能源市場",
                    "impact": "實現深度脫碳和能源系統優化"
                })
            
            if scenario in ["經濟衰退", "現行政策"]:
                recommendations.append({
                    "title": "加強政策支持",
                    "priority": "高",
                    "timeline": "立即",
                    "measures": "增加公共投資、提供就業培訓、確保公正轉型",
                    "impact": "克服經濟障礙，加速轉型"
                })
            
            # 通用建議
            recommendations.append({
                "title": "加強研發與創新",
                "priority": "中",
                "timeline": "持續進行",
                "measures": "支持清潔技術研發、產學研合作、國際技術轉讓",
                "impact": "降低技術成本，提升競爭力"
            })
            
            return recommendations
        
        recommendations = generate_policy_recommendations(scenario, main_results['renewable_share'])
        
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"建議 {i}: {rec['title']} ({rec['priority']}優先級)", expanded=i==1):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**時間框架**: {rec['timeline']}")
                    st.write(f"**具體措施**: {rec['measures']}")
                with col2:
                    st.write(f"**預期效果**: {rec['impact']}")
        
        # 重置按鈕
        st.markdown("---")
        if st.button("🔄 重置所有參數", use_container_width=True):
            # 重置所有參數到默認值
            st.session_state.forecast_year = 2035
            st.session_state.forecast_scenario = "技術突破"
            st.session_state.tech_advancement = 1.0
            st.session_state.policy_strength = 1.0
            st.session_state.investment_growth = 8.0
            st.session_state.carbon_price = 60
            st.rerun()

    # 投資概略
    with tab8:
        st.markdown('<h1 class="energy-header">📈 能源科技投資趨勢分析</h1>', unsafe_allow_html=True)
        
        # 即時市場動態
        st.markdown("---")
        st.subheader("🚨 最新市場動態")
        
        # 創建新聞卡片
        news_items = [
            {
                "title": "電動車銷量突破預期",
                "content": "2024年全球電動車銷量同比增長35%，中國市場佔比達60%",
                "impact": "🔴 高影響",
                "sector": "🚗 電動車",
                "date": "2024-12-15"
            },
            {
                "title": "儲能成本大幅下降",
                "content": "鋰電池儲能成本較2020年下降40%，推動可再生能源普及",
                "impact": "🟡 中影響", 
                "sector": "🔋 儲能技術",
                "date": "2024-12-10"
            },
            {
                "title": "氫能基礎設施投資激增",
                "content": "歐盟宣布投入200億歐元建設氫能基礎設施",
                "impact": "🟢 低影響",
                "sector": "💧 氫能源",
                "date": "2024-12-05"
            }
        ]
        
        for news in news_items:
            with st.expander(f"{news['sector']} | {news['title']} | {news['date']} | {news['impact']}", expanded=False):
                st.write(news['content'])
                if news['sector'] == "🚗 電動車":
                    st.info("**投資機會**: 充電基礎設施、電池技術、智能電網整合")
                elif news['sector'] == "🔋 儲能技術":
                    st.info("**投資機會**: 鋰電池創新、壓縮空氣儲能、飛輪儲能")
                else:
                    st.info("**投資機會**: 電解槽技術、氫燃料電池、運輸基礎設施")
        
        with st.expander("ℹ️ 關於能源科技投資", expanded=False):
            st.write("""
            **為何重要：**
            能源科技正在經歷前所未有的創新浪潮，了解前沿技術和投資趨勢對於把握未來機會至關重要。
            
            **新興領域：**
            - 🚗 **電動車與智能交通**: 電池技術、充電網絡、車網互動(V2G)
            - 🏠 **能源管理系統**: 智能電網、家庭能源管理、需求響應
            - 🔋 **先進儲能**: 固態電池、流電池、重力儲能
            - 💧 **綠色氫能**: 電解槽技術、燃料電池、氫能基礎設施
            - 🤖 **數字化能源**: AI優化、區塊鏈、物聯網監控
            
            **投資邏輯：**
            這些領域不僅符合碳中和趨勢，更具備技術突破和市場爆發的雙重潛力。
            """)
        
        # 投資熱點分析
        st.markdown("---")
        st.subheader("🔥 當前投資熱點")
        
        # 熱點技術卡片
        tech_spotlights = [
            {
                "name": "電動車智能充電",
                "description": "V2G技術讓電動車成為移動儲能單元",
                "growth": "45%",
                "maturity": "成長期",
                "investment_scale": "中大型",
                "risk_level": "中等"
            },
            {
                "name": "家庭能源管理系統", 
                "description": "AI優化家庭用電，降低電費20-30%",
                "growth": "60%",
                "maturity": "早期",
                "investment_scale": "中小型",
                "risk_level": "中高"
            },
            {
                "name": "固態電池技術",
                "description": "能量密度提升50%，安全性大幅改善",
                "growth": "35%",
                "maturity": "研發期",
                "investment_scale": "大型",
                "risk_level": "高"
            },
            {
                "name": "綠色氫能電解槽",
                "description": "可再生能源製氫成本持續下降",
                "growth": "55%", 
                "maturity": "示範期",
                "risk_level": "高"
            }
        ]
        
        cols = st.columns(2)
        for i, tech in enumerate(tech_spotlights):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="energy-card">
                    <h4>{tech['name']}</h4>
                    <p>{tech['description']}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                        <span class="energy-tag">📈 {tech['growth']}增長</span>
                        <span class="energy-tag">⚡ {tech['maturity']}</span>
                        <span class="energy-tag">🔄 {tech['risk_level']}風險</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 市場規模預測
        st.markdown("---")
        st.subheader("📊 細分市場規模預測（2030年）")
        
        market_data = {
            '電動車及基礎設施': 8500,
            '能源管理系統': 3200, 
            '先進儲能技術': 2800,
            '綠色氫能': 1800,
            '數字化能源': 2500,
            '碳捕捉技術': 1200
        }
        
        fig, ax = plt.subplots(figsize=(12, 6))
        markets = list(market_data.keys())
        values = list(market_data.values())
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#F7DC6F', '#BB8FCE']
        
        bars = ax.barh(markets, values, color=colors, alpha=0.8)
        ax.set_xlabel('市場規模（億美元）')
        ax.set_title('2030年能源科技細分市場規模預測')
        ax.grid(True, alpha=0.3, axis='x')
        
        # 添加數值標籤
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 100, bar.get_y() + bar.get_height()/2, 
                    f'{value}億', ha='left', va='center')
        
        st.pyplot(fig)
        plt.close(fig)
        
        # 技術成熟度分析
        st.markdown("---")
        st.subheader("🔬 技術成熟度與投資時機")
        
        maturity_data = {
            '技術領域': ['鋰離子電池', '太陽能光伏', '風力發電', '電動車', '能源管理AI', '固態電池', '綠色氫能', '核融合'],
            '成熟度': [8, 9, 8, 7, 5, 3, 4, 2],  # 1-10分，10為最成熟
            '投資風險': [2, 1, 2, 3, 5, 7, 6, 9],  # 1-10分，10為最高風險
            '增長潛力': [6, 7, 6, 8, 9, 9, 8, 10]  # 1-10分，10為最高潛力
        }
        
        df_maturity = pd.DataFrame(maturity_data)
        
        # 創建散點圖
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(df_maturity['成熟度'], df_maturity['增長潛力'], 
                            s=df_maturity['投資風險']*50, alpha=0.6,
                            c=df_maturity['投資風險'], cmap='RdYlGn_r')
        
        # 添加標籤
        for i, tech in enumerate(df_maturity['技術領域']):
            ax.annotate(tech, (df_maturity['成熟度'][i], df_maturity['增長潛力'][i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax.set_xlabel('技術成熟度（分數越高越成熟）')
        ax.set_ylabel('增長潛力（分數越高潛力越大）')
        ax.set_title('能源技術投資機會矩陣')
        ax.grid(True, alpha=0.3)
        
        # 添加顏色條
        plt.colorbar(scatter, label='投資風險（分數越高風險越大）')
        
        st.pyplot(fig)
        plt.close(fig)
        
        # 投資案例研究
        st.markdown("---")
        st.subheader("💼 成功投資案例分析")
        
        case_studies = [
            {
                "company": "特斯拉(Tesla)",
                "領域": "電動車/儲能",
                "投資時機": "2010年IPO",
                "回報": "超過100倍",
                "成功因素": "垂直整合、技術領先、品牌效應",
                "啟示": "早期識別技術趨勢並長期持有"
            },
            {
                "company": "Enphase Energy",
                "領域": "太陽能微逆變器", 
                "投資時機": "2012年技術突破期",
                "回報": "超過50倍",
                "成功因素": "專注細分市場、技術創新",
                "啟示": "在專業細分領域建立技術壁壘"
            },
            {
                "company": "QuantumScape",
                "領域": "固態電池",
                "投資時機": "2020年SPAC上市",
                "回報": "波動較大，潛力巨大",
                "成功因素": "突破性技術、巨頭背書",
                "啟示": "前沿技術投資需要風險分散"
            }
        ]
        
        for i, case in enumerate(case_studies):
            with st.expander(f"案例{i+1}: {case['company']} - {case['領域']}", expanded=i==0):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**投資時機**: {case['投資時機']}")
                    st.write(f"**投資回報**: {case['回報']}")
                    st.write(f"**成功因素**: {case['成功因素']}")
                with col2:
                    st.write(f"**關鍵啟示**: {case['啟示']}")
                    # 添加投資建議
                    if case['回報'] == "超過100倍":
                        st.success("**啟發**: 識別顛覆性技術並早期佈局")
                    elif "技術突破" in case['投資時機']:
                        st.info("**啟發**: 關注技術突破的拐點時機")
                    else:
                        st.warning("**啟發**: 前沿技術需要耐心和風險管理")
        
        # 新興技術深度分析
        st.markdown("---")
        st.subheader("🔍 新興技術深度分析")
        
        tech_analysis = st.selectbox(
            "選擇技術深入了解",
            ["電動車智能充電(V2G)", "家庭能源管理系統(HEMS)", "固態電池", "綠色氫能", "AI能源優化"]
        )
        
        if tech_analysis == "電動車智能充電(V2G)":
            st.markdown("""
            **技術原理**: 
            V2G技術讓電動車不僅能充電，還能向電網放電，成為分散式儲能資源。
            
            **市場前景**:
            - 2030年全球V2G市場預計達300億美元
            - 每輛電動車每年可創造1000-2000元收益
            - 有效平衡電網峰谷差，提高再生能源消納
            
            **投資機會**:
            1. **充電設備製造**: 雙向充電樁技術
            2. **平台軟體**: 充電調度優化算法  
            3. **運營服務**: 聚合商模式創造收益
            
            **風險提示**: 電池損耗、標準化、用戶接受度
            """)
            
        elif tech_analysis == "家庭能源管理系統(HEMS)":
            st.markdown("""
            **技術原理**:
            通過AI算法優化家庭用電行為，自動控制家電運行，實現節能省錢。
            
            **市場前景**:
            - 智能家居市場年複合增長率25%
            - 每個家庭年節省電費20-30%
            - 需求響應潛力巨大
            
            **投資機會**:
            1. **硬件設備**: 智能電表、控制器
            2. **軟體平台**: AI算法、用戶界面
            3. **數據服務**: 用電分析、個性化建議
            
            **風險提示**: 數據隱私、技術標準、用戶習慣
            """)
            
        elif tech_analysis == "固態電池":
            st.markdown("""
            **技術突破**:
            用固態電解質替代液態電解質，提升能量密度和安全性。
            
            **市場前景**:
            - 能量密度提升50%以上
            - 充電時間縮短至15分鐘
            - 2030年市場規模預估500億美元
            
            **投資機會**:
            1. **材料研發**: 固態電解質材料
            2. **製造設備**: 新工藝生產線
            3. **專利授權**: 核心技術專利
            
            **風險提示**: 量產難度、成本控制、技術路線
            """)
        
        # 投資策略建議
        st.markdown("---")
        st.subheader("🎯 個性化投資策略建議")
        
        investor_profile = st.selectbox(
            "選擇您的投資者類型",
            ["保守型", "穩健型", "積極型", "激進型"]
        )
        
        strategy_recommendations = {
            "保守型": {
                "配置建議": "70%成熟技術 + 30%成長技術",
                "重點領域": ["太陽能運營", "風電項目", "儲能電站"],
                "風險控制": "重點投資現金流穩定的運營類項目",
                "預期回報": "年化6-8%"
            },
            "穩健型": {
                "配置建議": "50%成熟技術 + 50%成長技術", 
                "重點領域": ["電動車產業鏈", "電池製造", "能源管理軟體"],
                "風險控制": "均衡配置，關注技術領先企業",
                "預期回報": "年化8-12%"
            },
            "積極型": {
                "配置建議": "30%成熟技術 + 70%成長技術",
                "重點領域": ["固態電池", "氫能技術", "AI能源優化"],
                "風險控制": "分散投資，關注技術突破",
                "預期回報": "年化12-20%"
            },
            "激進型": {
                "配置建議": "100%前沿技術",
                "重點領域": ["核融合", "量子儲能", "生物能源"],
                "風險控制": "極高風險，建議專業投資者參與",
                "預期回報": "年化20%+（波動巨大）"
            }
        }
        
        strategy = strategy_recommendations[investor_profile]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**💰 配置建議**: {strategy['配置建議']}")
            st.success(f"**🎯 重點領域**: {', '.join(strategy['重點領域'])}")
        with col2:
            st.warning(f"**⚠️ 風險控制**: {strategy['風險控制']}")
            st.info(f"**📈 預期回報**: {strategy['預期回報']}")
        
        # 投資工具和資源
        st.markdown("---")
        st.subheader("🛠️ 投資工具與資源")
        
        resources = [
            "📊 Bloomberg新能源財經(BNEF) - 行業數據權威",
            "🔬 IEA國際能源署 - 政策與技術報告", 
            "💹 綠色債券指數 - 固定收益投資參考",
            "🌍 MSCI低碳指數 - 股票投資基準",
            "📱 能源科技ETF - 分散投資工具"
        ]
        
        for resource in resources:
            st.write(f"- {resource}")
        
        # 互動問答
        st.markdown("---")
        st.subheader("❓ 能源投資問答")
        
        with st.expander("現在投資能源科技是否為時已晚？"):
            st.write("""
            **絕對不晚！** 能源轉型是持續數十年的長期趨勢，目前仍處於早期階段：
            - 可再生能源僅佔全球發電量30%左右
            - 電動車滲透率不足20%
            - 儲能、氫能等技術仍在快速發展
            
            **最佳投資時機**是現在，因為：
            1. 技術路線逐漸清晰
            2. 政策支持力度加大
            3. 成本持續下降
            4. 市場接受度提高
            """)
        
        with st.expander("如何降低能源科技投資風險？"):
            st.write("""
            **風險管理策略**：
            1. **分散投資**: 不要押注單一技術或公司
            2. **長期視角**: 能源技術需要時間成熟和推廣
            3. **專業諮詢**: 尋求行業專家建議
            4. **定期評估**: 跟蹤技術進展和市場變化
            5. **風險預算**: 設定最大虧損限度
            
            **具體工具**：
            - 能源科技ETF實現自動分散
            - 參與風險投資基金降低單項目風險
            - 使用期權等工具對沖風險
            """)
        
        # 投資趨勢預測
        st.markdown("---")
        st.subheader("🔮 2025年投資趨勢預測")
        
        trend_predictions = [
            "🔋 **固態電池商業化突破** - 多家企業將實現小批量量產",
            "🚗 **電動車價格戰加劇** - 入門級電動車價格降至燃油車水平", 
            "🏠 **家庭儲能普及加速** - 成本下降推動戶用儲能需求",
            "🤖 **AI能源管理成熟** - 智能優化算法大幅提升能效",
            "💧 **綠氫項目規模化** - 兆瓦級電解槽項目陸續投產"
        ]
        
        for prediction in trend_predictions:
            st.write(f"- {prediction}")
        
        # 頁腳聲明
        st.markdown("---")
        st.caption("""
        💡 **免責聲明**: 本頁面內容僅供教育參考，不構成投資建議。能源科技投資風險較高，請根據自身情況謹慎決策。
        📊 **數據來源**: BloombergNEF, IEA, 行業研究報告綜合整理（數據更新至2024年12月）
        """)

    # 頁腳
    st.markdown("---")
    st.caption("🌱 本模擬器僅用於教育目的，數據為簡化估算 | 打造永續未來需要每個人的參與")        
            





















