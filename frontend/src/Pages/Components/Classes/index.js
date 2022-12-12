import {useContext, useEffect, useState} from "react";
// import PlayersTable from "./PlayersTable";
// import APIContext from "../../Contexts/APIContext";
import GymClasses from "./GymClasses";
import React from 'react';
import APIContext from "../../../Contexts/APIContext";

const Classes = () => {
    // const perPage = 20;
    const [params, setParams] = useState({studio_id: 1, search: ""})
    // const [fullList, setFullList] = useState([]);
    // const [gymclasses, setClasses] = useState([]);

    const { setClasses } = useContext(APIContext);

    useEffect(() => {
        const { studio_id, search } = params;
        // const studio_id = 1;
        console.log({studio_id});
        fetch(
            `http://localhost:8000/classes/${studio_id}/view/?search=${search}`)
                        .then((res) => res.json())
                        .then((json) => {
                            // console.log(json["gym_classes"]);
                            console.log(setClasses);
                            setClasses(json["gym_classes"]);
                            // setFullList(json["gym_classes"]);
                        })
    }, [params])

    return (
        <>
            <strong style={{color:'#f00'}}>Search</strong>
            <input
                style={{width: 300, height: 20, fontSize: 18, margin: 4}}
                value={params.search}
                onChange={(event) => {
                    setParams({
                        search: event.target.value,
                        studio_id: params.studio_id
                    })
                }}
            />
            <br></br>
            <strong style={{color:'#00f'}}>Studio id</strong>
            <input
                style={{width: 280, height: 20, fontSize: 18, margin: 4}}
                value={params.studio_id}
                onChange={(event) => {
                    console.log("changed");
                    setParams({
                        search:params.search,
                        studio_id: event.target.value
                    })
                }}
            />
            <GymClasses params={params} />
            {/* <button onClick={() => setParams({
                ...params,
                // page: Math.max(1, params.page - 1)
            })}>
                prev
            </button>
            <button onClick={() => setParams({
                ...params,
                page: params.page + 1
            })}>
                next
            </button> */}
        </>
    )
}

export default Classes;