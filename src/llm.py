from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import gc
from os import environ
from transformers.utils import is_flash_attn_2_available
def init_llm(model_name=environ["LLM_MODEL"]):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if is_flash_attn_2_available():
        model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.float16,
        attn_implementation="flash_attention_2")
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.float16)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        try:
            model.to(device)
        except torch.cuda.OutOfMemoryError:
            model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype="auto")
            device = torch.device("cpu")
    return model, tokenizer, device



model, tokenizer, device = init_llm()
def generate_response(query, context=None, temperature:float=0.1, max_length=50, num_beams=5):
    if torch.cuda.is_available():
        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    if context:
        input_text = f"Context: {context}\nQuery: {query}\nResponse:"
    else:
        input_text = f"Query: {query}\nResponse:"
    
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=max_length,
            num_beams=num_beams,
            early_stopping=True,
            temperature=temperature 

        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    response_text = response.split("response:")[1].strip() if "response:" in response else response
    
    return response_text
