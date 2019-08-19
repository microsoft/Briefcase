using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using YamlDotNet.Serialization;

namespace Microsoft.Workspace.Azure.AD
{
    public class ServicePrincipal : Resource, ICredentialProvider
    {
        [YamlMember(Alias = "clientid")]
        public string ClientId { get; set; }

        public Task<string> GetSecretAsync(string key)
        {
            // ConfidentialClientApplicationBuilder.Create("abc")


            throw new NotImplementedException();
        }
    }
}
