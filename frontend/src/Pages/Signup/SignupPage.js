import { Link } from "react-router-dom";
import styles from "./SignupPage.module.css";
// import { API_URL } from "../constants";
import axios from 'axios'
import React, { useState } from 'react';

const URL = 'http://localhost:8000/accounts/register/';
const var_maps = {
  first_name: "First Name",
  last_name: "Last Name",
  username: "Username",
  email: "Email Address",
  phone_number: "Phone Number",
  password: "Password",
  password2: "Confirm Password",
  avatar: "Avatar",
};

const SignupPage = () => {
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
  const [error, setError] = useState("");
  const [errorMessage, setErrorMessage] = useState([]);

  // handles changes in form data
  function change(e){  
    const new_data = {... data}
    new_data[e.target.id] = e.target.value
    setData(new_data)
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = new FormData();
    form.append("first_name", data.fname);    
    form.append("last_name", data.lname);  
    form.append("username", data.username);  
    form.append("email", data.email);  
    form.append("password", data.password1);  
    form.append("password2", data.password2);  
    form.append("phone_number", data.phone); 
    if(data.avatar){
      form.append("avatar", data.avatar);
    }

    axios
      .post(URL, form, {
        headers: {
          'Content-Type': 'multipart/form-data'  
        }
      })
      .then((response) => {
        if (response.status == 201) {
          //redirect to home page
          alert("You have successfully signed up!");
          window.location.href = '/login';
        }
      })
      .catch((err) => {
        console.log(err);
        setError(true);
        const errors = Object.entries(err.response.data).map(([key, value])=>{
          return var_maps[key] + ": " + value
        });

        setErrorMessage(errors);
      });
  };

  const handleFileSelect = (e) => {
    const new_data = {... data};
    new_data.avatar = e.target.files[0];
    console.log(new_data);
    setData(new_data);
  }
  
  return (
    <form className={styles.form} onSubmit={(e) => handleSubmit(e)}>
      <div className={styles["form-content"]}>
        <h1 className={styles["form-title"]}>Please sign up</h1>

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
            ></input>
          </div>
        </div>

        <label className={styles["form-label"]} htmlFor="username">
          Username
        </label>
        <input type="text" className={styles["form-input"]} id="username" onChange={(e) => change(e)} ></input>

        <label className={styles["form-label"]} htmlFor="email">
          Email Address
        </label>
        <input type="email" className={styles["form-input"]} id="email" onChange={(e) => change(e)} ></input>

        <label className={styles["form-label"]} htmlFor="phone">
          Phone Number
        </label>
        <input
          type="tel"
          className={styles["form-input"]}
          id="phone"
          onChange={(e) => change(e)} 
          pattern='^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'
        ></input>

        <label className={styles["form-label"]} htmlFor="password1">
          Password
        </label>
        <input
          type="password"
          className={styles["form-input"]}
          id="password1"
          onChange={(e) => change(e)}
        ></input>

        <label className={styles["form-label"]} htmlFor="password2">
          Confirm Password
        </label>
        <input
          type="password"
          className={styles["form-input"]}
          id="password2"
          onChange={(e) => change(e)}
        ></input>

        <label className={styles["form-label"]} htmlFor="avatar">
          Upload Avatar
        </label>
          <input
            className={styles["file-input"]}
            type="file" onChange={handleFileSelect} id ="avatar"
          ></input>
        {error? <ul> {errorMessage.map((value)=>(<li>{value} </li>))} </ul>: null}
        <button className={styles["form-btn"]}>Sign up</button>
      </div>
    </form>
  );
};

export default SignupPage;