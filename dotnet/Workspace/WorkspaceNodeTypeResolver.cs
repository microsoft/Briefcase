using System;
using System.Text.RegularExpressions;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;
using System.Linq;
using System.Reflection;
using System.Collections.Generic;

namespace Microsoft.Workspace
{
    public class WorkspaceNodeTypeResolver : INodeTypeResolver
    {
        private readonly IDictionary<string, Type> tagToTypeMapping;

        public WorkspaceNodeTypeResolver()
        {
            Assembly asm = typeof(YamlTagAttribute).GetTypeInfo().Assembly;

            tagToTypeMapping = asm.DefinedTypes
                    .Select(t => new { Type = t, Attribute = t.GetCustomAttribute<YamlTagAttribute>() })
                    .Where(t => t.Attribute != null)
                    .ToDictionary(t => t.Attribute.Tag, t => t.Type.AsType());

            // TODO: since .NET Standard doesn't have appdomains nor module initializer I'm not sure how to find the other classes
            
            // difference 
            // tagToTypeMapping.Add("azure.serviceprincipal", Type.GetType("Microsoft.Workspace.Azure.AD.ServicePrincipal"))
        }

        public bool Resolve(NodeEvent nodeEvent, ref Type currentType)
        {
            // ignore non-tagged nodes
            if (string.IsNullOrEmpty(nodeEvent.Tag))
                return false;

            // lookup built in tags
            if (tagToTypeMapping.TryGetValue(nodeEvent.Tag,  out currentType))
                return true;

            // lookup using naming scheme
            var className = Regex.Replace(nodeEvent.Tag,
                @"(\b)([a-z])",
                m => m.Groups[1].Value + m.Groups[2].Value.ToUpperInvariant())
                .Substring(1);

            // Pattern: first 2 path elements define the package
            var assemblyName = string.Join(".", className.Split('.').Take(2));

            // e.g. tag name   = azure.storage.account
            // e.g. type name  = Microsoft.Workspace.Azure.Storage.Account
            var typeName = string.Format("Microsoft.Workspace.{0}, Microsoft.Workspace.{1}",
                className,
                assemblyName);

            currentType = Type.GetType(typeName);

            if (currentType == null)
                throw new InvalidOperationException("Unable to find type: " + typeName);

            return true;
        }
    }
}
