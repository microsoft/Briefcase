using YamlDotNet.Serialization;
using Microsoft.WindowsAzure.Storage;

namespace Microsoft.Workspace.Azure.Storage
{
    public class Account : Resource
    {
        [YamlMember(Alias = "accountname")]
        public string Name { get; set; }

        public CloudStorageAccount Client
        {
            get
            {
                // TODO: lookup subscriptions
                // search for storage account
                // TODO: lookup keyvault
                // TODO: support service prinicipal
                // TODO: support env variable
                // CloudStorageAccount.Parse
                return null;
            }
        }
    }
}
