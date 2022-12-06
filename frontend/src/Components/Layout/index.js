import {Link, Outlet} from "react-router-dom";
import './style.css'

const Layout = () => {
    return (
        <>
            <nav>
                <Link to="/converter">Converter</Link>
                <Link to="/calculator">Calculator</Link>
                <Link to="/players">Players</Link>
            </nav>
            <Outlet />
        </>
    )
}

export default Layout;