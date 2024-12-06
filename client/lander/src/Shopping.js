import React, { useState } from "react";
import Axios from "axios";
import Inventory from './Inventory';
import OrderModify from './OrderModify';
import { useNavigate, NavLink } from "react-router-dom";

function Shopping()
{
    return (
        <div>
            <OrderModify />
            <Inventory />
        </div>
    )
}

export default Shopping;