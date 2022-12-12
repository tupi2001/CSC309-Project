import React, { useState, useEffect } from "react";
import styles from "./Studio.module.css";
import {Link, useParams} from "react-router-dom"
import axios from "axios";
const Studio = (props) => {
    const [studio, setStudio] = useState({
        images: []
    })
    const {id} = useParams();
    useEffect(
        ()=>{
            axios.get(`http://localhost:8000/studios/${id}/info/`).then((response)=>{
                response.data.images = response.data.images.map((image)=>{
                    return "http://localhost:8000" + image
                })
                setStudio(response.data)
            })
        },
    []);
    return <img src={studio.images[0]} />
}
export default Studio;