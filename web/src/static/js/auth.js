window.addEventListener('load', function () {
    gapi.load('auth2', function () {
        gapi.auth2.init();
    });
});

function signIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    document.cookie = `token=${id_token}`;
    window.location.reload();
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        document.cookie = "token=";
        window.location.reload();
    });
}