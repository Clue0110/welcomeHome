import React, { useState } from "react";
import Axios from "axios";
import { useNavigate, NavLink } from "react-router-dom";
import Cookies from 'js-cookie';

function Orderstart() {

    console.log(document.cookie);

    const navigate = useNavigate();
    const changee = async() => {
        navigate("/OrderMain");  
    };

return (
    <div>
        <button onClick={changee}>Click to start your order</button>
    </div>
);
};

export default Orderstart;