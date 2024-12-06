import React, { useState } from "react";
import Axios from "axios";
import { useNavigate, NavLink } from "react-router-dom";

function OrderMain() {

    const [itemID , setItemID] = useState("");
    const navigate = useNavigate();

    const fetchLocations = async (e) => {
        e.preventDefault();
        try
        {
            console.log(itemID);
            const response = await Axios.post("http://127.0.0.1:5000/api/order/start",{client: itemID});
            navigate("/Shopping");
            console.log("This is");
            console.log(response);
        }
        catch(error)
        {
            if (error.response) {
                console.log(error.response.data.message); 
            } else {
                console.log("An error occurred!");
            }
        }
    }

    return (
        <div>
            <h1>Enter ClientID:</h1>
            <form onSubmit={fetchLocations}>
                <input
                    type="text"
                    placeholder="Enter ClientID"
                    value={itemID}
                    onChange={(e) => setItemID(e.target.value)}
                    style={{ padding: "10px", width: "300px", marginRight: "10px" }}
                />
                <button type="submit" style={{ padding: "10px" }}>
                    Search
                </button>
            </form>
        </div>
    )
}

export default OrderMain;