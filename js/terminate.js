import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
	name: "cg.customnodes.Terminate",
	version: 1,
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.description.includes('terminator')) {
			const onExecuted = nodeType.prototype.onExecuted;

			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				const terminate = message.terminate.join('');
				if (terminate==="yes") { 
					document.getElementById("autoQueueCheckbox").checked = false;
					api.interrupt(); 
				}
			}
		}
	},
});
