from typing import Any

from pandasai.pipelines.logic_unit_output import LogicUnitOutput
from ..base_logic_unit import BaseLogicUnit
from ..pipeline_context import PipelineContext
from ...prompts.generate_python_code import GeneratePythonCodePrompt
from ...prompts.generate_python_code_with_sql import GeneratePythonCodeWithSQLPrompt
from ...prompts.base import BasePrompt
from ...helpers.logger import Logger


class PromptGeneration(BaseLogicUnit):
    """
    Code Prompt Generation Stage
    """

    pass

    def execute(self, input: Any, **kwargs) -> Any:
        """
        This method will return output according to
        Implementation.

        :param input: Your input data.
        :param kwargs: A dictionary of keyword arguments.
            - 'logger' (any): The logger for logging.
            - 'config' (Config): Global configurations for the test
            - 'context' (any): The execution context.

        :return: The result of the execution.
        """
        self.context: PipelineContext = kwargs.get("context")
        self.logger: Logger = kwargs.get("logger")

        prompt = self.get_chat_prompt(self.context)
        self.logger.log(f"Using prompt: {prompt}")

        return LogicUnitOutput(
            prompt,
            True,
            "Prompt Generated Successfully",
            {"generated_prompt": prompt.render()},
        )

    def get_chat_prompt(self, context: PipelineContext) -> [str, BasePrompt]:
        viz_lib = ""
        if context.config.data_viz_library:
            viz_lib = context.config.data_viz_library

        output_type = context.get("output_type")

        return (
            GeneratePythonCodeWithSQLPrompt(
                context=context,
                last_code_generated=context.get("last_code_generated"),
                viz_lib=viz_lib,
                output_type=output_type,
            )
            if context.config.direct_sql
            else GeneratePythonCodePrompt(
                context=context,
                last_code_generated=context.get("last_code_generated"),
                viz_lib=viz_lib,
                output_type=output_type,
            )
        )