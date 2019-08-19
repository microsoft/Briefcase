using Microsoft.Azure.KeyVault;
using Microsoft.Workspace;
using System;
using System.Threading.Tasks;
using YamlDotNet.Serialization;

namespace Workspace.Azure.KeyVault
{
    public class KeyVault : Resource, ICredentialProvider
    {
        private readonly Lazy<KeyVaultClient> client = new Lazy<KeyVaultClient>(() =>
            null); // new KeyVaultClient(new KeyVaultClient.AuthenticationCallback("abc-securityToken")));

        public async Task<string> GetSecretAsync(string key)
        {
            //ClientCredential
            //// TODO: catch exception
            var secret = await client.Value.GetSecretAsync(key);

            return secret.Value;
        }

        [YamlMember(Alias = "dnsname")]
        public string DNSName { get; set; }
    }
}
