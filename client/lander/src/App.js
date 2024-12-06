import RegisterForm from "./RegisterForm";
import Login from "./Login";
import Donated from "./Donated";
import Locations from "./Locations"
import OrderLocations from "./OrderLocations"
import Orderstart from "./Orderstart";
import OrderMain from "./OrderMain";
import Shopping from "./Shopping";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Routes>
      <Route path="/RegisterForm" element={<RegisterForm/>}/>
        <Route path="/Login" element={<Login/>}/>
        <Route path="/Donated" element={<Donated/>} />
        <Route path="/ItemLocation" element={<Locations />} />
        <Route path="/OrderLocations" element={<OrderLocations />} />
        <Route path="/" element={<Orderstart />} />
        <Route path="/OrderMain" element={<OrderMain />} />
        <Route path="/Shopping" element={<Shopping />} />
      </Routes>
    </div>
  );
}

export default App;
