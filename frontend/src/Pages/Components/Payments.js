import styles from "./Payments.module.css";
import axios from "axios";
import React, { useState, useEffect } from "react";
const URL = 'http://localhost:8000/subscriptions/paymenthistory/';

const Payments = (props) => {
    const [classes, setClasses] = useState([]);
    const [subs, setSubs] = useState({});

    useEffect(() => {
        // gets all payments done by user
        axios.get('http://localhost:8000/subscriptions/paymenthistory/', {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            setClasses(response.data)
        })

        // gets all current subscription plans  
        axios.get(URL, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            setSubs(response.data)
        })

    }, []);

    function removeclass(e){
        
    }

    return (
        <div className={styles["phistory"]}>
            <h1 className={styles["title"]}>Payments</h1>

            <ul>
                {classes.map((inst) => (
                    <><li>{inst.date}, using card {inst.card}, for subscription ${inst.sub}</li></>
                ))}
            </ul>

        </div>
        );
        
    }

export default Payments;