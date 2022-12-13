import React, {useEffect, useState} from "react";
import Input from "../Input";
import {Link} from "react-router-dom";

const Converter = () => {
    const [celsius, setCelsius] = useState(0)

    useEffect(() => {
        console.log("Component mounted")
    }, [])

    const update = isCelsius => value => {
        setCelsius(isCelsius ? value : (value - 32) * 5 / 9);
    }

    return (
        <>
            <Link to="/calculator">To calculator</Link>
            <Input
                title="Celsius"
                value={celsius}
                update={update(true)}
            />
            <Input
                title="Fahrenheit"
                value={celsius * 9 / 5 + 32}
                update={update(false)}
            />
        </>
    )
}

export default Converter;