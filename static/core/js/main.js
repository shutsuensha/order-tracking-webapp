window.onload = function() {
    try {
        document.getElementById('target-element').scrollIntoView({ behavior: 'smooth' });
    } catch(err) {
        console.log('error')
    }
    try {
        document.getElementById('comments').scrollIntoView({ behavior: 'smooth' });
    } catch(err) {
        console.log('error')
    }

    //https://shutsuensha.pythonanywhere.com/oauth/complete/google/
    //https://shutsuensha.pythonanywhere.com/oauth/authorize/google-oauth2/
    //https://shutsuensha.pythonanywhere.com/oauth/complete/google-oauth2/

}
