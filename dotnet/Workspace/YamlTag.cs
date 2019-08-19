using System;
using System.Collections.Generic;
using System.Text;

namespace Microsoft.Workspace
{
    [System.AttributeUsage(AttributeTargets.Class, Inherited = false, AllowMultiple = false)]
    sealed class YamlTagAttribute : Attribute
    {
        public YamlTagAttribute(string tag)
        {
            this.Tag = tag;
        }

        public string Tag
        {
            get; private set;
        }
    }
}
