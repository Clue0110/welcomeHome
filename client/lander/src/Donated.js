import React, { useState } from "react";
import Axios from "axios";

const DonationForm = () => {
    const [formData, setFormData] = useState({
        ItemID: "",
        iDescription: "",
        photo: "",
        color: "",
        isNew: false,
        hasPieces: false,
        material: "",
        mainCategory: "",
        subCategory: "",
        donor_username: "",
        donateDate: "",
        current_user: "",
        pieces: [
            {
                pieceNum: 1,
                pDescription: "",
                length: "",
                width: "",
                height: "",
                roomNum: "",
                shelfNum: "",
                pNotes: "",
            },
        ],
    });

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: type === "checkbox" ? checked : value,
        }));
    };

    const handlePieceChange = (index, key, value) => {
        setFormData((prevState) => {
            const updatedPieces = [...prevState.pieces];
            updatedPieces[index][key] = value;
            return { ...prevState, pieces: updatedPieces };
        });
    };

    const addPiece = () => {
        setFormData((prevState) => ({
            ...prevState,
            pieces: [
                ...prevState.pieces,
                {
                    pieceNum: prevState.pieces.length + 1,
                    pDescription: "",
                    length: "",
                    width: "",
                    height: "",
                    roomNum: "",
                    shelfNum: "",
                    pNotes: "",
                },
            ],
        }));
    };
    

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await Axios.post("http://127.0.0.1:5000/api/donation/", formData);
            console.log(response.data);
            alert("Donation submitted successfully!");
        } catch (error) {
            console.log(formData);
            console.error(error.response ? error.response.data : error.message);
            alert("Error submitting donation!");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Donation Form</h2>

            <label>
                Item ID:
                <input
                    type="text"
                    name="ItemID"
                    value={formData.ItemID}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <label>
                Item Description:
                <input
                    type="text"
                    name="iDescription"
                    value={formData.iDescription}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <label>
                Photo:
                <input
                    type="text"
                    name="photo"
                    value={formData.photo}
                    onChange={handleInputChange}
                />
            </label>

            <label>
                Material:
                <input
                    type="text"
                    name="material"
                    value={formData.material}
                    onChange={handleInputChange}
                />
            </label>

            <label>
                Main Category:
                <input
                    type="text"
                    name="mainCategory"
                    value={formData.mainCategory}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <label>
                Sub Category:
                <input
                    type="text"
                    name="subCategory"
                    value={formData.subCategory}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <label>
                Donate Date:
                <input
                    type="date"
                    name="donateDate"
                    value={formData.donateDate}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <label>
                Color:
                <input
                    type="text"
                    name="color"
                    value={formData.color}
                    onChange={handleInputChange}
                />
            </label>

            <label>
                Is New:
                <input
                    type="checkbox"
                    name="isNew"
                    checked={formData.isNew}
                    onChange={handleInputChange}
                />
            </label>

            <label>
                Has Pieces:
                <input
                    type="checkbox"
                    name="hasPieces"
                    checked={formData.hasPieces}
                    onChange={handleInputChange}
                />
            </label>

            <label>
                Donor Username:
                <input
                    type="text"
                    name="donor_username"
                    value={formData.donor_username}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <label>
                Current User:
                <input
                    type="text"
                    name="current_user"
                    value={formData.current_user}
                    onChange={handleInputChange}
                    required
                />
            </label>

            <h3>Pieces</h3>
            {formData.pieces.map((piece, index) => (
                <div key={index}>
                    <h4>Piece {index + 1}</h4>
                    <label>
                        Description:
                        <input
                            type="text"
                            value={piece.pDescription}
                            onChange={(e) => handlePieceChange(index, "pDescription", e.target.value)}
                            required
                        />
                    </label>
                    <label>
                        Length:
                        <input
                            type="number"
                            value={piece.length}
                            onChange={(e) => handlePieceChange(index, "length", e.target.value)}
                            required
                        />
                    </label>
                    <label>
                        Width:
                        <input
                            type="number"
                            value={piece.width}
                            onChange={(e) => handlePieceChange(index, "width", e.target.value)}
                            required
                        />
                    </label>
                    <label>
                        Height:
                        <input
                            type="number"
                            value={piece.height}
                            onChange={(e) => handlePieceChange(index, "height", e.target.value)}
                            required
                        />
                    </label>
                    <label>
                        Room Number:
                        <input
                            type="text"
                            value={piece.roomNum}
                            onChange={(e) => handlePieceChange(index, "roomNum", e.target.value)}
                        />
                    </label>
                    <label>
                        Shelf Number:
                        <input
                            type="text"
                            value={piece.shelfNum}
                            onChange={(e) => handlePieceChange(index, "shelfNum", e.target.value)}
                        />
                    </label>
                    <label>
                        Notes:
                        <input
                            type="text"
                            value={piece.pNotes}
                            onChange={(e) => handlePieceChange(index, "pNotes", e.target.value)}
                        />
                    </label>
                </div>
            ))}

            <button type="button" onClick={addPiece}>
                Add Another Piece
            </button>

            <button type="submit">Submit Donation</button>
        </form>
    );
};

export default DonationForm;

