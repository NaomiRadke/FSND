/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fstutorial.eu', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'mOD7j164KJYPgWTlOkLxGkPgaw287nkL', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:8100/tabs/user-page', // the base url of the running ionic application. 
  }
};
