import axios from 'axios';
/*
function Auth() {    
    axios.post("/api/isLoggedIn",null)
        .then(res => {
            console.log('Login Status::');
            console.log(res.data.login_status);
            if(res.data.login_status)
            {                
                return true;
            }
            else
            {
                return false;
            }            
        });    
}*/

const Auth = () => {
    var login_status = null;
    axios.post("/api/isLoggedIn", null)
        .then(res => {
            console.log('Login Status::');
            console.log(res.data.login_status);
            login_status =  res.data.login_status;            
        });
    return login_status;
}

export default Auth;