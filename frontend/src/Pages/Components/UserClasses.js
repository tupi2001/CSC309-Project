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
                    <li>id{inst.id} {inst.class_name}: {inst.name} at {inst.start_date} from {inst.start_time}-{inst.end_time}</li>
                ))}
            </ul>

        </div>
        );
        
    }

export default UserClasses;