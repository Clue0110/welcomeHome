import React, { useState } from "react";
import Axios from "axios";

const ItemLocations = () => {
    const [itemID, setItemID] = useState(""); // State for ItemID input
    const [locations, setLocations] = useState([]); // State for storing locations
    const [error, setError] = useState(""); // State for error messages

    const fetchLocations = async (e) => {
        e.preventDefault(); // Prevent the form from reloading the page
        setError(""); // Clear previous error messages
        setLocations([]); // Clear previous results

        if (!itemID.trim()) {
            setError("ItemID cannot be empty");
            return;
        }

        try {
            const response = await Axios.get("http://127.0.0.1:5000/api/item/locations", {params:{ItemID: itemID}});
            console.log(locations);
            setLocations(response.data.locations); // Update locations state
        } catch (err) {
            console.log(locations);
            if (err.response) {
                setError(err.response.data.message); // Show error returned from API
            } else {
                setError("An error occurred while fetching data");
            }
        }
    };

    return (
        <div style={{ margin: "20px" }}>
            <h1>Find Item Locations</h1>
            <form onSubmit={fetchLocations}>
                <input
                    type="text"
                    placeholder="Enter ItemID"
                    value={itemID}
                    onChange={(e) => setItemID(e.target.value)}
                    style={{ padding: "10px", width: "300px", marginRight: "10px" }}
                />
                <button type="submit" style={{ padding: "10px" }}>
                    Search
                </button>
            </form>

            {error && <div style={{ color: "red", marginTop: "10px" }}>{error}</div>}

            {locations.length > 0 && (
                <div style={{ marginTop: "20px" }}>
                    <h2>Item Locations</h2>
                    <table border="1" cellPadding="10">
                        <thead>
                            <tr>
                                <th>Piece Number</th>
                                <th>Room Number</th>
                                <th>Shelf Number</th>
                                <th>Shelf Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {locations.map((loc, index) => (
                                <tr key={index}>
                                    <td>{loc.piecenum}</td>
                                    <td>{loc.roomnum}</td>
                                    <td>{loc.shelfnum}</td>
                                    <td>{loc.shelfdescription}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default ItemLocations;
