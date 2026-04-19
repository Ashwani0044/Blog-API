import { useState } from "react";
import API from "../api.api.js";

export default function login() {
    const [form, setform] = useState({ email = "", password=""});

    const handleLogin = async () => {
        const res = await API.post("/login", form);
        localStorage.setItem("token", res.data.access_token);
        alert("Login successfully");
    };

    return (
        <div>
            <h2>Login</h2>
            <input placeholder="Email" onChange={e => setForm({...form, email: e.target.value})}/>
            <input placeholder="Password" type="password" onChange={e => setForm({...form, password: e.target.value})}/>
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}