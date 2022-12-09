import { Link } from "react-router-dom";
import styles from "./SignupPage.module.css";
// import { API_URL } from "../constants";
import axios from 'axios'
import React, { useState } from 'react';

const URL = 'http://localhost:8000/accounts/register/';

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
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post(URL, {
        first_name: data.fname,
        last_name : data.lname,
        username: data.username,
        email: data.email,
        password: data.password1,
        password2: data.password2,
        phone_number: data.phone,
        avatar: data.avatar
      })
      .then((response) => {
        if (response.data.success) {
          //redirect to home page
          window.location.href = '/';
        } else {
          setError(true);
          setErrorMessage(response.data.message);
        }
      })
      .catch((err) => {
        setError(true);
        setErrorMessage(err.message);
      });
  };

  const handleFileSelect = (e) => {

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
            ></input>
          </div>

          <div className={styles["input-group"]}>
            <label className={styles["form-label"]} htmlFor="lname">
              Last Name
            </label>
            <input
              type="text"
              className={styles["form-input"]}
              id="email"
            ></input>
          </div>
        </div>

        <label className={styles["form-label"]} htmlFor="username">
          Username
        </label>
        <input type="text" className={styles["form-input"]} id="username"></input>

        <label className={styles["form-label"]} htmlFor="email">
          Email Address
        </label>
        <input type="email" className={styles["form-input"]} id="email"></input>

        <label className={styles["form-label"]} htmlFor="phone">
          Phone Number
        </label>
        <input
          type="tel"
          className={styles["form-input"]}
          id="phone"
          pattern="[0-9]{10}"
        ></input>

        <label className={styles["form-label"]} htmlFor="password1">
          Password
        </label>
        <input
          type="password"
          className={styles["form-input"]}
          id="password1"
        ></input>

        <label className={styles["form-label"]} htmlFor="password2">
          Confirm Password
        </label>
        <input
          type="password"
          className={styles["form-input"]}
          id="password2"
        ></input>

        <label className={styles["form-label"]} htmlFor="avatar">
          Upload Avatar
        </label>
          <input
            className={styles["file-input"]}
            type="file" onChange={handleFileSelect} id ="avatar"
          ></input>

        <button className={styles["form-btn"]}>Sign up</button>
      </div>
    </form>
  );
};

export default SignupPage;