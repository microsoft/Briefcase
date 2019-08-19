using Microsoft.VisualStudio.TestTools.UnitTesting;
using Microsoft.Workspace;
using Microsoft.Workspace.Azure.Storage;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Microsoft.WorkspaceTest.Desktop
{
    [TestClass]
    public class AzureStorageTest
    {
        [TestMethod]
        public async Task TestDownload()
        {
            var ws = new WorkspaceImpl("yamls/azure/storage");

            var dataset = ws["dataset"].First() as Blob; 
        }
    }
}
