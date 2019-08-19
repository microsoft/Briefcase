using System.IO;
using System.Threading.Tasks;
using YamlDotNet.Serialization;

namespace Microsoft.Workspace.Azure.Storage
{
    public class Blob : Resource
    {
        [YamlMember(Alias = "containername")]
        public string ContainerName { get; set; }

        public string Path { get; set; }

        [YamlMember(Alias = "datasource")]
        public Account DataSource { get; set; }

        public Task DownloadToAsync(Stream target)
        {
            return Task.FromResult(true);
        }
    }
}
