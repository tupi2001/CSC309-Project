import axios from "axios";
import React, { useState, useEffect } from "react";
import styles from "./UserClasses.module.css";
const URL = 'http://localhost:8000/classes/user/view/';

const UserClasses = (props) => {

    const [classes, setClasses] = useState([]);
    const [user, setUser] = useState({});

    useEffect(() => {
        // gets all current subscription plans  
        axios.get(URL, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            setClasses(response.data)
        })

    }, []);

    function removeclass(e){
        
    }

    return (
        <div className={styles["div"]}>
            <h1 className={styles["title"]}>Enrolled Classes</h1>

            <ul>
                {classes.map((inst) => (
                    <li>{inst.user}</li>
                ))}
            </ul>

        </div>
        );
        
    }

export default UserClasses;