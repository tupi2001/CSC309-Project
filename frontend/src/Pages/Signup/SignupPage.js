import { Link } from "react-router-dom";
import styles from "./SignupPage.module.css";

const SignupPage = () => {
  return (
    <form className={styles.form}>
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

        <Link to="/login/" className={styles["form-redirect"]}>
          Already have an account?
        </Link>
        <button className={styles["form-btn"]}>Sign up</button>
      </div>
    </form>
  );
};

export default SignupPage;