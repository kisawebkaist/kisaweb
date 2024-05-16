function getCookies() {
    const cookiesVal = document.cookie.split("; ");
    let cookies = {};
    for (let i=0; i<cookiesVal.length; i++) {
      let pair = cookiesVal[i].split("=");
      cookies[pair[0]] = decodeURIComponent(pair[1]);
    }
    return cookies;
}

function sso_login(url, next) {
    fetch(url,{
        method: "POST",
        mode: 'same-origin',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookies()['csrftoken'],
        },
        body: JSON.stringify({"next": next})
    }).then(r => r.json()).then(
        (response) => {
            window.location.href = response['redirect'];
    });
}

function check_otp(url, next) {
    let form = new FormData(document.getElementById('2fa_form'));
    fetch(url, {
        method: "POST",
        mode: 'same-origin',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookies()['csrftoken'],
        },
        body: JSON.stringify({
            "token": form.get("token"),
            "next": next
        })
    }).then(r=>r.json()).then(
        (response) => {
            window.location.href = response['redirect'];
    })
}