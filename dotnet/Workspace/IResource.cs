namespace Microsoft.Workspace
{
    public interface IResource
    {
        string Name { get; set; }

        string[] Path { get; set; }

        WorkspaceImpl Workspace { get; set; }
    }
}
