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
        navigator.geolocation.getCurrentPosition((result)=>{
            setUserLoc([result.coords.latitude, result.coords.longitude]);
            const form = new FormData();
            form.append("latitude", result.coords.latitude.toString());
            form.append("longitude", result.coords.longitude.toString());
            axios.post(API_URL, form).then((response) => {
                setMap(response.data.studio)
            }) 
        });
    }, []);
    return <MapContainer style={{"height": "500px"}} center={[43.6616965, -79.392341]} zoom={15} scrollWheelZoom={true}>
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
    
  </MapContainer>;
};

export default Home;

// import { Grid, Button } from '@material-ui/core'
// import Typed from 'react-typed'

// export class Home {
//     render() {
//         return (
//             <div id='home'>
//                 <div id='homeContent'>
//                     <Grid container spacing={5}>
//                         <Grid item xs={12} id='typing'>
//                             <Typed
//                                 strings={[
//                                     "Fantastic Studios",
//                                     "Experienced Coaches",
//                                     "Challenging Classes",
//                                     "Just do it"
//                                 ]}
//                                 typeSpeed={100}
//                                 backDelay={1125}
//                                 backSpeed={50}
//                                 loop
//                             />
//                         </Grid>
//                         <Grid item xs={12} id="introBtn">
//                             <a href="https://docs.google.com/forms/d/e/1FAIpQLSfMfyBJFZSd2z9ZOthc2fp5ANqMPdamUi2GQegsRWtq8FQdlg/viewform">
//                                 <Button style={{minWidth: '150px', minHeight: '45px'}} variant="contained" id="joinBtn">
//                                     Join the Club
//                                 </Button>
//                             </a>
//                         </Grid>
//                     </Grid>
//                 </div>
//             </div>
//         )
//     }
// }

// export default Home