function validate(inputvalue,span)
{
    var loginData = $("#"+ inputvalue).val();
    //$("#"+span).html("");

    if (loginData == ''){
        //$("#" + inputvalue).addClass('error');
        $("#" + span).addClass('has-error');
        /*$("#" + span).attr("class", "show");

        switch (inputvalue) {
            case 'logInEmail' :
                $("#" + span).html("Please provide email id");
                break;
            case 'logInPassword' :
                $("#" + span).html("Please provide password");
                break;
            case 'registerName' :
                $("#" + span).html("Name can not be blank");
                break;
            case 'registerEmail' :
                $("#" + span).html("Email can not be blank");
                break;
            case 'registerPassword' :
                $("#" + span).html("Please provide any password");
                break;
            case 'registerPassword1' :
                $("#" + span).html("Please type the password again");
                break;
            case 'typeOfRegister' :
                $("#" + span).html("Please select the user type");
                break;
        }*/

    }else
        $("#" + span).removeClass('has-error');
        /*$("#" + inputvalue).removeClass('error');
        $("#" + inputvalue).addClass('valid');*/

    if (inputvalue =='registerPassword1' && loginData !== $("#registerPassword").val()){
     //   alert('password match');
        $("#" + span).addClass('has-error');
        /*html("Password doesn't match");
        $("#" + span).attr("class", "show");*/
    }else $("#" + span).removeClass('has-error');

};

function loginValidate(login)
{
    $("#error1").html("");
    var email = login.logInEmail.value;
    var pwd = login.logInPassword.value;

    if (email == '' || pwd == '' ) {

        $("#error1").html("Please provide all the inputs");
        $("#error1").attr("class", "show text-center");
        return false;

}


};

function registerValidate(register)
{
    $("#error2").html("");
    var name = register.registerName.value;
    var email = register.registerEmail.value;
    var pwd = register.registerPassword.value;
    var pwd1 = register.registerPassword1.value;
    var typeOfReg = register.typeOfRegister.value;
    var tnc = register.tnCcheckbox.value;



    if (name == '' || email == '' || pwd == '' || pwd1 == '' || typeOfReg == '' || tnc == '') {

        $("#error2").html("Please provide all the inputs");
        $("#error2").attr("class", "show text-center");
        return false;

    }


};

function inputCheck(search){
    var input = search.examName.value;
    if (input == ''){
        return false;
    }
}