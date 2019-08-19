using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace Microsoft.Workspace
{
    public interface ICredentialProvider
    {
        Task<string> GetSecretAsync(string key);
    }
}
