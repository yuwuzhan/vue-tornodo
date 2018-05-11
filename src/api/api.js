import baseUrls from './baseUrl'
const pas = {
    token: {
        method: 'post',
        url: baseUrls.pas + '/auth/get_token/v2/',
        data: {   
            platform: 4,
        }
    },
    login:{
        method: 'post',
        url: baseUrls.pas+'/auth/login/v2/',
        data: {		
              username:'itmaster',
              password:'123456',
              platform:4,
              code:1,
              login_type:'user',
        }
    },
    logout:{
        method: 'get',
        url: baseUrls.pas + '/user/logout/v2/',
        params: {
        }
    }
};
export default pas