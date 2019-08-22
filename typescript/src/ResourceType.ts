import { ResourceTypeInfo } from './ResourceTypeInfo';

export const resourceTypes: ResourceTypeInfo[] = [];
export default function ResourceType(tag: string) {
	return function (target: Function) {
		resourceTypes.push(new ResourceTypeInfo(target, tag));
	};
}
