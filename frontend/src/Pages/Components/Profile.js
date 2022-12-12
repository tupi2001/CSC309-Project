import axios from "axios";
import React, { useState, useEffect } from "react";
import styles from "./Profile.module.css";
import {Link} from "react-router-dom"
import Card from "./Card"
import Subscriptions from "./Subscriptions"
import Payments from "./Payments";
const URL = 'http://localhost:8000/accounts/me/';

const Profile = (props) => {

    const [data, setData] = useState({
        fname: "",
        lname: "",
        email: "",
        username: "",
        password1: "",
        password2: "",
        phone: "",
        avatar: null, 
      })
    const [user, setUser] = useState({});

    function change(e){  
        const new_data = {... data}
        new_data[e.target.id] = e.target.value
        setData(new_data)
    }
    const handleFileSelect = (e) => {
        const new_data = {... data};
        new_data.avatar = e.target.files[0];
        console.log(new_data);
        setData(new_data);
    }
    function handleSubmit (e) {
        e.preventDefault();
        const tobeUpdated = Object.fromEntries(Object.entries(data).filter(([key, value]) => !!value));
        const form = new FormData();
        if(tobeUpdated.fname){
            form.append("first_name", tobeUpdated.fname);
        }
        if(tobeUpdated.lname){
            form.append("last_name", tobeUpdated.lname);
        }
        if(tobeUpdated.username){
            form.append("username", tobeUpdated.username); 
        }   
        if(tobeUpdated.email){
            form.append("email", tobeUpdated.email); 
        }
        if(tobeUpdated.phone){
            form.append("phone_number", tobeUpdated.phone);
        } 
        if(tobeUpdated.avatar){
            form.append("avatar", tobeUpdated.avatar);
        }
        axios.patch(`http://localhost:8000/accounts/${user.pk}/profile/edit/`, form, {
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: "Token " + localStorage.getItem("SessionToken") 
            }
        }).then((response) => {
            if(response.status == 200){
                window.location.reload()
            }
        })
    }

    useEffect(() => {
        axios.get(URL, {
            headers: {
                Authorization: "Token " + localStorage.getItem("SessionToken")
            }
        }).then((response) => {
            if(!response.data["avatar"]){
                response.data["avatar"] = "/Images/blank.webp"
            }else{
                response.data["avatar"] = "http://localhost:8000" + response.data["avatar"];
            }
            setUser(response.data)
        })
    }, []);
    return (
        <div>
        <form className={styles.form} onSubmit={(e) => handleSubmit(e)}>
          <div className={styles["form-content"]}>
            <h1 className={styles["form-title"]}>Profile</h1>
            <img src={user["avatar"]}/>
            <div className={styles["form-input-group"]}>
              <div className={styles["input-group"]}>
                <label className={styles["form-label"]} htmlFor="fname">
                  First Name
                </label>
                <input
                  type="text"
                  autoFocus
                  className={styles["form-input"]}
                  id="fname"
                  onChange={(e) => change(e)}
                  placeholder={user["first_name"]}
                ></input>
              </div>
    
              <div className={styles["input-group"]}>
                <label className={styles["form-label"]} htmlFor="lname">
                  Last Name
                </label>
                <input
                  type="text"
                  className={styles["form-input"]}
                  id="lname"
                  onChange={(e) => change(e)} 
                  placeholder={user["last_name"]}
                ></input>
              </div>
            </div>
    
            <label className={styles["form-label"]} htmlFor="username">
              Username
            </label>
            <input type="text" className={styles["form-input"]} id="username" onChange={(e) => change(e)} placeholder={user["username"]}></input>
    
            <label className={styles["form-label"]} htmlFor="email">
              Email Address
            </label>
            <input type="email" className={styles["form-input"]} id="email" onChange={(e) => change(e) } placeholder={user["email"]}></input>
    
            <label className={styles["form-label"]} htmlFor="phone">
              Phone Number
            </label>
            <input
              type="tel"
              className={styles["form-input"]}
              id="phone"
              onChange={(e) => change(e)} 
              placeholder={user["phone_number"]}
              pattern='^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'
            ></input>
            <label className={styles["form-label"]} htmlFor="avatar">
              Upload Avatar
            </label>
              <input
                className={styles["file-input"]}
                type="file" onChange={handleFileSelect} id ="avatar"
              ></input>
            <button className={styles["form-btn"]}>Save</button>
          </div>
        </form>
        <Card></Card>
        <Subscriptions></Subscriptions>
        <Payments></Payments>
        </div>
      );
}
export default Profile;