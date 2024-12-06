import React, { useState } from "react";
import Axios from "axios";
import { useNavigate, NavLink } from "react-router-dom";
Axios.defaults.withCredentials = true;

function Login() {
    const navigate = useNavigate();
    const [usname, setUsname] = useState("");
    const [passname, setPassname] = useState("");

    const verify = async (e) => {
        e.preventDefault();
        try {
            const responsee = await Axios.post("http://127.0.0.1:5000/api/login/", {
                username: usname, 
                password: passname 
            });
            console.log(responsee.data);
            navigate("/");
        } 
        catch (error) {
            if (error.response) {
                console.log(error.response.data.message); 
            } else {
                console.log("An error occurred!");
            }
        }
    };
    

    return (
        <div className="outer">
            <div className="inner">
                <div className="nam">Login</div>
                <div className="nam1">
                    Don't have an account? <NavLink to="/RegisterForm">Click here</NavLink>
                </div>
                <input
                    type="text"
                    className="uname"
                    placeholder="Enter Username"
                    onChange={(event) => setUsname(event.target.value)}
                />
                <input
                    type="password"
                    className="pass"
                    placeholder="Enter Password"
                    onChange={(event) => setPassname(event.target.value)}
                />
                <button className="but" onClick={verify}>
                    Login
                </button>
            </div>
        </div>
    );
}

export default Login;
