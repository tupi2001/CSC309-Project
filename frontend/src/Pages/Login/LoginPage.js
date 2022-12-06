import { Link } from "react-router-dom";
import styles from "./LoginPage.module.css";

const LoginPage = () => {
  const dosomething = (event) => {
    event.preventDefault();
    console.log("hello");
  };
  return (
    <form className={styles.form} onSubmit={dosomething}>
      <div className={styles["form-content"]}>
        <h1 className={styles["form-title"]}>Please sign in</h1>
        <input
          type="email"
          placeholder="Email address"
          className={styles["form-input"]}
        ></input>
        <input
          type="password"
          placeholder="Password"
          className={styles["form-input"]}
        ></input>
        <Link to="/signup/" className={styles["form-redirect"]}>
          Don't have an account?
        </Link>
        <button className={styles["form-btn"]}>Sign in</button>
        <p className={styles["copyright-tag"]}>
          Copyright MKA Group &copy; 2022
        </p>
      </div>
    </form>
  );
};

export default LoginPage;