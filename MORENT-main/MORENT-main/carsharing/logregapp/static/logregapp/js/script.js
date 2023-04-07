function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhoneNumber(phoneNumber) {
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    return phoneRegex.test(phoneNumber);
}

function check_input(){
    //checking if input text is an email adress
    if ( isValidEmail(document.getElementById('mail_input').value) == false ){
        document.getElementById('mail_warning').style.visibility = "visible"
        document.getElementById('mail_img').src = './resources/mail_red.svg'
        document.getElementById('mail_area').style.borderColor = "#881600"
    }else{
        document.getElementById('mail_warning').style.visibility = "hidden"
        document.getElementById('mail_img').src = './resources/mail_black.svg'
        document.getElementById('mail_area').style.borderColor = "#1A202C"
    }


    //checking if input text is a phone number
    if (isValidPhoneNumber(document.getElementById('phone_input').value) == false){
        document.getElementById('phone_warning').style.visibility = "visible"
        document.getElementById('phone_img').src = './resources/phone_red.svg'
        document.getElementById('phone_img').style.width = "25"
        document.getElementById('phone_img').style.height = "25"
        document.getElementById('phone_area').style.borderColor = "#881600"
    }else{
        document.getElementById('phone_warning').style.visibility = "hidden"
        document.getElementById('phone_img').src = './resources/phone_black.svg'
        document.getElementById('phone_area').style.borderColor = "#1A202C"
    }

    //checking if passwords are the same
    p = document.getElementById('confirm_password_input').value
    cp = document.getElementById('password_input').value
    if (p != cp || p == "") {
        document.getElementById('lock_img').src = './resources/lock_red.svg'
        document.getElementById('lock_img').style.opacity = '1'
        document.getElementById('lock_warning').style.visibility = "visible"
        document.getElementById('lock_area').style.borderColor = "#881600"
    }else{
        document.getElementById('lock_img').src = './resources/lock_black.svg'
        document.getElementById('lock_img').style.opacity = '0.5'
        document.getElementById('lock_warning').style.visibility = "hidden"
        document.getElementById('lock_area').style.borderColor = "#1A202C"
    }
}