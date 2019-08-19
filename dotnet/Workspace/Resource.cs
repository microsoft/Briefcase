using System.Collections.Generic;

namespace Microsoft.Workspace
{
    public class Resource : IResource
    {
        string IResource.Name { get; set; }

        WorkspaceImpl IResource.Workspace { get; set; }

        string[] IResource.Path { get; set; }

        public ICredentialProvider CredentialProvider { get; set; }

        IEnumerable<ICredentialProvider> GetCredentialProviders()
        {
            if (CredentialProvider != null)
            {
                yield return CredentialProvider;
                yield break;
            }

            yield return EnvironmentCredentialProvider.Instance;
        }
    }
}
