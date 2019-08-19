using Microsoft.Identity.Client;
using System.Threading.Tasks;
using System.Linq;

namespace Microsoft.Workspace.Azure.AD
{
    public class SilentAuthentication
    {
        private string clientId;
        private string tenantId;

        public SilentAuthentication()
        {
            clientId = "42e402c8-afee-41a0-99f8-ab51ca6c6dce";
            tenantId = "72f988bf-86f1-41af-91ab-2d7cd011db47";
        }

        public string ClientId { get; set; }

        public async Task<AuthenticationResult> GetATokenForGraphAsync()
        {
            // string authority = "https://login.microsoftonline.com/contoso.com";
            string[] scopes = new string[] { "user.read" };


            IPublicClientApplication app = PublicClientApplicationBuilder
                .Create(clientId)
                .WithTenantId(tenantId)
                .Build();

            var accounts = await app.GetAccountsAsync();

            AuthenticationResult result = null;
            if (accounts.Any())
            {
                result = await app
                    .AcquireTokenSilent(scopes, accounts.FirstOrDefault())
                    .ExecuteAsync();
            }
            else
            {
                try
                {
                    result = await app
                            .AcquireTokenByIntegratedWindowsAuth(scopes)
                            .ExecuteAsync();
                }
                catch (MsalUiRequiredException)
                {
                    // MsalUiRequiredException: AADSTS65001: The user or administrator has not consented to use the application 
                    // with ID '{appId}' named '{appName}'.Send an interactive authorization request for this user and resource.

                    // you need to get user consent first. This can be done, if you are not using .NET Core (which does not have any Web UI)
                    // by doing (once only) an AcquireToken interactive.

                    // If you are using .NET core or don't want to do an AcquireTokenInteractive, you might want to suggest the user to navigate
                    // to a URL to consent: https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={clientId}&response_type=code&scope=user.read

                    var url = string.Format("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={0}&response_type=code&response_mode=query&scope=user.read",
                        clientId);

                    System.Diagnostics.Process.Start(url);

                    // AADSTS50079: The user is required to use multi-factor authentication.
                    // There is no mitigation - if MFA is configured for your tenant and AAD decides to enforce it, 
                    // you need to fallback to an interactive flows such as AcquireTokenAsync or AcquireTokenByDeviceCode
                }
                catch (MsalServiceException)
                {
                    // Kind of errors you could have (in ex.Message)

                    // MsalServiceException: AADSTS90010: The grant type is not supported over the /common or /consumers endpoints. Please use the /organizations or tenant-specific endpoint.
                    // you used common.
                    // Mitigation: as explained in the message from Azure AD, the authoriy needs to be tenanted or otherwise organizations

                    // MsalServiceException: AADSTS70002: The request body must contain the following parameter: 'client_secret or client_assertion'.
                    // Explanation: this can happen if your application was not registered as a public client application in Azure AD 
                    // Mitigation: in the Azure portal, edit the manifest for your application and set the `allowPublicClient` to `true` 
                }
                catch (MsalClientException)
                {
                    // Error Code: unknown_user Message: Could not identify logged in user
                    // Explanation: the library was unable to query the current Windows logged-in user or this user is not AD or AAD 
                    // joined (work-place joined users are not supported). 

                    // Mitigation 1: on UWP, check that the application has the following capabilities: Enterprise Authentication, 
                    // Private Networks (Client and Server), User Account Information

                    // Mitigation 2: Implement your own logic to fetch the username (e.g. john@contoso.com) and use the 
                    // AcquireTokenByIntegratedWindowsAuthAsync overload that takes in the username

                    // Error Code: integrated_windows_auth_not_supported_managed_user
                    // Explanation: This method relies on an a protocol exposed by Active Directory (AD). If a user was created in Azure 
                    // Active Directory without AD backing ("managed" user), this method will fail. Users created in AD and backed by 
                    // AAD ("federated" users) can benefit from this non-interactive method of authentication.
                    // Mitigation: Use interactive authentication
                }
            }

            return result;
        }
    }
}
