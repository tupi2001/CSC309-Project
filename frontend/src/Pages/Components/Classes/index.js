import {useContext, useEffect, useState} from "react";
// import PlayersTable from "./PlayersTable";
// import APIContext from "../../Contexts/APIContext";
import styles from "../Studios.module.css";
import GymClasses from "./GymClasses";
import React from 'react';
import APIContext from "../../../Contexts/APIContext";
import EnrolClass from "./Enrol";
import EnrolClassAll from "./EnrolAll";

const Classes = () => {
    // const perPage = 20;
    const [params, setParams] = useState({studio_id: 1, class_id:0, class2_id: 0, search: ""})
    // const [fullList, setFullList] = useState([]);
    // const [gymclasses, setClasses] = useState([]);

    const { setClasses } = useContext(APIContext);

    useEffect(() => {
        const { studio_id, class_id, class2_id, search } = params;
        // const studio_id = 1;
        console.log({studio_id});
        fetch(
            `http://localhost:8000/classes/${studio_id}/view/?search=${search}`)
                        .then((res) => res.json())
                        .then((json) => {
                            // console.log(json["gym_classes"]);
                            // console.log(json["gym_classes"]);
                            // setClasses(json["gym_classes"]);
                            // setFullList(json["gym_classes"]);
                            setClasses(json["gym_classes"])
                            return(json["gym_classes"]);
                        }, [params])
            // fetch(
            //     `http://localhost:8000/classes/user/${studio_id}/enrol/${class_id}`, {
            //         headers: {
            //             Authorization: "Token " + localStorage.getItem("SessionToken")
            //         }
            //     })
            //     .then((res) => res.json())
            //     .then((json) => {
            //         console.log(json["gym_classes"]);
            //         // console.log(setClasses);
            //         // setClasses(json["gym_classes"]);
            //         // setFullList(json["gym_classes"]);
            //     }, [studio_id, class_id])
            // fetch(
            //         `http://localhost:8000/classes/user/${studio_id}/enrol/${class2_id}/all/`)
            //         .then((res) => res.json())
            //         .then((json) => {
            //             // console.log(json["gym_classes"]);
            //             // setFullList(json["gym_classes"]);
            //         }, [studio_id, class2_id])
    })

    return (
        <>
            <strong>Search</strong>
            <input
                className={styles["searchTerm"]} 
                style={{width: 300, height: 20, fontSize: 18, margin: 4}}
                value={params.search}
                onChange={(event) => {
                    setParams({
                        search: event.target.value,
                        studio_id: params.studio_id,
                        class_id: params.class_id,
                        class2_id: params.class2_id
                    })
                }}
            />
            <br></br>
            <strong style={{color:'#00f'}}>Studio id</strong>
            <input
                className={styles["searchTerm"]}
                style={{width: 280, height: 20, fontSize: 18, margin: 4}}
                value={params.studio_id}
                onChange={(event) => {
                    console.log("changed");
                    setParams({
                        search:params.search,
                        studio_id: event.target.value,
                        class_id: params.class_id,
                        class2_id: params.class2_id
                    })
                }}
            />
            {/* <br></br>
            <strong style={{color:'#0ff'}}>Enter ID of gym class you want to enrol in</strong>
            <input
                className={styles["searchTerm"]}
                style={{width: 280, height: 20, fontSize: 18, margin: 4}}
                value={params.class_id}
                onChange={(event) => {
                    console.log("changed");
                    setParams({
                        search:params.search,
                        studio_id: params.studio_id,
                        class_id: event.target.value,
                        class2_id: params.class2_id
                    })
                }}
            />
            <br></br>
            <strong style={{color:'#f0f'}}>Enter ID of gym class type you want to enrol in</strong>
            <input
                className={styles["searchTerm"]}
                style={{width: 280, height: 20, fontSize: 18, margin: 4}}
                value={params.class2_id}
                onChange={(event) => {
                    console.log("changed");
                    setParams({
                        search:params.search,
                        studio_id: params.studio_id,
                        class_id: params.class_id,
                        class2_id: event.target.value
                    })
                }} */}
            {/* /> */}
            <GymClasses params={params} />
            <EnrolClass />
            <EnrolClassAll />

        </>
    )
}

export default Classes;