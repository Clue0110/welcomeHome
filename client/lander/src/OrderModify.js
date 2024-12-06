import React, { useState } from 'react';
import axios from 'axios';

const OrderModify = () => {
  const [orderID, setOrderID] = useState('');
  const [client, setClient] = useState('');
  const [itemID, setItemID] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleAddItem = async () => {
    try {
      const response = await axios.post('/api/order/modify', {
        OrderID: orderID,
        client: client,
        ItemID: itemID,
      });
      setResponseMessage(response.data.message);
    } catch (error) {
      setResponseMessage(error.response?.data?.message || 'Error adding item');
    }
  };

  const handleRemoveItem = async () => {
    try {
      const response = await axios.delete('/api/order/modify', {
        data: { OrderID: orderID, client: client, ItemID: itemID },
      });
      setResponseMessage(response.data.message);
    } catch (error) {
      setResponseMessage(error.response?.data?.message || 'Error removing item');
    }
  };

  return (
    <div>
      <h2>Modify Order</h2>
      <label>Order ID:</label>
      <input type="text" value={orderID} onChange={(e) => setOrderID(e.target.value)} />
      <label>Client ID:</label>
      <input type="text" value={client} onChange={(e) => setClient(e.target.value)} />
      <label>Item ID:</label>
      <input type="text" value={itemID} onChange={(e) => setItemID(e.target.value)} />
      <button onClick={handleAddItem}>Add Item</button>
      <button onClick={handleRemoveItem}>Remove Item</button>
      <p>{responseMessage}</p>
    </div>
  );
};

export default OrderModify;
