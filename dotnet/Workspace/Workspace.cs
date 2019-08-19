using System;
using System.Collections.Generic;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;
using System.Linq;

namespace Microsoft.Workspace
{
    public delegate T ResourceSelector<T>(Resource resource, IEnumerable<string> path, string name);
    public delegate void ResourceAction(Resource resource, IEnumerable<string> path, string name);

    public class WorkspaceImpl
    {
        private object root;

        public WorkspaceImpl(string path = ".")
        {
            using (var reader = new StreamReader(File.OpenRead(Path.Combine(path, "resources.yaml"))))
            {
                Parse(reader);
            }
        }

        public WorkspaceImpl(TextReader resourcesYamlReader)
        {
            Parse(resourcesYamlReader);
        }

        private void Parse(TextReader resourcesYamlReader)
        {
            var deserializer = new DeserializerBuilder()
                .WithNamingConvention(new CamelCaseNamingConvention())
                .WithNodeTypeResolver(new WorkspaceNodeTypeResolver())
                .Build();

            root = deserializer.Deserialize(resourcesYamlReader);

            // setup path, name and workspace
            Resources = Select((resource, path, name) =>
            {
                IResource res = resource as IResource;
                res.Workspace = this;
                res.Path = path.ToArray();
                res.Name = name;
                return resource;
            })
            .ToList();
        }

        private IEnumerable<T> SelectImpl<T>(ResourceSelector<T> visitor, List<string> path, object node, string name)
        {
            if (node is Resource resource)
            {
                var ret = visitor(resource, path, name);

                yield return ret;
                yield break;
            }

            if (node is IDictionary<object, object> dict)
            {
                if (name != null)
                    path.Add(name);

                foreach (var item in dict)
                {
                    var ret = SelectImpl(visitor, path, item.Value, item.Key.ToString());

                    // if we found something
                    foreach (var r in ret)
                        yield return r;
                }

                if (name != null)
                    path.RemoveAt(path.Count - 1);

                yield break;
            }

            throw new ArgumentException("Unknown type in tree: " + node.GetType());
        }
        private IEnumerable<T> Select<T>(ResourceSelector<T> visitor)
        {
            return SelectImpl(visitor, new List<string>(), root, null);
        }

        public List<Resource> Resources { get; private set; }

        public IEnumerable<Resource> this[string key]
        {
            get
            {
                var components = key.Split('.', '/').ToArray();
                var path = string.Join(".", components.Take(components.Count() - 1));
                var name = components.Last();

                // find by name
                if (path.Length == 0)
                    return Resources
                        .OfType<IResource>()
                        .Where(r => r.Name == name)
                        .OfType<Resource>();

                // find by path
                return Resources
                    .OfType<IResource>()
                    .Where(r => r.Name == name && string.Join(".", r.Path) == path)
                    .OfType<Resource>();
            }
        }
    }
}
