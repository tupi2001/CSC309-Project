import styles from "./Card.module.css";
import axios from "axios";
import React, { useState, useEffect } from "react";
const URL = 'http://localhost:8000/subscriptions/showcard/';

const Card = (props) => {
    const [data, setData] = useState({
        user: "",
        name: "",
        card: "",
      });
    const [hasCard, sethasCard] = useState(false);

    function change(e){  
        const new_data = {... data}
        new_data[e.target.id] = e.target.value
        setData(new_data)
    }

    function handleSubmit (e) {
        e.preventDefault();
        const tobeUpdated = Object.fromEntries(Object.entries(data).filter(([key, value]) => !!value));
        const form = new FormData();
        form.append("user", data['user']);
        if(tobeUpdated.name){
            form.append("name", tobeUpdated.name);
        }
        if(tobeUpdated.card){
            form.append("card", tobeUpdated.card); 
        }   
        if(hasCard === true){
            // user already has a card, update current one

            axios.put(`http://localhost:8000/subscriptions/updatecard/${data.user}/`, form, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: "Token " + localStorage.getItem("SessionToken") 
                }
            }).then((response) => {
                if(response.status === 200){
                    window.location.reload()
                }
            })
        }
        
        else{
            // add new card to current user

            axios.post(`http://localhost:8000/subscriptions/addcard/`, form, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: "Token " + localStorage.getItem("SessionToken") 
                }
            }).then((response) => {
                if(response.status === 200){
                    window.location.reload()
                }
            })
        }
        
    }

    useEffect(() => {
        // get previous card data

        axios.get(URL, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            setData(response.data)
            sethasCard(true)
        }).catch(function (error) {
            if (error.response) {
                sethasCard(false);
              }
            });

        // get user pk

        axios.get('http://localhost:8000/accounts/me/', {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            data['user'] = response.data.pk;
        })
    }, []);

    return (
        <form className={styles.form} onSubmit={(e) => handleSubmit(e)}>
          <div className={styles["form-content"]}>
            <h1 className={styles["form-title"]}>Card</h1>
            
            <label className={styles["form-label"]} htmlFor="name">
              Name
            </label>
            <input type="text" className={styles["form-input"]} id="name"  placeholder={data["name"]} onChange={(e) => change(e)}></input>
    
            <label className={styles["form-label"]} htmlFor="card">
              Card
            </label>
            <input type="text" className={styles["form-input"]} id="card" onChange={(e) => change(e)}></input>

            <button className={styles["form-btn"]}>Update card</button>
          </div>
        </form>
      );
};

export default Card;