import './App.css';
import LoginPage from './Pages/Login/LoginPage'
import SignupPage from './Pages/Signup/SignupPage'
import Coaches from './Pages/Components/Coaches'
// import GymClasses from './Pages/Components/Classes/GymClasses'
import Studios from './Pages/Components/Studios'
import Profile from './Pages/Components/Profile'
import NavBar from './Pages/Components/NavBar'
import Studio from './Pages/Components/Studio'
import Home from './Pages/Home/Home'
import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import APIContext, {useAPIContext} from "./Contexts/APIContext";
// import GymClasses from './Pages/Components/Classes/GymClasses';
import Classes from './Pages/Components/Classes';

function App() {

  const gymclasses = (
    <APIContext.Provider value={useAPIContext()}>
        <Classes />
    </APIContext.Provider>
  )
  return (
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<NavBar/>}>
                <Route index element={<Navigate to="/login/" />}/>
                <Route path="home/" element={<Home />} />
                <Route path="studios/" element={<Studios />} />
                <Route path="studios/:id" element={<Studio/>}/>
                <Route path="classes/" element={gymclasses} />
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
