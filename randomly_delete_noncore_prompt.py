import random

class RandomlyDeleteNoncorePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True}),
                "core_element": ("STRING", {"default": "爱心"}),
                "separator": ("STRING", {"default": "，"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
            }
        }

    @classmethod
    def IS_CHANGED(cls):
        return True

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("kept_prompt", "deleted_prompt",)
    FUNCTION = "filter_elements"
    CATEGORY = "提示词处理☕️"

    def filter_elements(self, input_text, core_element, separator, seed):
        if seed != -1:
            random.seed(seed)
        else:
            random.seed()

        elements = [e.strip() for e in input_text.split(separator) if e.strip()]
        core_elements = [e.strip() for e in core_element.split(separator) if e.strip()]
        
        kept = [e for e in elements if e in core_elements]
        deleted = []

        remaining = [e for e in elements if e not in core_elements]
        temp_kept = []

        for item in remaining:
            if random.choice([True, False]):
                temp_kept.append(item)
            else:
                deleted.append(item)

        # ✅ 强制至少删除一个非核心元素
        if not deleted and temp_kept:
            force_delete = random.choice(temp_kept)
            temp_kept.remove(force_delete)
            deleted.append(force_delete)

        kept += temp_kept

        return (
            separator.join(kept),
            separator.join(deleted)
        )
