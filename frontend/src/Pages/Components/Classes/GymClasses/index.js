import {useContext} from "react";
import APIContext from "../../../../Contexts/APIContext";
import React from "react";

const GymClasses = ({ perPage, params }) => {
    const { gymclasses } = useContext(APIContext);
    // console.log("gym");
    // console.log(APIContext);
    if (gymclasses !== null) {
        return <table>
            <thead>
            <tr>
                {/* <th> # </th> */}
                {/* <th> Studio id </th> */}
                <th> Name </th>
                <th> Coach </th>
                <th> Start-time </th>
                <th> End-time </th>
                <th> Date </th>
            </tr>
            </thead>
            <tbody>
            {gymclasses.map((gymclass, index) => (
                <tr key={gymclass.id}>
                    {/* <td>{ gymclass.studio }</td> */}
                    <td>{ gymclass.name }</td>
                    <td>{ gymclass.coach }</td>
                    <td>{ gymclass.start_time }</td>
                    <td>{ gymclass.end_time }</td>
                    <td>{ gymclass.start_date }</td>
                </tr>
            ))}

            </tbody>
        </table>
    }
}

export default GymClasses