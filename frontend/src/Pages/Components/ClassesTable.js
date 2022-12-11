import {useContext} from "react";
import APIContext from "./ApiContext";

const ClassesTable = ({ studio_id }) => {
    const { classes } = useContext(APIContext);

    return <table>
        <thead>
        <tr>
            <th> # </th>
            <th> Class Name </th>
            <th> Class ID </th>
            <th> Coach </th>
            <th> Start time </th>
            <th> End time </th>
            <th> Start date </th>
        </tr>
        </thead>
        <tbody>
        {classes.map((class, index) => (
            <tr key={class.id}>
                {/* <td>{ (params.page - 1) * perPage + index + 1 }</td> */}
                <td>{ class.name }</td>
                <td>{ class.coach }</td>
                <td>
                    { class.start_time}
                </td>
                <td>{ class.end_time }</td>
                <td>{ class.start_date }</td>
            </tr>
        ))}
        </tbody>
    </table>
}

export default ClassesTable;