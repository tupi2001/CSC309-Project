import { Link } from "react-router-dom";
import styles from "./LoginPage.module.css";
import NavLink from "react-router-dom"
// import { API_URL } from "../constants";
import axios from 'axios'
import { useState } from "react";

// to obtain pair token
const URL = 'http://localhost:8000/accounts/api/token/'

function LoginPage() {
  // initializes fields to empty
  const [data, setData] = useState({
    email: "",
    password: "",
  })

  // handles changes in form data
  function change(e){  
    const new_data = {... data}
    new_data[e.target.id] = e.target.value
    console.log(new_data)
    setData(new_data)
  }
  
  // handles submitting of form
  function handleSubmit(e) {
    e.preventDefault();
    axios
      .post(URL, {
        email: data.email,
        password: data.password
      }).then((response)=>{
        if(response.status === 200){
            localStorage.setItem("SessionToken", response.data.access)
            // route to home page
            window.location.href = "/home"
        }else{
            alert("Email or Password is invalid")
        }
      }).catch((e)=>{alert("Email or Password is invalid")})
  }
  return (
    <div>
      <form className={styles.form} onSubmit={(e) => handleSubmit(e)}>
        <div className={styles["form-content"]}>
          <h1 className={styles["form-title"]}>Please sign in</h1>
          <h4 className={styles["form-subtitle"]}>to continue to Toronto Fitness</h4>
          <input id='email' onChange={(e) => change(e)} placeholder="email" type="Email" className={styles["form-input"]}></input>
          <input id='password' onChange={(e) => change(e)} type="password" placeholder="Password" className={styles["form-input"]}></input>
          <Link to="/signup/">Don't have an account? Sign up here!</Link>
          <button className={styles["form-btn"]}>Sign in</button>
        </div>
      </form>
    </div>
  );
};

export default LoginPage;