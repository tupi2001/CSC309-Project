import styles from "./NavBar.module.css"
import {Outlet, useNavigate, Link} from "react-router-dom"
import React from "react";

const NavBar = () => {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("SessionToken");
        navigate('/login/');
    } 
    return <>
        <header className={styles['navbar']}>
            <Link to="/classes"> <div className={styles['navbar__title']}>Classes</div> </Link>
            <Link to="/studios"><div className={styles['navbar__title']}>Studios</div></Link>
            <Link style={{"marginRight": "auto"}} to="/coaches"><div className={styles['navbar__last']}>Coaches</div></Link>
            <div className={styles['navbar__item']}>About Us</div>
            <Link to="/profile"><div className={styles['navbar__item']}>Profile</div></Link>
            <div onClick={logout} className={styles['navbar__item']}>Log Out</div>        
        </header>
        <Outlet/>
    </>
};
export default NavBar;
