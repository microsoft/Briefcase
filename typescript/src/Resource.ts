import Workspace from "./Workspace";

export default class Resource {
	_name: (string | undefined);
	_workspace: (Workspace | undefined);
	_path: (string[] | undefined);

	init(name: string, workspace: Workspace, path: string[]) {
		this._name = name;
		this._workspace = workspace;
		this._path = path;
	}

	get name() {
		return this._name;
	}

	get workspace() {
		return this._workspace;
	}

	get path() {
		return this._path;
	}
}