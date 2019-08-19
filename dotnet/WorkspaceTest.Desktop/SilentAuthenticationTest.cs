using Microsoft.VisualStudio.TestTools.UnitTesting;
using Microsoft.Workspace.Azure.AD;
using System.Threading.Tasks;

namespace WorkspaceTest
{
    [TestClass]
    public class SilentAuthenticationTest
    {
        [TestMethod]
        public async Task TestSilentAuth()
        {
            var silentAuth = new SilentAuthentication();
            var result = await silentAuth.GetATokenForGraphAsync();
        }
    }
}
