import Workspace from "../src/Workspace"
import AzureStorageAccount from "../src/azure/storage/account";

/**
 * Basic YAML Tests
 */
describe("YAML test", () => {
  let yaml1 = `
datasources: # just convention, support arbitrary structure
  folder1:
    myblobsource1: &myblobsource1 
      !azure.storage.account
      accountname: webscaleai
`;

  it("validate object w/o properties", () => {
    let yaml = `
 blob1:
  !azure.storage.account
 `;

    let ws = new Workspace(yaml)

    let blob1 = ws.getAllOfType(AzureStorageAccount)
    expect(blob1.length).toEqual(1)
    expect(blob1[0]).toBeInstanceOf(AzureStorageAccount)
  })

  it("validate unknown element", () => {
    let ws = new Workspace(yaml1);

    let obj = ws.get("unknown_element")
    expect(obj.length).toEqual(0)

    obj = ws.getAllOfType(Workspace)
    expect(obj.length).toEqual(0)
  })


  it("validate getAllOfType", () => {
    let ws = new Workspace(yaml1);

    let blob1 = ws.getAllOfType(AzureStorageAccount)
    expect(blob1.length).toEqual(1)
    expect(blob1[0]).toBeInstanceOf(AzureStorageAccount)
  })

  it("validate paths are populated", () => {
    let ws = new Workspace(yaml1);
    let blob1 = ws.get('myblobsource1');

    expect(blob1.length).toEqual(1)
    expect(blob1[0]).toBeInstanceOf(AzureStorageAccount)
  })

  it("validate path using /", () => {
    let ws = new Workspace(yaml1);

    let blob1 = ws.get('datasources/folder1/myblobsource1');

    expect(blob1.length).toEqual(1)
    expect(blob1[0]).toBeInstanceOf(AzureStorageAccount)
  })

  it("Parse simple yaml", () => {
    var ws = new Workspace(yaml1);

    var blob = ws.root.datasources.folder1.myblobsource1;
    expect(blob).toBeInstanceOf(AzureStorageAccount);

    blob.getClient();

    expect(ws).toBeInstanceOf(Workspace);
  })
})
