using Microsoft.VisualStudio.TestTools.UnitTesting;
using Microsoft.Workspace;
using Microsoft.Workspace.Azure.Storage;
using System.IO;
using System.Linq;

namespace Microsoft.WorkspaceTest
{
    [TestClass]
    public class YamlTest
    {
        private string yaml = @"
datasources: # just convention, support arbitrary structure
  folder1:
    myblobsource1: &myblobsource1 
      !azure.storage.account
      accountname: webscaleai
";

        [TestMethod]
        public void TestTypeResolution()
        {
            var ws = new WorkspaceImpl(new StringReader(yaml));

            var resources = ws.Resources.ToList();

            Assert.AreEqual(1, resources.Count);
            Assert.IsInstanceOfType(resources.First(), typeof(Account));

            var storageAccount = resources.First() as Account;
            Assert.AreEqual("webscaleai", storageAccount.Name);

            IResource storageAccountResource = storageAccount;
            Assert.AreEqual("myblobsource1", storageAccountResource.Name);
            CollectionAssert.AreEqual(new[] { "datasources", "folder1" }, storageAccountResource.Path);
            Assert.AreSame(ws, storageAccountResource.Workspace);
        }

        [TestMethod]
        public void TestLookupByKey()
        {
            var ws = new WorkspaceImpl(new StringReader(yaml));

            var q = ws["myblobsource1"];
            Assert.AreEqual(1, q.Count());

            Assert.IsInstanceOfType(q.First(), typeof(Account));
        }

        [TestMethod]
        public void TestLookupByPath()
        {
            var ws = new WorkspaceImpl(new StringReader(yaml));

            var q = ws["datasources/folder1/myblobsource1"];
            Assert.AreEqual(1, q.Count());

            Assert.IsInstanceOfType(q.First(), typeof(Account));
        }
    }
}
