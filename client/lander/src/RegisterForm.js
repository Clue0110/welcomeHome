import React, { useState } from "react";
import axios from "axios";

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        fname: "",
        lname: "",
        email: "",
        phone: [""],
        roleID: ""
    });

    const [responseMessage, setResponseMessage] = useState("");

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handlePhoneChange = (index, value) => {
        const updatedPhones = [...formData.phone];
        updatedPhones[index] = value;
        setFormData({ ...formData, phone: updatedPhones });
    };

    const addPhoneField = () => {
        setFormData({ ...formData, phone: [...formData.phone, ""] });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:5000/api/register/", formData);
            setResponseMessage(response.data.message);
            console.log(formData)
        } catch (error) {
            if (error.response) {
                console.log(formData)
                setResponseMessage(error.response.data.message);
            } else {
                setResponseMessage("An error occurred!");
            }
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="text"
                    name="fname"
                    placeholder="First Name"
                    value={formData.fname}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="text"
                    name="lname"
                    placeholder="Last Name"
                    value={formData.lname}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                />
                {formData.phone.map((phone, index) => (
                    <div key={index}>
                        <input
                            type="text"
                            placeholder="Phone Number"
                            value={phone}
                            onChange={(e) => handlePhoneChange(index, e.target.value)}
                            required
                        />
                    </div>
                ))}
                <button type="button" onClick={addPhoneField}>
                    Add Phone Number
                </button>
                <input
                    type="number"
                    name="roleID"
                    placeholder="Role ID"
                    value={formData.roleID}
                    onChange={handleInputChange}
                    required
                />
                <button type="submit">Register</button>
            </form>
            
            {responseMessage && <p>{responseMessage}</p>}
        </div>
    );
};

export default RegisterForm;