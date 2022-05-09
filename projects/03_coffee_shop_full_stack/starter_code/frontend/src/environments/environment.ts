/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'iam-udacity.us', // the auth0 domain prefix
    audience: 'coffee shop', // the audience set for the auth0 app
    clientId: 'mLdqTju0F6z6G4bwwD9CMIblNTI9tJ75', // the client id generated for the auth0 app
    //callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
    callbackURL: 'https://127.0.0.1:8080', // the base url of the running ionic application. 
  }
};
