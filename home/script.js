const API_URL = "http://192.168.1.13:5000";

async function signup() {
    const username = document.getElementById("signupUsername").value;
    const password = document.getElementById("signupPassword").value;
    
    const res = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: 'include', 
        body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    alert(data.message);
}

async function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: 'include', 
        body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    alert(data.message);
}

async function check() {
    const res = await fetch(`${API_URL}/status`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include"
    });
    const data = await res.json();
    alert(data.loggedIn);
}