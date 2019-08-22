// TODO: I'd like to understand what the namespace jsyaml is doing here...
import * as yaml from 'js-yaml';
import { resourceTypes } from './ResourceType';
import './azure/storage/account';
import Resource from './Resource';

export default class Workspace {
  root: any;

  // constructor()
  // constructor(resourcesYaml?: string) {
  constructor(resourcesYaml: string) {
    // if (typeof resourcesYaml === 'undefined' || resourcesYaml === null) {
    // resourcesYaml = fs.readFileSync('./resources.yaml', 'utf8');
    // }

    let yamlTypes = resourceTypes.map(t => {
      return new yaml.Type('!' + t.tag, {
        kind: 'mapping',

        construct: function (data) {
          data = data || {}; // in case of empty node

          // create the specified type
          let obj = Object.create(t.type.prototype);

          // copy data into type
          for (const key in data) {
            obj[key] = data[key];
          }

          return obj
        },

        instanceOf: t,
      });
    });

    let schema = yaml.Schema.create(yamlTypes);

    this.root = yaml.safeLoad(resourcesYaml, { schema: schema });

    // make sure workspace, path and name are assigned to each Resource
    this.visit((node, path, name) => node.init(name, this, path))
  }

  private visit<T>(action: (node: Resource, path: string[], name: string) => (T | undefined),
    path: string[] = [],
    node: any = undefined): T[] {

    if (node instanceof Workspace) {
      return [];
    }

    if (node === undefined) {
      node = this.root;
    }

    let ret: T[] = []

    if (node instanceof Resource) {
      let v = action(node, path, path[path.length - 1]);
      if (v !== undefined) {
        ret.push(v);
      }
    }

    for (const key in node) {
      let child = node[key];

      if (child instanceof Resource || child instanceof Object) {
        ret = [...ret, ...this.visit(action, [...path, key], child)];
      }
    }

    return ret
  }

  /**
   * Find resoure by name or path.
   * @param name name or path to resource. can be split by / or .
   */
  get(name: string): Resource[] {
    let path = name.split(/[\\\/\.]/)
    if (path.length === 1) {
      return this.visit((node, _path, nodeName) => nodeName === name ? node : undefined)
    }
    else {
      let r = this.root;

      for (const n of path) {
        r = r[n];
      }

      return [r];
    }

  }

  /**
   * Find all resources of a given type.
   * @param type Type of the resources.
   */
  getAllOfType(type: Function): Resource[] {
    return this.visit((node, _path, _nodeName) => node instanceof type ? node : undefined)
  }
}
