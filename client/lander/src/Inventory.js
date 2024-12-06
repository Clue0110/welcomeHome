import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
axios.defaults.withCredentials = true;

const Inventory = () => {

  const [inventory, setInventory] = useState([]);
  const [client, setClient] = useState('');
  const [cate, setCate] = useState('');
  const [subcate, setSubcate] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const fetchInventory = async () => {
    try {
        console.log(client);
        console.log(cate);
        console.log(subcate);

        const allCookies = Cookies.get("session");
        console.log('All cookies:', allCookies);
        
      const response = await axios.get("http://127.0.0.1:5000//api/inventory", {
        params: { client: client, mainCategory: cate , sub_category: subcate},
      });
      console.log(response);
      setInventory(response.data.inventory);
    } catch (error) {
      setResponseMessage(error.response?.data?.message || 'Error fetching inventory');
    }
  };

  return (
    <div>
      <h2>Inventory</h2>
      <label>Client ID:</label>
      <input type="text" value={client} onChange={(e) => setClient(e.target.value)} />
      <label>Category:</label>
      <input type="text" value={cate} onChange={(e) => setCate(e.target.value)} />
      <label>Sub-Category:</label>
      <input type="text" value={subcate} onChange={(e) => setSubcate(e.target.value)} />
      <button onClick={fetchInventory}>Fetch Inventory</button>
      <p>{responseMessage}</p>
      <table border="1" cellPadding="10">
                        <thead>
                            <tr>
                                <th>itemid</th>
                                <th>idescription</th>
                                <th>photo</th>
                                <th>isnew</th>
                                <th>haspieces</th>
                                <th>material</th>
                                <th>maincategory</th>
                                <th>subcategory</th>
                            </tr>
                        </thead>
                        <tbody>
                            {inventory.map((loc, index) => (
                                <tr key={index}>
                                    <td>{loc.itemid}</td>
                                    <td>{loc.idescription}</td>
                                    <td>{loc.photo}</td>
                                    <td>{loc.isnew ? 'true' : 'false'}</td>
                                    <td>{loc.haspieces ? 'true' : "false"}</td>
                                    <td>{loc.material}</td>
                                    <td>{loc.maincategory}</td>
                                    <td>{loc.subcategory}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
    </div>
  );
};

export default Inventory;
