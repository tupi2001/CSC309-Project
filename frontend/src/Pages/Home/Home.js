import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from "axios";
import styles from "./Home.module.css";

const API_URL = "http://localhost:8000/studios/allstudios/"


require('leaflet/dist/leaflet.css');
let L = require('leaflet/dist/leaflet.js');
let i = require('leaflet/dist/images/marker-icon.png');
let s = require('leaflet/dist/images/marker-shadow.png');

let DefaultMarkerIcon = L.icon({
    iconUrl: i,
    shadowUrl: s,
});

let redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const Home = (props) => {
    const [map, setMap] = useState([]);
    const [userLoc, setUserLoc] = useState([0, 0]);
    useEffect(() => {
        navigator.geolocation.getCurrentPosition((result) => {
            setUserLoc([result.coords.latitude, result.coords.longitude]);
            const form = new FormData();
            form.append("latitude", result.coords.latitude.toString());
            form.append("longitude", result.coords.longitude.toString());
            axios.post(API_URL, form).then((response) => {
                setMap(response.data.studio)
            })
        });
    }, []);
    return <> <MapContainer style={{ "height": "500px" }} center={[43.6616965, -79.392341]} zoom={15} scrollWheelZoom={true}>
        <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker key={0} icon={redIcon} position={userLoc}>
            <Popup>
                User Location
            </Popup>
        </Marker>
        {map.map((studio) => {
            return <Marker key={studio.id} icon={DefaultMarkerIcon} position={[studio.latitude, studio.longitude]}>
                <Popup>
                    {studio.name}
                </Popup>
            </Marker>
        })}

    </MapContainer>
    <div className={styles['about-container']}>
        <h1> About Us!</h1>
        <p> We are the Toronto Fitness Club and our mission is to help you obtain a healthy lifstyle.
            With over 200 studios all over the world, each equipped with state-of-the-art equipment and highly
            trained professionals that are available to your every need. At the Toronto Fitness Club, we value
            our customers above all else and we strive to hear your feedback.
        </p>
    </div>
    <footer>
        <div class="footer-column">
            <h2> Contact Us: </h2>
            <p><a href="mailto:tfc@gmail.com" className={styles['footer-link']}>tfc@gmail.com</a>
                <br /> <a href="tel:(416)-397-6217" className={styles['footer-link']}>(416)-397-6217</a></p>
        </div>
        <div class="footer-column">
            <h2> Opening Hours: </h2>
            <p>Weekdays: <time> 10:00 am </time>to <time>4:00 pm</time> <br></br>
                Weekends: <time>12:00 pm</time> to <time>2:00 pm</time>
            </p>
        </div>
    </footer>
    </>;
};

export default Home;