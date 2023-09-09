import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "cg.customnodes.ShowText",
	version: 2,
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.description.includes('displays_text')) {
			const onExecuted = nodeType.prototype.onExecuted;
			const onExecutionStart = nodeType.prototype.onExecutionStart;

			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				var text = message.text_displayed.join('');
				var w = this.widgets?.find((w) => w.name === "text_display");
				if (w === undefined) {
					w = ComfyWidgets["STRING"](this, "text_display", ["STRING", { multiline: true }], app).widget;
					w.inputEl.readOnly = true;
					w.inputEl.style.opacity = 0.6;
				}
				w.value = text;
				this.onResize?.(this.size);
			}
				
			nodeType.prototype.onExecutionStart = function () {
				onExecutionStart?.apply(this);
				var w = this.widgets?.find((w) => w.name === "text_display"); 
				if (w !== undefined) {
					w.value = '';
					this.onResize?.(this.size);
				}
			};
		}
	},
});
