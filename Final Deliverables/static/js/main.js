function Signup(URL){
    let username=document.getElementById("username").value;
    let email=document.getElementById("email").value;
    let password=document.getElementById("password").value;
    let re_password=document.getElementById("re_password").value;
    let which_condiction="signup";

    let data={
        username:username,
        email:email,
        password:password,
        re_password:re_password,
        which_condiction:which_condiction
        
    }

    if(username=="" || email=="" || password=="" || re_password ==""  ){
        alert("please enter all fields")
        }

else{

if (password!=re_password){
    alert("passwor dosent match")
}

else{

    passcheck=CheckPassword(password);
    emailcheck=validateEmail(email)
    if(passcheck==true){
        if(emailcheck==true){
            SubmitData(data,URL,path='/')
        }
        else{
            alert("enter a valid email")
        }
    }
else{
    alert("enter a stong password")

}

}
}
}
























function Login(URL){
    let username=document.getElementById("login_username").value;
    let password=document.getElementById("login_password").value;
    let which_condiction="login";

    let data={
        username:username,
        password:password,
        which_condiction:which_condiction
}
if(username=="" &&  password==""){
    alert("please enter all fields")
}
else{
    SubmitData(data,URL,path='/home')

}

}




function CheckPassword(inputtxt) 
{ 
    console.log(inputtxt)
var passw=  /^[A-Za-z]\w{7,14}$/;
if(inputtxt.match(passw)) 
{ 
console.log("correct")
return true;
}
else
{ 
console.log("false")

return false;
}
}

function validateEmail(email_id) {
    const regex_pattern =      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    
    if (regex_pattern.test(email_id)) {
        return true;
    }
    else {
        return false;
    }
}

