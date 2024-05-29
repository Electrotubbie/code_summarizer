from transformers import AutoTokenizer
from transformers import AutoModelWithLMHead
from transformers import SummarizationPipeline


hug_repo = "SEBIS/code_trans_t5_base_code_documentation_generation_python"

summarize = SummarizationPipeline(
    model=AutoModelWithLMHead.from_pretrained(hug_repo),
    tokenizer=AutoTokenizer.from_pretrained(hug_repo, skip_special_tokens=True),
    # device=0
)


def get_model_result(code):
    if isinstance(code, str):
        return summarize(code)[0]['summary_text']
    elif isinstance(code, list):
        return {obj['name']: summarize(obj['code'])[0]['summary_text'] for obj in code}
    else:
        raise ValueError(f'{code} is not list or str.')
