import styles from "./NavBar.module.css"
import {Outlet, Link} from "react-router-dom"
const NavBar = () => (
    <>
    <header className={styles['navbar']}>
        <Link to="/classes"> <div className={styles['navbar__title']}>Classes</div> </Link>
        <Link to="/Studios"><div className={styles['navbar__title']}>Studios</div></Link>
        <Link style={{"marginRight": "auto"}} to="/Coaches"><div className={styles['navbar__last']}>Coaches</div></Link>
        <div className={styles['navbar__item']}>About Us</div>
        <div className={styles['navbar__item']}>Contact</div>
        <div className={styles['navbar__item']}>Help</div>        
    </header>
    <Outlet/>
    </>
);
export default NavBar;
