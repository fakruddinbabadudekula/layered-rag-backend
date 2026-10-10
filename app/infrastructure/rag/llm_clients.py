from dataclasses import dataclass
from app.rag.interface.llm_client import AsyncLLMClient
from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import time
import asyncio
import logging
from logging import getLogger

logger = getLogger(__name__)



@dataclass
class RetryConfig:
    max_llm_call_retries: int
    llm_call_asyn_timeout: int
    retryable_llm_exceptions: set[BaseException]


class LLMClient(AsyncLLMClient):
    def __init__(self, llm: BaseChatModel, retry_config: RetryConfig):
        self._llm = llm
        self._retry_config = retry_config

    async def _call_llm_with_retries(self, prompt: str):
        config = self._retry_config

        @retry(
            stop=stop_after_attempt(config.max_llm_call_retries),
            wait=wait_exponential(multiplier=1, min=2, max=32),  # 2s, 4s, 8s, 16s, 32s
            retry=retry_if_exception_type(config.retryable_llm_exceptions),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,  # Raise the original exception after all retries fail
        )
        async def _call(prompt: str) -> AIMessage:
            try:
                start = time.perf_counter()
                response = await asyncio.wait_for(
                    self._llm.ainvoke(prompt), timeout=config.llm_call_asyn_timeout
                )
                duration = time.perf_counter() - start
                logger.info(
                    "response_is_generated_successfully", extra={"duration": duration}
                )
                return response
            except config.retryable_llm_exceptions as e:
                logger.warning("llm_call_failed_retrying", extra={"error": str(e)})
                raise

        return await _call(prompt)

    async def call(self, prompt: str) -> AIMessage:
        """Generate a response from the language model.

        Args:
            prompt: str
                prompt sent to the language model.

        Returns:
            AIMessage:
                Generated response.
        """
        return await self._call_llm_with_retries(prompt=prompt)
