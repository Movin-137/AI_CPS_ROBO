from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMInteraction:
    def __init__(self):
        model_name = "microsoft/phi-2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float16
        ).to("cpu")

    def get_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs["input_ids"], max_length=50, num_beams=2
        )
        reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return reply
