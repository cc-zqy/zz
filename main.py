"""main.py - 自助式数据分析（数据分析智能体）

Author: 骆昊
Version: 0.1
Date: 2025/6/25
"""
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import streamlit as st
import json
import io
import seaborn as sns
import numpy as np

from utils import dataframe_agent, load_data_file

# 设置页面配置
st.set_page_config(
    page_title="深藏Blue组数据分析智能体",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 创建侧边栏
with st.sidebar:
    st.markdown("### 🎯 导航菜单")
    st.markdown("---")
    st.markdown("#### 📊 数据分析工具")
    st.markdown("- 数据上传与预处理")
    st.markdown("- 智能分析与可视化")
    st.markdown("---")
    st.markdown("#### 🔧 系统设置")
    st.markdown("- 主题与样式")
    st.markdown("- 关于我们")
    st.markdown("\n")
    st.markdown("*Version 1.0.0*")


# 添加科技感CSS样式
st.markdown("""
<style>
/* 主题色彩定义 */
:root {
    --primary-color: #00d4ff;
    --secondary-color: #0066cc;
    --accent-color: #ff6b35;
    --bg-dark: #2a5a8a;
    --bg-light: #3a6a9a;
    --text-light: #ffffff;
    --text-secondary: #e0e9f4;
    --gradient-bg: linear-gradient(135deg, #2a5a8a 0%, #3a6a9a 50%, #4a7aaa 100%);
    --neon-glow: 0 0 20px rgba(0, 212, 255, 0.4);
}

/* 全局背景 */
.stApp {
    background: linear-gradient(135deg, #2a5a8a 0%, #3a6a9a 50%, #4a7aaa 100%);
    color: var(--text-light);
}

/* 全局文字大小 */
.stMarkdown, .stText, .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect, .stFileUploader {
    font-size: 1.6rem !important;
    line-height: 1.8 !important;
    font-weight: 500 !important;
}

/* 文件上传区域样式优化 */
[data-testid="stFileUploader"] {
    background: rgba(58, 106, 154, 0.4);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--primary-color);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25), 0 0 10px rgba(0, 212, 255, 0.3);
    transform: translateY(-2px);
}

/* 文件上传按钮样式 */
[data-testid="stFileUploader"] button {
    background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 1.4rem;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    margin-top: 0.5rem;
}

/* 响应式设计 */
@media screen and (max-width: 1200px) {
    .stMarkdown h1 {
        font-size: 2.6rem !important;
    }
    .stMarkdown h2 {
        font-size: 2.2rem !important;
    }
    .stMarkdown h3 {
        font-size: 1.8rem !important;
    }
    .stMarkdown, .stText, .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect, .stFileUploader {
        font-size: 1.4rem !important;
        line-height: 1.6 !important;
    }
}

@media screen and (max-width: 992px) {
    .stMarkdown h1 {
        font-size: 2.4rem !important;
    }
    .stMarkdown h2 {
        font-size: 2rem !important;
    }
    .stMarkdown h3 {
        font-size: 1.6rem !important;
    }
    .stMarkdown, .stText, .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect, .stFileUploader {
        font-size: 1.2rem !important;
        line-height: 1.5 !important;
    }
    [data-testid="stFileUploader"] button {
        font-size: 1.2rem;
        padding: 0.5rem 1.2rem;
    }
}

@media screen and (max-width: 768px) {
    .stMarkdown h1 {
        font-size: 2.2rem !important;
        margin-bottom: 1.5rem;
    }
    .stMarkdown h2 {
        font-size: 1.8rem !important;
        margin-bottom: 1.2rem;
    }
    .stMarkdown h3 {
        font-size: 1.4rem !important;
        margin-bottom: 1rem;
    }
    .stMarkdown, .stText, .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect, .stFileUploader {
        font-size: 1.1rem !important;
        line-height: 1.4 !important;
    }
    .tech-card {
        padding: 1.2rem;
        margin: 0.8rem 0;
    }
}

/* 标题文字大小 */
.stMarkdown h1 {
    font-size: 3rem !important;
    font-weight: 800;
    margin-bottom: 2rem;
    color: var(--text-light);
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
}

.stMarkdown h2 {
    font-size: 2.4rem !important;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: var(--text-light);
    text-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
}

.stMarkdown h3 {
    font-size: 2rem !important;
    font-weight: 600;
    margin-bottom: 1.2rem;
    color: var(--text-light);
    text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

/* 侧边栏样式优化 */
.css-1d391kg, [data-testid="stSidebar"] {
    background: rgba(58, 106, 154, 0.95);
    border-right: 1px solid rgba(0, 212, 255, 0.3);
    padding: 2rem 1rem;
    width: 25% !important;
    flex: 0 0 25% !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #b8c5d6;
}

[data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
    color: #00d4ff;
    margin-bottom: 1.5rem;
    font-size: 2.2rem;
    font-weight: 600;
    text-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
}

[data-testid="stSidebar"] ul {
    list-style: none;
    padding-left: 1rem;
}

[data-testid="stSidebar"] li {
    margin: 1.2rem 0;
    font-size: 1.8rem;
    transition: all 0.3s ease;
    cursor: pointer;
    color: var(--text-secondary);
}

[data-testid="stSidebar"] li:hover {
    color: #00d4ff;
    text-shadow: 0 0 8px rgba(0, 212, 255, 0.4);
    transform: translateX(5px);
}

/* 主标题样式 */
.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(45deg, #00d4ff, #ff6b35, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 2rem 0;
    text-shadow: var(--neon-glow);
    animation: gradient 3s ease infinite, glow 2s ease-in-out infinite alternate;
    letter-spacing: 2px;
    position: relative;
    display: inline-block;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-title::before, .main-title::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.main-title::before {
    text-shadow: 2px 0 5px rgba(0, 212, 255, 0.4);
    animation: glitch-1 5s infinite linear alternate-reverse;
}

.main-title::after {
    text-shadow: -2px 0 5px rgba(255, 107, 53, 0.4);
    animation: glitch-2 3s infinite linear alternate-reverse;
}

@keyframes glitch-1 {
    0%, 100% { clip-path: inset(80% 0 0 0); }
    20% { clip-path: inset(20% 0 40% 0); }
    40% { clip-path: inset(40% 0 60% 0); }
    60% { clip-path: inset(60% 0 20% 0); }
    80% { clip-path: inset(0 0 80% 0); }
}

@keyframes glitch-2 {
    0%, 100% { clip-path: inset(0 0 70% 0); }
    25% { clip-path: inset(60% 0 10% 0); }
    50% { clip-path: inset(10% 0 50% 0); }
    75% { clip-path: inset(40% 0 30% 0); }
}

@keyframes glow {
    from { filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3)); }
    to { filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)); }
}

/* 卡片容器样式 */
.tech-card {
    background: rgba(58, 106, 154, 0.6);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

/* 卡片内文字样式 */
.tech-card h1, .tech-card h2, .tech-card h3 {
    font-size: 2.4rem;
    color: #00d4ff;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
    font-weight: 600;
}

.tech-card p {
    font-size: 1.8rem;
    line-height: 2;
    color: var(--text-light);
    margin-bottom: 1.2rem;
    font-weight: 500;
}

.tech-card:hover {
    border-color: var(--primary-color);
    box-shadow: 0 12px 40px rgba(0, 212, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.tech-card::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    opacity: 0.7;
}

/* 侧边栏样式 */
.css-1d391kg {
    background: rgba(58, 106, 154, 0.95);
    border-right: 1px solid rgba(0, 212, 255, 0.3);
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 1.6rem;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
    background: linear-gradient(45deg, var(--secondary-color), var(--primary-color));
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: all 0.6s ease;
    z-index: -1;
}

.stButton > button:hover::before {
    left: 100%;
}

/* 指标卡片样式 */
.metric-card {
    background: rgba(58, 106, 154, 0.6);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.metric-card:hover {
    border-color: var(--primary-color);
    box-shadow: var(--neon-glow);
    transform: translateY(-3px);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover::before {
    opacity: 1;
}

/* 数据表格样式 */
.stDataFrame {
    background: rgba(58, 106, 154, 0.8);
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(0, 212, 255, 0.3);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25), 0 0 15px rgba(0, 212, 255, 0.1);
    position: relative;
    transition: all 0.3s ease;
}

.stDataFrame:hover {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 212, 255, 0.15);
    transform: translateY(-2px);
}

/* 表格内容样式优化 */
.stDataFrame [data-testid="stDataFrameResizable"] {
    font-family: 'Roboto Mono', monospace;
    position: relative;
    z-index: 1;
}

.stDataFrame::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, transparent 49.5%, rgba(0, 212, 255, 0.1) 49.5%, rgba(0, 212, 255, 0.1) 50.5%, transparent 50.5%);
    background-size: 10px 10px;
    opacity: 0.3;
    pointer-events: none;
}

/* 表格标题行 */
.stDataFrame [data-testid="stDataFrameResizable"] th {
    background-color: rgba(0, 212, 255, 0.15);
    color: var(--primary-color);
    font-weight: 600;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0, 212, 255, 0.3);
    position: relative;
    transition: all 0.2s ease;
    text-shadow: 0 0 5px rgba(0, 212, 255, 0.3);
    font-size: 1.6rem;
}

.stDataFrame [data-testid="stDataFrameResizable"] th::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.5), transparent);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.stDataFrame [data-testid="stDataFrameResizable"] th:hover {
    background-color: rgba(0, 212, 255, 0.2);
}

.stDataFrame [data-testid="stDataFrameResizable"] th:hover::after {
    transform: scaleX(1);
}

/* 表格数据行 */
.stDataFrame [data-testid="stDataFrameResizable"] td {
    padding: 10px 16px;
    border-bottom: 1px solid rgba(0, 212, 255, 0.1);
    color: var(--text-light);
    transition: all 0.2s ease;
    font-size: 1.6rem;
}

/* 表格行悬停效果 */
.stDataFrame [data-testid="stDataFrameResizable"] tr:hover td {
    background-color: rgba(0, 212, 255, 0.08);
    color: #ffffff;
    text-shadow: 0 0 3px rgba(0, 212, 255, 0.2);
}

/* 输入框样式 */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stMultiselect > div > div > div {
    background: rgba(42, 90, 138, 0.9);
    border: 1px solid rgba(0, 212, 255, 0.5);
    border-radius: 6px;
    color: #ffffff;
    font-size: 1.8rem;
    padding: 10px 15px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1), inset 0 1px 3px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
}

.stTextInput > div > div > input::before,
.stTextArea > div > div > textarea::before,
.stSelectbox > div > div > select::before,
.stMultiselect > div > div > div::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
    transition: all 0.8s ease;
}

/* 输入框焦点样式 */
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus,
.stMultiselect > div > div > div:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3), inset 0 1px 3px rgba(0, 0, 0, 0.1);
    outline: none;
    background: rgba(58, 106, 154, 0.9);
}

.stTextInput > div > div > input:hover,
.stTextArea > div > div > textarea:hover,
.stSelectbox > div > div > select:hover,
.stMultiselect > div > div > div:hover {
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 输入框标签样式 */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stMultiselect label {
    color: #00d4ff;
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
    text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
    position: relative;
    display: inline-block;
}

/* 下拉菜单样式 */
.stSelectbox > div[data-baseweb="select"] > div {
    background: rgba(42, 90, 138, 0.9);
    border: 1px solid rgba(0, 212, 255, 0.5);
    border-radius: 6px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    color: #ffffff;
}

.stSelectbox > div[data-baseweb="select"] > div:hover {
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), 0 0 8px rgba(0, 212, 255, 0.2);
}

.stSelectbox > div[data-baseweb="select"] > div:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

/* 下拉菜单选项样式 */
div[data-baseweb="popover"] {
    background: rgba(42, 90, 138, 0.95) !important;
    border: 1px solid rgba(0, 212, 255, 0.5) !important;
    border-radius: 6px !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), 0 0 15px rgba(0, 212, 255, 0.2) !important;
    backdrop-filter: blur(10px);
}

div[data-baseweb="popover"] ul {
    background: transparent !important;
}

div[data-baseweb="popover"] li {
    color: #ffffff !important;
    transition: all 0.2s ease;
    font-size: 1.6rem !important;
}

div[data-baseweb="popover"] li:hover {
    background: rgba(0, 212, 255, 0.1) !important;
    color: #ffffff !important;
}

div[data-baseweb="popover"] li[aria-selected="true"] {
    background: rgba(0, 212, 255, 0.2) !important;
    color: var(--primary-color) !important;
}

/* 文本区域高度调整 */
.stTextArea > div > div > textarea {
    min-height: 120px;
}

/* 消息样式 */
.stAlert {
    background: rgba(58, 106, 154, 0.8);
    border-radius: 8px;
    border-left: 4px solid var(--primary-color);
    padding: 1rem;
    margin: 0.8rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
    font-size: 1.8rem !important;
}

/* 成功消息样式 */
.stSuccess {
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid var(--primary-color);
    border-radius: 8px;
    color: var(--primary-color);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

/* 信息消息样式 */
.stInfo {
    background: rgba(0, 102, 204, 0.1);
    border: 1px solid var(--secondary-color);
    border-radius: 8px;
    color: var(--secondary-color);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

/* 错误消息样式 */
.stError {
    background: rgba(255, 107, 53, 0.1);
    border: 1px solid var(--accent-color);
    border-radius: 8px;
    color: var(--accent-color);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

/* 消息图标样式 */
.stSuccess svg, .stInfo svg, .stError svg, .stWarning svg {
    margin-right: 10px;
    filter: drop-shadow(0 0 5px currentColor);
}

/* 展开器样式 */
.streamlit-expanderHeader {
    background: rgba(58, 106, 154, 0.6);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 8px;
    color: var(--text-light);
    padding: 0.8rem 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    font-size: 1.8rem !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(58, 106, 154, 0.8);
    border-color: var(--primary-color);
    transform: translateY(-2px);
}

/* 展开器内容样式 */
.streamlit-expanderContent {
    font-size: 1.8rem !important;
    background: rgba(58, 106, 154, 0.4);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 1rem;
    margin-top: -5px;
}

/* 进度条样式 */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    border-radius: 10px;
    height: 8px;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

.stProgress > div > div {
    background-color: rgba(26, 31, 58, 0.4);
    border-radius: 10px;
    height: 8px;
}

/* 滑块样式 */
.stSlider > div > div > div {
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

.stSlider > div > div > div > div {
    background: white;
    border: 2px solid var(--primary-color);
    box-shadow: 0 0 5px rgba(0, 212, 255, 0.8);
    transform: scale(1.2);
}

.stSlider > div > div > div > div:hover {
    transform: scale(1.4);
}

/* 复选框样式 */
.stCheckbox > label {
    color: var(--text-light);
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.stCheckbox > label > div[data-testid="stCheckbox"] {
    transform: scale(1.1);
}

.stCheckbox > label > div[data-testid="stCheckbox"] > svg {
    fill: var(--primary-color);
    filter: drop-shadow(0 0 3px rgba(0, 212, 255, 0.5));
}

/* 科技感装饰元素 */
.tech-decoration {
    position: relative;
    overflow: hidden;
}

.tech-decoration::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
    animation: scan 3s linear infinite;
}

.tech-decoration::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
    animation: scan-reverse 4s linear infinite;
}

@keyframes scan {
    0% { left: -100%; }
    100% { left: 100%; }
}

@keyframes scan-reverse {
    0% { right: -100%; }
    100% { right: 100%; }
}

/* 添加科技感边框效果 */
.tech-border {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
}

.tech-border::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    background: linear-gradient(45deg, var(--primary-color), transparent, var(--accent-color), transparent, var(--primary-color));
    background-size: 400%;
    z-index: -1;
    animation: border-animate 10s linear infinite;
}

@keyframes border-animate {
    0% { background-position: 0 0; }
    50% { background-position: 100% 0; }
    100% { background-position: 0 0; }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
    }
    
    .tech-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
}
</style>
""", unsafe_allow_html=True)


def render_chart(chart_data, style="默认"):
    """渲染图表，支持不同样式"""
    try:
        # 设置图表样式
        if style == "简洁":
            plt.style.use('seaborn-v0_8-whitegrid')
            colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        elif style == "专业":
            plt.style.use('seaborn-v0_8-darkgrid')
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        elif style == "彩色":
            plt.style.use('seaborn-v0_8-bright')
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        else:
            plt.style.use('default')
            colors = plt.cm.Set3.colors
        
        if "bar" in chart_data:
            bar_data = chart_data["bar"]
            fig, ax = plt.subplots(figsize=(12, 7))
            # 兼容两种数据格式：columns/data 和 categories/values
            categories = bar_data.get("columns", bar_data.get("categories", []))
            values = bar_data.get("data", bar_data.get("values", []))
            
            # 确保categories和values是一维数组
            if isinstance(categories[0], list) and len(categories[0]) == 1:
                categories = [item[0] for item in categories]
            if isinstance(values[0], list) and len(values[0]) == 1:
                values = [item[0] for item in values]
            
            bars = ax.bar(categories, values, color=colors[:len(categories)])
            ax.set_title("柱状图", fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel("类别", fontsize=12)
            ax.set_ylabel("数值", fontsize=12)
            
            # 添加数值标签
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                       f'{value:.1f}', ha='center', va='bottom', fontsize=10)
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            
        elif "line" in chart_data:
            line_data = chart_data["line"]
            fig, ax = plt.subplots(figsize=(12, 7))
            
            line_color = colors[0] if colors else '#1f77b4'
            
            # 获取数据并确保是一维数组
            columns = line_data["columns"]
            data = line_data["data"]
            
            # 确保columns和data是一维数组
            if isinstance(columns[0], list) and len(columns[0]) == 1:
                columns = [item[0] for item in columns]
            if isinstance(data[0], list) and len(data[0]) == 1:
                data = [item[0] for item in data]
                
            ax.plot(columns, data, 
                   marker='o', linewidth=2.5, markersize=6, color=line_color)
            ax.set_title("折线图", fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel("类别", fontsize=12)
            ax.set_ylabel("数值", fontsize=12)
            
            # 添加网格
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            
        elif "scatter" in chart_data:
            scatter_data = chart_data["scatter"]
            fig, ax = plt.subplots(figsize=(10, 8))
            
            scatter_color = colors[0] if colors else '#1f77b4'
            
            # 获取数据并确保是一维数组
            x_data = scatter_data["x_data"]
            y_data = scatter_data["y_data"]
            
            # 确保x_data和y_data是一维数组
            if isinstance(x_data[0], list) and len(x_data[0]) == 1:
                x_data = [item[0] for item in x_data]
            if isinstance(y_data[0], list) and len(y_data[0]) == 1:
                y_data = [item[0] for item in y_data]
                
            ax.scatter(x_data, y_data, 
                      c=scatter_color, alpha=0.7, s=60, edgecolors='white', linewidth=1)
            ax.set_title("散点图", fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel("X轴", fontsize=12)
            ax.set_ylabel("Y轴", fontsize=12)
            
            if "labels" in scatter_data:
                for i, label in enumerate(scatter_data["labels"]):
                    if i < len(scatter_data["x_data"]) and i < len(scatter_data["y_data"]):
                        ax.annotate(label, (scatter_data["x_data"][i], scatter_data["y_data"][i]),
                                  xytext=(5, 5), textcoords='offset points', fontsize=9)
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            
        elif "pie" in chart_data:
            pie_data = chart_data["pie"]
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # 获取数据并确保是一维数组
            values = pie_data["values"]
            labels = pie_data["labels"]
            
            # 确保values和labels是一维数组
            if isinstance(values[0], list) and len(values[0]) == 1:
                values = [item[0] for item in values]
            if isinstance(labels[0], list) and len(labels[0]) == 1:
                labels = [item[0] for item in labels]
                
            wedges, texts, autotexts = ax.pie(values, labels=labels, 
                                            autopct='%1.1f%%', colors=colors[:len(values)],
                                            startangle=90, explode=[0.05]*len(values))
            
            ax.set_title("饼图", fontsize=16, fontweight='bold', pad=20)
            
            # 美化文字
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            plt.tight_layout()
            st.pyplot(fig)
            
        elif "heatmap" in chart_data:
            heatmap_data = chart_data["heatmap"]
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # 根据样式选择色彩映射
            cmap_dict = {
                "简洁": 'Blues',
                "专业": 'viridis',
                "彩色": 'plasma',
                "默认": 'coolwarm'
            }
            cmap = cmap_dict.get(style, 'coolwarm')
            
            # 获取数据并确保格式正确
            data = heatmap_data["data"]
            x_labels = heatmap_data.get("x_labels", [])
            y_labels = heatmap_data.get("y_labels", [])
            
            # 确保x_labels和y_labels是一维数组
            if x_labels and isinstance(x_labels[0], list) and len(x_labels[0]) == 1:
                x_labels = [item[0] for item in x_labels]
            if y_labels and isinstance(y_labels[0], list) and len(y_labels[0]) == 1:
                y_labels = [item[0] for item in y_labels]
                
            # 确保data是二维数组，如果是嵌套列表的列表，则提取内部值
            if data and isinstance(data[0], list) and isinstance(data[0][0], list):
                data = [[item[0] if isinstance(item, list) and len(item) == 1 else item for item in row] for row in data]
                
            sns.heatmap(data, 
                       xticklabels=x_labels,
                       yticklabels=y_labels,
                       annot=True, cmap=cmap, ax=ax, fmt='.2f',
                       cbar_kws={'shrink': 0.8})
            
            ax.set_title("热力图", fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)
            
        else:
            st.error("不支持的图表类型")
            
    except Exception as e:
        st.error(f"图表渲染失败: {str(e)}")


# 主标题和欢迎界面
st.markdown('<h1 class="main-title tech-decoration" data-text="🤖 深藏Blue组数据分析智能体">🤖 深藏Blue组数据分析智能体</h1>', unsafe_allow_html=True)

# 欢迎信息卡片
st.markdown("""
<div class="tech-card tech-border">
    <div style="text-align: center; padding: 1.2rem;">
        <h3 style="color: #00d4ff; margin-bottom: 1.2rem; position: relative; display: inline-block;">🚀 欢迎使用AI驱动的数据分析平台</h3>
        <p style="color: #b8c5d6; font-size: 1.2rem; line-height: 1.5; margin-bottom: 1.2rem;">
            基于先进的人工智能技术，为您提供智能化的数据分析体验<br>
            支持多种数据格式 • 智能图表生成 • 深度洞察分析
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; flex-wrap: wrap;">
            <div style="text-align: center; transition: all 0.3s ease;" class="tech-decoration" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 3rem; color: #00d4ff; margin-bottom: 0.6rem; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);">📊</div>
                <div style="color: #b8c5d6; font-size: 1.8rem; font-weight: 500;">多格式支持</div>
            </div>
            <div style="text-align: center; transition: all 0.3s ease;" class="tech-decoration" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 3rem; color: #00d4ff; margin-bottom: 0.6rem; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);">🤖</div>
                <div style="color: #b8c5d6; font-size: 1.8rem; font-weight: 500;">AI智能分析</div>
            </div>
            <div style="text-align: center; transition: all 0.3s ease;" class="tech-decoration" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 3rem; color: #00d4ff; margin-bottom: 0.6rem; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);">📈</div>
                <div style="color: #b8c5d6; font-size: 1.8rem; font-weight: 500;">可视化图表</div>
            </div>
            <div style="text-align: center; transition: all 0.3s ease;" class="tech-decoration" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 3rem; color: #00d4ff; margin-bottom: 0.6rem; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);">⚡</div>
                <div style="color: #b8c5d6; font-size: 1.8rem; font-weight: 500;">实时处理</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 文件上传区域
st.markdown("""
<div class="tech-card tech-border">
    <h3 style="color: #00d4ff; margin-bottom: 1.2rem; text-align: center;" class="tech-decoration">📁 数据文件上传</h3>
    <div class="tech-decoration" style="position: absolute; top: 10px; right: 10px; width: 15px; height: 15px;"></div>
    <div class="tech-decoration" style="position: absolute; bottom: 10px; left: 10px; width: 15px; height: 15px;"></div>
</div>
""", unsafe_allow_html=True)

# 支持的文件类型
file_types = {
    "Excel (.xlsx/.xls)": ["xlsx", "xls"],
    "CSV (.csv)": ["csv"],
    "JSON (.json)": ["json"],
    "TSV (.tsv)": ["tsv"],
    "Parquet (.parquet)": ["parquet"],
    "TXT (.txt)": ["txt"]
}

# 创建两列布局
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    option = st.selectbox(
        "📋 选择数据文件类型:", 
        list(file_types.keys()),
        help="选择您要上传的文件格式类型"
    )
    selected_extensions = file_types[option]
    
    # 显示支持的格式信息
    st.markdown(f"""
    <div style="margin-top: 0.8rem; padding: 0.8rem; background: rgba(0, 212, 255, 0.15); border-radius: 8px; border: 1px solid rgba(0, 212, 255, 0.5);">
        <h4 style="color: #00d4ff; margin: 0 0 0.4rem 0; font-size: 1.4rem;">📄 当前选择格式</h4>
        <p style="color: #ffffff; margin: 0; font-size: 1.4rem;">{option}</p>
        <p style="color: #ffffff; margin: 0.4rem 0 0 0; font-size: 1.2rem;">支持扩展名: {', '.join(selected_extensions)}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    data = st.file_uploader(
        f"🚀 上传你的{option}数据文件", 
        type=selected_extensions,
        help="支持多种数据格式：Excel、CSV、JSON、TSV、Parquet、TXT等"
    )
    
    # 文件格式说明
    if not data:
        st.markdown("""
        <div style="margin-top: 1rem; padding: 1.2rem; background: rgba(26, 31, 58, 0.6); border-radius: 10px; border: 1px solid rgba(0, 212, 255, 0.2);">
            <h4 style="color: #00d4ff; margin: 0 0 0.8rem 0; font-size: 1.8rem;">💡 支持的文件格式</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.8rem;">
                <div style="padding: 0.8rem; background: rgba(0, 212, 255, 0.05); border-radius: 6px; border: 1px solid rgba(0, 212, 255, 0.2);">
                    <div style="color: #00d4ff; font-weight: bold; margin-bottom: 0.3rem; font-size: 1.4rem;">📊 Excel</div>
                        <div style="color: #b8c5d6; font-size: 1.2rem;">支持多工作表<br>.xlsx, .xls</div>
                    </div>
                    <div style="padding: 0.8rem; background: rgba(0, 212, 255, 0.05); border-radius: 6px; border: 1px solid rgba(0, 212, 255, 0.2);">
                        <div style="color: #00d4ff; font-weight: bold; margin-bottom: 0.3rem; font-size: 1.4rem;">📄 CSV/TSV</div>
                        <div style="color: #b8c5d6; font-size: 1.2rem;">逗号/制表符分隔<br>.csv, .tsv</div>
                    </div>
                    <div style="padding: 0.8rem; background: rgba(0, 212, 255, 0.05); border-radius: 6px; border: 1px solid rgba(0, 212, 255, 0.2);">
                        <div style="color: #00d4ff; font-weight: bold; margin-bottom: 0.3rem; font-size: 1.4rem;">🔧 JSON</div>
                        <div style="color: #b8c5d6; font-size: 1.2rem;">结构化数据<br>.json</div>
                    </div>
                    <div style="padding: 0.8rem; background: rgba(0, 212, 255, 0.05); border-radius: 6px; border: 1px solid rgba(0, 212, 255, 0.2);">
                        <div style="color: #00d4ff; font-weight: bold; margin-bottom: 0.3rem; font-size: 1.4rem;">⚡ Parquet</div>
                        <div style="color: #b8c5d6; font-size: 1.2rem;">高性能格式<br>.parquet</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if data:
    try:
        # 显示加载进度
        with st.spinner('正在加载文件...'):
            # 使用工具函数加载数据
            df_result = load_data_file(data, option)
        
        if isinstance(df_result, dict) and "sheets" in df_result:
            # Excel文件有多个工作表
            st.markdown("""
            <div class="tech-card">
                <div style="text-align: center; padding: 0.8rem;">
                    <h3 style="color: #00d4ff; margin-bottom: 0.8rem;">✅ Excel文件加载成功</h3>
                    <p style="color: #b8c5d6; font-size: 1.2rem;">检测到多个工作表，请选择要分析的工作表</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 显示所有工作表的基本信息
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1rem;">📊 工作表概览</h3>
            </div>
            """, unsafe_allow_html=True)
            
            sheet_info = []
            for sheet_name, sheet_df in df_result['sheets'].items():
                # 安全地处理数据类型，避免pyarrow转换错误
                try:
                    dtype_str = ", ".join([str(dt) for dt in sheet_df.dtypes.unique()[:3]])
                except Exception:
                    dtype_str = "混合类型"
                
                sheet_info.append({
                    "工作表名称": sheet_name,
                    "行数": sheet_df.shape[0],
                    "列数": sheet_df.shape[1],
                    "数据类型": dtype_str
                })
            
            # 使用科技感的表格显示
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(sheet_info), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Excel文件有多个工作表
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            sheet_option = st.radio(
                label="🎯 请选择要加载的工作表：", 
                options=list(df_result["sheets"].keys()),
                help="选择您要进行分析的工作表"
            )
            st.session_state["df"] = df_result["sheets"][sheet_option]
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示详细的数据信息
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1.5rem; text-align: center;">📊 数据统计概览</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 2rem; color: #00d4ff; text-align: center;">📏</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.5rem 0;">{}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.9rem;">总行数</div>
                </div>
                """.format(st.session_state["df"].shape[0]), unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 2rem; color: #00d4ff; text-align: center;">📋</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.5rem 0;">{}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.9rem;">总列数</div>
                </div>
                """.format(st.session_state["df"].shape[1]), unsafe_allow_html=True)
            with col3:
                missing_count = st.session_state["df"].isnull().sum().sum()
                color = "#ff6b35" if missing_count > 0 else "#00d4ff"
                icon = "⚠️" if missing_count > 0 else "✅"
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 2rem; color: {}; text-align: center;">{}</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.5rem 0;">{}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.9rem;">缺失值</div>
                </div>
                """.format(color, icon, missing_count), unsafe_allow_html=True)
            
            # 数据类型信息
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1.5rem;">📈 列信息详情</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 安全地处理数据类型，避免pyarrow转换错误
            try:
                dtype_strings = [str(dt) for dt in st.session_state["df"].dtypes]
            except Exception:
                dtype_strings = ["未知类型"] * len(st.session_state["df"].columns)
            
            column_info = pd.DataFrame({
                "列名": st.session_state["df"].columns,
                "数据类型": dtype_strings,
                "非空值数量": st.session_state["df"].count(),
                "缺失值数量": st.session_state["df"].isnull().sum()
            })
            
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            st.dataframe(column_info, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # 单个数据框
            st.session_state["df"] = df_result
            
            # 成功加载提示
            st.markdown("""
            <div class="tech-card">
                <div style="text-align: center; padding: 1rem;">
                    <h3 style="color: #00d4ff; margin-bottom: 1rem;">✅ 文件加载成功</h3>
                    <p style="color: #b8c5d6; font-size: 1.1rem;">数据已成功加载，可以开始分析了</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 数据筛选器
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1.5rem; text-align: center;">🔍 智能数据筛选器</h3>
                <p style="color: #b8c5d6; text-align: center; margin-bottom: 1.5rem;">自定义数据范围和列选择，精确控制分析数据</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 创建筛选器容器
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            filter_container = st.container()
            
            with filter_container:
                # 行数筛选
                st.markdown("**📏 行数范围筛选**")
                col1, col2 = st.columns(2)
                with col1:
                    start_row = st.number_input(
                        "起始行", 
                        min_value=0, 
                        max_value=len(st.session_state["df"])-1, 
                        value=0,
                        help="选择数据的起始行号"
                    )
                with col2:
                    end_row = st.number_input(
                        "结束行", 
                        min_value=start_row+1, 
                        max_value=len(st.session_state["df"]), 
                        value=min(100, len(st.session_state["df"])),
                        help="选择数据的结束行号"
                    )
                
                st.markdown("---")
                
                # 列筛选
                st.markdown("**📋 列选择筛选**")
                selected_columns = st.multiselect(
                    "选择要显示的列",
                    options=st.session_state["df"].columns.tolist(),
                    default=st.session_state["df"].columns.tolist()[:5] if len(st.session_state["df"].columns) > 5 else st.session_state["df"].columns.tolist(),
                    help="选择您要在分析中包含的列"
                )
                
                # 数值列筛选
                numeric_columns = st.session_state["df"].select_dtypes(include=[np.number]).columns.tolist()
                if numeric_columns:
                    st.markdown("---")
                    st.markdown("**📊 数值列范围筛选**")
                    filter_cols = st.columns(min(3, len(numeric_columns)))
                    filters = {}
                    
                    for i, col in enumerate(numeric_columns[:3]):  # 最多显示3个数值列的筛选器
                        with filter_cols[i % 3]:
                            min_val = float(st.session_state["df"][col].min())
                            max_val = float(st.session_state["df"][col].max())
                            filters[col] = st.slider(
                                f"{col} 范围",
                                min_value=min_val,
                                max_value=max_val,
                                value=(min_val, max_val),
                                key=f"filter_{col}",
                                help=f"设置{col}列的数值范围"
                            )
                
                # 应用筛选
                filtered_df = st.session_state["df"].copy()
                
                # 应用行筛选
                filtered_df = filtered_df.iloc[start_row:end_row]
                
                # 应用列筛选
                if selected_columns:
                    filtered_df = filtered_df[selected_columns]
                
                # 应用数值筛选
                if numeric_columns:
                    for col, (min_range, max_range) in filters.items():
                        if col in filtered_df.columns:
                            filtered_df = filtered_df[
                                (filtered_df[col] >= min_range) & (filtered_df[col] <= max_range)
                            ]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示筛选后的数据统计信息
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1.5rem; text-align: center;">📊 筛选后数据统计</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                delta_rows = len(filtered_df) - len(st.session_state["df"])
                delta_color = "#00d4ff" if delta_rows == 0 else "#ff6b35" if delta_rows < 0 else "#00ff88"
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 1.5rem; color: #00d4ff; text-align: center;">📏</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.3rem 0;">{}</div>
                    <div style="color: {}; text-align: center; font-size: 0.8rem;">{:+d}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.8rem;">筛选后行数</div>
                </div>
                """.format(len(filtered_df), delta_color, delta_rows), unsafe_allow_html=True)
            with col2:
                delta_cols = len(filtered_df.columns) - len(st.session_state["df"].columns)
                delta_color = "#00d4ff" if delta_cols == 0 else "#ff6b35" if delta_cols < 0 else "#00ff88"
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 1.5rem; color: #00d4ff; text-align: center;">📋</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.3rem 0;">{}</div>
                    <div style="color: {}; text-align: center; font-size: 0.8rem;">{:+d}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.8rem;">显示列数</div>
                </div>
                """.format(len(filtered_df.columns), delta_color, delta_cols), unsafe_allow_html=True)
            with col3:
                numeric_count = len(filtered_df.select_dtypes(include=[np.number]).columns)
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 1.5rem; color: #00d4ff; text-align: center;">🔢</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.3rem 0;">{}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.8rem;">数值列数</div>
                </div>
                """.format(numeric_count), unsafe_allow_html=True)
            with col4:
                text_count = len(filtered_df.select_dtypes(include=['object']).columns)
                st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 1.5rem; color: #00d4ff; text-align: center;">📝</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #ffffff; text-align: center; margin: 0.3rem 0;">{}</div>
                    <div style="color: #b8c5d6; text-align: center; font-size: 0.8rem;">文本列数</div>
                </div>
                """.format(text_count), unsafe_allow_html=True)
            
            # 筛选后数据的列信息
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1.5rem;">📋 筛选后列信息</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 安全地处理数据类型，避免pyarrow转换错误
            try:
                dtype_strings = [str(dt) for dt in filtered_df.dtypes]
            except Exception:
                dtype_strings = ["未知类型"] * len(filtered_df.columns)
            
            col_info = pd.DataFrame({
                '列名': filtered_df.columns,
                '数据类型': dtype_strings,
                '非空值数量': filtered_df.count(),
                '缺失值数量': filtered_df.isnull().sum()
            })
            
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            st.dataframe(col_info, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 筛选后数据预览
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1.5rem;">👀 筛选后数据预览</h3>
                <p style="color: #b8c5d6; margin-bottom: 1rem;">显示前20行筛选后的数据</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            st.dataframe(filtered_df.head(20), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 将筛选后的数据保存到session_state中供AI分析使用
            st.session_state["filtered_df"] = filtered_df
            
        # 原始数据预览
        st.markdown("""
        <div class="tech-card">
            <details>
                <summary style="color: #00d4ff; font-size: 1.1rem; font-weight: bold; cursor: pointer; padding: 0.5rem 0;">🔍 原始数据预览</summary>
                <div style="margin-top: 1rem; padding: 1rem; background: rgba(26, 31, 58, 0.6); border-radius: 8px; border: 1px solid rgba(0, 212, 255, 0.2);">
        """, unsafe_allow_html=True)
        
        st.dataframe(st.session_state["df"].head(10), use_container_width=True)
        
        st.markdown("""
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)
            
    except Exception as e:
        st.markdown(f"""
        <div class="tech-card" style="border-color: #ff4757; background: rgba(255, 71, 87, 0.1);">
            <h3 style="color: #ff4757; margin-bottom: 1rem;">❌ 文件加载失败</h3>
            <p style="color: #ff8a9b; margin-bottom: 1.5rem;">错误信息: {str(e)}</p>
            
            <h4 style="color: #00d4ff; margin-bottom: 1rem;">💡 支持的文件格式</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem;">
                <div style="padding: 0.5rem; background: rgba(0, 212, 255, 0.1); border-radius: 6px; border-left: 3px solid #00d4ff;">
                    <strong style="color: #00d4ff;">📊 Excel文件</strong><br>
                    <span style="color: #b8c5d6;">.xlsx, .xls</span>
                </div>
                <div style="padding: 0.5rem; background: rgba(0, 212, 255, 0.1); border-radius: 6px; border-left: 3px solid #00d4ff;">
                    <strong style="color: #00d4ff;">📄 CSV/TSV文件</strong><br>
                    <span style="color: #b8c5d6;">.csv, .tsv</span>
                </div>
                <div style="padding: 0.5rem; background: rgba(0, 212, 255, 0.1); border-radius: 6px; border-left: 3px solid #00d4ff;">
                    <strong style="color: #00d4ff;">🔗 JSON文件</strong><br>
                    <span style="color: #b8c5d6;">.json</span>
                </div>
                <div style="padding: 0.5rem; background: rgba(0, 212, 255, 0.1); border-radius: 6px; border-left: 3px solid #00d4ff;">
                    <strong style="color: #00d4ff;">⚡ Parquet文件</strong><br>
                    <span style="color: #b8c5d6;">.parquet</span>
                </div>
                <div style="padding: 0.5rem; background: rgba(0, 212, 255, 0.1); border-radius: 6px; border-left: 3px solid #00d4ff;">
                    <strong style="color: #00d4ff;">📝 TXT文件</strong><br>
                    <span style="color: #b8c5d6;">.txt</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 提供详细的错误处理建议
        error_msg = str(e).lower()
        if "expected 2 fields" in error_msg or "saw 3" in error_msg:
            st.info("💡 **解决建议**: 这可能是TXT文件的分隔符问题。请尝试：\n"
                    "- 检查文件是否使用了一致的分隔符（逗号、制表符等）\n"
                    "- 确保每行的字段数量一致\n"
                    "- 尝试将文件另存为CSV格式")
        elif "json" in error_msg:
            st.info("💡 **解决建议**: JSON文件格式问题。请确保：\n"
                    "- JSON语法正确（使用双引号、正确的括号匹配）\n"
                    "- 文件编码为UTF-8\n"
                    "- JSON结构包含数组或对象")
        elif "excel" in error_msg or "openpyxl" in error_msg:
            st.info("💡 **解决建议**: Excel文件问题。请尝试：\n"
                    "- 确保文件未损坏\n"
                    "- 检查文件是否被其他程序占用\n"
                    "- 尝试另存为新的Excel文件")
        else:
            st.info("💡 **通用解决建议**：\n"
                    "- 检查文件格式是否与选择的类型匹配\n"
                    "- 确保文件未损坏且可以正常打开\n"
                    "- 尝试选择不同的文件类型选项\n"
                    "- 检查文件编码（建议使用UTF-8）")

# AI分析部分
if "df" in st.session_state:
    st.markdown("""
    <div class="tech-card tech-border">
        <h2 style="color: #00d4ff; margin-bottom: 1.5rem; text-align: center;" class="tech-decoration">🤖 AI智能分析</h2>
        <p style="color: #b8c5d6; text-align: center; margin-bottom: 2rem;">基于人工智能的数据洞察与可视化分析</p>
        <div class="tech-decoration" style="position: absolute; top: 15px; right: 15px; width: 25px; height: 25px;"></div>
        <div class="tech-decoration" style="position: absolute; bottom: 15px; left: 15px; width: 25px; height: 25px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 用户输入查询
    st.markdown("""
    <div class="tech-card tech-border">
        <h3 style="color: #00d4ff; margin-bottom: 1rem;" class="tech-decoration">💭 分析需求输入</h3>
        <p style="color: #b8c5d6; margin-bottom: 1rem;">请详细描述您的数据分析需求，AI将为您提供专业的分析建议</p>
        <div class="tech-decoration" style="position: absolute; top: 10px; right: 10px; width: 15px; height: 15px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    query = st.text_area(
        "请输入你关于以上数据集的问题或数据可视化需求：",
        placeholder="例如：分析销售数据的趋势，找出最重要的影响因素，预测未来发展方向",
        height=120,
        help="💡 提示：描述越详细，AI分析结果越精准",
        disabled="df" not in st.session_state
    )
    
    # 图表类型和样式选择
    st.markdown("""
    <div class="tech-card tech-border">
        <h3 style="color: #00d4ff; margin-bottom: 1rem;" class="tech-decoration">📊 可视化配置</h3>
        <p style="color: #b8c5d6; margin-bottom: 1rem;">选择合适的图表类型和样式来展示分析结果</p>
        <div class="tech-decoration" style="position: absolute; top: 10px; right: 10px; width: 15px; height: 15px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        chart_type = st.selectbox(
            "🎯 图表类型",
            options=[
                "自动选择",
                "柱形图 (Bar Chart)",
                "折线图 (Line Chart)", 
                "散点图 (Scatter Plot)",
                "饼图 (Pie Chart)",
                "热力图 (Heatmap)"
            ],
            help="选择您希望生成的图表类型，或选择'自动选择'让AI根据数据特征自动决定"
        )
    
    with col2:
        # 图表样式选项
        chart_style = st.selectbox(
            "🎨 图表样式",
            options=["默认", "简洁", "专业", "彩色"],
            help="选择图表的视觉样式"
        )
    
    with col3:
        # 根据选择的图表类型显示相关参数
        if chart_type == "柱形图 (Bar Chart)":
            st.info("💡 适用于分类数据的比较")
        elif chart_type == "折线图 (Line Chart)":
            st.info("💡 适用于时间序列或趋势分析")
        elif chart_type == "散点图 (Scatter Plot)":
            st.info("💡 适用于两个数值变量的关系分析")
        elif chart_type == "饼图 (Pie Chart)":
            st.info("💡 适用于部分与整体的比例关系")
        elif chart_type == "热力图 (Heatmap)":
            st.info("💡 适用于相关性分析或矩阵数据")
        else:
            st.info("💡 AI将根据数据特征自动选择最合适的图表")

    # 分析选项
    st.markdown("""
    <div class="tech-card tech-border">
        <h3 style="color: #00d4ff; margin-bottom: 1rem;" class="tech-decoration">⚙️ 分析选项</h3>
        <p style="color: #b8c5d6; margin-bottom: 1rem;">配置AI分析的高级选项</p>
        <div class="tech-decoration" style="position: absolute; top: 10px; right: 10px; width: 15px; height: 15px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        enable_streaming = st.checkbox("🔄 启用流式输出", value=False, help="实时显示AI分析过程")
    with col2:
        enable_cache = st.checkbox("💾 启用缓存", value=True, help="缓存分析结果以提高响应速度")
else:
    # 当没有数据时显示提示
    st.markdown("""
    <div class="tech-card tech-border" style="text-align: center; padding: 3rem 2rem;">
        <h3 style="color: #b8c5d6; margin-bottom: 1.5rem;" class="tech-decoration">📤 请先上传数据文件</h3>
        <p style="color: #7a8ba0; font-size: 1.1rem;">上传数据后即可开始AI智能分析</p>
        <div class="tech-decoration" style="position: absolute; top: 15px; right: 15px; width: 20px; height: 20px;"></div>
        <div class="tech-decoration" style="position: absolute; bottom: 15px; left: 15px; width: 20px; height: 20px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    query = None

if query:
    if "df" not in st.session_state:
        st.markdown("""
        <div class="tech-card" style="border-color: #ffa502; background: rgba(255, 165, 2, 0.1);">
            <p style="color: #ffa502; text-align: center; margin: 0;">⚠️ 请先上传数据文件</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # 分析按钮
    st.markdown("""
    <div class="tech-card" style="text-align: center; padding: 2rem;">
        <h3 style="color: #00d4ff; margin-bottom: 1rem;">🚀 开始分析</h3>
        <p style="color: #b8c5d6; margin-bottom: 1.5rem;">点击下方按钮，让AI为您进行深度数据分析</p>
    </div>
    """, unsafe_allow_html=True)
        
    if st.button("🤖 开始AI智能分析", type="primary", use_container_width=True):
        # 检查是否有筛选后的数据
        analysis_df = st.session_state.get("filtered_df", st.session_state["df"])
        
        # 构建包含图表类型要求的查询
        enhanced_query = query
        
        # 根据用户选择的图表类型添加特定要求
        if chart_type != "自动选择":
            chart_instructions = {
                "柱形图 (Bar Chart)": "请生成柱形图(bar chart)来展示数据。使用bar格式返回结果，包含categories和values字段。",
                "折线图 (Line Chart)": "请生成折线图(line chart)来展示数据趋势。使用line格式返回结果，包含columns和data字段。",
                "散点图 (Scatter Plot)": "请生成散点图(scatter plot)来展示两个变量的关系。使用scatter格式返回结果，包含x_data和y_data字段。",
                "饼图 (Pie Chart)": "请生成饼图(pie chart)来展示数据的比例关系。使用pie格式返回结果，包含labels和values字段。",
                "热力图 (Heatmap)": "请生成热力图(heatmap)来展示数据的相关性或分布。使用heatmap格式返回结果，包含data、x_labels和y_labels字段。"
            }
            
            chart_instruction = chart_instructions.get(chart_type, "")
            enhanced_query = f"{query}\n\n图表要求：{chart_instruction}"
            
            # 添加样式要求
            style_instructions = {
                "简洁": "图表样式要求：使用简洁清晰的设计，避免过多装饰。",
                "专业": "图表样式要求：使用专业的商务风格，适合正式报告。",
                "彩色": "图表样式要求：使用丰富的色彩搭配，使图表更加生动。"
            }
            
            if chart_style != "默认":
                style_instruction = style_instructions.get(chart_style, "")
                enhanced_query += f"\n{style_instruction}"
        
        if enable_streaming:
            # 流式输出模式
            st.markdown("""
            <div class="tech-card">
                <h3 style="color: #00d4ff; margin-bottom: 1rem;">🔄 AI分析过程</h3>
                <p style="color: #b8c5d6; margin-bottom: 1rem;">实时显示AI分析进度</p>
            </div>
            """, unsafe_allow_html=True)
            
            stream_container = st.empty()
            
            with st.spinner("🤖 AI正在深度分析数据中，请稍候..."):
                result = dataframe_agent(analysis_df, enhanced_query, stream_container=stream_container)
                
        else:
            # 普通模式（支持缓存）
            if not enable_cache:
                # 清除相关缓存
                if hasattr(st, 'cache_data'):
                    st.cache_data.clear()
                    
            with st.spinner("🤖 AI正在深度分析数据中，请稍候..."):
                result = dataframe_agent(analysis_df, enhanced_query)
                
        if result:
            # 分析完成提示
            st.markdown("""
            <div class="tech-card" style="border-color: #2ed573; background: rgba(46, 213, 115, 0.1); text-align: center;">
                <h3 style="color: #2ed573; margin: 0;">✅ 分析完成！</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 显示分析结果
            if "answer" in result:
                st.markdown("""
                <div class="tech-card">
                    <h3 style="color: #00d4ff; margin-bottom: 1rem;">📝 AI分析结果</h3>
                    <p style="color: #b8c5d6; margin-bottom: 1rem;">基于数据特征的智能分析报告</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                st.write(result["answer"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示表格
            if "table" in result:
                st.markdown("""
                <div class="tech-card">
                    <h3 style="color: #00d4ff; margin-bottom: 1rem;">📊 数据表格</h3>
                    <p style="color: #b8c5d6; margin-bottom: 1rem;">分析过程中生成的数据表格</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(data=result["table"]["data"],
                                         columns=result["table"]["columns"]), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示图表（传递用户选择的样式）
            chart_style_param = chart_style if 'chart_style' in locals() else "默认"
            if "bar" in result:
                st.markdown("""
                <div class="tech-card">
                    <h3 style="color: #00d4ff; margin-bottom: 1rem;">📈 可视化图表</h3>
                    <p style="color: #b8c5d6; margin-bottom: 1rem;">基于分析结果生成的智能图表</p>
                </div>
                """, unsafe_allow_html=True)
                
                render_chart(result, chart_style_param)
            if "line" in result:
                render_chart(result, chart_style_param)
            if "scatter" in result:
                render_chart(result, chart_style_param)
            if "pie" in result:
                render_chart(result, chart_style_param)
            if "heatmap" in result:
                render_chart(result, chart_style_param)
                
# 添加数据分析建议功能
if "df" in st.session_state:
    st.markdown("""
    <div class="tech-card tech-border">
        <h2 style="color: #00d4ff; margin-bottom: 1.5rem; text-align: center; font-size: 2.2rem;" class="tech-decoration">🎯 智能数据分析建议</h2>
        <p style="color: #ffffff; text-align: center; margin-bottom: 2rem; font-size: 1.4rem;">基于数据特征的专业分析建议与快速分析选项</p>
        <div class="tech-decoration" style="position: absolute; top: 15px; right: 15px; width: 25px; height: 25px;"></div>
        <div class="tech-decoration" style="position: absolute; bottom: 15px; left: 15px; width: 25px; height: 25px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 获取当前数据（筛选后的或原始的）
    current_df = st.session_state.get("filtered_df", st.session_state["df"])
    
    # 生成数据分析建议
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="tech-card tech-border">
            <h3 style="color: #00d4ff; margin-bottom: 1rem; font-size: 1.8rem;" class="tech-decoration">📊 基于数据特征的分析建议</h3>
            <p style="color: #ffffff; margin-bottom: 1rem; font-size: 1.4rem;">AI根据您的数据特征智能推荐的分析方向</p>
            <div class="tech-decoration" style="position: absolute; top: 10px; right: 10px; width: 15px; height: 15px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 数据基本信息分析
        num_rows, num_cols = current_df.shape
        numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = current_df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = current_df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # 生成建议
        suggestions = []
        
        # 基于数据类型的建议
        if len(numeric_cols) >= 2:
            suggestions.append("📈 **相关性分析**: 探索数值变量之间的相关关系")
            suggestions.append("📊 **散点图分析**: 可视化两个数值变量的关系")
        
        if len(categorical_cols) >= 1:
            suggestions.append("🥧 **分类分析**: 分析分类变量的分布情况")
            if len(numeric_cols) >= 1:
                suggestions.append("📊 **分组统计**: 按分类变量分组分析数值变量")
        
        if len(datetime_cols) >= 1:
            suggestions.append("📅 **时间序列分析**: 分析数据随时间的变化趋势")
            if len(numeric_cols) >= 1:
                suggestions.append("📈 **趋势分析**: 观察数值指标的时间变化")
        
        if num_rows > 1000:
            suggestions.append("🔍 **大数据集分析**: 考虑数据采样或聚合分析")
            suggestions.append("📊 **统计摘要**: 重点关注数据的统计特征")
        
        # 基于数据质量的建议
        missing_data = current_df.isnull().sum().sum()
        if missing_data > 0:
            suggestions.append("⚠️ **数据质量检查**: 处理缺失值和异常值")
        
        # 显示建议
        if suggestions:
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"""
                <div style="padding: 0.8rem; margin: 0.5rem 0; background: rgba(0, 212, 255, 0.15); border-radius: 8px; border-left: 3px solid #00d4ff;">
                    <span style="color: #00d4ff; font-weight: bold; font-size: 1.2rem;">{i}.</span> 
                    <span style="color: #ffffff; font-size: 1.2rem;">{suggestion}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="tech-card" style="text-align: center;">
                <p style="color: #ffffff; margin: 0; font-size: 1.2rem;">💡 上传更多数据以获得更详细的分析建议</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-card tech-border">
             <h3 style="color: #00d4ff; margin-bottom: 1rem; font-size: 1.8rem;" class="tech-decoration">🚀 快速分析</h3>
             <p style="color: #ffffff; margin-bottom: 1rem; font-size: 1.4rem;">一键生成常用的数据分析报告</p>
             <div class="tech-decoration" style="position: absolute; top: 10px; right: 10px; width: 15px; height: 15px;"></div>
          </div>
        """, unsafe_allow_html=True)
        
        # 快速分析的图表类型选择
        quick_chart_type = st.selectbox(
            "📊 快速分析图表类型",
            options=["自动选择", "柱形图", "折线图", "散点图", "饼图", "热力图"],
            key="quick_chart_type",
            help="为快速分析选择特定的图表类型"
        )
        
        # 快速分析按钮
        if st.button("📊 数据概览分析", help="生成数据的基本统计概览", use_container_width=True):
            overview_query = f"""
            请对这个数据集进行全面的概览分析，包括：
            1. 数据集基本信息（行数、列数、数据类型）
            2. 数值变量的统计摘要
            3. 分类变量的分布情况
            4. 数据质量评估（缺失值、异常值）
            5. 主要发现和洞察
            
            数据集包含 {num_rows} 行，{num_cols} 列。
            数值列：{', '.join(numeric_cols[:5]) if numeric_cols else '无'}
            分类列：{', '.join(categorical_cols[:5]) if categorical_cols else '无'}
            """
            
            # 如果选择了特定图表类型，添加图表要求
            if quick_chart_type != "自动选择":
                chart_map = {
                    "柱形图": "请生成柱形图展示主要分类变量的分布。",
                    "折线图": "请生成折线图展示数值变量的趋势。",
                    "散点图": "请生成散点图展示两个主要数值变量的关系。",
                    "饼图": "请生成饼图展示主要分类变量的比例。",
                    "热力图": "请生成热力图展示数值变量间的相关性。"
                }
                overview_query += f"\n\n图表要求：{chart_map.get(quick_chart_type, '')}"
            
            with st.spinner("🔍 正在生成数据概览分析..."):
                result = dataframe_agent(current_df, overview_query)
                if result and "answer" in result:
                    st.markdown("""
                    <div class="tech-card">
                        <h4 style="color: #00d4ff; margin-bottom: 1rem; font-size: 1.6rem;">📋 数据概览结果</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                    st.write(result["answer"])
                    st.markdown('</div>', unsafe_allow_html=True)
        
        if len(numeric_cols) >= 2 and st.button("🔗 相关性分析", help="分析数值变量间的相关关系", use_container_width=True):
            correlation_query = f"""
            请分析数值变量之间的相关性，包括：
            1. 计算相关系数矩阵
            2. 识别强相关关系（|r| > 0.7）
            3. 生成相关性热力图
            4. 解释相关性的业务含义
            
            重点分析这些数值列：{', '.join(numeric_cols[:10])}
            """
            
            # 根据快速分析图表类型添加特定要求
            if quick_chart_type == "热力图":
                correlation_query += "\n\n图表要求：请生成热力图展示相关性矩阵。"
            elif quick_chart_type == "散点图":
                correlation_query += "\n\n图表要求：请生成散点图展示最相关的两个变量关系。"
            elif quick_chart_type != "自动选择":
                correlation_query += f"\n\n图表要求：请尽量生成{quick_chart_type}来展示相关性分析结果。"
            
            with st.spinner("🔍 正在分析数据相关性..."):
                result = dataframe_agent(current_df, correlation_query)
                if result:
                    if "answer" in result:
                        st.markdown("""
                        <div class="tech-card">
                            <h4 style="color: #00d4ff; margin-bottom: 1rem; font-size: 1.6rem;">🔗 相关性分析结果</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('<div class="tech-card">', unsafe_allow_html=True)
                        st.write(result["answer"])
                        st.markdown('</div>', unsafe_allow_html=True)
                    if "heatmap" in result:
                        render_chart(result, chart_style_param)
        
        if len(categorical_cols) >= 1 and st.button("📊 分布分析", help="分析分类变量的分布"):
            distribution_query = f"""
            请分析分类变量的分布情况，包括：
            1. 各分类变量的频次统计
            2. 生成条形图或饼图
            3. 识别主要类别和异常分布
            4. 提供分布特征的解释
            
            重点分析这些分类列：{', '.join(categorical_cols[:5])}
            """
            
            # 根据快速分析图表类型添加特定要求
            if quick_chart_type == "柱形图":
                distribution_query += "\n\n图表要求：请生成柱形图展示分类变量的频次分布。"
            elif quick_chart_type == "饼图":
                distribution_query += "\n\n图表要求：请生成饼图展示分类变量的比例分布。"
            elif quick_chart_type != "自动选择":
                distribution_query += f"\n\n图表要求：请尽量生成{quick_chart_type}来展示分布分析结果。"
            
            with st.spinner("正在分析分布..."):
                result = dataframe_agent(current_df, distribution_query)
                if result:
                    if "answer" in result:
                        st.write("##### 📊 分布分析结果")
                        st.write(result["answer"])
                    if any(chart_type in result for chart_type in ["bar", "pie"]):
                        render_chart(result, chart_style_param)

# 添加缓存管理功能
if "df" in st.session_state:
    with st.expander("🛠️ 缓存管理"):
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ 清除分析缓存"):
                if hasattr(st, 'cache_data'):
                    st.cache_data.clear()
                    st.success("缓存已清除！")
        with col2:
            cache_info = st.empty()
            cache_info.info("💾 缓存有效期：1小时")
        with col3:
            st.info("📊 缓存基于数据和查询内容生成唯一键")
