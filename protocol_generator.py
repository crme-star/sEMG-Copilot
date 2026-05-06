import os
import logging
from typing import Dict, Optional
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sEMG_Deployer")

class ProtocolGenerator:
    """
    负责生成上下位机通信协议及部署代码的生成器类。
    """
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        
        if not self.api_key:
            logger.warning("LLM_API_KEY is not set. API calls will fail.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.model = "gpt-3.5-turbo" 

    def _build_prompts(self, context: Dict[str, any]) -> tuple[str, str]:
        """构建底层系统和用户提示词"""
        sys_prompt = (
            "You are an expert embedded software engineer. "
            "Your task is to generate robust serial communication protocols between a host and an MCU. "
            "The protocol MUST include explicit frame headers, data payload definition, "
            "checksum calculation, and frame tails. Output ONLY valid Markdown code blocks for Python (Host) and C (MCU)."
        )

        user_prompt = (
            "Generate deployment code based on the following hardware context:\n"
            f"- Host System: {context.get('host_system', 'Unknown')}\n"
            f"- MCU Architecture: {context.get('mcu_arch', 'Unknown')}\n"
            f"- Output Classes: {context.get('output_classes', 0)} discrete actions\n"
            f"- Target Baudrate: {context.get('baudrate', 115200)}\n"
        )
        return sys_prompt, user_prompt

    def generate(self, context: Dict[str, any]) -> Optional[str]:
        """
        基于硬件上下文生成部署代码
        
        Args:
            context (Dict[str, any]): 包含系统硬件信息的字典
            
        Returns:
            Optional[str]: 生成的代码字符串，若失败则返回 None
        """
        sys_prompt, user_prompt = self._build_prompts(context)

        logger.info(f"Initiating protocol generation for MCU: {context.get('mcu_arch')}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1, 
                max_tokens=1500
            )
            logger.info("Generation completed successfully.")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"API Request failed: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    hardware_context = {
        "host_system": "Raspberry Pi 4 (Python 3.8+)",
        "mcu_arch": "STM32F407 (C99)",
        "output_classes": 5,
        "baudrate": 115200
    }
    
    generator = ProtocolGenerator()
    generated_code = generator.generate(hardware_context)
    
    if generated_code:
        print("\n--- GENERATED PROTOCOL ---\n")
        print(generated_code)
        print("\n--- END OF PROTOCOL ---\n")
