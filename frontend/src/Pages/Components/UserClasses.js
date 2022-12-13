import axios from "axios";
import React, { useState, useEffect } from "react";
import styles from "./UserClasses.module.css";
const URL = 'http://localhost:8000/classes/user/view/';

const UserClasses = (props) => {

    const [classes, setClasses] = useState([]);
    const [studio_id, setStudio_id] = useState({});
    const [class_id, setClass_id] = useState({});

    function unenroll(){
        axios.get(`http://localhost:8000/classes/user/${studio_id}/unenrol/${class_id}/`, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            if(response.status === 200){
                window.location.reload()
            }
        })
    }
    

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
        <div className={styles["page"]}>
            <h1 className={styles["title"]}>Enrolled Classes</h1>

            <ul>
                {classes.map((inst) => (
                    <li>Classid{inst.id} {inst.class_name} from Studioid{inst.studio}: {inst.name} at {inst.start_date} from {inst.start_time}-{inst.end_time}</li>
                ))}
            </ul>

            <form className={styles.form} onSubmit={unenroll}>
                <div className={styles["form-content"]}>
                    <h3>Would you like to unenroll from any of these classes?</h3>
                        <div className={styles["input-group"]}>
                            <label className={styles["form-label"]} htmlFor="studioid">
                                Studio id
                            </label>
                            <input
                                id = "studioid" className={styles["form-input"]} style={{width: 280, height: 20, fontSize: 18, margin: 4}} onChange={(e) => {setStudio_id(e.target.value)}}/>

                            <label className={styles["form-label"]} htmlFor="classid">
                                Class id
                            </label>
                            <input
                                id = "classid" className={styles["form-input"]} style={{width: 280, height: 20, fontSize: 18, margin: 4}} onChange={(e) => {setClass_id(e.target.value)}}/>   

                        <button className={styles["form-btn"]}>Unenroll from class</button>
                    </div>
                </div>
            </form>

        </div>
        );
        
    }

export default UserClasses;