import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'
import styles from "./Studios.module.css";
import { Link } from "react-router-dom"
import axios from "axios";

const URL = 'http://localhost:8000/studios/allstudios/';
const Studios = (props) => {
    const [fullList, setFullList] = useState([]);
    const [studios, setStudios] = useState([]);
    const [pagedStudios, setPagedStudios] = useState([]);
    const [pagination, setPagination] = useState({
        currentPage: 1, 
        perPage: 5
    });
    const [pageNumbers, setPageNumbers] = useState([]);
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

    const setPage = (pageNum) => {
        setPagination({
            ...pagination,
            currentPage: pageNum
        });
    }
    
    useEffect(() => {
        const arr = [];
        for (let i = 1; i <= Math.ceil(studios.length / pagination.perPage); i++) {
            arr.push(i);
        }
        if (pageNumbers.length != arr.length) {
            setPageNumbers(arr);
        }
        if (studios.length) {
            const indexOfLastPost = pagination.currentPage * pagination.perPage;
            const indexOfFirstPost = indexOfLastPost - pagination.perPage;
            setPagedStudios(studios.slice(indexOfFirstPost, indexOfLastPost));
        }
    }, [studios, pagination]);
    


    return (<>
        <div className={styles["wrap"]}>
            <div className={styles["search"]}>
                <input type="text" className={styles["searchTerm"]} placeholder="What are you looking for?" onChange={filterStuff} />
                <button type="submit" className={styles["searchButton"]}>
                    <FontAwesomeIcon icon={faMagnifyingGlass} />
                </button>
            </div>

            <dl>
                {pagedStudios.map((studio, i) => {
                    return <React.Fragment key={i.toString()}>
                        <dt><Link key={i} to={`/studios/${studio.id}`}>{studio.name}</Link></dt>
                        <dd>{studio.distance.toFixed(2)} km away</dd>
                    </React.Fragment>
                })}
            </dl>
            <p>{error}</p>

            <div>
                {pageNumbers.map((num) => {
                    return <button key={num.toString()} style={{'marginRight': '5px'}} onClick={(e) => setPage(num)}>{num}</button>
                })}
            </div>
        </div>

    </>);
}
export default Studios;