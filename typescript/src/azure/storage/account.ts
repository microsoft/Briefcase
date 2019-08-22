import Resource from "../../Resource";
import ResourceType from "../../ResourceType";

@ResourceType('azure.storage.account')
export default class AzureStorageAccount extends Resource {
	constructor()
	constructor(public accountname?: string) {
		super();
	}

	getClient() {
		console.log("get_client invoked")
	}

}