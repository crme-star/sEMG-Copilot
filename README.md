# 🦾 sEMG-Copilot: 面向肌电信号与具身智能的多智能体协作框架

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Concept%20%26%20Demo-orange)

## 项目背景与核心痛点
在表面肌电（sEMG）信号处理与具身智能（如仿生机械手）的协同控制领域，研究人员长期面临以下痛点：
1. **跨设备对齐难**：不同采集设备的采样率、噪声分布差异巨大，数据清洗规则繁琐。
2. **模型试错成本高**：从传统特征工程到深度学习（CNN/RNN/Mamba）的架构搭建极度依赖人工经验。
3. **软硬件部署断层**：上位机（Python/深度学习框架）与下位机（STM32/C语言）之间的通信协议编写与动作映射耗时费力。

**sEMG-Copilot** 旨在引入大语言模型（LLM）与多智能体（Multi-Agent）架构，将自然语言指令转化为端到端的信号处理代码、模型架构及嵌入式通信协议，极大降低开发门槛。

##  核心架构：多智能体协作流 (Multi-Agent Workflow)
本项目由三个核心 Agent 组成，通过长链推理实现全流程覆盖：

- Agent A (预处理专家)**：输入原始数据集描述，自动生成带异常检测、滤波去噪、重采样对齐的 Python 脚本。
- Agent B (模型拓扑构建器)**：根据特征维度和实时性要求，动态生成 PyTorch 网络结构（如适用于边缘计算的轻量级 CNN-GRU）。
- Agent C (软硬件协同部署助手)**：核心难点攻坚。接收控制意图，自动生成上位机串口推理脚本及下位机（如 STM32）的 C 语言解析与执行机构驱动代码。

## 快速开始 (Demo)
目前本项目已提供 **Agent C** 的概念验证（PoC）代码，演示如何通过大模型 API 自动生成上下位机通信协议。

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置你的 LLM API Key (支持兼容 OpenAI 格式的 API)
export LLM_API_KEY="your_api_key_here"
export LLM_BASE_URL="your_base_url_here"

# 3. 运行下位机代码生成 Demo
python agent_c_demo.py
