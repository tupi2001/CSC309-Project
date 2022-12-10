import './App.css';
import LoginPage from './Pages/Login/LoginPage'
import SignupPage from './Pages/Signup/SignupPage'
import Coaches from './Pages/Components/Coaches'
import Classes from './Pages/Components/Classes'
import Studios from './Pages/Components/Studios'
import Profile from './Pages/Components/Profile'
import NavBar from './Pages/Components/NavBar'
import Home from './Pages/Home/Home'
import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<NavBar/>}>
                <Route index element={<Navigate to="/login/" />}/>
                <Route path="home/" element={<Home />} />
                <Route path="studios/" element={<Studios />} />
                <Route path="classes/" element={<Classes />} />
                <Route path="coaches/" element={<Coaches />} />
                <Route path="profile/" element={<Profile />} />
            </Route>
            <Route index element={<LoginPage />} path="/login/" />
            <Route path="/signup/" element={<SignupPage />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
