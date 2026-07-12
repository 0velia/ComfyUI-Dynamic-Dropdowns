import os
import sys
import json
import webview

class Api:
    def __init__(self):
        # Resolve project directories correctly relative to the execution root
        self.base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.lists_dir = os.path.join(self.base_dir, "lists")
        
        if not os.path.exists(self.lists_dir):
            os.makedirs(self.lists_dir)

    def save_list_asset(self, filename, content):
        """Catches text asset streams from the UI and commits them to the local filesystem."""
        try:
            # Ensure safe filename structure
            safe_name = os.path.basename(filename)
            if not safe_name.endswith('.txt'):
                safe_name += '.txt'
                
            target_path = os.path.join(self.lists_dir, safe_name)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            print(f"[Backend] Synced list asset: {safe_name}")
            return {"status": "success", "message": f"Saved {safe_name}"}
        except Exception as e:
            print(f"[Backend Error] Failed to save asset: {str(e)}")
            return {"status": "error", "message": str(e)}

    def build_node(self, slots_json):
        """Generates a highly robust, dynamic custom node pipeline __init__.py inside the workspace."""
        try:
            slots = json.loads(slots_json)
            print(f"[Backend] Compiling custom node architecture for {len(slots)} configuration slots.")
            
            # Formulate code block template to deploy into __init__.py
            code_template = f'''import os
import glob

class DynamicDropdownNode:
    @classmethod
    def INPUT_TYPES(cls):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        lists_dir = os.path.join(base_dir, "lists")
        
        inputs = {{
            "required": {{}},
            "optional": {{
                "input_string": ("STRING", {{"forceInput": True}}),
                "clip": ("CLIP",),
            }}
        }}
        
        # Statically declared base order sequence built via Desktop Companion App
        ui_order = {[slot['name'].replace(" ", "_").lower() for slot in slots]}
        
        # Pre-seed slots from directory
        if os.path.exists(lists_dir):
            # Dynamic lookup for lists assets
            for key in ui_order:
                file_path = os.path.join(lists_dir, f"{{key}}.txt")
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        options = [line.strip() for line in f.readlines() if line.strip()]
                    inputs["required"][key] = (options if options else ["None"],)
            
            # Grab any floating text assets dropped into the folder later
            all_txt_files = glob.glob(os.path.join(lists_dir, "*.txt"))
            for file_path in all_txt_files:
                file_name = os.path.basename(file_path).replace(".txt", "")
                if file_name not in inputs["required"]:
                    with open(file_path, "r", encoding="utf-8") as f:
                        options = [line.strip() for line in f.readlines() if line.strip()]
                    inputs["required"][file_name] = (options if options else ["None"],)
        
        # Fallback layout validation layer
        if not inputs["required"]:
            inputs["required"]["placeholder"] = (["(Add your .txt files inside lists/)"],)
            
        return inputs

    RETURN_TYPES = ("STRING", "CONDITIONING")
    RETURN_NAMES = ("PROMPT_STRING", "CONDITIONING")
    FUNCTION = "execute"
    CATEGORY = "🎭 Dynamic Dropdowns"

    def execute(self, clip=None, input_string="", **kwargs):
        selections = []
        
        # Bundle values matching the keyword arguments mapping order sequence
        for key, val in kwargs.items():
            clean_val = str(val).strip()
            if clean_val and clean_val != "None" and not clean_val.startswith("("):
                selections.append(clean_val)
                
        if input_string and input_string.strip():
            selections.insert(0, input_string.strip())
            
        final_string = ", ".join(selections)
        # Deep scrub structural syntax blocks
        final_string = final_string.replace('"', '').replace('\\\\', '').replace(', ,', ',')
        
        conditioning = []
        if clip is not None:
            tokens = clip.tokenize(final_string)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            conditioning = [[cond, {{"pooled_output": pooled}}]]
            
        return (final_string, conditioning)

NODE_CLASS_MAPPINGS = {{
    "DynamicDropdownNode": DynamicDropdownNode
}}

NODE_DISPLAY_NAME_MAPPINGS = {{
    "DynamicDropdownNode": "🎭 Dynamic Dropdowns"
}}
'''
            # Deploy output direct to root configuration layout context path
            target_init_path = os.path.join(self.base_dir, "__init__.py")
            with open(target_init_path, "w", encoding="utf-8") as f:
                f.write(code_template)
                
            print(f"[Backend] Custom node compilation committed to target path: {target_init_path}")
            return {"status": "success", "message": "Node built successfully!"}
        except Exception as e:
            print(f"[Backend Error] Node building sequence failure: {str(e)}")
            return {"status": "error", "message": str(e)}

def load_ui_interface():
    # Resolve absolute resource paths to point directly to interface documents
    current_dir = os.path.dirname(os.path.realpath(__file__))
    html_ui_path = os.path.join(current_dir, "generator.html")
    
    if not os.path.exists(html_ui_path):
        print(f"[Fatal Launch Failure] Missing interface component template file mapping asset: {html_ui_path}")
        sys.exit(1)
        
    api = Api()
    
    # Initialize high-performance framework window with hardware layer bindings
    window = webview.create_window(
        title="🎭 ComfyUI Dynamic Dropdowns - Node Builder Assistant",
        url=html_ui_path,
        js_api=api,
        width=460,
        height=720,
        resizable=True,
        min_size=(380, 640),
        background_color='#09090f'
    )
    
    webview.start(debug=False)

if __name__ == "__main__":
    load_ui_interface()