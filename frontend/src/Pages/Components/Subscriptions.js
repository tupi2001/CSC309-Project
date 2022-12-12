import axios from "axios";
import React, { useState, useEffect } from "react";
import styles from "./Subscriptions.module.css";
const URL = 'http://localhost:8000/subscriptions/showsubs/';

const Profile = (props) => {

    const [subs, setSubs] = useState([]);
    const [card, setCard] = useState({
        name: "",
        card: "",
      });
    const [data, setData] = useState({
        user: "",
        subscription: "",
        card: "",
        renew: false,
      });
    const [user, setUser] = useState({});
    const [hasSub, sethasSub] = useState(false);

    useEffect(() => {
        // gets all current subscription plans  
        axios.get(URL, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            setSubs(response.data)
        })

        // get user pk

        axios.get('http://localhost:8000/accounts/me/', {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            data['user'] = response.data.pk;
            setUser(response.data)
        })

        // checks to see if user has card associated to their account
        axios.get('http://localhost:8000/subscriptions/showcard/', {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            data['card'] = response.data.id;
            setCard(response.data);
        })
        
        // check if user has subscription
        axios.get('http://localhost:8000/subscriptions/showsub/', {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            setData(response.data);
            sethasSub(true);
        })
    }, []);

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
        if(tobeUpdated.subscription){
            form.append("subscription", tobeUpdated.subscription);
        }
        else{
            form.append("subscription", data['subscription']);       
        }
        form.append("card", data['card']);   
        form.append("renew", data['renew']);
        if(hasSub === true){
            // user already has subscription, update current one

            axios.patch(`http://localhost:8000/subscriptions/updatesub/${user.pk}/`, form, {
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
            // add new subscription to current user

            axios.post(`http://localhost:8000/subscriptions/addsub/`, form, {
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

    return (
        <form className={styles.form} onSubmit={(e) => handleSubmit(e)}>
            <div className={styles["form-content"]}>
            <h1 className={styles["form-title"]}>Subscriptions</h1>

            <h3>Current Subscription: ${data.subscription}</h3>
            
            <label className={styles["form-label"]} htmlFor="subscription">
                Subscription Plans
            </label>
            <select onChange={(e) => change(e)} id="subscription" value={data.subscription}>
            {subs.map((sub) => (
              <option value={sub.id}>{sub.value}, {sub.charge_every}</option>
            ))}
          </select>
    
            <h3>Current card: {card.name} {card.card}</h3>

            <label className={styles["form-label"]} htmlFor="renew">
                Renew?
            </label>
            <input type="checkbox" className={styles["form-input"]} id="renew" onChange={(e) => change(e)} value={data.renew} ></input>
            <button className={styles["form-btn"]}>Update Subscription</button>
            </div>
        </form>
        );
        
    }

export default Profile;