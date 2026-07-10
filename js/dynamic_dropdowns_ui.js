import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Ovelia.DynamicDropdownsPro",
    async beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
        if (nodeData.name === "ComfyUI_Dynamic_Dropdowns_Demo") {
            
            // 1. Core initialization when the node is spawned on the canvas
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                
                // Set the default size to accommodate the sleek layout
                this.size = [550, 350];
                
                // Add the dynamic interactive buttons directly onto the node layout
                this.addWidget("button", "➕ Add Slot", null, () => {
                    const dropdownCount = this.widgets.filter(w => w.name.startsWith("custom_slot_")).length;
                    this.addWidget("combo", `custom_slot_${dropdownCount + 1}`, "Select...", () => {}, { values: ["Option A", "Option B"] });
                    this.setSize([550, Math.max(350, 150 + (this.widgets.length * 40))]);
                });

                this.addWidget("button", "➖ Remove Slot", null, () => {
                    const dropdowns = this.widgets.filter(w => w.name.startsWith("custom_slot_"));
                    if (dropdowns.length > 0) {
                        this.removeWidget(dropdowns[dropdowns.length - 1]);
                        this.setSize([550, Math.max(350, 150 + (this.widgets.length * 40))]);
                    }
                });
            };

            // 2. Overriding the background draw call to inject custom hardware style
            nodeType.prototype.onDrawBackground = function (ctx, canvas) {
                // If the node is collapsed, let LiteGraph handle the default minimized render
                if (this.flags.collapsed) return;

                ctx.save();

                // --- 🛡️ CUSTOM CARD BASE & PREMIUM BORDER ---
                ctx.lineWidth = 1;
                
                // Outer subtle cyan/blue trim glow
                ctx.strokeStyle = "rgba(0, 206, 209, 0.5)"; 
                
                // Premium deep dark metallic gray base color
                ctx.fillStyle = "rgba(22, 26, 32, 0.98)";   
                
                // Rounding the card profile corners
                ctx.beginPath();
                ctx.roundRect(0, 0, this.size[0], this.size[1], 15);
                ctx.fill();
                ctx.stroke();

                // --- 🏷️ PRO LABELS & SLIDER ACCENTS ---
                ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
                ctx.font = "bold 16px sans-serif";
                ctx.textAlign = "left";
                ctx.fillText("🎭 Dynamic Dropdowns (Pro Mode)", 40, 30);

                ctx.restore();
            };
        }
    }
});
