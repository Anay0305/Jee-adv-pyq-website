const API_URL = "http://192.168.1.13:5000";

async function check() {
    const res = await fetch(`${API_URL}/status`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include"
    });
    const data = await res.json();
    if (data.loggedIn) {
        const navbarMenu = document.querySelector(".navbar__menu");
        if (navbarMenu) {
            const listItem = document.createElement("li");
            listItem.classList.add("navbar__item");

            const link = document.createElement("a");
            link.classList.add("navbar__links");
            link.textContent = data.user;
            listItem.appendChild(link);
            navbarMenu.appendChild(listItem);
        }
    }
    else {
        window.location.href = "/";
    }
}
check()

const urlParams = new URLSearchParams(window.location.search);
const testId = parseInt(urlParams.get('testid'), 10);



const navbarLogo = document.querySelector("#navbar__logo");

navbarLogo.textContent = `JEE ADVANCE 20${Math.floor(testId / 10)} Paper ${testId % 10}`;