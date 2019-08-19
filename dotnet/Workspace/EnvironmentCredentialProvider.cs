using System;
using System.Threading.Tasks;

namespace Microsoft.Workspace
{
    [YamlTag("env")]
    public class EnvironmentCredentialProvider : Resource, ICredentialProvider
    {
        public static readonly EnvironmentCredentialProvider Instance = new EnvironmentCredentialProvider();

        public Task<string> GetSecretAsync(string key)
        {
            return Task.FromResult(Environment.GetEnvironmentVariable(key));
        }
    }
}
