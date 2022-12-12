import styles from "./Card.module.css";
import axios from "axios";
import React, { useState, useEffect } from "react";
const URL = 'http://localhost:8000/subscriptions/showcard/';

const Payments = (props) => {
    const [payments, setPayments] = useState({});

    useEffect(() => {
        // gets payment history for currently logged in user
        axios.get('http://localhost:8000/subscriptions/paymenthistory/', {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken"),
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }).then((response) => {
            setPayments(response.data);
        })

    }, []);

    return (
        <div>
            <tbody>
        <tr>
          <th>User</th>
          <th>Date</th>
          <th>Card used</th>
          <th>Subscription</th>
        </tr>

        <div>
            {Object.keys(payments).map((item) => (
            <tr>
                <td>{payments[item].user}</td>
                <td>{payments[item].date}</td>
                <td>{payments[item].card}</td>
                <td>{payments[item].sub}</td>
            </tr>
            ))}
        </div>
        
      </tbody>
        </div>
      );
};

export default Payments;