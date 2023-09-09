import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "cg.customnodes.SelfModify",
	version: 1,
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.description.includes('self_modify')) {
			const onExecuted = nodeType.prototype.onExecuted;

			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				message.self_modify.forEach(self_modify => {
                    var w = this.widgets?.find((w) => w.name === self_modify[0])
                    if (w) {
                        w.value = self_modify[1];
                        this.onResize?.(this.size);
                    }
                });

			}
		}
	},
});