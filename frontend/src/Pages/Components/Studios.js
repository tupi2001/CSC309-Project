import React, { useState, useEffect } from "react";
import styles from "./Studios.module.css";
import { Link } from "react-router-dom"
import axios from "axios";
const URL = 'http://localhost:8000/studios/allstudios/';
const Studios = (props) => {
    const [fullList, setFullList] = useState([]);
    const [studios, setStudios] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        navigator.geolocation.getCurrentPosition((result) => {
            const form = new FormData();
            form.append("latitude", result.coords.latitude.toString());
            form.append("longitude", result.coords.longitude.toString());
            axios.post(URL, form).then((response) => {
                response.data.studio.sort((a, b) => a.distance - b.distance)
                setStudios(response.data.studio)
                setFullList(response.data.studio)
            })
        });
    }, []);
    const filterStuff = (e) => {
        setError("");
        if (!e.target.value) {
            // reset 
            setStudios(fullList);
            return;
        }
        const filteredStudios = fullList.filter((studio) => {
            return studio.amenities.some((amenity) => {
                return amenity.type.toLowerCase().startsWith(e.target.value.toLowerCase())
            })
        })
        setStudios(filteredStudios)
        if (filteredStudios.length == 0) {
            setError("No studio was found")
        }
    }

    return (<>
        <div className={styles["wrap"]}>
            <div className={styles["search"]}>
                <input type="text" className={styles["searchTerm"]} placeholder="What are you looking for?" onChange={filterStuff}/>
                    <button type="submit" className={styles["searchButton"]}>
                        <i class="fa fa-search"></i>
                    </button>
            </div>
        </div>
        <ul>
            {studios.map((studio, i) => {
                return <Link key={i} to={`/studios/${studio.id}`}><li>{studio.name}</li></Link>
            })}
        </ul>
        <p>{error}</p>
    </>);
}
export default Studios;