import {useContext, useEffect, useState} from "react";
// import PlayersTable from "./PlayersTable";
// import APIContext from "../../Contexts/APIContext";
import React from "react";

const Classes = () => {
    // const perPage = 20;
    // const [params, setParams] = useState({page: 1, search: ""})

    // const { setPlayers } = useContext(APIContext);
    const studio_id = 1;
    var data = [];    

    useEffect(() => {
        // const { page, search } = params;
        fetch(`http://localhost:8000/classes/${studio_id}/view/`)
            .then(res => { return res.json();})
            .then(json => {
                data = json["gym_classes"];
                console.log(data);
                return(json.data);
            })
    }, )

    return (
        <ul>
            {data.map((item) => (
                <li key={item.id}>{item.name}</li>
            ))}
        </ul>
    )  

    // return (
    //     <>
    //         Search
    //         <input
    //             style={{width: 300, height: 20, fontSize: 18, margin: 4}}
    //             value={params.search}
    //             onChange={(event) => {
    //                 setParams({
    //                     search: event.target.value,
    //                     page: 1,
    //                 })
    //             }}
    //         />
    //         <PlayersTable perPage={perPage} params={params} />
    //         <button onClick={() => setParams({
    //             ...params,
    //             page: Math.max(1, params.page - 1)
    //         })}>
    //             prev
    //         </button>
    //         <button onClick={() => setParams({
    //             ...params,
    //             page: params.page + 1
    //         })}>
    //             next
    //         </button>
    //     </>
    // )
}

export default Classes;