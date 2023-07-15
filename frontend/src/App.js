import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Landing from './components/Landing/Landing.js';
import StaffLanding from './components/Staff/StaffLanding.js'
import TableSelection from './components/Customer/TableSelection.js';
import Customer from './components/Customer/Customer.js';
import Kitchen from './components/Staff/Kitchen.js';
import WaitStaff from './components/Staff/WaitStaff.js';
import ManagerLanding from './components/Manager/ManagerLanding.js';
import MenuEditor from './components/Manager/MenuEditor.js';
import RestaurantManager from './components/Manager/RestaurantManager.js';
import Login from './components/Common/Login.js'

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/staff" element={<StaffLanding />} />
          <Route path="/select-table" element={<TableSelection />} />
          <Route path="/customer/:tableNumber" element={<Customer />} />
          <Route path="/kitchen" element={<Kitchen />} />
          <Route path="/wait-staff" element={<WaitStaff />} />
          <Route path="/manager" element={<ManagerLanding />} />
          <Route path="/menu-editor" element={<MenuEditor />} />
          <Route path="/restaurant-manager" element={<RestaurantManager />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;
