import React, { useState, useEffect } from "react";
import styles from "./Studio.module.css";
import { Link, useParams } from "react-router-dom"
import axios from "axios";
const Studio = (props) => {
    const [studio, setStudio] = useState({
        images: []
    })
    const { id } = useParams();
    useEffect(
        () => {
            axios.get(`http://localhost:8000/studios/${id}/info/`).then((response) => {
                response.data.images = response.data.images.map((image) => {
                    return "http://localhost:8000" + image
                })
                setStudio(response.data)
            })
        },
        []);
    return (
        <>
            <h3>Images</h3>
            <ul style={{listStyleType: 'none'}}>
                {studio.images ? studio.images.map((image, i) => {
                    return <>
                        <li><img className={styles['studio-image']} src={image}/></li>
                    </>
                }) : null}
            </ul>
            <h3>Amenities</h3>
            <ul>
                {studio.amenities ? studio.amenities.map((single, i) => {
                    return <>
                        <li className={styles['amenities-list']}><p>Type:  {single.type}</p> Quantity: {single.quantity}</li>
                    </>
                }) : null}
            </ul>
        </>
    );
};

export default Studio;