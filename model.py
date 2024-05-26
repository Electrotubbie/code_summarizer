from transformers import AutoTokenizer
from transformers import AutoModelWithLMHead
from transformers import SummarizationPipeline


hug_repo = "SEBIS/code_trans_t5_base_code_documentation_generation_python"

summarize = SummarizationPipeline(
    model=AutoModelWithLMHead.from_pretrained(hug_repo),
    tokenizer=AutoTokenizer.from_pretrained(hug_repo, skip_special_tokens=True),
    # device=0
)
