// import React from "react";
import React, { useState, useContext } from "react";
import styles from "./Classes.module.css";
import axios from "axios";

const EnrolClassAll = (props) => {
    const [classes, setClasses] = useState([]);
    const [studio_id, setStudio_id] = useState([]);
    const [class_id, setClass_id] = useState([]);
    function enrol(){
        axios.get(`http://localhost:8000/classes/user/${studio_id}/enrol/${class_id}/`, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            if(response.status === 200){
                window.location.reload();
            }
        })
    }

    return (
        <div className={styles["div"]}>
            <h3>Which classes would you like to enrol in?</h3>
            <label className={styles["label"]} htmlFor="studioid">Studio id</label>
            <input
                id = "studioid" className={styles["searchTerm"]} style={{width: 280, height: 20, fontSize: 18, margin: 4}} onChange={(e) => {setStudio_id(e.target.value)}}/>
            <label className={styles["label"]} htmlFor="classid">Class id</label>
            <input
                id = "classid" className={styles["searchTerm"]} style={{width: 280, height: 20, fontSize: 18, margin: 4}} onChange={(e) => {setClass_id(e.target.value)}}/>   

            <button className={styles["btn"]} onClick={enrol}>Enrol in classes</button>

        </div>
        );
    
}

export default EnrolClassAll;