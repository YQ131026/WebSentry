import requests
import openai
from config.config import AI_CONFIG
from utils.logger_config import logger

def summarize_results(results):
    if 'enabled' not in AI_CONFIG:
        logger.error("AI_CONFIG 中缺少 'enabled' 键")
        return None
    if not AI_CONFIG['enabled']:
        logger.info("AI 总结功能未启用")
        return None

    logger.info(f"使用 {AI_CONFIG['provider']} 进行 AI 总结")

    if AI_CONFIG['provider'] == 'ollama':
        return _summarize_ollama(results)
    elif AI_CONFIG['provider'] == 'openai':
        return _summarize_openai(results)
    else:
        logger.error(f"不支持的 AI 提供商: {AI_CONFIG['provider']}")
        return None

def _summarize_ollama(results):
    config = AI_CONFIG['ollama']
    prompt = f"请对以下网站监控结果进行简要总结，突出重要信息：\n\n{results}"

    try:
        logger.info(f"正在调用 Ollama API: {config['api_base']}")
        response = requests.post(
            f"{config['api_base']}/api/generate",
            json={
                "model": config['model'],
                "prompt": prompt,
                "stream": False
            },
            timeout=config['timeout']
        )
        response.raise_for_status()
        summary = response.json()['response']
        logger.info("Ollama API 调用成功")
        return summary
    except Exception as e:
        logger.error(f"Ollama API 调用失败: {str(e)}")
        return None

def _summarize_openai(results):
    config = AI_CONFIG['openai']
    openai.api_key = config['api_key']
    openai.api_base = config['api_base']

    try:
        logger.info(f"正在调用 OpenAI API: {config['api_base']}")
        response = openai.ChatCompletion.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": "你是一个网站监控结果分析助手。请提供简洁的总结。"},
                {"role": "user", "content": f"请对以下网站监控结果进行简要总结，突出重要信息：\n\n{results}"}
            ],
            timeout=config['timeout']
        )
        summary = response.choices[0].message['content']
        logger.info("OpenAI API 调用成功")
        return summary
    except Exception as e:
        logger.error(f"OpenAI API 调用失败: {str(e)}")
        return None
